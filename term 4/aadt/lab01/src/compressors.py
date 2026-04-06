import pickle

from bwt import bwt_encode, bwt_decode
from mtf import mtf_encode, mtf_decode
from rle import rle_encode, rle_decode
from ha import huffman_encode, huffman_decode
from lz77 import lz77_encode, lz77_decode
from lz78 import lz78_encode, lz78_decode


def bwt_mtf_rle_ha_encode(data: bytes) -> bytes:
    bwt_data, indices = bwt_encode(data)
    mtf_data = mtf_encode(bwt_data)
    rle_data = rle_encode(mtf_data)
    ha_data, code_table, padding = huffman_encode(rle_data)

    metadata = {
        'indices': indices,
        'code_table': code_table,
        'padding': padding,
        'chunk_size': 1024
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + ha_data


def bwt_mtf_rle_ha_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    ha_data = compressed[4 + meta_len:]

    indices = metadata['indices']
    code_table = metadata['code_table']
    padding = metadata['padding']
    chunk_size = metadata.get('chunk_size', 1024)

    rle_data = huffman_decode(ha_data, code_table, padding)
    mtf_data = rle_decode(rle_data)
    bwt_data = mtf_decode(mtf_data)
    original = bwt_decode(bwt_data, indices, chunk_size)
    return original


def bwt_mtf_ha_encode(data: bytes) -> bytes:
    bwt_data, indices = bwt_encode(data)
    mtf_data = mtf_encode(bwt_data)
    ha_data, code_table, padding = huffman_encode(mtf_data)

    metadata = {
        'indices': indices,
        'code_table': code_table,
        'padding': padding,
        'chunk_size': 1024
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + ha_data


def bwt_mtf_ha_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    ha_data = compressed[4 + meta_len:]

    indices = metadata['indices']
    code_table = metadata['code_table']
    padding = metadata['padding']
    chunk_size = metadata.get('chunk_size', 1024)

    mtf_data = huffman_decode(ha_data, code_table, padding)
    bwt_data = mtf_decode(mtf_data)
    original = bwt_decode(bwt_data, indices, chunk_size)
    return original


def bwt_rle_encode(data: bytes) -> bytes:
    bwt_data, indices = bwt_encode(data)
    rle_data = rle_encode(bwt_data)

    metadata = {
        'indices': indices,
        'chunk_size': 1024
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + rle_data


def bwt_rle_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    rle_data = compressed[4 + meta_len:]

    bwt_data = rle_decode(rle_data)
    indices = metadata['indices']
    chunk_size = metadata.get('chunk_size', 1024)
    original = bwt_decode(bwt_data, indices, chunk_size)
    return original


def ha_lz77_encode(data: bytes) -> bytes:
    lz77_data = lz77_encode(data)
    ha_data, code_table, padding = huffman_encode(lz77_data)

    metadata = {
        'code_table': code_table,
        'padding': padding
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + ha_data


def ha_lz77_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    ha_data = compressed[4 + meta_len:]

    code_table = metadata['code_table']
    padding = metadata['padding']
    lz77_data = huffman_decode(ha_data, code_table, padding)
    original = lz77_decode(lz77_data)
    return original


def ha_lz78_encode(data: bytes) -> bytes:
    lz78_data = lz78_encode(data)
    ha_data, code_table, padding = huffman_encode(lz78_data)

    metadata = {
        'code_table': code_table,
        'padding': padding
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + ha_data


def ha_lz78_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    ha_data = compressed[4 + meta_len:]

    code_table = metadata['code_table']
    padding = metadata['padding']
    lz78_data = huffman_decode(ha_data, code_table, padding)
    original = lz78_decode(lz78_data)
    return original


def huffman_only_encode(data: bytes) -> bytes:
    ha_data, code_table, padding = huffman_encode(data)
    metadata = {
        'code_table': code_table,
        'padding': padding
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + ha_data


def huffman_only_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    ha_data = compressed[4 + meta_len:]
    code_table = metadata['code_table']
    padding = metadata['padding']
    return huffman_decode(ha_data, code_table, padding)


def bwt_only_encode(data: bytes) -> bytes:
    bwt_data, indices = bwt_encode(data)
    metadata = {
        'indices': indices,
        'chunk_size': 1024
    }
    meta_bytes = pickle.dumps(metadata)
    return len(meta_bytes).to_bytes(4, 'big') + meta_bytes + bwt_data


def bwt_only_decode(compressed: bytes) -> bytes:
    meta_len = int.from_bytes(compressed[:4], 'big')
    metadata = pickle.loads(compressed[4:4 + meta_len])
    bwt_data = compressed[4 + meta_len:]
    indices = metadata['indices']
    chunk_size = metadata.get('chunk_size', 1024)
    return bwt_decode(bwt_data, indices, chunk_size)


def mtf_only_encode(data: bytes) -> bytes:
    return mtf_encode(data)


def mtf_only_decode(compressed: bytes) -> bytes:
    return mtf_decode(compressed)


def rle_only_encode(data: bytes) -> bytes:
    return rle_encode(data)


def rle_only_decode(compressed: bytes) -> bytes:
    return rle_decode(compressed)


def lz77_only_encode(data: bytes) -> bytes:
    return lz77_encode(data)


def lz77_only_decode(compressed: bytes) -> bytes:
    return lz77_decode(compressed)


def lz78_only_encode(data: bytes) -> bytes:
    return lz78_encode(data)


def lz78_only_decode(compressed: bytes) -> bytes:
    return lz78_decode(compressed)
