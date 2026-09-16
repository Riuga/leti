import numpy as np
import math
import errors

# --- 4:2:0 chroma subsampling ---------------------------------------------
# Chroma channels carry far less visual information than luma, so they are
# downsampled by a factor of 2 in both axes: every 2x2 cell is averaged into
# a single sample (a diagonal blocks near the edge of odd-sized images are
# averaged over the real, non-padded samples only). During decompression the
# reduced channels are scaled back to the full size with nearest-neighbour
# duplication, which is the simplest and fastest upsampling scheme.


def downsample_channel_420(src):
    if type(src) is not np.ndarray:
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if src.ndim != 2:
        raise ValueError(errors.MATRIX_NOT_2D)

    h, w = src.shape
    h2, w2 = (math.ceil(h / 2), math.ceil(w / 2))

    # Pad so the height and width are even, then average every 2x2 block.
    src_float = src.astype(np.float64)
    pad_h = h2 * 2 - h
    pad_w = w2 * 2 - w
    padded = np.pad(src_float, ((0, pad_h), (0, pad_w)))

    sums = padded.reshape(h2, 2, w2, 2).sum(axis=(1, 3))

    # Count the number of real (non-padded) samples in each 2x2 cell.
    ones_padded = np.pad(np.ones_like(src_float), ((0, pad_h), (0, pad_w)))
    counts = ones_padded.reshape(h2, 2, w2, 2).sum(axis=(1, 3))

    output = sums / np.maximum(counts, 1)

    return np.round(output).astype(np.uint8)


def upsample_channel_nearest_neighbor(input_channel, out_h, out_w):
    if not isinstance(input_channel, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if input_channel.ndim != 2:
        raise ValueError(errors.MATRIX_NOT_2D)

    if input_channel.size == 0:
        print(f"{errors.EMPTY_INPUT}. Zero matrix {out_h}x{out_w} is returned.")
        return np.zeros((out_h, out_w), dtype=np.uint8)

    enlarged = np.repeat(np.repeat(input_channel, 2, axis=0), 2, axis=1)

    trimmed = enlarged[:out_h, :out_w]
    result = np.zeros((out_h, out_w), dtype=np.uint8)
    result[:trimmed.shape[0], :trimmed.shape[1]] = trimmed

    return result
