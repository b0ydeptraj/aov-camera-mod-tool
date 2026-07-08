"""
Phan tich sau vao cu truc resourceverification ban moi.
So sanh byte-by-byte giua file goc va file da strip.
"""
import sys, struct, re, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

try:
    import lz4.block as lz4b
except ImportError:
    lz4b = None

def parse_unityfs(data):
    """Parse UnityFS header, return payload + metadata."""
    assert data[:8] == b'UnityFS\x00', "Not UnityFS"
    pos = 8
    fmt_ver = struct.unpack_from('>I', data, pos)[0]; pos += 4
    end = data.index(0, pos); unity_ver = data[8+4:end]; pos = end + 1
    end = data.index(0, pos); unity_rev = data[pos:end]; pos = end + 1
    file_size = struct.unpack_from('>Q', data, pos)[0]; pos += 8
    comp_info_size = struct.unpack_from('>I', data, pos)[0]; pos += 4
    uncomp_info_size = struct.unpack_from('>I', data, pos)[0]; pos += 4
    flags = struct.unpack_from('>I', data, pos)[0]; pos += 4
    header_end = pos

    compression = flags & 0x3F
    info_start = (header_end + 15) & ~15 if (flags & 0x200) else header_end
    if flags & 0x80:
        info_start = len(data) - comp_info_size

    # Decompress block info
    comp_data = data[info_start:info_start + comp_info_size]
    if compression == 0:
        raw = bytes(comp_data)
    elif compression == 3:
        raw = lz4b.decompress(bytes(comp_data), uncompressed_size=uncomp_info_size)
    else:
        raise ValueError(f"Unsupported block info compression: {compression}")

    # Parse blocks
    bpos = 16
    nb = struct.unpack_from('>I', raw, bpos)[0]; bpos += 4
    blocks = []
    for _ in range(nb):
        b_u = struct.unpack_from('>I', raw, bpos)[0]; bpos += 4
        b_c = struct.unpack_from('>I', raw, bpos)[0]; bpos += 4
        b_f = struct.unpack_from('>H', raw, bpos)[0]; bpos += 2
        blocks.append((b_u, b_c, b_f))

    # Read payload
    off = info_start + comp_info_size
    payload = bytearray()
    for b_u, b_c, b_f in blocks:
        raw_block = data[off:off+b_c]
        b_ct = b_f & 0x3F
        if b_ct == 0:
            payload += raw_block
        elif b_ct == 3:
            payload += lz4b.decompress(bytes(raw_block), uncompressed_size=b_u)
        off += b_c

    return {
        'header_end': header_end,
        'info_start': info_start,
        'comp_info_size': comp_info_size,
        'data_start': info_start + comp_info_size,
        'blocks': blocks,
        'payload': payload,
        'compression': compression,
        'flags': flags,
    }

def scan_all_entries(payload):
    """Scan payload for ALL verification entries (path + hash)."""
    entries = []
    pos = 0
    while pos < len(payload) - 12:
        try:
            length = struct.unpack_from('<I', payload, pos)[0]
            if 5 <= length <= 300:
                path_start = pos + 4
                if path_start + length > len(payload):
                    pos += 1
                    continue
                path_bytes = bytes(payload[path_start:path_start+length])
                if path_bytes.startswith(b'Ages/') and all(32 <= b < 128 for b in path_bytes):
                    # Padding: (length+1) round up to 4
                    padded = ((length + 1 + 3) // 4) * 4
                    null_pad_size = padded - length
                    hash_start = path_start + length + null_pad_size
                    if hash_start + 8 > len(payload):
                        pos += 1
                        continue
                    hash_bytes = bytes(payload[hash_start:hash_start+8])
                    entry_end = hash_start + 8
                    entry_size = entry_end - pos
                    entries.append({
                        'offset': pos,
                        'length_prefix': length,
                        'path': path_bytes.decode(),
                        'hash': hash_bytes.hex(),
                        'entry_size': entry_size,
                        'entry_end': entry_end,
                    })
                    pos = entry_end
                    continue
        except:
            pass
        pos += 1
    return entries

def find_commonactions_entry(entries):
    """Find CommonActions entry among all entries."""
    for e in entries:
        if 'CommonActions' in e['path']:
            return e
    return None

# ================================================================
# MAIN
# ================================================================
ver_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle')
data = ver_file.read_bytes()

print(f"File: {ver_file}")
print(f"Size: {len(data)} bytes")
print(f"MD5:  {hashlib.md5(data).hexdigest()}")
print()

info = parse_unityfs(data)
payload = info['payload']
print(f"Payload size: {len(payload)} bytes")
print(f"Block compression: {info['compression']}")
print(f"Blocks: {len(info['blocks'])}")
for i, (bu, bc, bf) in enumerate(info['blocks']):
    print(f"  block[{i}]: uncomp={bu}, comp={bc}, flags=0x{bf:04X} (type={bf&0x3F})")
print()

# Scan entries
entries = scan_all_entries(payload)
print(f"Total entries found: {len(entries)}")

# Find CA entry
ca = find_commonactions_entry(entries)
if ca:
    print(f"\n=== CommonActions Entry ===")
    print(f"  Offset:       0x{ca['offset']:05X} ({ca['offset']})")
    print(f"  Path length:  {ca['length_prefix']}")
    print(f"  Path:         {ca['path']}")
    print(f"  Hash:         {ca['hash']}")
    print(f"  Entry size:   {ca['entry_size']} bytes")
    print(f"  Entry end:    0x{ca['entry_end']:05X}")
    
    # Hex dump of EXACT entry bytes
    entry_bytes = payload[ca['offset']:ca['entry_end']]
    print(f"\n  Entry hex dump ({len(entry_bytes)} bytes):")
    for i in range(0, len(entry_bytes), 16):
        c = entry_bytes[i:i+16]
        h = ' '.join(f'{b:02x}' for b in c)
        a = ''.join(chr(b) if 32<=b<127 else '.' for b in c)
        print(f"    {ca['offset']+i:05X}: {h:<48}  {a}")
    
    # Find neighbors
    ca_idx = entries.index(ca)
    if ca_idx > 0:
        prev = entries[ca_idx - 1]
        print(f"\n  PREV entry: {prev['path']} (offset=0x{prev['offset']:05X}, end=0x{prev['entry_end']:05X}, size={prev['entry_size']})")
        gap = ca['offset'] - prev['entry_end']
        print(f"  Gap between prev and CA: {gap} bytes")
    if ca_idx < len(entries) - 1:
        next_e = entries[ca_idx + 1]
        print(f"  NEXT entry: {next_e['path']} (offset=0x{next_e['offset']:05X})")
        gap2 = next_e['offset'] - ca['entry_end']
        print(f"  Gap between CA and next: {gap2} bytes")
else:
    print("\n!!! CommonActions KHONG TIM THAY !!!")

# Find array count
print(f"\n=== Array Count Scan ===")
if entries:
    first_offset = entries[0]['offset']
    print(f"First entry at: 0x{first_offset:05X}")
    # Scan backward
    for dist in [4, 8, 12, 16, 20, 24]:
        check_pos = first_offset - dist
        if check_pos >= 0 and check_pos + 4 <= len(payload):
            val = struct.unpack_from('<I', payload, check_pos)[0]
            print(f"  -{dist:2d} bytes (0x{check_pos:05X}): value={val} {'<-- LIKELY COUNT' if abs(val - len(entries)) <= 5 else ''}")

# Strip verification tool's pattern check
print(f"\n=== Tool's Strip Pattern Check ===")
ca_path = b"Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
prefix = struct.pack('<I', len(ca_path)) + ca_path
idx = payload.find(prefix)
print(f"Tool pattern (length_prefix + path) found at: {idx} (0x{idx:X})")

if idx >= 0:
    # What tool thinks is the entry
    tool_entry_start = idx
    tool_str_end = idx + 4 + len(ca_path)
    tool_entry_end = tool_entry_start + 72  # Tool assumes 72 bytes
    print(f"Tool entry range: 0x{tool_entry_start:05X} - 0x{tool_entry_end:05X} ({72} bytes)")
    
    # What ACTUAL entry looks like
    if ca:
        actual_start = ca['offset']
        actual_end = ca['entry_end']
        actual_size = ca['entry_size']
        print(f"Actual entry:    0x{actual_start:05X} - 0x{actual_end:05X} ({actual_size} bytes)")
        
        if tool_entry_start != actual_start or tool_entry_end != actual_end:
            print(f"\n!!! MISMATCH !!! Tool dang cat nhay entry !!!")
            print(f"  Tool cat tu  0x{tool_entry_start:05X} den 0x{tool_entry_end:05X}")
            print(f"  Thuc te la   0x{actual_start:05X} den 0x{actual_end:05X}")
            print(f"  Sai lech:    start={tool_entry_start-actual_start}, end={tool_entry_end-actual_end}")
        else:
            print(f"  -> MATCH! Tool strip dung cho.")

# Now do the strip and verify
print(f"\n=== Thu Strip va Verify ===")
from strip_verification import strip_common_actions_from_bundle
import tempfile
out_tmp = Path(tempfile.mktemp(suffix='.assetbundle'))
result = strip_common_actions_from_bundle(ver_file, out_tmp)
print(f"Result: success={result.success}")
print(f"Message: {result.message}")

if result.success and out_tmp.exists():
    stripped_data = out_tmp.read_bytes()
    print(f"\nStripped file size: {len(stripped_data)} (diff from original: {len(stripped_data)-len(data)})")
    
    stripped_info = parse_unityfs(stripped_data)
    stripped_payload = stripped_info['payload']
    
    # Verify no CommonActions remains
    ca_check = stripped_payload.find(b'CommonActions')
    print(f"CommonActions in stripped payload: {'FOUND at '+hex(ca_check) if ca_check >= 0 else 'NOT FOUND (good)'}")
    
    # Re-scan entries
    stripped_entries = scan_all_entries(stripped_payload)
    print(f"Entries after strip: {len(stripped_entries)} (was {len(entries)})")
    
    # Check array count
    if stripped_entries:
        first_off = stripped_entries[0]['offset']
        for dist in [4, 8]:
            check_pos = first_off - dist
            if check_pos >= 0:
                val = struct.unpack_from('<I', stripped_payload, check_pos)[0]
                print(f"  Array count at -{dist} (0x{check_pos:05X}): {val} (should be {len(entries)-1})")
    
    # Compare bytes before the first entry - check if anything was corrupted
    if entries and stripped_entries:
        orig_before = payload[:entries[0]['offset']]
        strip_before = stripped_payload[:stripped_entries[0]['offset']]
        if orig_before == strip_before:
            print("Header before entries: UNCHANGED (good)")
        else:
            # Find differences
            for i in range(min(len(orig_before), len(strip_before))):
                if orig_before[i] != strip_before[i]:
                    print(f"Header diff at 0x{i:05X}: orig=0x{orig_before[i]:02X} strip=0x{strip_before[i]:02X}")
    
    # Check trailing zeros
    tail = stripped_payload[-100:]
    zero_count = sum(1 for b in tail if b == 0)
    print(f"Last 100 bytes: {zero_count} zeros")
    
    out_tmp.unlink()
