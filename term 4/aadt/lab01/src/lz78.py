def lz78_encode(data: bytes) -> bytes:
    """
    Сжимает данные алгоритмом LZ78.
    Алгоритм:
        1. Инициализируется пустой словарь. Индексация начинается с 1.
        2. Текущая строка (current_string) накапливается, пока она есть в словаре.
        3. Как только добавление следующего символа приводит к строке, которой нет в словаре:
            - Кодируется пара (индекс предыдущей фразы, последний символ).
              Если предыдущей фразы нет (пустая строка), индекс = 0.
            - Новая фраза добавляется в словарь.
            - Текущая строка сбрасывается.
        4. После цикла, если осталась непустая строка, она кодируется аналогично.
    Формат вывода:
        Для каждой пары:
            - индекс (4 байта, big-endian)
            - символ (1 байт)
        Итоговый поток байтов: (индекс4)(символ)(индекс4)(символ)...
    Аргументы:
        data: исходные байты
    Возвращает:
        сжатые байты
    """
    # ключ: байтовая строка (фраза), значение: индекс (1,2,3...)
    dictionary = {}
    # список пар (индекс, символ)
    output = []
    current_string = bytearray()
    index = 1
    i = 0
    while i < len(data):
        current_string.append(data[i])
        current_bytes = bytes(current_string)
        # Фраза уже есть в словаре — продолжаем наращивать
        if current_bytes in dictionary:
            i += 1
        else:
            # Новая фраза: кодируем как (индекс_предыдущей, последний_символ)
            # current_string[:-1] — это предыдущая фраза (без последнего символа)
            output.append(
                (dictionary.get(bytes(current_string[:-1]), 0), current_string[-1]))
            # Добавляем новую фразу в словарь
            dictionary[current_bytes] = index
            index += 1
            # сброс для следующей фразы
            current_string = bytearray()
            i += 1

    # Обработка остатка, если current_string не пуст (конец данных)
    if current_string:
        output.append(
            (dictionary.get(bytes(current_string[:-1]), 0), current_string[-1]))

    # Упаковка пар в байтовый поток
    compressed_data = bytearray()
    for pair in output:
        index_bytes = pair[0].to_bytes(4, 'big')
        char_bytes = bytes([pair[1]])
        compressed_data.extend(index_bytes + char_bytes)

    return bytes(compressed_data)


def lz78_decode(compressed_data: bytes) -> bytes:
    """
    Восстанавливает исходные данные из сжатых LZ78.
    Алгоритм:
        1. Инициализируется пустой словарь (индексация с 1).
        2. Из входного потока последовательно читаются пары (индекс, символ).
        3. Если индекс == 0, то фраза состоит из одного символа.
           Иначе фраза = словарь[индекс] + символ.
        4. Добавляем восстановленную фразу в словарь.
        5. Выводим фразу в выходной поток.
    Аргументы:
        compressed_data: байты, полученные из lz78_encode
    Возвращает:
        исходные байты
    """
    dictionary = {}
    output = bytearray()
    index = 1
    i = 0

    while i < len(compressed_data):
        # Читаем 4 байта индекса (big-endian)
        index_bytes = compressed_data[i:i + 4]
        current_index = int.from_bytes(index_bytes, 'big')
        i += 4

        # Читаем 1 байт символа
        char_bytes = compressed_data[i:i + 1]
        char = char_bytes[0]
        i += 1

        if current_index == 0:
            # Индекс 0 означает, что фраза состоит только из этого символа
            output.append(char)
            dictionary[index] = bytearray([char])
        else:
            # Иначе фраза = словарь[current_index] + символ
            string_from_dict = dictionary[current_index]
            output.extend(string_from_dict)
            output.append(char)
            dictionary[index] = string_from_dict + bytearray([char])
        index += 1

    return bytes(output)
