import sys, struct, re, hashlib, binascii
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
raw_info = lz4b.decompress(comp_data, uncompressed_size=uncomp_info_size) if (flags & 0x3F) == 3 else comp_data
bpos = 16
nb = struct.unpack_from('>I', raw_info, bpos)[0]; bpos += 4
blocks = []
for _ in range(nb):
    bu = struct.unpack_from('>I', raw_info, bpos)[0]; bpos += 4
    bc = struct.unpack_from('>I', raw_info, bpos)[0]; bpos += 4
    bf = struct.unpack_from('>H', raw_info, bpos)[0]; bpos += 2
    blocks.append((bu, bc, bf))
off = info_start + comp_info_size
payload = bytearray()
for bu, bc, bf in blocks:
    payload += data[off:off+bc]; off += bc

# CommonActions hash in verification
ca_path = b'Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes'
idx = payload.find(ca_path)
padded = ((len(ca_path) + 1 + 3) // 4) * 4
null_pad = padded - len(ca_path)
hash_start = idx + len(ca_path) + null_pad
hash_bytes = bytes(payload[hash_start:hash_start+8])
print(f"Verification hash (8 bytes): {hash_bytes.hex()}")

orig_ca = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes').read_bytes()
crc32_val = binascii.crc32(orig_ca) & 0xFFFFFFFF
print(f"CRC32:  {crc32_val:08x}")
print(f"MD5:    {hashlib.md5(orig_ca).hexdigest()}")
print(f"SHA1:   {hashlib.sha1(orig_ca).hexdigest()}")

md5_8 = hashlib.md5(orig_ca).digest()[:8]
sha1_8 = hashlib.sha1(orig_ca).digest()[:8]
sha256_8 = hashlib.sha256(orig_ca).digest()[:8]

print()
if hash_bytes == md5_8: print(">>> MATCH: hash = MD5[:8]")
elif hash_bytes == sha1_8: print(">>> MATCH: hash = SHA1[:8]")
elif hash_bytes == sha256_8: print(">>> MATCH: hash = SHA256[:8]")
else: print(">>> NO MATCH - Custom hash (xxHash, SpookyHash, or game-specific)")

# File size check
file_size = len(orig_ca)
print(f"\nFile size: {file_size} (0x{file_size:08X})")
size_le = struct.pack('<I', file_size)
size_be = struct.pack('>I', file_size)
print(f"Hash 4 bytes dau: {hash_bytes[:4].hex()}")
print(f"Hash 4 bytes cuoi: {hash_bytes[4:].hex()}")
print(f"File size LE: {size_le.hex()}")
print(f"File size BE: {size_be.hex()}")

# Kiem tra 3 entries lien tiep de hieu format hash
print("\n=== So sanh hash format qua nhieu entries ===")
# Scan entries
entries = []
pos2 = 0x1663
while pos2 < len(payload) - 12:
    ln = struct.unpack_from('<I', payload, pos2)[0]
    if ln < 1 or ln > 300: break
    ps = pos2 + 4
    if ps + ln > len(payload): break
    pb = bytes(payload[ps:ps+ln])
    if not all(32 <= b < 128 for b in pb): break
    pad2 = ((ln + 1 + 3) // 4) * 4
    np2 = pad2 - ln
    hs = ps + ln + np2
    if hs + 8 > len(payload): break
    hb = bytes(payload[hs:hs+8])
    ee = hs + 8
    entries.append({'path': pb.decode(), 'hash': hb.hex(), 'offset': pos2, 'end': ee})
    pos2 = ee

print(f"Total entries: {len(entries)}")
# Show first 5
for e in entries[:5]:
    print(f"  {e['path']}: hash={e['hash']}")
# Show CommonActions
for e in entries:
    if 'CommonActions' in e['path']:
        print(f"\n  >>> {e['path']}: hash={e['hash']}")
        break

# CRITICAL TEST: User said game was working BEFORE update with OLD tool
# So the strip approach WORKED before. The question is what changed.
# Let me check if maybe the user just forgot to use BOTH files

print("\n=== CRITICAL ANALYSIS ===")
print("1. Strip verification: CORRECT (all 294 entries intact)")
print("2. CommonActions patch: CORRECT (valid XML, 2 files changed)")
print("3. File sizes changed: +270 bytes (may trigger size check)")
print()
print("MOST LIKELY CAUSE OF CRASH:")
print("A) User phai replace CA HAI file DONG THOI:")
print("   - CommonActions.pkg.bytes (da patch)")
print("   - resourceverificationinfosetall.assetbundle (da strip)")
print("B) Neu da replace ca 2 ma van crash -> game co co che bao ve MOI")
print("   - Co the check file size cua CommonActions (510981 vs 511251)")
print("   - Co the co manifest khac ngoai resourceverification")
print()

# Test: Kiem tra xem game co the dang check file SIZE khong
patched_ca_path = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions_patched.pkg.bytes')
if patched_ca_path.exists():
    patched_size = patched_ca_path.stat().st_size
    orig_size = len(orig_ca)
    print(f"Original size:  {orig_size}")
    print(f"Patched size:   {patched_size}")
    print(f"Difference:     {patched_size - orig_size} bytes")
    print()
    if patched_size != orig_size:
        print("!!! FILE SIZE KHAC NHAU !!!")
        print("Game co the dang check file size va reject file co size khac.")
        print("Can dieu chinh tool de giu nguyen file size sau khi patch.")
