import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from math import log2

from bwt import bwt_decode, bwt_encode
from mtf import mtf_decode, mtf_encode


def calculate_entropy(data):
    """
    Вычисляет энтропию Шеннона для последовательности байтов.

    Энтропия измеряет среднее количество информации (в битах) на символ.
    Формула: H = -Σ p_i * log2(p_i), где p_i — вероятность i-го символа.

    Аргументы:
        data: входные байты

    Возвращает:
        значение энтропии (float). Для пустых данных возвращает 0.
    """
    if not data:
        return 0
    # Подсчёт частот каждого байта
    counter = Counter(data)
    # Длина данных (количество символов)
    probabilities = [count / len(data) for count in counter.values()]
    # Вычисление энтропии: сумма по всем символам
    entropy = -sum(p * log2(p) for p in probabilities)
    return entropy


def analyze_bwt_mtf_entropy(file_path, block_sizes):
    """
    Анализирует влияние размера блока BWT на энтропию после применения BWT+MTF.

    Для каждого размера блока:
        1. Применяет BWT к исходным данным с заданным chunk_size.
        2. Применяет MTF к результату BWT.
        3. Вычисляет энтропию полученных данных.
        4. Проверяет корректность обратного преобразования (декодирования).
    Строит график зависимости энтропии от размера блока.

    Аргументы:
        file_path: путь к файлу с исходными данными (бинарный режим)
        block_sizes: список размеров блоков (в байтах) для тестирования
    """
    # Чтение всего файла в байтовую строку
    with open(file_path, 'rb') as f:
        data = f.read()
    print(f'размер файла: {len(data)}')
    entropy_values = []
    for chunk_size in block_sizes:
        # 1. BWT-преобразование с разбиением на блоки указанного размера
        bwt_data, ind = bwt_encode(data, chunk_size)
        print(bwt_data)
        mtf_data = mtf_encode(bwt_data)
        print(mtf_data)
        # 2. Расчёт энтропии после BWT+MTF
        entropy = calculate_entropy(mtf_data)
        entropy_values.append(entropy)
        print(f"Block size: {chunk_size}, Entropy: {entropy}")
        # 3. Проверка возможности обратного восстановления (корректность)
        mtf_decoded = mtf_decode(mtf_data)
        bwt_decoded = bwt_decode(mtf_decoded, ind, chunk_size)
        if bwt_decoded == data:
            print(f"Block size {chunk_size}: Data restored correctly.")
        else:
            print(f"Block size {chunk_size}: Data restoration failed!")

    plt.plot(block_sizes, entropy_values, marker='o', color='orange')
    plt.xlabel('Размер блока (в байтах)')
    plt.ylabel('Энтропия')
    plt.title('Зависимость энтропии от размера блока')
    plt.grid(True)
    plt.show()


file_path = "../data/enwik7.txt"
block_sizes = [x for x in range(500, 15000, 1000)]

analyze_bwt_mtf_entropy(file_path, block_sizes)
