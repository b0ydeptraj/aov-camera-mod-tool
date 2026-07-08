"""
Phan tich toan bo cau truc du lieu trong verification bundle
Tim tat ca cac vi tri co the lien quan den CommonActions
"""
import sys, struct
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

verif = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle').read_bytes()
res   = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resources.assets').read_bytes()

# === Part 1: Dump ALL int32 count candidates in verification file
# Tim tat ca vi tri co count >= 10 theo sau la du lieu look like entries

print("=" * 60)
print("Part 1: Full hex dump of verification data block")
print("=" * 60)

# UnityFS structure
magic = verif[:8]
print(f"Magic: {magic}")
# Header: magic(8) + version(4) + unity_version_str + unity_revision_str + size(8) + compressed_size(4) + uncompressed_size(4) + flags(4)
# Sau header la block info (compressed)
# Data block bat dau sau header + block_info

# Tim tat ca string "pkg.bytes" de biet range cua data
needle = b"pkg.bytes"
positions = []
start = 0
while True:
    idx = verif.find(needle, start)
    if idx < 0: break
    positions.append(idx)
    start = idx + 1

print(f"\nFound {len(positions)} 'pkg.bytes' occurrences in verification file")
print(f"First at: 0x{positions[0]:05X}")
print(f"Last at:  0x{positions[-1]:05X}")

# Tim range du lieu chinh
first_entry_area = positions[0] - 30
last_entry_area  = positions[-1] + 50
print(f"Data range: 0x{first_entry_area:05X} - 0x{last_entry_area:05X}")

# Tim tat ca int32 truoc first entry - do can biet cau truc MonoBehaviour
print("\n=== Scanning for array counts before first pkg.bytes entry ===")
scan_start = max(0, first_entry_area - 200)
for i in range(scan_start, first_entry_area, 4):
    val = struct.unpack_from('<I', verif, i)[0]
    if 1 <= val <= 1000:
        print(f"  0x{i:05X}: {val}")

# === Part 2: Tim CommonActions trong resources.assets
print("\n" + "=" * 60)
print("Part 2: CommonActions in resources.assets")
print("=" * 60)

needle_ca = b"CommonActions"
start = 0
count = 0
while True:
    idx = res.find(needle_ca, start)
    if idx < 0: break
    count += 1
    ctx_start = max(0, idx - 30)
    ctx_end   = min(len(res), idx + 80)
    ctx = res[ctx_start:ctx_end]
    ascii_ctx = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
    print(f"\n  [{count}] Offset 0x{idx:06X}: {ascii_ctx}")
    start = idx + 1

print(f"\nTotal CommonActions occurrences in resources.assets: {count}")

# === Part 3: Tim structure truoc/sau moi int32 count
print("\n" + "=" * 60)
print("Part 3: All arrays in verification data block")
print("=" * 60)

# Scan verif file tim tat ca int32 trong [100, 1000] tai boundary 4
data_start = 129  # sau header
data_end   = len(verif) - 15  # bo trailing

def looks_like_path(d, pos, length):
    if pos + length > len(d): return False
    chunk = d[pos:pos+length]
    return (all(32 <= b < 128 for b in chunk) and b'.' in chunk)

print("Scanning for all array-count-like int32 in data block:")
for i in range(data_start, min(data_end, 0x2000), 4):
    val = struct.unpack_from('<I', verif, i)[0]
    if 50 <= val <= 2000:
        # Kiem tra xem co phai la array count khong
        next_int = struct.unpack_from('<I', verif, i+4)[0] if i+4 < data_end else 0
        if 5 <= next_int <= 300:  # looks like string length
            path_pos = i + 8
            if looks_like_path(verif, path_pos, next_int):
                path = verif[path_pos:path_pos+next_int].decode(errors='replace')
                print(f"  ARRAY at 0x{i:05X}: count={val}, first entry len={next_int}, path='{path[:50]}'")
