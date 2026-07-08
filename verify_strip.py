"""
So sanh tung entry truoc va sau strip de xem co bi sai hay khong.
Verify rang strip khong lam hong du lieu.
"""
import sys, struct, hashlib, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
import lz4.block as lz4b

def get_payload(filepath):
    """Parse UnityFS and return raw payload."""
    data = bytearray(Path(filepath).read_bytes())
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
    return payload


def scan_entries(payload, start_offset):
    """Scan ALL entries from start_offset."""
    entries = []
    pos = start_offset
    while pos < len(payload) - 12:
        ln = struct.unpack_from('<I', payload, pos)[0]
        if ln < 1 or ln > 300:
            break
        ps = pos + 4
        if ps + ln > len(payload):
            break
        pb = bytes(payload[ps:ps+ln])
        if not all(32 <= b < 128 for b in pb):
            break
        pad = ((ln + 1 + 3) // 4) * 4
        np = pad - ln
        hs = ps + ln + np
        if hs + 8 > len(payload):
            break
        hb = bytes(payload[hs:hs+8])
        ee = hs + 8
        entries.append({
            'offset': pos,
            'path': pb.decode(),
            'hash': hb.hex(),
            'end': ee,
            'size': ee - pos,
            'raw': bytes(payload[pos:ee]),
        })
        pos = ee
    return entries


# ======== MAIN ========

orig_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle')

# Do strip
from strip_verification import strip_common_actions_from_bundle
stripped_file = Path(tempfile.mktemp(suffix='.assetbundle'))
result = strip_common_actions_from_bundle(orig_file, stripped_file)
print(f"Strip result: {result.success}")
print(f"Strip msg: {result.message}")
print()

# Get payloads
orig_payload = get_payload(orig_file)
strip_payload = get_payload(stripped_file)

print(f"Orig payload: {len(orig_payload)} bytes")
print(f"Strip payload: {len(strip_payload)} bytes")

# Find array count + entries start offset
# Array count at 0x165F, first entry at 0x1663
count_offset = 0x165F
first_entry_offset = 0x1663

orig_count = struct.unpack_from('<I', orig_payload, count_offset)[0]
strip_count = struct.unpack_from('<I', strip_payload, count_offset)[0]
print(f"\nArray count: orig={orig_count}, stripped={strip_count}")

# Scan entries
orig_entries = scan_entries(orig_payload, first_entry_offset)
strip_entries = scan_entries(strip_payload, first_entry_offset)
print(f"Entries scanned: orig={len(orig_entries)}, stripped={len(strip_entries)}")
print(f"Array count matches entries: orig={orig_count == len(orig_entries)}, stripped={strip_count == len(strip_entries)}")

# Find CommonActions in original
ca_idx = None
for i, e in enumerate(orig_entries):
    if 'CommonActions' in e['path']:
        ca_idx = i
        print(f"\nCommonActions in original: index={i}, path={e['path']}")
        break

if ca_idx is None:
    print("CommonActions NOT FOUND in original!")
    sys.exit(1)

# Check CommonActions NOT in stripped
for e in strip_entries:
    if 'CommonActions' in e['path']:
        print("!!! CommonActions STILL IN STRIPPED FILE !!!")
        break
else:
    print("CommonActions removed from stripped: OK")

# Compare entries one by one (skip CommonActions in original)
print(f"\n=== Entry-by-entry comparison ===")
errors = 0
orig_filtered = [e for e in orig_entries if 'CommonActions' not in e['path']]
print(f"Original entries (minus CA): {len(orig_filtered)}")
print(f"Stripped entries: {len(strip_entries)}")

if len(orig_filtered) != len(strip_entries):
    print(f"!!! COUNT MISMATCH: {len(orig_filtered)} vs {len(strip_entries)} !!!")
    errors += 1

for i in range(min(len(orig_filtered), len(strip_entries))):
    oe = orig_filtered[i]
    se = strip_entries[i]
    if oe['path'] != se['path']:
        print(f"  Entry {i}: PATH MISMATCH! orig='{oe['path']}' strip='{se['path']}'")
        errors += 1
    elif oe['hash'] != se['hash']:
        print(f"  Entry {i}: HASH MISMATCH! path={oe['path']} orig_hash={oe['hash']} strip_hash={se['hash']}")
        errors += 1
    elif oe['raw'] != se['raw']:
        print(f"  Entry {i}: RAW BYTES MISMATCH! path={oe['path']}")
        # Show diffs
        for j in range(len(oe['raw'])):
            if j < len(se['raw']) and oe['raw'][j] != se['raw'][j]:
                print(f"    byte {j}: orig=0x{oe['raw'][j]:02X} strip=0x{se['raw'][j]:02X}")
        errors += 1

if errors == 0:
    print("  All entries match perfectly!")
else:
    print(f"\n!!! {errors} ERRORS FOUND !!!")

# Check bytes before entries (header area)
print(f"\n=== Header area comparison (0x0000 - 0x{first_entry_offset:04X}) ===")
orig_header = orig_payload[:count_offset]
strip_header = strip_payload[:count_offset]
if orig_header == strip_header:
    print("Header before count: IDENTICAL")
else:
    print("!!! HEADER CORRUPTED !!!")
    for i in range(len(orig_header)):
        if orig_header[i] != strip_header[i]:
            print(f"  Diff at 0x{i:04X}: orig=0x{orig_header[i]:02X} strip=0x{strip_header[i]:02X}")

# Check last N bytes
print(f"\n=== Tail area ===")
if strip_entries:
    last_entry_end = strip_entries[-1]['end']
    tail = strip_payload[last_entry_end:]
    non_zero = sum(1 for b in tail if b != 0)
    print(f"Bytes after last entry (from 0x{last_entry_end:05X}): {len(tail)} bytes, {non_zero} non-zero")
    if non_zero > 0:
        print("Non-zero tail bytes:")
        for i, b in enumerate(tail):
            if b != 0:
                print(f"  0x{last_entry_end+i:05X}: 0x{b:02X}")

# Cleanup
stripped_file.unlink()

print(f"\n=== FINAL VERDICT ===")
if errors == 0:
    print("Strip verification tool xoa dung cho, du lieu khong bi hong.")
    print("Van de crash co the do nguyen nhan khac (VD: patching CommonActions.pkg.bytes)")
else:
    print(f"Strip verification tool CO LOI: {errors} van de.")
