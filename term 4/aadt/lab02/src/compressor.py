import numpy as np
from PIL import Image
import json
import math
import sys

# --- JPEG-like compressor --------------------------------------------------
# Compression pipeline, applied channel by channel:
#   1. RGB -> YCbCr color conversion (ycbcr.py).
#   2. 4:2:0 downsampling of the Cb and Cr channels (downsampling.py).
#   3. Splitting the channel into 8x8 blocks (blocks.py).
#   4. 2D DCT-II of every block (dct.py).
#   5. Quantization using the luma/chroma matrices scaled by quality
#      (quantization.py, tables.py).
#   6. Zigzag scanning (zigzag.py).
#   7. Difference (DPCM) coding of the DC coefficients (differential_dc.py)
#      and run-length coding of the AC coefficients (rle_ac.py).
#   8. Variable-length integer encoding (vli.py) and Huffman entropy coding
#      (huffman.py) into one bit stream.
# The result is written to disk as the magic 'MYJPEG', a JSON header with the
# metadata (dimensions, quantization matrices, Huffman table specs, lengths)
# and the three compressed bit streams.

import errors
import constants
from tables import (CHROMA_QTABLE, LUMA_QTABLE,
                    DEFAULT_DC_LUMINANCE_BITS, DEFAULT_DC_LUMINANCE_HUFFVAL,
                    DEFAULT_AC_LUMINANCE_BITS, DEFAULT_AC_LUMINANCE_HUFFVAL,
                    DEFAULT_DC_CHROMINANCE_BITS, DEFAULT_DC_CHROMINANCE_HUFFVAL,
                    DEFAULT_AC_CHROMINANCE_BITS, DEFAULT_AC_CHROMINANCE_HUFFVAL)
import ycbcr
import downsampling
import blocks as block_ops
import dct
import quantization
import zigzag
import differential_dc
import rle_ac
import vli
import huffman


def write_encoded_file(filename, meta, y_bytes, cb_bytes, cr_bytes):
    header_json = json.dumps(meta, indent=4).encode('utf-8')
    header_size = len(header_json)

    with open(filename, 'wb') as file:
        file.write(b'MYJPEG')
        file.write(header_size.to_bytes(
            constants.PARAM_BYTES, constants.BYTE_ORDER))
        file.write(header_json)
        file.write(y_bytes)
        file.write(cb_bytes)
        file.write(cr_bytes)

    original_pixels = meta['original_width'] * meta['original_height'] * 3
    final_size = len(b'MYJPEG') + constants.PARAM_BYTES + header_size \
        + len(y_bytes) + len(cb_bytes) + len(cr_bytes)
    compression_ratio = original_pixels / final_size if final_size > 0 else 0

    print(f"\n File saved: {filename}")
    print(f" Header size: {header_size} bytes")
    print(
        f" Y: {len(y_bytes)} bytes, Cb: {len(cb_bytes)} bytes, Cr: {len(cr_bytes)} bytes")
    print(f" Compression: ~{compression_ratio:.2f}x")
    return final_size


def compress_image(input_image, output_file, quality=75, tile_size=8):
    if not (0 <= quality <= 100):
        raise ValueError(errors.QUALITY_RANGE)
    if tile_size <= 0:
        raise ValueError(errors.BLOCK_SIZE_POSITIVE)

    print(f"\n Start processing: {input_image} (quality: {quality})")

    try:
        with Image.open(input_image) as im:
            if im.mode != 'RGB':
                print(f" Converting from {im.mode} to RGB")
                im = im.convert('RGB')
            rgb_array = np.array(im)

    except FileNotFoundError:
        print(f" File not found: {input_image}", file=sys.stderr)
        return None
    except Exception as err:
        print(f" Error loading image: {err}", file=sys.stderr)
        return None

    height, width, channels = rgb_array.shape
    if channels != 3:
        print(f" Expected 3 RGB channels, got: {channels}", file=sys.stderr)
        return None

    print(f" Size: {width}x{height}")

    # Color conversion
    ycbcr_img = ycbcr.rgb_to_ycbcr(rgb_array)
    y_plane, cb_plane, cr_plane = ycbcr_img[:, :,
                                            0], ycbcr_img[:, :, 1], ycbcr_img[:, :, 2]

    print(" Downsampling...")
    cb_ds = downsampling.downsample_channel_420(cb_plane)
    cr_ds = downsampling.downsample_channel_420(cr_plane)

    print(" Preparing matrices and tables...")
    q_y = quantization.adjust_quantization_matrix(LUMA_QTABLE, quality)
    q_c = quantization.adjust_quantization_matrix(CHROMA_QTABLE, quality)

    try:
        huff_tables = {
            "Y_DC": huffman.HuffmanTable(DEFAULT_DC_LUMINANCE_BITS, DEFAULT_DC_LUMINANCE_HUFFVAL),
            "Y_AC": huffman.HuffmanTable(DEFAULT_AC_LUMINANCE_BITS, DEFAULT_AC_LUMINANCE_HUFFVAL),
            "C_DC": huffman.HuffmanTable(DEFAULT_DC_CHROMINANCE_BITS, DEFAULT_DC_CHROMINANCE_HUFFVAL),
            "C_AC": huffman.HuffmanTable(DEFAULT_AC_CHROMINANCE_BITS, DEFAULT_AC_CHROMINANCE_HUFFVAL),
        }
    except ValueError as err:
        print(f" Huffman initialization error: {err}", file=sys.stderr)
        return None

    # Processing all the components
    all_encoded = {}
    padded_sizes = {}

    for label, channel, q_matrix, dc_huff, ac_huff in [
        ('Y', y_plane, q_y, huff_tables["Y_DC"], huff_tables["Y_AC"]),
        ('Cb', cb_ds, q_c, huff_tables["C_DC"], huff_tables["C_AC"]),
        ('Cr', cr_ds, q_c, huff_tables["C_DC"], huff_tables["C_AC"]),
    ]:
        print(f"\n Component: {label}")
        h, w = channel.shape
        h_padded = math.ceil(h / tile_size) * tile_size
        w_padded = math.ceil(w / tile_size) * tile_size
        padded_sizes[label] = (h_padded, w_padded)

        block_list = block_ops.split_into_blocks(
            channel, tile_size, fill_value=128)
        blocks_arr = np.stack(block_list)

        # 4) DCT, 5) quantization, 6) zigzag, 7) DC difference + AC RLE.
        shifted = blocks_arr.astype(np.float64) - 128.0
        transformed = dct.dct2_blocks(shifted)
        quantized = quantization.quantize_blocks(transformed, q_matrix)

        dc_values = quantized[:, 0, 0].tolist()
        zz_rows = zigzag.zigzag_scan_blocks(
            quantized)[:, 1:].astype(int).tolist()
        ac_encoded = [rle_ac.prepare_ac_coefficients_for_rle(row)
                      for row in zz_rows]
        dct_blocks = [[None, None, ac] for ac in ac_encoded]

        dc_deltas = differential_dc.dpcm_encode_dc(dc_values)
        for i, delta in enumerate(dc_deltas):
            category, bits = vli.get_vli_category_and_value(delta)
            dct_blocks[i][0] = category
            dct_blocks[i][1] = bits

        print(f" Huffman {label}")
        encoded_stream = huffman.huff_encode_blocks(
            dct_blocks, dc_huff, ac_huff)
        all_encoded[label] = encoded_stream
        print(f" {label} done: {len(encoded_stream)} bytes")

    # Metadata
    image_info = {
        "original_width": width,
        "original_height": height,
        "block_size": tile_size,
        "quality": quality,
        "padded_dims_y": padded_sizes['Y'],
        "padded_dims_cb": padded_sizes['Cb'],
        "padded_dims_cr": padded_sizes['Cr'],
        "q_table_y": q_y.tolist(),
        "q_table_c": q_c.tolist(),
        "huff_dc_y_bits": huff_tables["Y_DC"].bit_counts,
        "huff_dc_y_huffval": huff_tables["Y_DC"].symbols,
        "huff_ac_y_bits": huff_tables["Y_AC"].bit_counts,
        "huff_ac_y_huffval": huff_tables["Y_AC"].symbols,
        "huff_dc_c_bits": huff_tables["C_DC"].bit_counts,
        "huff_dc_c_huffval": huff_tables["C_DC"].symbols,
        "huff_ac_c_bits": huff_tables["C_AC"].bit_counts,
        "huff_ac_c_huffval": huff_tables["C_AC"].symbols,
        "data_len_y": len(all_encoded['Y']),
        "data_len_cb": len(all_encoded['Cb']),
        "data_len_cr": len(all_encoded['Cr']),
    }

    print("\n Saving...")
    final_size = write_encoded_file(
        output_file,
        image_info,
        all_encoded['Y'],
        all_encoded['Cb'],
        all_encoded['Cr']
    )

    print(f"\n Done: {input_image} -> {output_file}")
    return final_size
