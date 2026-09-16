import numpy as np
import errors

# --- Discrete Cosine Transform (DCT-II) -----------------------------------
# Each 8x8 block of samples is converted from the spatial domain into the
# frequency domain. The energy of a typical photo concentrates in the
# low-frequency (top-left) coefficients, so the rest can be strongly
# quantized without visible damage. The transform is separable: a 2D DCT is
# just a 1D DCT applied to rows and then to columns, written as
#        F = 0.25 * scale .* ( T @ block @ T.T )
# with the matrix T built from cosines and `scale` holding the C(k) factors
# (1/sqrt(2) for k=0, 1 otherwise). The inverse transform restores the block
# samples. T and scale are the same for every block, so they are cached.

_T_CACHE = {}


def _c_factor(k):
    return 1.0 / np.sqrt(2) if k == 0 else 1.0


def _build_dct_matrix(size):
    n = np.arange(size)
    k = n.reshape(-1, 1)
    return np.cos((2 * n + 1) * k * np.pi / (2 * size))


def _dct_tables(size):
    if size not in _T_CACHE:
        T = _build_dct_matrix(size)
        C = np.array([_c_factor(i) for i in range(size)])
        scale = np.outer(C, C)
        _T_CACHE[size] = (T, scale)
    return _T_CACHE[size]


def dct2(block):
    if block.ndim != 2 or block.shape[0] != block.shape[1]:
        raise ValueError(errors.BLOCK_MUST_BE_SQUARE)

    N = block.shape[0]
    block = block.astype(np.float64)
    if block.dtype == np.uint8:
        block -= 128

    T, scale = _dct_tables(N)
    dct_core = T @ block @ T.T

    return 0.25 * scale * dct_core


def idct2(coeffs):
    if coeffs.ndim != 2 or coeffs.shape[0] != coeffs.shape[1]:
        raise ValueError(errors.COEFFICIENTS_MUST_BE_SQUARE)

    N = coeffs.shape[0]
    T, scale = _dct_tables(N)

    restored = T.T @ (coeffs * scale) @ T
    return 0.25 * restored


def dct2_matrix(block):
    N = block.shape[0]
    if block.shape[1] != N:
        raise ValueError(errors.BLOCK_MUST_BE_SQUARE)

    block = block.astype(np.float64)
    if block.dtype == np.uint8:
        block -= 128

    T, scale = _dct_tables(N)
    dct_unscaled = T @ block @ T.T

    return 0.25 * scale * dct_unscaled


def idct2_matrix(dct_coeffs):
    N = dct_coeffs.shape[0]
    if dct_coeffs.shape[1] != N:
        raise ValueError(errors.COEFFICIENTS_MUST_BE_SQUARE)

    T, scale = _dct_tables(N)

    S_prime = scale * dct_coeffs
    restored = T.T @ S_prime @ T

    return 0.25 * restored


def dct2_blocks(blocks):
    """Apply a 2D DCT-II to a stack of square blocks of shape (B, N, N)."""
    if blocks.ndim != 3 or blocks.shape[1] != blocks.shape[2]:
        raise ValueError(errors.COEFFICIENTS_MUST_BE_SQUARE)

    N = blocks.shape[1]
    blocks = blocks.astype(np.float64)
    T, scale = _dct_tables(N)
    core = np.einsum('ij,bjk,kl->bil', T, blocks, T.T)

    return 0.25 * scale * core


def idct2_blocks(coeffs):
    """Apply an inverse 2D DCT to a stack of square blocks of shape (B, N, N)."""
    if coeffs.ndim != 3 or coeffs.shape[1] != coeffs.shape[2]:
        raise ValueError(errors.COEFFICIENTS_MUST_BE_SQUARE)

    N = coeffs.shape[1]
    T, scale = _dct_tables(N)
    scaled = coeffs.astype(np.float64) * scale
    restored = np.einsum('ia,bik,kl->bal', T, scaled, T)

    return 0.25 * restored
