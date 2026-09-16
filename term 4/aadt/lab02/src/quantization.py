import numpy as np
import errors

# --- Quantization ---------------------------------------------------------
# This is the lossy step of the codec. Every DCT coefficient is divided by a
# weight from an 8x8 quantization matrix and rounded. Small weights keep the
# important low frequencies almost untouched; large weights crush the
# high-frequency detail that is barely visible anyway. The coefficients are
# scaled by the quality factor using the standard JPEG formula, and the
# adjusted matrix is clamped to 1..255. Dequantization (multiplying back) is
# only an approximation of the original coefficients, which is why quantized
# images are never lossless.


def adjust_quantization_matrix(base_matrix, quality_factor):
    if not isinstance(base_matrix, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if not (0 <= quality_factor <= 100):
        raise ValueError(errors.QUALITY_RANGE)

    # Clamp the quality factor if it goes beyond the valid range
    quality_factor = min(max(quality_factor, 0), 100)
    # Quality 0 is not defined by the scaling formula, so use the
    # coarsest valid value (1) to compute the scale factor.
    scale_quality = max(quality_factor, 1)

    base_matrix_float = base_matrix.astype(np.float64)

    # Compute the scaling coefficient depending on the quality
    if scale_quality < 50:
        scale_factor = 5000.0 / scale_quality
    else:
        scale_factor = 200.0 - 2.0 * scale_quality

    adjusted_matrix_float = (base_matrix_float * scale_factor + 50.0) / 100.0
    adjusted_matrix_int = np.floor(adjusted_matrix_float)

    # Clamp the values to the range from 1 to 255
    adjusted_matrix_int[adjusted_matrix_int < 1] = 1
    adjusted_matrix_int[adjusted_matrix_int > 255] = 255

    return adjusted_matrix_int.astype(np.uint8)


def quantize(dct_coeffs_block, quantization_matrix):
    if dct_coeffs_block.shape != quantization_matrix.shape:
        raise ValueError(errors.COEFFICIENT_BLOCK_MATCHES_QUANTIZATION)
    if not np.all(quantization_matrix >= 1):
        raise ValueError(errors.VALUES_MUST_BE_EQUAL_OR_GREATER_THAN_ONE)

    # Convert the DCT coefficients to float64 for accuracy when dividing
    dct_coeffs_block_float = dct_coeffs_block.astype(np.float64)

    # Perform the quantization
    quantized_coeffs = np.round(
        dct_coeffs_block_float / quantization_matrix.astype(np.float64))

    # Return the result as int32
    return quantized_coeffs.astype(np.int32)


def quantize_blocks(dct_coeffs_blocks, quantization_matrix):
    """Quantize a stack of DCT coefficient blocks of shape (B, N, N)."""
    if dct_coeffs_blocks.shape[1:] != quantization_matrix.shape:
        raise ValueError(errors.COEFFICIENT_BLOCK_MATCHES_QUANTIZATION)
    if not np.all(quantization_matrix >= 1):
        raise ValueError(errors.VALUES_MUST_BE_EQUAL_OR_GREATER_THAN_ONE)

    quantized = np.round(
        dct_coeffs_blocks.astype(np.float64) /
        quantization_matrix.astype(np.float64))

    return quantized.astype(np.int32)


def dequantize_blocks(quantized_coeffs_blocks, quantization_matrix):
    """Dequantize a stack of quantized coefficient blocks of shape (B, N, N)."""
    if quantized_coeffs_blocks.shape[1:] != quantization_matrix.shape:
        raise ValueError(errors.COEFFICIENT_BLOCK_MATCHES_QUANTIZATION)

    dequantized = (quantized_coeffs_blocks.astype(np.float64) *
                   quantization_matrix.astype(np.float64))

    return dequantized


def dequantize(quantized_coeffs_block, quantization_matrix):
    if quantized_coeffs_block.shape != quantization_matrix.shape:
        raise ValueError(errors.COEFFICIENT_BLOCK_MATCHES_QUANTIZATION)

    # Convert the quantized coefficients and the quantization matrix to
    # float64 for accuracy during the computations
    quantized_coeffs_block_float = quantized_coeffs_block.astype(np.float64)
    quantization_matrix_float = quantization_matrix.astype(np.float64)

    # Perform the de-quantization
    dequantized_coeffs = quantized_coeffs_block_float * quantization_matrix_float

    # Return the result as float64 for accuracy
    return dequantized_coeffs
