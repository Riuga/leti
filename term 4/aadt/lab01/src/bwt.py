def bwt_encode(data, chunk_size=1024):
    """
    Преобразование Барроуза-Уилера (BWT) с разбиением на блоки.
    BWT переставляет символы во входном блоке так, чтобы одинаковые символы
    группировались, что улучшает сжатие последующими алгоритмами (RLE, MTF).
    Алгоритм для каждого чанка:
        1. Создаёт все циклические сдвиги (ротации) исходной строки.
        2. Сортирует их лексикографически.
        3. Запоминает индекс строки, соответствующей исходному порядку.
        4. Берёт последние символы каждой отсортированной ротации — это и есть
           преобразованные данные.
    Поскольку BWT требует O(n²) памяти при наивной реализации (из-за создания всех ротаций),
    разбиение на чанки ограничивает максимальный размер блока.
    Аргументы:
        data: исходные байты
        chunk_size: размер блока в байтах (по умолчанию 1024)
    Возвращает:
        кортеж (transformed_data, indices):
            transformed_data: байты после BWT (склеенные чанки)
            indices: список индексов исходных строк для каждого чанка
    """
    transformed_data = bytearray()
    ind = []
    for start in range(0, len(data), chunk_size):
        chunk = data[start:start + chunk_size]
        index, encoded_chunk = transform_chunk(chunk)
        transformed_data.extend(encoded_chunk)
        ind.append(index)
    return bytes(transformed_data), ind


def transform_chunk(chunk):
    """
    Выполняет BWT над одним блоком (чанком).
    Для строки длины n:
        - Создаёт n ротаций (каждая — сдвиг на 0..n-1).
        - Сортирует ротации как строки.
        - Находит позицию исходной строки в отсортированном списке.
        - Формирует результат из последних символов каждой ротации.
    Аргументы:
        chunk: блок байт (не пустой)
    Возвращает:
        (original_index, encoded_chunk):
            original_index: индекс исходной строки в отсортированных ротациях
            encoded_chunk: байты BWT (длина равна длине chunk)
    """
    rotations = [chunk[i:] + chunk[:i] for i in range(len(chunk))]
    rotations.sort()  # лексикографическая сортировка
    original_index = rotations.index(chunk)
    # последний байт каждой ротации
    encoded_chunk = bytes(rotation[-1] for rotation in rotations)
    return original_index, encoded_chunk


def bwt_decode(encoded_data, indices, chunk_size):
    """
    Обратное преобразование BWT (восстановление исходных данных).
    Для каждого чанка:
        1. Извлекает блок encoded_data длиной chunk_size.
        2. Использует индекс original_index для обратного преобразования.
        3. Склеивает восстановленные чанки.
    Аргументы:
        encoded_data: байты, полученные из bwt_encode (склеенные чанки)
        indices: список индексов для каждого чанка (тот же, что вернул bwt_encode)
        chunk_size: размер блока, использованный при кодировании
    Возвращает:
        восстановленные исходные байты
    """
    restored_data = bytearray()
    position = 0
    index = 0
    while position < len(encoded_data):
        end = position + chunk_size if position + \
            chunk_size <= len(encoded_data) else len(encoded_data)
        chunk = encoded_data[position:end]
        original_index = indices[index]
        restored_chunk = reverse_transform_chunk(original_index, chunk)
        restored_data.extend(restored_chunk)
        position = end
        index += 1
    return bytes(restored_data)


def reverse_transform_chunk(original_index, encoded_chunk):
    """
    Восстанавливает исходный блок по его BWT-представлению и индексу.
    Алгоритм (классический для BWT):
        1. Создаёт список пар (символ, порядковый номер) для стабильной сортировки.
        2. Сортирует эти пары по символу (лексикографически).
        3. Начиная с строки с индексом original_index, многократно переходит
           по ссылке на следующий символ в отсортированной таблице.
        4. Собранные символы в порядке обхода дают исходную строку.
    Аргументы:
        original_index: индекс, под которым исходная строка находилась в отсортированных ротациях
        encoded_chunk: блок после BWT (длина n)
    Возвращает:
        восстановленный исходный блок (bytes длины n)
    """
    # Таблица: каждый элемент — (символ, вспомогательный индекс для стабильности)
    table = [(char, idx) for idx, char in enumerate(encoded_chunk)]
    # сортировка по символу, при равенстве — по индексу (стабильно)
    table.sort()
    result = bytearray()
    current_row = original_index
    for _ in range(len(encoded_chunk)):
        # берём символ и следующий индекс
        char, current_row = table[current_row]
        result.append(char)
    return bytes(result)
