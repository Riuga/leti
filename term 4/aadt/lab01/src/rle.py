def rle_encode(data):
    """
    Сжимает данные с помощью RLE.
    Алгоритм:
        Проходит по входным байтам, подсчитывает длину текущего повтора (run).
        Для каждого повтора:
            - Если длина повтора >= 2, кодирует как (счётчик, байт).
            - Одиночные байты (длина 1) тоже кодируются как (1, байт), что увеличивает размер,
              но упрощает реализацию. Альтернативно можно оставлять как есть, но для единообразия
              используется единый формат.
        Длина повтора ограничена 255 (максимальное значение байта). Если повтор длиннее,
        он разбивается на несколько пар (255, байт) + остаток.
    Формат вывода:
        Последовательность пар (счётчик, байт), где счётчик — число от 1 до 255,
        байт — значение повторяющегося байта.
    Аргументы:
        data: исходные байты
    Возвращает:
        сжатые байты (длина всегда чётная, если data не пуста)
    """
    encoded_data = bytearray()
    n = len(data)
    i = 0
    while i < n:
        # Текущий байт, с которого начинается повтор
        current_char = data[i]
        count = 1
        # Считаем, сколько раз подряд встречается current_byte
        while i + count < n and data[i + count] == current_char and count < 127:
            count += 1
        if count > 1:
            # Записываем пару (счётчик, значение)
            encoded_data.append(count)
            encoded_data.append(current_char)
            # Перемещаем указатель вперёд на длину повтора
            i += count
        else:
            non_repeat_chars = bytearray()
            non_repeat_chars.append(current_char)
            i += 1
            while i < n and (i + 1 >= n or data[i] != data[i + 1]) and len(non_repeat_chars) < 127:
                non_repeat_chars.append(data[i])
                i += 1
            encoded_data.append(0x80 | len(non_repeat_chars))
            encoded_data.extend(non_repeat_chars)
    return bytes(encoded_data)


def rle_decode(encoded_data):
    """
    Восстанавливает исходные данные из сжатых RLE.
    Алгоритм:
        Читает пары (счётчик, байт) и разворачивает их в последовательность
        из счётчик копий байта.
    Аргументы:
        compressed: байты, полученные из rle_encode
    Возвращает:
        исходные байты
    """
    decoded_data = bytearray()
    n = len(encoded_data)
    i = 0
    while i < n:
        control_byte = encoded_data[i]
        i += 1
        if control_byte & 0x80:
            length = control_byte & 0x7F
            decoded_data.extend(encoded_data[i:i + length])
            i += length
        else:
            count = control_byte
            char = encoded_data[i]
            decoded_data.extend([char] * count)
            i += 1
    return bytes(decoded_data)
