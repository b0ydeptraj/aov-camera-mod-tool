import sys, struct
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
import lz4.block as lz4b

ver_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle')
data = bytearray(ver_file.read_bytes())

pos = 8
struct.unpack_from('>I', data, pos)[0]; pos += 4
end = data.index(0, pos); pos = end + 1
end = data.index(0, pos); pos = end + 1
pos += 8
comp_info_size = struct.unpack_from('>I', data, pos)[0]; pos += 4
uncomp_info_size = struct.unpack_from('>I', data, pos)[0]; pos += 4
flags = struct.unpack_from('>I', data, pos)[0]; pos += 4
header_end = pos
info_start = (header_end + 15) & ~15 if (flags & 0x200) else header_end
if flags & 0x80: info_start = len(data) - comp_info_size
comp_data = bytes(data[info_start:info_start + comp_info_size])
raw = lz4b.decompress(comp_data, uncompressed_size=uncomp_info_size) if (flags & 0x3F) == 3 else comp_data
bpos = 16
nb = struct.unpack_from('>I', raw, bpos)[0]; bpos += 4
blocks = []
for _ in range(nb):
    bu = struct.unpack_from('>I', raw, bpos)[0]; bpos += 4
    bc = struct.unpack_from('>I', raw, bpos)[0]; bpos += 4
    bf = struct.unpack_from('>H', raw, bpos)[0]; bpos += 2
    blocks.append((bu, bc, bf))
off = info_start + comp_info_size
payload = bytearray()
for bu, bc, bf in blocks:
    payload += data[off:off+bc]; off += bc

# Hex dump quanh 0x1643 - 0x16A0
print("=== Hex dump 0x1640 - 0x1700 ===")
start = 0x1640
end2 = 0x1700
chunk = payload[start:end2]
for i in range(0, len(chunk), 16):
    c = chunk[i:i+16]
    h = ' '.join(f'{b:02x}' for b in c)
    a = ''.join(chr(b) if 32 <= b < 127 else '.' for b in c)
    print(f"  {start+i:05X}: {h:<48}  {a}")

# Entry thu nhat that su
print("\n=== Entry thu nhat (0x1663) ===")
pos2 = 0x1663
length = struct.unpack_from('<I', payload, pos2)[0]
print(f"Length: {length}")
path_data = payload[pos2+4:pos2+4+length]
print(f"Path: {path_data}")
padded = ((length + 1 + 3) // 4) * 4
null_pad = padded - length
hash_start = pos2 + 4 + length + null_pad
hash_bytes = payload[hash_start:hash_start+8]
entry_end_pos = hash_start + 8
print(f"Hash: {hash_bytes.hex()}")
print(f"Entry end: 0x{entry_end_pos:05X}")
print(f"Entry size: {entry_end_pos - pos2}")

print(f"\nNext entry at 0x{entry_end_pos:05X}:")
pos3 = entry_end_pos
length2 = struct.unpack_from('<I', payload, pos3)[0]
path_data2 = payload[pos3+4:pos3+4+length2]
print(f"Length: {length2}, Path: {path_data2}")

# Dem tat ca entries
print("\n=== Dem tat ca entries (from 0x1663) ===")
all_entries = []
pos4 = 0x1663
while pos4 < len(payload) - 12:
    try:
        ln = struct.unpack_from('<I', payload, pos4)[0]
        if 1 <= ln <= 300:
            ps = pos4 + 4
            if ps + ln > len(payload):
                break
            pb = bytes(payload[ps:ps+ln])
            if all(32 <= b < 128 for b in pb) and (b'.' in pb):
                pad = ((ln + 1 + 3) // 4) * 4
                np = pad - ln
                hs = ps + ln + np
                if hs + 8 > len(payload):
                    break
                hb = payload[hs:hs+8]
                ee = hs + 8
                entry_info = {
                    'offset': pos4,
                    'path': pb.decode(),
                    'hash': hb.hex(),
                    'end': ee,
                    'size': ee - pos4
                }
                all_entries.append(entry_info)
                pos4 = ee
                continue
    except:
        pass
    pos4 += 1

print(f"Total all entries: {len(all_entries)}")
print(f"Array count value at 0x165F: 295")
print(f"Match: {len(all_entries) == 295}")

# Show first 5
print("\nFirst 5:")
for e in all_entries[:5]:
    off_val = e['offset']
    path_val = e['path']
    sz = e['size']
    hsh = e['hash']
    print(f"  0x{off_val:05X}: {path_val} ({sz}B) hash={hsh}")

# Find CommonActions
ca_idx = None
for i, e in enumerate(all_entries):
    if 'CommonActions' in e['path']:
        ca_idx = i
        off_val = e['offset']
        path_val = e['path']
        sz = e['size']
        hsh = e['hash']
        print(f"\nCommonActions at index {i}: 0x{off_val:05X}: {path_val} ({sz}B) hash={hsh}")
        break

# Verify: after removing CA entry and shifting, does the file still make sense?
if ca_idx is not None:
    print(f"\nEntry before CA: index={ca_idx-1}")
    e = all_entries[ca_idx-1]
    print(f"  0x{e['offset']:05X}: {e['path']} end=0x{e['end']:05X}")
    e2 = all_entries[ca_idx+1]
    print(f"Entry after CA: index={ca_idx+1}")
    print(f"  0x{e2['offset']:05X}: {e2['path']}")
