"""
Tim tat ca hash algorithm cho CommonActions entry.
Fix lai cach scan entries.
"""
import sys, struct, binascii, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

data = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle').read_bytes()

# CA entry la tai offset 0x1730 (length=58) -> path tai 0x1734
# Hash tai 0x1734 + 58 + pad(58%4=2 -> pad=2) = 0x1734+60 = 0x1770
ca_len_offset = 0x1730
ca_path_offset = 0x1734
ca_path = data[ca_path_offset:ca_path_offset+58]
pad = (4 - (58 % 4)) % 4
ca_hash_offset = ca_path_offset + 58 + pad
ca_hash = data[ca_hash_offset:ca_hash_offset+8]

print(f"CA path: {ca_path.decode()}")
print(f"Hash offset: 0x{ca_hash_offset:05X}")
print(f"Hash (8 bytes): {ca_hash.hex()}")
print(f"As two LE uint32: {struct.unpack_from('<II', ca_hash)}")
print(f"As LE uint64: {struct.unpack_from('<Q', ca_hash)[0]}")

# Count at 0x16E0
count_offset = 0x16E0
count = struct.unpack_from('<I', data, count_offset)[0]
print(f"\nArray count at 0x{count_offset:X}: {count}")

# Test hash algorithms on original CommonActions
ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
ca_data = ca_file.read_bytes()
print(f"CommonActions size: {len(ca_data)}")

target = ca_hash.hex()
print(f"Target hash: {target}")

try:
    import xxhash
    algorithms = {
        'xxh64':         xxhash.xxh64(ca_data).digest(),
        'xxh64_seed1':   xxhash.xxh64(ca_data, seed=1).digest(),
        'xxh32_x2':      xxhash.xxh32(ca_data).digest() * 2,
        'xxh3_64':       xxhash.xxh3_64(ca_data).digest(),
        'xxh3_128_lo':   xxhash.xxh3_128(ca_data).digest()[:8],
        'xxh3_128_hi':   xxhash.xxh3_128(ca_data).digest()[8:],
    }
    for name, h in algorithms.items():
        match = "<<< MATCH!" if h.hex() == target else ""
        print(f"  {name:20s}: {h.hex()} {match}")
except ImportError:
    print("xxhash not available")

# Standard
std = {
    'md5[:8]':   hashlib.md5(ca_data).digest()[:8],
    'md5[8:]':   hashlib.md5(ca_data).digest()[8:],
    'sha1[:8]':  hashlib.sha1(ca_data).digest()[:8],
    'sha256[:8]':hashlib.sha256(ca_data).digest()[:8],
    'crc32+sz':  struct.pack('<II', binascii.crc32(ca_data)&0xFFFFFFFF, len(ca_data)),
    'sz+crc32':  struct.pack('<II', len(ca_data), binascii.crc32(ca_data)&0xFFFFFFFF),
}
for name, h in std.items():
    match = "<<< MATCH!" if h.hex() == target else ""
    print(f"  {name:20s}: {h.hex()} {match}")

# FNV-1a 64
def fnv1a_64(d):
    h = 14695981039346656037
    for b in d: h = ((h ^ b) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

fnv = struct.pack('<Q', fnv1a_64(ca_data))
match = "<<< MATCH!" if fnv.hex() == target else ""
print(f"  {'fnv1a_64':20s}: {fnv.hex()} {match}")

# MurmurHash3
try:
    import mmh3
    m3 = struct.pack('<q', mmh3.hash64(ca_data)[0])
    match = "<<< MATCH!" if m3.hex() == target else ""
    print(f"  {'murmur3_64':20s}: {m3.hex()} {match}")
except ImportError:
    print("  mmh3 not available")

# Now check another entry to correlate - Behaviac.pkg.bytes (hash=01b7d018489038be)
# Find Behaviac
beh_pattern = b"Behaviac.pkg.bytes"
beh_idx = data.find(beh_pattern)
if beh_idx > 0:
    beh_len_offset = beh_idx - 4
    beh_len = struct.unpack_from('<I', data, beh_len_offset)[0]
    beh_pad = (4 - (beh_len % 4)) % 4
    beh_hash_off = beh_idx + beh_len + beh_pad
    beh_hash = data[beh_hash_off:beh_hash_off+8]
    print(f"\nBehaviac.pkg.bytes hash: {beh_hash.hex()}")
    print(f"As uint64 LE: {struct.unpack_from('<Q', beh_hash)[0]}")

# Also check the SysEvent entry
sys_pattern = b"Ages/Actions/SysEvent.pkg.bytes"
sys_idx = data.find(sys_pattern)
if sys_idx > 0:
    sys_len_offset = sys_idx - 4
    sys_len = struct.unpack_from('<I', data, sys_len_offset)[0]
    sys_pad = (4 - (sys_len % 4)) % 4
    sys_hash_off = sys_idx + sys_len + sys_pad
    sys_hash = data[sys_hash_off:sys_hash_off+8]
    print(f"\nSysEvent.pkg.bytes hash: {sys_hash.hex()}")
    # Do these files exist?
    for f in [
        Path(r'C:\Users\b0ydeptrai\Downloads\zin\Behaviac.pkg.bytes'),
        Path(r'C:\Users\b0ydeptrai\Downloads\zin\SysEvent.pkg.bytes'),
    ]:
        if f.exists():
            print(f"Found {f.name}")
