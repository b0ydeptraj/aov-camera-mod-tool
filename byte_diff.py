"""
So sanh TUNG BYTE giua file goc va file da strip de tim chinh xac cho bi hong.
"""
import sys, struct, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

orig_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle')
stripped_file = Path(tempfile.mktemp(suffix='.assetbundle'))

from strip_verification import strip_common_actions_from_bundle
result = strip_common_actions_from_bundle(orig_file, stripped_file)
print(f"Strip result: {result.success}")

orig = orig_file.read_bytes()
stripped = stripped_file.read_bytes()

print(f"Original size:  {len(orig)}")
print(f"Stripped size:   {len(stripped)}")
print(f"Same size: {len(orig) == len(stripped)}")

# Byte-by-byte diff
diffs = []
for i in range(min(len(orig), len(stripped))):
    if orig[i] != stripped[i]:
        diffs.append((i, orig[i], stripped[i]))

print(f"\nTotal differing bytes: {len(diffs)}")

if diffs:
    # Group diffs into regions
    regions = []
    current_start = diffs[0][0]
    current_end = diffs[0][0]
    for offset, o, s in diffs:
        if offset > current_end + 4:
            regions.append((current_start, current_end))
            current_start = offset
        current_end = offset
    regions.append((current_start, current_end))
    
    print(f"Diff regions: {len(regions)}")
    for start, end in regions:
        length = end - start + 1
        print(f"\n=== Region 0x{start:05X} - 0x{end:05X} ({length} bytes) ===")
        if length <= 100:
            # Show all bytes
            for i in range(start, end + 1):
                if orig[i] != stripped[i]:
                    o_chr = chr(orig[i]) if 32 <= orig[i] < 127 else '.'
                    s_chr = chr(stripped[i]) if 32 <= stripped[i] < 127 else '.'
                    print(f"  0x{i:05X}: orig=0x{orig[i]:02X}({o_chr}) strip=0x{stripped[i]:02X}({s_chr})")
        else:
            # Show summary + first/last 10
            print(f"  First 10 diffs:")
            count = 0
            for i in range(start, end + 1):
                if orig[i] != stripped[i] and count < 10:
                    print(f"    0x{i:05X}: orig=0x{orig[i]:02X} strip=0x{stripped[i]:02X}")
                    count += 1
            print(f"  Last 10 diffs:")
            tail_diffs = [(i, orig[i], stripped[i]) for i in range(start, end+1) if orig[i] != stripped[i]]
            for i, o, s in tail_diffs[-10:]:
                print(f"    0x{i:05X}: orig=0x{o:02X} strip=0x{s:02X}")

    # CRITICAL: Compute data_start (where payload begins in file)
    # Parse header to find data_start
    import lz4.block as lz4b
    pos = 8
    struct.unpack_from('>I', orig, pos)[0]; pos += 4
    end_pos = orig.index(0, pos); pos = end_pos + 1
    end_pos = orig.index(0, pos); pos = end_pos + 1
    pos += 8
    comp_info_size = struct.unpack_from('>I', orig, pos)[0]; pos += 4
    uncomp_info_size = struct.unpack_from('>I', orig, pos)[0]; pos += 4
    flags = struct.unpack_from('>I', orig, pos)[0]; pos += 4
    header_end = pos
    info_start = (header_end + 15) & ~15 if (flags & 0x200) else header_end
    if flags & 0x80: info_start = len(orig) - comp_info_size
    data_start = info_start + comp_info_size

    # Parse block info for block size
    comp_data = bytes(orig[info_start:info_start + comp_info_size])
    raw_info = lz4b.decompress(comp_data, uncompressed_size=uncomp_info_size) if (flags & 0x3F) == 3 else comp_data
    bpos = 16
    nb = struct.unpack_from('>I', raw_info, bpos)[0]; bpos += 4
    block_uncomp = struct.unpack_from('>I', raw_info, bpos)[0]; bpos += 4
    block_comp = struct.unpack_from('>I', raw_info, bpos)[0]; bpos += 4

    print(f"\n=== File structure ===")
    print(f"Header + block_info: [0, {data_start-1}] ({data_start} bytes)")
    print(f"Data block: [{data_start}, {data_start+block_comp-1}] ({block_comp} bytes)")
    print(f"Trailing: [{data_start+block_comp}, {len(orig)-1}] ({len(orig)-data_start-block_comp} bytes)")

    # Show diffs in context of file structure  
    header_diffs = [d for d in diffs if d[0] < data_start]
    data_diffs = [d for d in diffs if data_start <= d[0] < data_start + block_comp]
    trail_diffs = [d for d in diffs if d[0] >= data_start + block_comp]

    print(f"\nDiffs in header: {len(header_diffs)}")
    print(f"Diffs in data block: {len(data_diffs)}")
    print(f"Diffs in trailing: {len(trail_diffs)}")

    # Check specifically what the last N bytes of original data block look like
    data_end = data_start + block_comp
    print(f"\n=== Last 80 bytes of ORIGINAL data block ===")
    chunk = orig[data_end-80:data_end]
    for i in range(0, len(chunk), 16):
        c = chunk[i:i+16]
        h = ' '.join(f'{b:02x}' for b in c)
        a = ''.join(chr(b) if 32 <= b < 127 else '.' for b in c)
        offset = data_end - 80 + i
        print(f"  {offset:05X}: {h:<48}  {a}")

    print(f"\n=== Last 80 bytes of STRIPPED data block ===")
    chunk = stripped[data_end-80:data_end]
    for i in range(0, len(chunk), 16):
        c = chunk[i:i+16]
        h = ' '.join(f'{b:02x}' for b in c)
        a = ''.join(chr(b) if 32 <= b < 127 else '.' for b in c)
        offset = data_end - 80 + i
        print(f"  {offset:05X}: {h:<48}  {a}")

    # Is trailing data different?
    print(f"\n=== Trailing bytes comparison ===")
    orig_trail = orig[data_end:]
    strip_trail = stripped[data_end:]
    if orig_trail == strip_trail:
        print("Trailing bytes: IDENTICAL")
    else:
        print("Trailing bytes: DIFFERENT!")
        for i in range(len(orig_trail)):
            if orig_trail[i] != strip_trail[i]:
                print(f"  +{i}: orig=0x{orig_trail[i]:02X} strip=0x{strip_trail[i]:02X}")

stripped_file.unlink()
