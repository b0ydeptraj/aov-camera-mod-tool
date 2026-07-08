import sys, zipfile, io, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
data = ca_file.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(data))

# Phan tich format cua 1 file dau tien
entry = zf.infolist()[0]
raw = zf.read(entry.filename)
print(f'File: {entry.filename}')
print(f'Raw size: {len(raw)} bytes')
print(f'Raw hex (32 bytes dau): {raw[:32].hex()}')
print(f'Byte 8-12: {raw[8:12].hex()} (zstd magic la 28b52ffd)')

# Tim zstd magic trong raw
zstd_magic = b'\x28\xb5\x2f\xfd'
idx = raw.find(zstd_magic)
print(f'Zstd magic tai offset: {idx}')

if idx >= 0:
    print(f'Header truoc zstd ({idx} bytes): {raw[:idx].hex()}')
    # Giai nen phan sau header
    zstd_data = raw[idx:]
    ctx = zstd.ZstdDecompressor()
    try:
        xml_bytes = ctx.decompress(zstd_data, max_output_size=1024*1024)
        xml = xml_bytes.decode('utf-8')
        print(f'\nXML decompressed ({len(xml)} chars):')
        print(xml[:500])
    except Exception as e:
        print(f'Loi: {e}')
        # Thu streaming
        try:
            reader = ctx.stream_reader(io.BytesIO(zstd_data))
            xml_bytes = reader.read()
            xml = xml_bytes.decode('utf-8')
            print(f'Streaming OK: {len(xml)} chars')
            print(xml[:500])
        except Exception as e2:
            print(f'Streaming loi: {e2}')

zf.close()
