import sys, zipfile, io, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
data = ca_file.read_bytes()

zf = zipfile.ZipFile(io.BytesIO(data))
entries = zf.infolist()
print(f'ZIP chua {len(entries)} files:')
for e in entries:
    print(f'  [{e.compress_type}] {e.filename}  comp={e.compress_size}B  orig={e.file_size}B')

print()
camera_keywords = ['heightRate', 'CameraHeight', 'CameraDistance', 'cameraHeight', 'NormalFOV', 'zoomRate', 'fov']

for entry in entries:
    raw = zf.read(entry.filename)
    try:
        ctx = zstd.ZstdDecompressor()
        xml = ctx.decompress(raw).decode('utf-8')
        found = [kw for kw in camera_keywords if kw in xml]
        if found:
            print(f'=== {entry.filename} === (camera keywords: {found})')
            # In tat ca float nodes
            for node in re.findall(r'<float name="[^"]*(?:height|Height|camera|Camera|fov|FOV|zoom|Zoom|rate|Rate)[^"]*"[^/]*/>', xml, re.I):
                print(f'  {node}')
    except Exception:
        pass

zf.close()
