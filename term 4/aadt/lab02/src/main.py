from decompressor import decompress_image
from compressor import compress_image
import matplotlib.pyplot as plt
import os
import csv
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
COMPRESSED_DIR = os.path.join(PROJECT_ROOT, 'compressed')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
DECOMPRESSED_DIR = os.path.join(RESULTS_DIR, 'decompressed')
GRAPHS_DIR = os.path.join(RESULTS_DIR, 'graphs')
REPORT_DIR = os.path.join(RESULTS_DIR, 'report')

# Image groups: each input image is stored in several color variants.
# Each group maps the variant label to the file name in DATA_DIR; the group
# name is used as a prefix for all output file names.
IMAGE_GROUPS = [
    ('Lenna', {
        'color': 'Lenna_color.png',
        'grayscale': 'Lenna_grayscale.png',
        'bw': 'Lenna_bw.png',
        'bw_dithering': 'Lenna_bw_dithering.png',
    }),
    ('second', {
        'color': 'color.jpg',
        'grayscale': 'grayscale.jpg',
        'bw': 'bw.jpg',
        'bw_dithering': 'bw dithering.jpg',
    }),
]

# Flat list of (image prefix, variant label, input filename) tuples.
TEST_IMAGES = [
    (prefix, label, filename)
    for prefix, variants in IMAGE_GROUPS
    for label, filename in variants.items()
]

# Quality grid for the size-vs-quality graphs (step is no more than 5).
GRAPH_QUALITIES = list(range(0, 101, 5))
# Qualities required by the assignment for the decompression part.
REPORT_QUALITIES = (0, 20, 40, 60, 80, 100)


def _ensure_dirs():
    for directory in (COMPRESSED_DIR, DECOMPRESSED_DIR, GRAPHS_DIR, REPORT_DIR):
        os.makedirs(directory, exist_ok=True)


def _compressed_path(image_prefix, image_label, quality):
    return os.path.join(COMPRESSED_DIR, f"{image_prefix}_{image_label}_q{quality}.bin")


def _decompressed_path(image_prefix, image_label, quality):
    return os.path.join(DECOMPRESSED_DIR, f"{image_prefix}_{image_label}_q{quality}.png")


def compress_all(qualities):
    """Compress every test image at every quality.

    Returns a dict {(image_prefix, image_label, quality): size_in_bytes}.
    """
    sizes = {}
    for prefix, label, filename in TEST_IMAGES:
        input_path = os.path.join(DATA_DIR, filename)
        for quality in qualities:
            output_path = _compressed_path(prefix, label, quality)
            size = compress_image(input_path, output_path, quality=quality)
            sizes[(prefix, label, quality)] = size
    return sizes


def decompress_all(qualities):
    """Decompress the compressed files of the given qualities."""
    for prefix, label, _ in TEST_IMAGES:
        for quality in qualities:
            output_path = _decompressed_path(prefix, label, quality)
            decompress_image(_compressed_path(prefix, label, quality), output_path)


def write_sizes_csv(sizes):
    """Write a summary CSV with size and compression ratio per image/quality."""
    csv_path = os.path.join(RESULTS_DIR, 'compressed_sizes.csv')
    rows = []
    for prefix, label, filename in TEST_IMAGES:
        original_path = os.path.join(DATA_DIR, filename)
        with Image.open(original_path) as im:
            original_pixels = im.size[0] * im.size[1] * 3
        for quality in GRAPH_QUALITIES:
            size = sizes.get((prefix, label, quality))
            if size:
                rows.append({
                    'image': f'{prefix}_{label}',
                    'quality': quality,
                    'size_bytes': size,
                    'compression_ratio': round(original_pixels / size, 3),
                })

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'image', 'quality', 'size_bytes', 'compression_ratio'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV summary saved: {csv_path}")


def build_graphs(sizes):
    """Build compressed-size-vs-quality graphs (one per image + combined)."""
    for prefix, label, _ in TEST_IMAGES:
        qualities = [q for q in GRAPH_QUALITIES if sizes.get((prefix, label, q))]
        values = [sizes[(prefix, label, q)] / 1024.0 for q in qualities]
        plt.figure(figsize=(8, 5))
        plt.plot(qualities, values, marker='o',
                 linewidth=1.5, color='tab:blue')
        plt.xlabel('Quality factor')
        plt.ylabel('Compressed file size, KB')
        plt.title(f'{prefix}_{label}: compressed size vs quality')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        per_image_path = os.path.join(
            GRAPHS_DIR, f'{prefix}_{label}_compressed_size.png')
        plt.savefig(per_image_path, dpi=150)
        plt.close()
        print(f"Graph saved: {per_image_path}")

    plt.figure(figsize=(9, 6))
    for prefix, label, _ in TEST_IMAGES:
        qualities = [q for q in GRAPH_QUALITIES if sizes.get((prefix, label, q))]
        values = [sizes[(prefix, label, q)] / 1024.0 for q in qualities]
        plt.plot(qualities, values, marker='o', linewidth=1.5,
                 label=f'{prefix}_{label}')
    plt.xlabel('Quality factor')
    plt.ylabel('Compressed file size, KB')
    plt.title('Compressed size vs quality for all test images')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    combined_path = os.path.join(GRAPHS_DIR, 'all_images_compressed_size.png')
    plt.savefig(combined_path, dpi=150)
    plt.close()
    print(f"Graph saved: {combined_path}")


def build_report_montages():
    """Combine the original and the report-quality decompression results
    into a single labelled montage image per test image (for the report)."""
    captions = ['original'] + [f'q{q}' for q in REPORT_QUALITIES]

    for prefix, label, filename in TEST_IMAGES:
        original = Image.open(os.path.join(DATA_DIR, filename)).convert('RGB')
        versions = [original]
        for quality in REPORT_QUALITIES:
            versions.append(
                Image.open(_decompressed_path(prefix, label, quality)).convert('RGB'))

        thumb = 320
        caption_h = 28
        margin = 6
        width = len(versions) * thumb
        height = thumb + caption_h

        canvas = Image.new('RGB', (width, height), 'white')
        try:
            font = ImageFont.load_default(size=18)
        except TypeError:
            font = ImageFont.load_default()

        for idx, (version, caption) in enumerate(zip(versions, captions)):
            version = version.resize((thumb - 2 * margin, thumb - 2 * margin),
                                     Image.LANCZOS)
            canvas.paste(version, (idx * thumb + margin, 0))
            draw = ImageDraw.Draw(canvas)
            draw.text((idx * thumb + margin, thumb + 4), caption,
                      fill='black', font=font)

        montage_path = os.path.join(REPORT_DIR, f'{prefix}_{label}_montage.png')
        canvas.save(montage_path)
        print(f"Montage saved: {montage_path}")


def main():
    _ensure_dirs()
    print("=" * 60)
    print("STEP 1: compressing all test images over the quality grid")
    sizes = compress_all(GRAPH_QUALITIES)
    write_sizes_csv(sizes)

    print("=" * 60)
    print("STEP 2: decompressing report-quality versions")
    decompress_all(REPORT_QUALITIES)

    print("=" * 60)
    print("STEP 3: building size-vs-quality graphs")
    build_graphs(sizes)

    print("=" * 60)
    print("STEP 4: building report montages")
    build_report_montages()

    print("=" * 60)
    print("All steps finished.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
