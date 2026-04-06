class HuffmanNode:
    """
    Узел дерева Хаффмана.
    Хранит символ (если лист), частоту и ссылки на левого и правого потомков.
    """

    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def build_frequency_map(data):
    """
    Подсчитывает частоту каждого байта во входных данных.
    Аргументы:
        data: последовательность байт (bytes)
    Возвращает:
        словарь {байт: частота}
    """
    freq_map = {}
    for byte in data:
        freq_map[byte] = freq_map.get(byte, 0) + 1
    return freq_map


def build_huffman_tree(freq_map):
    """
    Строит дерево Хаффмана на основе карты частот.
    Алгоритм:
        1. Создаёт список листовых узлов для каждого символа.
        2. Пока в списке больше одного узла:
            - извлекает два узла с наименьшими частотами,
            - создаёт родительский узел с суммой их частот,
            - добавляет его обратно в список.
        3. Оставшийся узел — корень дерева.
    Аргументы:
        freq_map: словарь {байт: частота}
    Возвращает:
        корневой узел дерева Хаффмана
    """
    nodes = [HuffmanNode(char=char, freq=freq)
             for char, freq in freq_map.items()]
    while len(nodes) > 1:
        # Сортировка для нахождения двух минимальных частот.
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(freq=left.freq + right.freq,
                             left=left, right=right)
        nodes.append(merged)
    return nodes[0]


def build_code_table(root, code="", code_table=None):
    """
    Рекурсивно обходит дерево Хаффмана и строит таблицу кодов для каждого символа.
    Код формируется из пути: '0' для левого ребра, '1' для правого.
    Аргументы:
        root: текущий узел дерева
        code: накопленный двоичный код (строка из '0' и '1')
        code_table: таблица кодов (заполняется по мере обхода)
    Возвращает:
        словарь {байт: код_бит_в_строке}
    """
    if code_table is None:
        code_table = {}
    if root is not None:
        if root.char is not None:
            code_table[root.char] = code
        build_code_table(root.left, code + "0", code_table)
        build_code_table(root.right, code + "1", code_table)

    return code_table


def huffman_encode(data):
    """
    Сжимает данные алгоритмом Хаффмана.
    Этапы:
        1. Построение частотного словаря.
        2. Построение дерева Хаффмана.
        3. Построение таблицы кодов.
        4. Кодирование каждого байта в битовую строку.
        5. Добавление выравнивающих битов (padding), чтобы длина строки была кратна 8.
        6. Преобразование битовой строки в байты.
    Аргументы:
        data: исходные байты
    Возвращает:
        кортеж (сжатые_байты, таблица_кодов, количество_выравнивающих_битов)
    """
    if not data:
        return b"", {}, 0
    freq_map = build_frequency_map(data)
    root = build_huffman_tree(freq_map)
    code_table = build_code_table(root)
    # Формируем битовую строку для всего сообщения
    encoded_bits = "".join(code_table[byte] for byte in data)
    # Выравнивание: добавляем нули, чтобы длина стала кратной 8
    padding = (8 - len(encoded_bits) % 8)  # кол-во добавленных битов (0..7)
    encoded_bits += "0" * padding
    # Разбиваем на байты и собираем в bytes
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = encoded_bits[i:i + 8]
        encoded_bytes.append(int(byte, 2))

    return bytes(encoded_bytes), code_table, padding


def huffman_decode(encoded_data, code_table, padding):
    """
    Восстанавливает исходные данные из сжатых алгоритмом Хаффмана.
    Аргументы:
        encoded_data: сжатые байты (без таблицы, только кодированные данные)
        code_table: таблица кодов {символ: битовая_строка}
        padding: количество выравнивающих битов, добавленных в конце
    Возвращает:
        исходные байты
    """
    if not encoded_data:
        return b""
    # Преобразуем сжатые байты обратно в битовую строку
    encoded_bits = "".join(f"{byte:08b}" for byte in encoded_data)
    # Удаляем выравнивающие биты
    encoded_bits = encoded_bits[:-padding] if padding > 0 else encoded_bits
    # Строим обратную таблицу: код -> символ
    reverse_code_table = {code: char for char, code in code_table.items()}
    # Декодируем последовательно, накапливая текущий код
    decoded_data = bytearray()
    current_code = ""
    for bit in encoded_bits:
        current_code += bit
        if current_code in reverse_code_table:
            decoded_data.append(reverse_code_table[current_code])
            current_code = ""
    return bytes(decoded_data)
