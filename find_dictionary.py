import sys, zipfile, io, struct, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
res_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resources.assets')

# Doc dict ID tu zstd frame
data = ca_file.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(data))
raw = zf.read(zf.infolist()[0].filename)

# Tim zstd magic
zstd_magic = b'\x28\xb5\x2f\xfd'
idx = raw.find(zstd_magic)
frame = raw[idx:]

# Parse zstd frame header de lay dict_id
# FHD byte
fhd = frame[4]
fcs_flag = (fhd >> 6) & 0x3
single_segment = (fhd >> 5) & 0x1
checksum_flag = (fhd >> 2) & 0x1
dict_id_flag = fhd & 0x3

print(f'FHD: 0x{fhd:02X}')
print(f'  FCS_Flag: {fcs_flag}')
print(f'  Single_Segment: {single_segment}')
print(f'  Dict_ID_Flag: {dict_id_flag} (0=no dict, 1=1byte, 2=2bytes, 3=4bytes)')

# Doc dict_id
pos = 5
if single_segment:
    pass  # Window_Descriptor is skipped

dict_id_sizes = [0, 1, 2, 4]
dict_id_size = dict_id_sizes[dict_id_flag]
if dict_id_size > 0:
    dict_id_bytes = frame[pos:pos+dict_id_size]
    dict_id = int.from_bytes(dict_id_bytes, 'little')
    print(f'Dictionary ID: {dict_id} (0x{dict_id:08X})')
    print(f'Dict ID hex bytes: {dict_id_bytes.hex()}')
else:
    print('Khong dung dictionary!')
    dict_id = None

if dict_id is None:
    sys.exit(0)

# Tim dictionary trong resources.assets
print(f'\n=== Tim dict ID={dict_id} trong resources.assets ({res_file.stat().st_size} bytes) ===')
res_data = res_file.read_bytes()

# Zstd dictionary frame bat dau bang magic 37A4 30EC
dict_magic = b'\x37\xa4\x30\xec'
dict_id_bytes_le = dict_id.to_bytes(4, 'little')

# Tim tat ca dict magic
matches = [m.start() for m in re.finditer(re.escape(dict_magic), res_data)]
print(f'Tim thay {len(matches)} zstd dictionary frames trong resources.assets')

for m_pos in matches:
    # Doc dict ID tai offset+4
    d_id_bytes = res_data[m_pos+4:m_pos+8]
    d_id = int.from_bytes(d_id_bytes, 'little')
    if d_id == dict_id:
        print(f'FOUND! Dictionary tai offset 0x{m_pos:X} voi ID={d_id}')
        # Xac dinh kich thuoc dictionary (can scan hoac thu size khac nhau)
        # Thu cac size pho bien
        for try_size in [65536, 32768, 16384, 8192, 4096, 131072, 262144]:
            dict_data = res_data[m_pos:m_pos+try_size]
            try:
                zstd_dict = zstd.ZstdCompressionDict(dict_data)
                ctx = zstd.ZstdDecompressor(dict_data=zstd_dict)
                xml = ctx.decompress(frame, max_output_size=1024*1024)
                print(f'  Size {try_size}: OK! XML = {len(xml)} bytes')
                print(f'  Preview: {xml[:200].decode("utf-8")}')
                break
            except Exception as e:
                pass
        break
else:
    print('KHONG tim thay dictionary! Cac ID co san:')
    for m_pos in matches[:10]:
        d_id = int.from_bytes(res_data[m_pos+4:m_pos+8], 'little')
        print(f'  Offset 0x{m_pos:X}: dict_id={d_id} (0x{d_id:08X})')
