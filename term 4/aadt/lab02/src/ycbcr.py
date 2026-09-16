import numpy as np
import errors

# --- Color conversion RGB -> YCbCr ----------------------------------------
# YCbCr separates the image into one luma channel (Y) and two chroma
# channels (Cb, Cr). The human eye is far more sensitive to brightness than
# to color, so the chroma channels can be stored at half resolution (see
# downsampling.py) almost without visible loss. The RGB->YCbCr coefficients
# below follow the standard ITU-R BT.601 formula; Cb and Cr are biased by
# +128 so they fit the 0..255 range like plain 8-bit samples. The reverse
# conversion is applied after decompression.


def rgb_to_ycbcr(image_rgb):
    if not isinstance(image_rgb, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
        raise ValueError(errors.WRONG_FORMAT)
    if image_rgb.dtype != np.uint8 and (np.any(image_rgb < 0) or np.any(image_rgb > 255)):
        print(errors.RGB_VALUES_RANGE)

    image_rgb_float = image_rgb.astype(np.float32)

    r = image_rgb_float[:, :, 0]
    g = image_rgb_float[:, :, 1]
    b = image_rgb_float[:, :, 2]

    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.168736 * r - 0.331264 * g + 0.5 * b + 128.0
    cr = 0.5 * r - 0.418688 * g - 0.081312 * b + 128.0

    image_ycbcr = np.zeros_like(image_rgb_float)
    image_ycbcr[:, :, 0] = y
    image_ycbcr[:, :, 1] = cb
    image_ycbcr[:, :, 2] = cr

    image_ycbcr = np.clip(image_ycbcr, 0, 255)

    return image_ycbcr.astype(np.uint8)


def ycbcr_to_rgb(image_ycbcr):
    if not isinstance(image_ycbcr, np.ndarray):
        raise TypeError(errors.NOT_NUMPY_ARRAY)
    if image_ycbcr.ndim != 3 or image_ycbcr.shape[2] != 3:
        raise ValueError(errors.WRONG_FORMAT)

    image_ycbcr_float = image_ycbcr.astype(np.float32)

    y = image_ycbcr_float[:, :, 0]
    cb = image_ycbcr_float[:, :, 1]
    cr = image_ycbcr_float[:, :, 2]

    r = y + 1.402 * (cr - 128.0)
    g = y - 0.344136 * (cb - 128.0) - 0.714136 * (cr - 128.0)
    b = y + 1.772 * (cb - 128.0)

    image_rgb = np.zeros_like(image_ycbcr_float)
    image_rgb[:, :, 0] = r
    image_rgb[:, :, 1] = g
    image_rgb[:, :, 2] = b

    image_rgb = np.clip(image_rgb, 0, 255)

    return image_rgb.astype(np.uint8)
