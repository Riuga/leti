import numpy as np
import errors

# --- DPCM on the DC coefficients ------------------------------------------
# The top-left coefficient of every block (DC) stores the block's average
# brightness. Neighbouring blocks usually have very similar averages, so the
# raw values are replaced by the differences with the previous block
# (DPCM). The differences are much smaller numbers and therefore need fewer
# bits, further improving the compression. The first difference is taken
# against a zero predictor, exactly as in JPEG. Decoding simply adds the
# differences back together.


def dpcm_encode_dc(dc_coefficients):
    if not isinstance(dc_coefficients, (list, np.ndarray)):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if len(dc_coefficients) == 0:
        return []

    dc_coeffs = np.array(dc_coefficients, dtype=np.int32)
    diff_dc = np.empty_like(dc_coeffs)

    # Initialize the prediction for the first DC coefficient (equals 0 for the first block in JPEG).
    pred_dc = 0
    diff_dc[0] = dc_coeffs[0] - pred_dc

    # Differential encoding for the remaining coefficients.
    for i in range(1, len(dc_coeffs)):
        diff_dc[i] = dc_coeffs[i] - dc_coeffs[i - 1]

    return diff_dc.tolist()


def dpcm_decode_dc(diff_dc_coefficients):
    if not isinstance(diff_dc_coefficients, (list, np.ndarray)):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if len(diff_dc_coefficients) == 0:
        return []

    diff_dc_coeffs = np.array(diff_dc_coefficients, dtype=np.int32)
    dc_coeffs = np.empty_like(diff_dc_coeffs)

    # Restore the first coefficient (the predictor is assumed to be 0).
    pred_dc = 0
    dc_coeffs[0] = diff_dc_coeffs[0] + pred_dc

    # Restore the remaining coefficients.
    for i in range(1, len(diff_dc_coeffs)):
        dc_coeffs[i] = dc_coeffs[i - 1] + diff_dc_coeffs[i]

    return dc_coeffs.tolist()
