import sys, zipfile, io, struct, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
res_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resources.assets')

# Load dictionary  
res_data = res_file.read_bytes()
dict_magic = b'\x37\xa4\x30\xec'
target_id = 188962279
matches = [m.start() for m in re.finditer(re.escape(dict_magic), res_data)]

# Thu ca 2 dict sizes
for dict_size_label, dict_size in [('131072', 131072), ('262144', 262144)]:
    for m_pos in matches:
        d_id = int.from_bytes(res_data[m_pos+4:m_pos+8], 'little')
        if d_id == target_id:
            dict_data = res_data[m_pos:m_pos+dict_size]
            zstd_dict = zstd.ZstdCompressionDict(dict_data)
            ctx = zstd.ZstdDecompressor(dict_data=zstd_dict)
            break

    data = ca_file.read_bytes()
    zf = zipfile.ZipFile(io.BytesIO(data))
    ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'

    # Doc 5 file dau tien va in noi dung
    print(f'\n=== Dict size {dict_size_label} ===')
    for i, entry in enumerate(zf.infolist()[:5]):
        raw = zf.read(entry.filename)
        idx = raw.find(ZSTD_MAGIC)
        if idx < 0:
            print(f'{entry.filename}: no zstd magic')
            continue
        try:
            xml_bytes = ctx.decompress(raw[idx:], max_output_size=2*1024*1024)
            xml = xml_bytes.decode('utf-8', errors='replace')
            print(f'{entry.filename} ({len(xml)} chars):')
            print(f'  {xml[:200]}')
        except Exception as e:
            print(f'{entry.filename}: ERROR {e}')

    # Tim tat ca files ten chua "camera" hoac "Camera"
    print(f'\nFiles ten chua camera:')
    for entry in zf.infolist():
        if 'camera' in entry.filename.lower() or 'cam' in entry.filename.lower():
            print(f'  {entry.filename}')

    # Tim tat ca files ten chua "height" 
    print(f'Files ten chua height/Height:')
    for entry in zf.infolist():
        if 'height' in entry.filename.lower():
            print(f'  {entry.filename}')

    zf.close()
    break  # Chi can chay voi 1 dict size
