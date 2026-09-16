import numpy as np
import errors

# --- Zigzag scan ----------------------------------------------------------
# Frequency coefficients are read in a zigzag order: low frequencies carry
# most of the information and tend to be large, high frequencies are mostly
# zeros. Ordering the coefficients from bottom-left to top-right clusters the
# zeros at the end of the row, which makes the subsequent run-length encoding
# much more effective.


def zigzag_scan(block):
    if not isinstance(block, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if block.ndim != 2:
        raise ValueError(errors.MATRIX_NOT_2D)
    h, w = block.shape
    if h != w:
        raise ValueError(errors.BLOCK_MUST_BE_SQUARE)

    n = h
    # Pre-allocate the result
    result = np.empty(n * n, dtype=block.dtype)
    index = 0
    row, col = 0, 0
    going_up = True

    for _ in range(n * n):
        result[index] = block[row, col]  # Fill the result
        index += 1

        # Walk along the diagonals, alternating the direction
        if going_up:
            if col == n - 1:
                row += 1
                going_up = False
            elif row == 0:
                col += 1
                going_up = False
            else:
                row -= 1
                col += 1
        else:
            if row == n - 1:
                col += 1
                going_up = True
            elif col == 0:
                row += 1
                going_up = True
            else:
                row += 1
                col -= 1

    return result


def inverse_zigzag_scan(arr, n):
    if not isinstance(arr, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if arr.ndim != 1:
        raise ValueError(errors.MATRIX_NOT_1D)
    if arr.size != n * n:
        raise ValueError(errors.INPUT_MUST_BE_SQUARE)
    if n <= 0:
        raise ValueError(errors.BLOCK_SIZE_POSITIVE)

    block = np.zeros((n, n), dtype=arr.dtype)
    idx = 0
    row, col = 0, 0
    going_up = True

    for _ in range(n * n):
        block[row, col] = arr[idx]
        idx += 1

        # Walk along the diagonals, alternating the direction
        if going_up:
            if col == n - 1:
                row += 1
                going_up = False
            elif row == 0:
                col += 1
                going_up = False
            else:
                row -= 1
                col += 1
        else:
            if row == n - 1:
                col += 1
                going_up = True
            elif col == 0:
                row += 1
                going_up = True
            else:
                row += 1
                col -= 1

    return block


_ZIGZAG_CACHE = {}


def _zigzag_order(n):
    """Precompute (rows, cols) index arrays in zigzag order for an n x n block."""
    if n not in _ZIGZAG_CACHE:
        grid = np.arange(n * n, dtype=np.int64).reshape(n, n)
        seq = zigzag_scan(grid)
        rows = seq // n
        cols = seq % n
        _ZIGZAG_CACHE[n] = (rows, cols)
    return _ZIGZAG_CACHE[n]


def zigzag_scan_blocks(blocks):
    """Scan a stack of square blocks (B, N, N) into zigzag order (B, N*N)."""
    if not isinstance(blocks, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if blocks.ndim != 3 or blocks.shape[1] != blocks.shape[2]:
        raise ValueError(errors.MATRIX_NOT_2D)

    n = blocks.shape[1]
    rows, cols = _zigzag_order(n)
    idx = np.arange(blocks.shape[0])
    return blocks[idx[:, None], rows[None, :], cols[None, :]]


def inverse_zigzag_scan_blocks(rows_array, n):
    """Restore a stack of zigzag rows (B, N*N) into square blocks (B, N, N)."""
    if not isinstance(rows_array, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if rows_array.ndim != 2:
        raise ValueError(errors.MATRIX_NOT_1D)
    if rows_array.shape[1] != n * n:
        raise ValueError(errors.INPUT_MUST_BE_SQUARE)
    if n <= 0:
        raise ValueError(errors.BLOCK_SIZE_POSITIVE)

    rows, cols = _zigzag_order(n)
    idx = np.arange(rows_array.shape[0])
    blocks = np.zeros((rows_array.shape[0], n, n), dtype=rows_array.dtype)
    blocks[idx[:, None], rows[None, :], cols[None, :]] = rows_array
    return blocks
