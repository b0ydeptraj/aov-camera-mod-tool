import sys, zipfile, io, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
res_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resources.assets')

# Load dictionary
res_data = res_file.read_bytes()
dict_magic = b'\x37\xa4\x30\xec'
target_id = 188962279
for m_pos in [m.start() for m in re.finditer(re.escape(dict_magic), res_data)]:
    d_id = int.from_bytes(res_data[m_pos+4:m_pos+8], 'little')
    if d_id == target_id:
        dict_data = res_data[m_pos:m_pos+131072]
        zstd_dict = zstd.ZstdCompressionDict(dict_data)
        ctx = zstd.ZstdDecompressor(dict_data=zstd_dict)
        print(f'Dict OK at 0x{m_pos:X}')
        break

data = ca_file.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(data))
ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'

# In tat ca ten file
all_names = [e.filename for e in zf.infolist()]
print(f'Tong {len(all_names)} files')

# Tim file theo ten
print('\nFiles ten chua camera/Camera/cam/height/fov/zoom:')
for name in all_names:
    nl = name.lower()
    if any(k in nl for k in ['camera', 'cam', 'height', 'fov', 'zoom', 'view']):
        print(f'  {name}')

# In tat ca folder
folders = set()
for name in all_names:
    parts = name.split('/')
    if len(parts) > 1:
        folders.add(parts[0])
print(f'\nFolders: {sorted(folders)}')

# Scan binary content cua tat ca files cho "heightRate" hoac "Height"
print('\nQuet binary content cho heightRate/Height/Camera...')
found_height = []
for entry in zf.infolist():
    raw = zf.read(entry.filename)
    # Tim trong raw binary (truoc khi decode)
    if b'heightRate' in raw or b'HeightRate' in raw or b'height_rate' in raw:
        print(f'  [RAW heightRate] {entry.filename}')
        found_height.append(entry.filename)
    elif b'Camera' in raw or b'camera' in raw:
        print(f'  [RAW Camera] {entry.filename}')
    elif b'Height' in raw and b'float' in raw:
        print(f'  [RAW Height+float] {entry.filename}')

# Scan zstd decompressed
print('\nQuet XML decompressed...')
for entry in zf.infolist():
    raw = zf.read(entry.filename)
    idx = raw.find(ZSTD_MAGIC)
    if idx < 0:
        continue
    try:
        xml_b = ctx.decompress(raw[idx:], max_output_size=2*1024*1024)
        # Scan bytes truc tiep
        for kw in [b'heightRate', b'HeightRate', b'height_rate', b'CameraHeight',
                   b'camHeight', b'CamHeight', b'NormalFOV', b'CameraDistance',
                   b'zoomRate', b'ZoomRate']:
            if kw in xml_b:
                print(f'  [{kw.decode()}] {entry.filename}')
                found_height.append(entry.filename)
                break
    except:
        pass

zf.close()
print(f'\nTong ket: {len(found_height)} files co camera data')
