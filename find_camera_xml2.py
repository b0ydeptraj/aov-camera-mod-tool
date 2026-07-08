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
dict_offset = None
for m_pos in matches:
    d_id = int.from_bytes(res_data[m_pos+4:m_pos+8], 'little')
    if d_id == target_id:
        dict_offset = m_pos
        break

DICT_SIZE = 131072
dict_data = res_data[dict_offset:dict_offset+DICT_SIZE]
zstd_dict = zstd.ZstdCompressionDict(dict_data)
ctx = zstd.ZstdDecompressor(dict_data=zstd_dict)

print(f'Dict loaded at 0x{dict_offset:X}, size={DICT_SIZE}')

# Doc ZIP va giai nen tung file
data = ca_file.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(data))

ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'
HEADER_SIZE = 8  # 8 bytes custom header truoc zstd frame

camera_kw = ['heightRate', 'CameraHeight', 'CameraDistance', 'cameraHeight',
             'NormalFOV', 'zoomRate', 'CamHeight', 'cam_height']

print(f'\nQuet {len(zf.infolist())} files tim camera...\n')
camera_files = []

for entry in zf.infolist():
    raw = zf.read(entry.filename)
    idx = raw.find(ZSTD_MAGIC)
    if idx < 0:
        continue
    zstd_frame = raw[idx:]
    try:
        xml_bytes = ctx.decompress(zstd_frame, max_output_size=2*1024*1024)
        xml = xml_bytes.decode('utf-8')
        found = [kw for kw in camera_kw if kw in xml]
        if found:
            print(f'[CAMERA] {entry.filename}')
            print(f'  Keywords: {found}')
            # In cac node camera
            for node in re.findall(r'<float name="[^"]*"[^/]*/>', xml):
                if any(k.lower() in node.lower() for k in camera_kw):
                    print(f'  {node}')
            camera_files.append(entry.filename)
            print()
    except Exception as e:
        pass

if not camera_files:
    print('Khong tim thay file camera! Thu tim theo tu khoa rong hon...')
    for entry in zf.infolist():
        raw = zf.read(entry.filename)
        idx = raw.find(ZSTD_MAGIC)
        if idx < 0:
            continue
        zstd_frame = raw[idx:]
        try:
            xml_bytes = ctx.decompress(zstd_frame, max_output_size=2*1024*1024)
            xml = xml_bytes.decode('utf-8')
            if 'height' in xml.lower() and 'float' in xml:
                print(f'[height] {entry.filename}:')
                for node in re.findall(r'<float name="[^"]*height[^"]*"[^/]*/>', xml, re.I):
                    print(f'  {node}')
        except:
            pass

zf.close()
