import numpy as np
from PIL import Image
import json
import math
import sys
import os

# --- JPEG-like decompressor -------------------------------------------------
# Runs the compressor's pipeline in reverse, channel by channel:
#   1. Read and parse the header: dimensions, block size, quantization
#      matrices, Huffman table specs and data lengths.
#   2. Huffman-decode the bit stream back into (DC category, DC bits,
#      AC RLE pairs) per block (huffman.py).
#   3. Restore the AC zigzag rows and invert the VLI coding (vli.py, rle_ac.py).
#   4. Inverse DPCM to recover the true DC values (differential_dc.py).
#   5. Inverse zigzag, dequantization, inverse DCT (idct) and level shift
#      +128 back to pixel values (zigzag.py, quantization.py, dct.py).
#   6. Reassemble the blocks into padded channels (blocks.py).
#   7. Upsample the Cb/Cr channels back to full resolution (downsampling.py)
#      and convert YCbCr back to RGB (ycbcr.py).

import errors
import constants
import ycbcr
import downsampling
import dct
import quantization
import zigzag
import differential_dc
import rle_ac
import vli
import huffman


def load_compressed_data(filepath):
    metadata = None
    y_data, cb_data, cr_data = None, None, None

    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        return None, None, None, None

    try:
        with open(filepath, 'rb') as f:
            magic = f.read(len(b'MYJPEG'))
            if magic != b'MYJPEG':
                raise ValueError(errors.INVALID_FILE_FORMAT)

            header_len_bytes = f.read(constants.PARAM_BYTES)
            if len(header_len_bytes) != constants.PARAM_BYTES:
                raise EOFError(errors.HEADER_LENGTH_READ_FAILED)
            header_len = int.from_bytes(header_len_bytes, constants.BYTE_ORDER)

            metadata_bytes = f.read(header_len)
            if len(metadata_bytes) != header_len:
                raise EOFError(errors.HEADER_READ_FAILED)
            metadata = json.loads(metadata_bytes.decode('utf-8'))

            required_keys = [
                "data_len_y", "data_len_cb", "data_len_cr", "original_width", "original_height",
                "block_size", "q_table_y", "q_table_c", "huff_dc_y_bits", "huff_dc_y_huffval",
                "huff_ac_y_bits", "huff_ac_y_huffval", "huff_dc_c_bits", "huff_dc_c_huffval",
                "huff_ac_c_bits", "huff_ac_c_huffval", "padded_dims_y", "padded_dims_cb", "padded_dims_cr"
            ]
            for key in required_keys:
                if key not in metadata:
                    raise ValueError(
                        f"Required metadata key is missing: {key}")

            y_data = f.read(metadata["data_len_y"])
            cb_data = f.read(metadata["data_len_cb"])
            cr_data = f.read(metadata["data_len_cr"])

            if len(y_data) != metadata["data_len_y"] or \
               len(cb_data) != metadata["data_len_cb"] or \
               len(cr_data) != metadata["data_len_cr"]:
                raise EOFError(errors.COMPONENT_DATA_READ_FAILED)

            print(
                f"Metadata and compressed data successfully loaded from {filepath}")

    except FileNotFoundError:
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        return None, None, None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in metadata: {e}", file=sys.stderr)
        return None, None, None, None
    except (ValueError, EOFError) as e:
        print(
            f"Error reading or parsing the file {filepath}: {e}", file=sys.stderr)
        return None, None, None, None
    except Exception as e:
        print(f"Unexpected error while loading the file: {e}", file=sys.stderr)
        return None, None, None, None

    return metadata, y_data, cb_data, cr_data


def decompress_image(compressed_path, output_path):
    """Decompress an image from the MYJPEG format into a standard format (e.g. PNG)."""
    print(f"Decompressing '{compressed_path}'...")

    metadata, y_data, cb_data, cr_data = load_compressed_data(compressed_path)
    if metadata is None:
        return None

    try:
        print("Restoring tables and parameters...")
        block_size = metadata['block_size']
        original_width = metadata['original_width']
        original_height = metadata['original_height']
        padded_dims = {
            'Y': tuple(metadata['padded_dims_y']),
            'Cb': tuple(metadata['padded_dims_cb']),
            'Cr': tuple(metadata['padded_dims_cr'])
        }

        q_matrix_y = np.array(metadata['q_table_y'], dtype=np.uint8)
        q_matrix_c = np.array(metadata['q_table_c'], dtype=np.uint8)

        huff_dc_y = huffman.HuffmanTable(
            metadata['huff_dc_y_bits'], metadata['huff_dc_y_huffval'])
        huff_ac_y = huffman.HuffmanTable(
            metadata['huff_ac_y_bits'], metadata['huff_ac_y_huffval'])
        huff_dc_c = huffman.HuffmanTable(
            metadata['huff_dc_c_bits'], metadata['huff_dc_c_huffval'])
        huff_ac_c = huffman.HuffmanTable(
            metadata['huff_ac_c_bits'], metadata['huff_ac_c_huffval'])

        reconstructed_channels = {}

        for name, comp_data, dc_table, ac_table, q_matrix in [
            ('Y', y_data, huff_dc_y, huff_ac_y, q_matrix_y),
            ('Cb', cb_data, huff_dc_c, huff_ac_c, q_matrix_c),
            ('Cr', cr_data, huff_dc_c, huff_ac_c, q_matrix_c)
        ]:
            print(f"Decoding component {name}...")
            h_pad, w_pad = padded_dims[name]
            num_blocks_comp = (h_pad // block_size) * (w_pad // block_size)
            if num_blocks_comp == 0 and len(comp_data) > 0:
                raise ValueError(
                    f"Computed block count is 0, but data exists for {name}")
            elif num_blocks_comp == 0 and len(comp_data) == 0:
                reconstructed_channels[name] = np.zeros((0, 0), dtype=np.uint8)
                continue

            # 2) Huffman-decoding: one (dc category, dc bits, ac RLE pairs)
            # tuple per block.
            decoded_block_data = huffman.huff_decode_blocks(
                comp_data, dc_table, ac_table, num_blocks_comp)
            if len(decoded_block_data) != num_blocks_comp:
                print(
                    f"Warning: decoded {len(decoded_block_data)} blocks for {name}, expected {num_blocks_comp}")
                num_blocks_comp = len(decoded_block_data)
                if num_blocks_comp == 0:
                    reconstructed_channels[name] = np.zeros(
                        (0, 0), dtype=np.uint8)
                    continue

            # 3) Restore zigzag rows from RLE and invert VLI for the DC parts.
            all_dc_diffs = []
            zigzag_rows = []

            print(
                f"  Restoring {num_blocks_comp} quantized blocks of {name}...")
            for dc_category, dc_vli_bits, ac_rle_pairs in decoded_block_data:
                ac_zigzag = rle_ac.restore_ac_coefficients_from_rle(
                    ac_rle_pairs, block_size * block_size - 1)
                dc_diff = vli.decode_vli(dc_category, dc_vli_bits)
                all_dc_diffs.append(dc_diff)
                if len(ac_zigzag) != block_size * block_size - 1:
                    raise ValueError(
                        f"Invalid length ({len(ac_zigzag)}) of the restored zigzag array for a block. Expected {block_size * block_size - 1}.")
                zigzag_rows.append([dc_diff] + ac_zigzag)

            zigzag_arr = np.array(zigzag_rows, dtype=np.int32)
            if zigzag_arr.shape[1] != block_size * block_size:
                raise ValueError(
                    f"Invalid length ({zigzag_arr.shape[1]}) of a restored zigzag row. Expected {block_size * block_size}.")

            # 4) Inverse DPCM for the DC values, then 5) inverse zigzag,
            # dequantization and IDCT back to pixel intensities.
            print(f"  Applying inverse DPCM to DC of {name}...")
            dc_actual_values = differential_dc.dpcm_decode_dc(all_dc_diffs)

            if len(dc_actual_values) != zigzag_arr.shape[0]:
                raise ValueError(
                    f"DC count ({len(dc_actual_values)}) does not match block count ({zigzag_arr.shape[0]}) for {name}")

            quantized_blocks = zigzag.inverse_zigzag_scan_blocks(
                zigzag_arr, block_size)
            quantized_blocks[:, 0, 0] = np.array(
                dc_actual_values, dtype=np.int32)

            print(f"  Dequantizing and IDCT for blocks of {name}...")
            dequantized = quantization.dequantize_blocks(
                quantized_blocks, q_matrix)
            reconstructed = dct.idct2_blocks(dequantized) + 128.0
            reconstructed = np.clip(reconstructed, 0, 255)
            final_component_blocks = np.round(reconstructed).astype(np.uint8)

            print(f"  Assembling component {name}...")
            if final_component_blocks.shape[0] == 0:
                reassembled_padded = np.zeros((h_pad, w_pad), dtype=np.uint8)
            else:
                num_blocks_h = h_pad // block_size
                num_blocks_w = w_pad // block_size
                block_grid = final_component_blocks.reshape(
                    num_blocks_h, num_blocks_w, block_size, block_size)
                reassembled_padded = block_grid.transpose(
                    0, 2, 1, 3).reshape(h_pad, w_pad)

            if name == 'Y':
                final_h, final_w = original_height, original_width
            else:
                final_h = math.ceil(original_height / 2)
                final_w = math.ceil(original_width / 2)

            final_h = min(final_h, h_pad)
            final_w = min(final_w, w_pad)

            reconstructed_channels[name] = reassembled_padded[:final_h, :final_w]
            print(
                f"    Final size of {name}: {reconstructed_channels[name].shape}")

        print("Upsampling Cb and Cr...")
        y_final = reconstructed_channels['Y']
        target_h, target_w = y_final.shape

        if reconstructed_channels['Cb'].size == 0 or reconstructed_channels['Cr'].size == 0:
            print("Warning: Cb/Cr channels are empty after decompression/cropping. The source image may be smaller than 2x2.")
            cb_upsampled = np.full((target_h, target_w), 128, dtype=np.uint8)
            cr_upsampled = np.full((target_h, target_w), 128, dtype=np.uint8)
        else:
            cb_upsampled = downsampling.upsample_channel_nearest_neighbor(
                reconstructed_channels['Cb'], target_h, target_w)
            cr_upsampled = downsampling.upsample_channel_nearest_neighbor(
                reconstructed_channels['Cr'], target_h, target_w)

        print(f"  Size of Y : {y_final.shape}")
        print(f"  Size of Cb (up): {cb_upsampled.shape}")
        print(f"  Size of Cr (up): {cr_upsampled.shape}")

        if not (y_final.shape == cb_upsampled.shape == cr_upsampled.shape):
            raise ValueError(
                f"Channel dimensions after upsampling do not match: "
                f"Y={y_final.shape}, Cb={cb_upsampled.shape}, Cr={cr_upsampled.shape}")

        final_ycbcr = np.stack((y_final, cb_upsampled, cr_upsampled), axis=-1)
        final_rgb = ycbcr.ycbcr_to_rgb(final_ycbcr)

        print(f"Saving the restored image to {output_path}...")
        img_out = Image.fromarray(final_rgb)
        img_out.save(output_path)

        print(
            f"Decompression of '{compressed_path}' finished. Result saved to '{output_path}'.")
        return final_rgb

    except Exception as e:
        print(f"Error during the decompression process: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def display_compressed_image(compressed_path):
    """Decompress and display an image using Pillow."""
    print(f"Trying to display the compressed image: {compressed_path}")
    if not os.path.exists(compressed_path):
        print(f"Error: file not found: {compressed_path}", file=sys.stderr)
        return

    import tempfile
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_f:
            temp_output_path = temp_f.name
        print(f"Decompressing into a temporary file: {temp_output_path}")

        decompressed_rgb = decompress_image(compressed_path, temp_output_path)

        if decompressed_rgb is not None:
            print(f"Showing the image from {temp_output_path}...")
            img_display = Image.open(temp_output_path)
            img_display.show()

        else:
            print("Decompression failed, cannot display the image.")

    except Exception as e:
        print(f"Error during decompression or display: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        if 'temp_output_path' in locals() and os.path.exists(temp_output_path):
            try:
                os.remove(temp_output_path)
                print(f"Temporary file {temp_output_path} removed.")
            except OSError as rm_err:
                print(
                    f"Failed to remove the temporary file {temp_output_path}: {rm_err}", file=sys.stderr)
