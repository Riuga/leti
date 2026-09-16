import io
import errors
# Block encoding/decoding functions
from vli import get_vli_category_and_value, decode_vli

# --- Entropy coding with Huffman tables -----------------------------------
# Huffman coding assigns short codes to frequent symbols and long codes to
# rare ones, which shrinks the total bit count. The tables used here are the
# standard JPEG luminance / chrominance tables (they store for every code
# length how many codes it contains and the list of symbols in order). Codes
# are "canonical": all codes of a given length are consecutive integers,
# which lets the encoder be rebuilt from the BITS + HUFFVAL description alone.
# The bit stream uses JPEG byte stuffing: every literal 0xFF byte is followed
# by a 0x00 byte so that 0xFF can never be mistaken for a marker.
# Each block is written as: Huffman-coded DC category, its VLI bits, then
# Huffman-coded (run, category) AC symbols with their VLI bits.


class HuffmanTable:
    """Generation and use of canonical Huffman codes."""

    def __init__(self, bit_counts, symbols):
        if len(bit_counts) != 16:
            raise ValueError(errors.BITS_LENGTH_MUST_BE_16)
        if sum(bit_counts) != len(symbols):
            raise ValueError(errors.BITS_SUM_MISMATCH)
        self.bit_counts = bit_counts[:]
        self.symbols = symbols[:]
        self.enc_map = {}
        self.dec_map = {}
        self.max_len = 0
        self._build_codes()
        self._build_decoder()

    def get_spec(self):
        return self.bit_counts, self.symbols

    def _build_codes(self):
        code = 0
        code_len = 1
        sym_idx = 0
        total = 0
        for i, cnt in enumerate(self.bit_counts):
            for _ in range(cnt):
                sym = self.symbols[sym_idx]
                self.enc_map[sym] = (code, code_len)
                sym_idx += 1
                code += 1
            total += cnt
            code <<= 1
            code_len += 1
            if cnt > 0:
                self.max_len = i+1
        if total != len(self.symbols):
            print(
                f"Warning: generated {total} codes, expected {len(self.symbols)}")

    def _build_decoder(self):
        for sym, (c, l) in self.enc_map.items():
            b = format(c, f'0{l}b')
            self.dec_map[b] = sym

    def encode(self, symbol):
        return self.enc_map.get(symbol)

    def decode(self, reader):
        buf = ""
        for _ in range(self.max_len):
            bit = reader.read_bit()
            if bit is None:
                return None
            buf += str(bit)
            if buf in self.dec_map:
                return self.dec_map[buf]
        return None


class BitWriter:
    """JPEG bit writing with byte stuffing."""

    def __init__(self):
        self._acc = 0
        self._pos = 0
        self._out = bytearray()

    def write_bit(self, b):
        if b not in (0, 1):
            raise ValueError(errors.BIT_MUST_BE_0_OR_1)
        self._acc = (self._acc << 1) | b
        self._pos += 1
        if self._pos == 8:
            self._flush()

    def write_bits(self, val, n):
        if n < 0:
            raise ValueError(errors.NEGATIVE_BIT_COUNT)
        for i in range(n-1, -1, -1):
            self.write_bit((val >> i) & 1)

    def _flush(self):
        byte = self._acc & 0xFF
        self._out.append(byte)
        if byte == 0xFF:
            self._out.append(0x00)
        self._acc = 0
        self._pos = 0

    def finish(self):
        if self._pos > 0:
            pad = 8-self._pos
            self._acc = (self._acc << pad) | ((1 << pad)-1)
            self._flush()
        return bytes(self._out)


class BitReader:
    """JPEG bit reading with byte-de-stuffing."""

    def __init__(self, data):
        self._stream = io.BytesIO(data)
        self._cur = 0
        self._bit = 8
        self._eom = False

    def _load(self):
        if self._eom:
            return False
        b = self._stream.read(1)
        if not b:
            self._eom = True
            return False
        v = b[0]
        if v == 0xFF:
            nxt = self._stream.read(1)
            if not nxt:
                self._eom = True
                return False
            if nxt[0] == 0x00:
                self._cur = 0xFF
                self._bit = 0
                return True
            else:
                self._stream.seek(-2, 1)
                self._eom = True
                return False
        else:
            self._cur = v
            self._bit = 0
            return True

    def read_bit(self):
        if self._bit > 7 and not self._load():
            return None
        b = (self._cur >> (7-self._bit)) & 1
        self._bit += 1
        return b

    def read_bits(self, n):
        if n < 0:
            raise ValueError(errors.NEGATIVE_BIT_COUNT)
        v = 0
        for _ in range(n):
            bit = self.read_bit()
            if bit is None:
                raise EOFError(errors.UNEXPECTED_EOF)
            v = (v << 1) | bit
        return v


def huff_encode_blocks(units, dc_tbl, ac_tbl):
    writer = BitWriter()
    for dc_cat, dc_bits, ac_pairs in units:
        code, length = dc_tbl.encode(dc_cat) or (None, None)
        if code is None:
            raise ValueError(f"DC symbol {dc_cat} not in table")
        writer.write_bits(code, length)
        if dc_cat > 0:
            val = int(dc_bits, 2)
            writer.write_bits(val, dc_cat)
        for run, val in ac_pairs:
            if (run, val) == (0, 0):
                sym = 0x00
                c, l = ac_tbl.encode(sym)
                writer.write_bits(c, l)
                break
            if (run, val) == (15, 0):
                sym = 0xF0
                c, l = ac_tbl.encode(sym)
                writer.write_bits(c, l)
            else:
                cat, bits = get_vli_category_and_value(val)
                sym = (run << 4) | cat
                c, l = ac_tbl.encode(sym) or (None, None)
                if c is None:
                    raise ValueError(f"AC symbol {sym:02X} not in table")
                writer.write_bits(c, l)
                writer.write_bits(int(bits, 2), cat)
    return writer.finish()


def huff_decode_blocks(data, dc_tbl, ac_tbl, blocks):
    reader = BitReader(data)
    out = []
    for i in range(blocks):
        dc_cat = dc_tbl.decode(reader)
        if dc_cat is None:
            raise EOFError(f"DC at block {i+1}")
        dc_bits = ""
        if dc_cat > 0:
            v = reader.read_bits(dc_cat)
            dc_bits = format(v, f'0{dc_cat}b')
        ac_list = []
        cnt = 0
        while cnt < 64:
            sym = ac_tbl.decode(reader)
            if sym is None:
                raise EOFError(f"AC at blk {i+1}")
            if sym == 0x00:
                ac_list.append((0, 0))
                break
            if sym == 0xF0:
                ac_list.append((15, 0))
                cnt += 16
                continue
            run = sym >> 4
            cat = sym & 0xF
            v = reader.read_bits(cat)
            bits = format(v, f'0{cat}b')
            val = decode_vli(cat, bits)
            ac_list.append((run, val))
            cnt += run+1
            if cnt > 63:
                print(f"Warn: ACcount {cnt}>63 blk{i+1}")
        out.append((dc_cat, dc_bits, ac_list))
    return out
