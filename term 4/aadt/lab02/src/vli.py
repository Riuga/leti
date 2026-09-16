import errors

# --- Variable-Length Integer (VLI) coding ----------------------------------
# Values are encoded as a (category, bits) pair: `category` is the number of
# bits the value needs, `bits` is that value in binary. For zero the pair is
# (0, ""). Positive numbers use the plain binary magnitude, while negatives
# use the "one's complement" convention of JPEG: a category-k value in range
# [-2^k+1, -1] is stored as its binary complement within k bits. The category
# (not the value itself) is entropy-coded with Huffman; only the `bits` tail
# is written literally.


def get_vli_category_and_value(integer):
    if integer == 0:
        return 0, ""

    magnitude = abs(integer)
    category = magnitude.bit_length()

    if integer > 0:
        value_bits = bin(magnitude)[2:].zfill(category)
    else:
        temp_val_for_neg = (1 << category) - 1 - magnitude
        value_bits = bin(temp_val_for_neg)[2:].zfill(category)

    return category, value_bits


def decode_vli(category, value_bits_str):
    if category == 0:
        if value_bits_str == "":
            return 0
        else:
            raise ValueError(errors.CATEGORY_ZERO_BITS_MUST_BE_EMPTY)

    if len(value_bits_str) != category:
        raise ValueError(
            f"{errors.BIT_STRING_LENGTH_MISMATCH} ({len(value_bits_str)} vs {category}).")

    value_from_bits = int(value_bits_str, 2)

    sign_threshold = 1 << (category - 1)

    if value_from_bits >= sign_threshold:
        return value_from_bits
    else:
        return value_from_bits - ((1 << category) - 1)


def prepare_dc_coefficient_for_huffman(dc_difference):
    # Get the category and extra bits for encoding
    category, extra_bits = get_vli_category_and_value(dc_difference)
    return category, extra_bits


def prepare_ac_coefficients_for_huffman(rle_encoded_ac):
    result = []
    for run_length, value in rle_encoded_ac:
        # Check for EOB and ZRL
        if (run_length, value) == (0, 0):
            result.append(((0, 0), ""))  # EOB
        elif (run_length, value) == (15, 0):
            result.append(((15, 0), ""))  # ZRL
        elif value != 0:
            # For non-zero coefficients get the category and extra bits
            category, extra_bits = get_vli_category_and_value(value)
            result.append(((run_length, category), extra_bits))

    return result
