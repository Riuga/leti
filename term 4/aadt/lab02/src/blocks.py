import numpy as np
import errors

# --- Block splitting / assembly -------------------------------------------
# The DCT is applied to square blocks (8x8 by default). DCT is easiest to
# compute on complete blocks, so images whose size is not a multiple of the
# block size are first padded: extra pixels on the right and bottom edges are
# filled with a constant (128, the neutral level). After processing, the
# blocks are merged back into one image and the padding is cropped off.


def split_into_blocks(image_channel, block_size, fill_value=0):

    if not isinstance(image_channel, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if image_channel.ndim != 2:
        raise ValueError(errors.MATRIX_NOT_2D)
    if not isinstance(block_size, int) or block_size <= 0:
        raise ValueError(errors.BLOCK_SIZE_POSITIVE)

    h, w = image_channel.shape
    pad_h = (block_size - h % block_size) % block_size
    pad_w = (block_size - w % block_size) % block_size

    padded = np.pad(image_channel, ((0, pad_h), (0, pad_w)),
                    mode='constant', constant_values=fill_value)

    blocks = []
    for i in range(0, padded.shape[0], block_size):
        for j in range(0, padded.shape[1], block_size):
            blocks.append(padded[i:i + block_size, j:j + block_size])

    return blocks


def assemble_from_blocks(blocks_list, padded_height, padded_width, original_height=None, original_width=None):
    if not blocks_list:
        return np.zeros((0, 0), dtype=np.uint8)

    block_shape = blocks_list[0].shape
    if block_shape[0] != block_shape[1] or block_shape[0] == 0:
        raise ValueError(errors.BLOCK_MUST_BE_SQUARE)
    block_size = block_shape[0]

    if padded_height % block_size != 0 or padded_width % block_size != 0:
        raise ValueError(errors.MULTIPLE_OF_BLOCK_SIZE)

    num_blocks_h = padded_height // block_size
    num_blocks_w = padded_width // block_size

    expected_blocks = num_blocks_h * num_blocks_w
    if len(blocks_list) != expected_blocks:
        raise ValueError(
            f"Expected {expected_blocks} blocks, got {len(blocks_list)}.")

    reassembled = np.zeros((padded_height, padded_width),
                           dtype=blocks_list[0].dtype)

    index = 0
    for r in range(num_blocks_h):
        for c in range(num_blocks_w):
            start_r = r * block_size
            end_r = start_r + block_size
            start_c = c * block_size
            end_c = start_c + block_size

            block = blocks_list[index]
            if block.shape != (block_size, block_size):
                raise ValueError(
                    f"Incorrect block size {index}: {block.shape}, expected {(block_size, block_size)}")

            reassembled[start_r:end_r, start_c:end_c] = block
            index += 1

    if original_height is not None and original_width is not None:
        return reassembled[:original_height, :original_width]

    return reassembled
