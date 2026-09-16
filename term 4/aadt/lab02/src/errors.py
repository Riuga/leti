BLOCK_SIZE_POSITIVE = "Block size must be positive."
BLOCK_MUST_BE_SQUARE = "Block must be square."
BLOCK_SIZE_EXCEEDED = "Block size exceeded."

COEFFICIENTS_MUST_BE_SQUARE = "The coefficients must be in a square block."
COEFFICIENT_BLOCK_MATCHES_QUANTIZATION = "The size of the coefficient block and the quantization matrix must match."

INPUT_MUST_BE_SQUARE = "Input must be square."
EMPTY_INPUT = "Input is empty."
NOT_NUMPY_ARRAY = "Input is not an instance of NumPy array."
NOT_A_LIST = "Input must be a list."
WRONG_FORMAT = "Wrong input format."

MATRIX_NOT_1D = "The matrix is not one-dimensional."
MATRIX_NOT_2D = "The matrix is not two-dimensional."

MULTIPLE_OF_BLOCK_SIZE = "The padded size must be a multiple of the block size."
VALUES_MUST_BE_EQUAL_OR_GREATER_THAN_ONE = "Values must be >= 1."
RGB_VALUES_RANGE = "RGB values must be in the correct range [0, 255]."
QUALITY_RANGE = "Quality must be in the range [0, 100]."

BITS_LENGTH_MUST_BE_16 = "The BITS table length must be 16."
BITS_SUM_MISMATCH = "SUM(BITS) does not match len(HUFFVAL)."
BIT_MUST_BE_0_OR_1 = "A bit must be 0 or 1."
NEGATIVE_BIT_COUNT = "Number of bits cannot be negative."
UNEXPECTED_EOF = "Unexpected end of stream."

CATEGORY_ZERO_BITS_MUST_BE_EMPTY = "For category 0 the bit string must be empty."
BIT_STRING_LENGTH_MISMATCH = "Bit-string length does not match the category."

INVALID_FILE_FORMAT = "Invalid file format ('MYJPEG' magic not found)."
HEADER_LENGTH_READ_FAILED = "Failed to read the header length."
HEADER_READ_FAILED = "Failed to read the full header."
COMPONENT_DATA_READ_FAILED = "Failed to read the full compressed component data."
