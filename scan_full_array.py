import sys, struct
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

data = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle').read_bytes()

# Count offset at 0x16E0 (file offset), value = 295
count_offset = 0x16E0
count_val = struct.unpack_from('<I', data, count_offset)[0]
print(f"Array count at 0x{count_offset:05X}: {count_val}")

# First entry starts at 0x16E4
first_entry = count_offset + 4
print(f"First entry at 0x{first_entry:05X}")

# Scan ALL entries from first_entry
def entry_size_at(d, pos):
    if pos + 4 > len(d):
        return None
    str_len = struct.unpack_from('<I', d, pos)[0]
    if str_len < 1 or str_len > 300:
        return None
    ps = pos + 4
    if ps + str_len > len(d):
        return None
    pb = d[ps:ps+str_len]
    if not all(32 <= b < 128 for b in pb):
        return None
    if ord('.') not in pb:
        return None
    padded = ((str_len + 1 + 3) // 4) * 4
    np2 = padded - str_len
    hs = ps + str_len + np2
    ee = hs + 8
    if ee > len(d):
        return None
    if d[ps + str_len] != 0:
        return None
    return ee - pos

pos = first_entry
entries = []
for i in range(count_val + 10):  # scan up to count+10
    sz = entry_size_at(data, pos)
    if sz is None:
        print(f"Entry scan stopped at index {i}, offset 0x{pos:05X}")
        # Show what's at this position
        chunk = data[pos:pos+20]
        h = ' '.join(f'{b:02x}' for b in chunk)
        a = ''.join(chr(b) if 32<=b<127 else '.' for b in chunk)
        print(f"  Data: {h}  {a}")
        break
    path = data[pos+4:pos+4+struct.unpack_from('<I', data, pos)[0]].decode()
    padded = ((struct.unpack_from('<I', data, pos)[0] + 1 + 3) // 4) * 4
    np2 = padded - struct.unpack_from('<I', data, pos)[0]
    hs = pos + 4 + struct.unpack_from('<I', data, pos)[0] + np2
    hashval = data[hs:hs+8].hex()
    entries.append({'idx': i, 'offset': pos, 'path': path, 'hash': hashval, 'size': sz})
    pos += sz

print(f"\nTotal entries scanned: {len(entries)}")
print(f"Array end at: 0x{pos:05X}")
print(f"Array count says: {count_val}")
print(f"Match: {len(entries) == count_val}")

# Find CommonActions
for e in entries:
    if 'CommonActions' in e['path']:
        print(f"\nCommonActions found at index {e['idx']}:")
        print(f"  Offset: 0x{e['offset']:05X}")
        print(f"  Path: {e['path']}")
        print(f"  Hash: {e['hash']}")
        print(f"  Size: {e['size']} bytes")

# Show first and last entries
print(f"\nFirst 3 entries:")
for e in entries[:3]:
    print(f"  [{e['idx']}] 0x{e['offset']:05X}: {e['path']} hash={e['hash']}")
print(f"Last 3 entries:")
for e in entries[-3:]:
    print(f"  [{e['idx']}] 0x{e['offset']:05X}: {e['path']} hash={e['hash']}")

# NOW check: what's the NEXT array after this one?
array_end = pos
print(f"\n=== Data after array (0x{array_end:05X}) ===")
chunk = data[array_end:array_end+100]
for i in range(0, len(chunk), 16):
    c = chunk[i:i+16]
    h = ' '.join(f'{b:02x}' for b in c)
    a = ''.join(chr(b) if 32<=b<127 else '.' for b in c)
    print(f"  {array_end+i:05X}: {h:<48}  {a}")

# Check if there's a second array with its own count
next_count_pos = array_end
if next_count_pos + 4 <= len(data):
    next_count = struct.unpack_from('<I', data, next_count_pos)[0]
    print(f"\nNext int32 at 0x{next_count_pos:05X}: {next_count}")
