import os
import csv
from datetime import datetime

from compressors import *


def select_input_file():
    print('Выберите файл для сжатия:')
    print('1 - enwik7')
    print('2 - текст на русском')
    print('3 - bin файл')
    print('4 - чб изображение')
    print('5 - изображение в серых оттенках')
    print('6 - цветное изображение')
    print('7 - текст на английском')
    choice = int(input())
    print(f'Ваш выбор: {choice}')

    if choice == 1:
        return "enwik7.txt", "enwik7"
    elif choice == 2:
        return "ru.txt", "ru"
    elif choice == 3:
        return "git", "bin"
    elif choice == 4:
        return "bw.bmp", "bw"
    elif choice == 5:
        return "grayscale.bmp", "grayscale"
    elif choice == 6:
        return "color.bmp", "color"
    elif choice == 7:
        return "english.txt", "english"
    else:
        print("Неверный выбор, используется enwik7 по умолчанию")
        return "enwik7", "enwik7"


def get_full_path(base_dir, filename):
    return os.path.join(base_dir, filename)


def run_chain(chain_name, encode_func, decode_func, input_path, compressed_path, decompressed_path):
    print(f"\n=== Цепочка: {chain_name} ===")
    with open(input_path, 'rb') as f:
        original = f.read()

    compressed_data = encode_func(original)
    with open(compressed_path, 'wb') as f:
        f.write(compressed_data)

    with open(compressed_path, 'rb') as f:
        compressed_read = f.read()
    decompressed = decode_func(compressed_read)

    with open(decompressed_path, 'wb') as f:
        f.write(decompressed)

    orig_size = len(original)
    comp_size = len(compressed_data)
    ratio = orig_size / comp_size if comp_size else 0
    correct = (original == decompressed)

    print(f"Исходный размер: {orig_size} байт")
    print(f"Размер после сжатия: {comp_size} байт")
    print(f"Коэффициент сжатия: {ratio:.3f}")
    print(f"Декодированные данные правильные: {correct}")
    print(f"Сжатый файл: {compressed_path}")
    print(f"Восстановленный файл: {decompressed_path}\n")


def run_all_benchmarks():
    """
    Автоматически прогоняет все файлы через все компрессоры.
    Результаты выводятся в консоль и сохраняются в CSV.
    """
    # Определяем все компрессоры: (имя, функция_кодирования, функция_декодирования)
    compressors = []
    # Одиночные алгоритмы (mode=2)
    compressors.append(("HA", huffman_only_encode, huffman_only_decode))
    compressors.append(("BWT", bwt_only_encode, bwt_only_decode))
    compressors.append(("MTF", mtf_only_encode, mtf_only_decode))
    compressors.append(("RLE", rle_only_encode, rle_only_decode))
    compressors.append(("LZ77", lz77_only_encode, lz77_only_decode))
    compressors.append(("LZ78", lz78_only_encode, lz78_only_decode))
    # Цепочки (mode=1)
    compressors.append(
        ("BWT+MTF+RLE+HA", bwt_mtf_rle_ha_encode, bwt_mtf_rle_ha_decode))
    compressors.append(("BWT+RLE", bwt_rle_encode, bwt_rle_decode))
    compressors.append(("BWT+MTF+HA", bwt_mtf_ha_encode, bwt_mtf_ha_decode))
    compressors.append(("LZ77+HA", ha_lz77_encode, ha_lz77_decode))
    compressors.append(("LZ78+HA", ha_lz78_encode, ha_lz78_decode))

    # Список файлов: (номер_выбора, отображаемое_имя, имя_файла, базовое_имя)
    file_choices = [
        ("enwik7", "enwik7.txt", "enwik7"),
        ("ru", "ru.txt", "ru"),
        ("bin", "git", "bin"),
        ("bw", "bw.bmp", "bw"),
        ("grayscale", "grayscale.bmp", "grayscale"),
        ("color", "color.bmp", "color"),
        ("english", "english.txt", "english")
    ]

    base_dir = "../data"
    results = []

    # Создаём папку для результатов, если нужно сохранять сжатые файлы (опционально)
    output_dir = os.path.join(base_dir, "benchmark_output")
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*80)
    print("ЗАПУСК ВСЕХ ТЕСТОВ")
    print("="*80)

    for display_name, filename, base_name in file_choices:
        input_path = get_full_path(base_dir, filename)
        if not os.path.exists(input_path):
            print(f"Пропуск {display_name}: файл {input_path} не найден")
            continue

        with open(input_path, 'rb') as f:
            original = f.read()
        orig_size = len(original)
        print(
            f"\n--- Обработка файла: {display_name} (размер {orig_size} байт) ---")

        for comp_name, enc_func, dec_func in compressors:
            # Кодируем
            try:
                compressed_data = enc_func(original)
            except Exception as e:
                print(f"  Ошибка кодирования {comp_name}: {e}")
                continue

            # Декодируем
            try:
                decompressed = dec_func(compressed_data)
            except Exception as e:
                print(f"  Ошибка декодирования {comp_name}: {e}")
                continue

            correct = (original == decompressed)
            comp_size = len(compressed_data)
            ratio = orig_size / comp_size if comp_size > 0 else 0

            # Сохраняем сжатый и восстановленный файлы (опционально, можно закомментировать)
            safe_comp_name = comp_name.replace("+", "_").replace("-", "_")
            compressed_path = os.path.join(
                output_dir, f"{base_name}_{safe_comp_name}_compressed.bin")
            decompressed_path = os.path.join(
                output_dir, f"{base_name}_{safe_comp_name}_decompressed")
            if '.' in filename:
                ext = filename.split('.')[-1]
                decompressed_path += f".{ext}"
            else:
                decompressed_path += ".bin"

            with open(compressed_path, 'wb') as f:
                f.write(compressed_data)
            with open(decompressed_path, 'wb') as f:
                f.write(decompressed)

            results.append({
                "Файл": display_name,
                "Компрессор": comp_name,
                "Размер_до": orig_size,
                "Размер_после": comp_size,
                "Коэффициент": ratio,
                "Корректно": correct
            })

            # Краткий вывод в консоль
            print(
                f"  {comp_name:20s} : {orig_size:8d} -> {comp_size:8d} байт, коэфф = {ratio:7.3f}, верно={correct}")

    # Вывод итоговой таблицы
    print("\n" + "="*80)
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("="*80)
    # Заголовки
    headers = ["Файл", "Компрессор", "Размер_до",
               "Размер_после", "Коэффициент", "Корректно"]
    # Определяем ширину колонок
    col_widths = {
        "Файл": max(len(r["Файл"]) for r in results) + 2,
        "Компрессор": max(len(r["Компрессор"]) for r in results) + 2,
        "Размер_до": 12,
        "Размер_после": 12,
        "Коэффициент": 10,
        "Корректно": 8
    }
    # Печатаем шапку
    header_line = "|".join([f"{h:^{col_widths[h]}}" for h in headers])
    print(header_line)
    print("-" * len(header_line))
    for r in results:
        line = (f"{r['Файл']:<{col_widths['Файл']}}|"
                f"{r['Компрессор']:<{col_widths['Компрессор']}}|"
                f"{r['Размер_до']:>{col_widths['Размер_до']}}|"
                f"{r['Размер_после']:>{col_widths['Размер_после']}}|"
                f"{r['Коэффициент']:>{col_widths['Коэффициент']}.3f}|"
                f"{str(r['Корректно']):^{col_widths['Корректно']}}")
        print(line)

    # Сохраняем в CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"benchmark_results_{timestamp}.csv"
    csv_path = os.path.join(base_dir, csv_filename)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Файл", "Компрессор", "Размер_до",
                      "Размер_после", "Коэффициент", "Корректно"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "Файл": r["Файл"],
                "Компрессор": r["Компрессор"],
                "Размер_до": r["Размер_до"],
                "Размер_после": r["Размер_после"],
                "Коэффициент": f"{r['Коэффициент']:.3f}",
                "Корректно": r["Корректно"]
            })
    print(f"\nРезультаты также сохранены в файл: {csv_path}")


def main():
    print("Выберите режим:")
    print("1 - Цепочка компрессоров")
    print("2 - Одиночный алгоритм")
    print("3 - Прогнать все файлы через все компрессоры")
    mode = int(input())

    if mode == 3:
        run_all_benchmarks()
        return

    if mode == 1:
        # Существующее меню цепочек
        print("\nВыберите цепочку компрессоров:")
        print("1 - BWT + MTF + RLE + Huffman")
        print("2 - BWT + RLE")
        print("3 - BWT + MTF + HA")
        print("4 - LZ77 + Huffman")
        print("5 - LZ78 + Huffman")
        chain_choice = int(input())
        chains = {
            1: ("BWT+MTF+RLE+HA", bwt_mtf_rle_ha_encode, bwt_mtf_rle_ha_decode),
            2: ("BWT+RLE", bwt_rle_encode, bwt_rle_decode),
            3: ("BWT+MTF+HA", bwt_mtf_ha_encode, bwt_mtf_ha_decode),
            4: ("LZ77+HA", ha_lz77_encode, ha_lz77_decode),
            5: ("LZ78+HA", ha_lz78_encode, ha_lz78_decode)
        }
        if chain_choice not in chains:
            print("Неверный выбор. Выход.")
            return
        chain_name, enc_func, dec_func = chains[chain_choice]
    elif mode == 2:
        print("\nВыберите одиночный алгоритм:")
        print("1 - Huffman")
        print("2 - BWT")
        print("3 - MTF")
        print("4 - RLE")
        print("5 - LZ77")
        print("6 - LZ78")
        algo_choice = int(input())
        algos = {
            1: ("Huffman", huffman_only_encode, huffman_only_decode),
            2: ("BWT", bwt_only_encode, bwt_only_decode),
            3: ("MTF", mtf_only_encode, mtf_only_decode),
            4: ("RLE", rle_only_encode, rle_only_decode),
            5: ("LZ77", lz77_only_encode, lz77_only_decode),
            6: ("LZ78", lz78_only_encode, lz78_only_decode)
        }
        if algo_choice not in algos:
            print("Неверный выбор. Выход.")
            return
        chain_name, enc_func, dec_func = algos[algo_choice]
    else:
        print("Неверный режим. Выход.")
        return

    input_filename, base_name = select_input_file()
    base_dir = "../data"
    input_path = get_full_path(base_dir, input_filename)

    suffix = chain_name.replace("+", "_").replace("-", "_")
    compressed_filename = f"{base_name}_{suffix}_compressed.bin"
    decompressed_filename = f"{base_name}_{suffix}_decompressed"
    if '.' in input_filename:
        ext = input_filename.split('.')[-1]
        decompressed_filename += f".{ext}"
    else:
        decompressed_filename += ".bin"

    compressed_path = get_full_path(base_dir, compressed_filename)
    decompressed_path = get_full_path(base_dir, decompressed_filename)

    run_chain(chain_name, enc_func, dec_func, input_path,
              compressed_path, decompressed_path)


if __name__ == "__main__":
    main()
