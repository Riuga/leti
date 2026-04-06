import matplotlib.pyplot as plt

from lz77 import lz77_encode


def to_bytes(data, encoding: str = 'utf-8') -> bytes:
    if isinstance(data, bytes):
        return data  # Если данные уже в байтах, возвращаем их как есть
    elif isinstance(data, str):
        return data.encode(encoding)  # Преобразуем строку в байты
    elif isinstance(data, (int, float)):
        # Преобразуем числа в строку, затем в байты
        return str(data).encode(encoding)
    elif isinstance(data, (list, tuple, set, dict)):
        # Преобразуем сложные структуры в строку, затем в байты
        return str(data).encode(encoding)
    else:
        raise TypeError(f"Неподдерживаемый тип данных: {type(data)}")


with open("../data/english.txt", 'r', encoding='UTF-8') as file:
    data = file.read()

prepared_data = to_bytes(data)
print(data)


def compression_ratio(original_size, compressed_size):
    return original_size/compressed_size


def test_lz77_compression(data, buffer_sizes):
    ratios = []
    for buffer_size in buffer_sizes:
        print(buffer_size)
        encoded_data = lz77_encode(data, buffer_size)
        ratio = compression_ratio(len(data), len(encoded_data))
        ratios.append(ratio)
        print(f"Buffer size: {buffer_size}, Compression ratio: {ratio:.2f}")
    return ratios


buffer_sizes = [2**i for i in range(0, 20)]

ratios = test_lz77_compression(prepared_data, buffer_sizes)
plt.plot(buffer_sizes, ratios, marker='o', color='orange')
plt.xlabel("Размер буфера")
plt.ylabel("Коэффициент сжатия")
plt.title("Зависимость коэффициента сжатия от размера буфера")
plt.grid(True)
plt.show()
