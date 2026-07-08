import sys, zipfile, io, struct, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
res_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resources.assets')

PKG_MAGIC = b'\x22\x4a\x00\xef'
ZSTD_DICT_MAGIC = b'\x37\xa4\x30\xec'

# Doc entry data cua 2 target entries de tim dict
data_pkg = ca_file.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(data_pkg))

entry_data = {}
for name in zf.namelist():
    raw = zf.read(name)
    if raw[:4] == PKG_MAGIC:
        entry_data[name] = raw

print(f'Files dung PKG_MAGIC: {len(entry_data)}/{len(zf.namelist())}')

# Lay 2 target entries de xac thuc dict
target_keys = list(entry_data.keys())[:2]
sample = {k: entry_data[k] for k in target_keys}

# Tim dict tu resources.assets
res_data = res_file.read_bytes()

def looks_like_xml(raw: bytes) -> bool:
    try:
        text = raw.decode('utf-8-sig')
        stripped = text.lstrip()
        return stripped.startswith('<?xml') and '<Project' in text
    except:
        return False

def find_dict(asset_data, sample_entries):
    for m in re.finditer(re.escape(ZSTD_DICT_MAGIC), asset_data):
        offset = m.start()
        # Thu sizes tu 1024 den 1MB theo tung buoc
        for size in range(1024, min(1024*1024, len(asset_data)-offset)+1, 1):
            candidate = asset_data[offset:offset+size]
            try:
                zdict = zstd.ZstdCompressionDict(candidate)
                dec = zstd.ZstdDecompressor(dict_data=zdict)
                # Kiem tra voi tat ca sample entries
                ok = True
                for name, raw in sample_entries.items():
                    if not raw[:4] == PKG_MAGIC:
                        ok = False
                        break
                    expected = struct.unpack('<I', raw[4:8])[0]
                    try:
                        decompressed = dec.decompress(raw[8:])
                    except:
                        ok = False
                        break
                    if len(decompressed) != expected or not looks_like_xml(decompressed):
                        ok = False
                        break
                if ok:
                    print(f'Dict found at offset=0x{offset:X}, size={size}')
                    return candidate, offset, size
            except:
                pass
    return None, -1, -1

print('\nDang tim dictionary chinh xac (co the mat vai phut)...')
dict_data, dict_offset, dict_size = find_dict(res_data, sample)

if dict_data is None:
    print('KHONG tim thay dictionary!')
    sys.exit(1)

print(f'Dictionary OK: offset=0x{dict_offset:X}, size={dict_size}')

# Giai nen tat ca entries va tim camera
zstd_dict = zstd.ZstdCompressionDict(dict_data)
dec = zstd.ZstdDecompressor(dict_data=zstd_dict)

camera_keys = [
    b'SetCameraHeightDuration', b'heightRate', b'CameraHeight',
    b'cameraHeight', b'CameraDistance', b'NormalFOV'
]

print('\nQuet tat ca ZIP entries cho camera keywords...')
found = []
for name, raw in entry_data.items():
    expected = struct.unpack('<I', raw[4:8])[0]
    try:
        xml_b = dec.decompress(raw[8:])
        if len(xml_b) == expected:
            for kw in camera_keys:
                if kw in xml_b:
                    print(f'[FOUND] {name} has keyword: {kw.decode()}')
                    found.append((name, kw.decode()))
                    break
    except:
        pass

if not found:
    print('Khong tim thay camera keywords trong bat ky file nao!')
    print('\nIn 1 XML mau de kiem tra:')
    first_name = list(entry_data.keys())[0]
    first_raw = entry_data[first_name]
    expected = struct.unpack('<I', first_raw[4:8])[0]
    xml_b = dec.decompress(first_raw[8:])
    print(f'{first_name}: {xml_b[:300]}')

zf.close()
