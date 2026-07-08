import sys, zipfile, io, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

import zstandard as zstd

ca_file = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
data = ca_file.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(data))

camera_keywords = ['heightRate', 'CameraHeight', 'CameraDistance', 
                   'cameraHeight', 'NormalFOV', 'zoomRate', 'fov',
                   'SpeedScale', 'camera', 'Camera', 'height', 'Height']

found_any = False
for entry in zf.infolist():
    raw = zf.read(entry.filename)
    # Thu plain text truoc
    content = None
    try:
        content = raw.decode('utf-8')
    except Exception:
        pass
    
    # Neu khong phai text, thu zstd
    if content is None:
        try:
            ctx = zstd.ZstdDecompressor()
            content = ctx.decompress(raw).decode('utf-8')
        except Exception:
            continue
    
    # Tim camera keywords
    found_kw = [kw for kw in camera_keywords if kw in content]
    if 'camera' in entry.filename.lower() or 'height' in content.lower() or 'heightrate' in content.lower():
        print(f'=== {entry.filename} (keywords: {found_kw}) ===')
        # In 300 chars dau
        print(content[:300])
        print('...')
        found_any = True

if not found_any:
    print('Khong tim thay camera XML. Listing tat ca files:')
    for e in zf.infolist():
        raw = zf.read(e.filename)
        # Check if text/xml
        try:
            txt = raw.decode('utf-8')
            if '<' in txt:
                print(f'  XML: {e.filename}')
        except:
            try:
                ctx = zstd.ZstdDecompressor()
                txt = ctx.decompress(raw).decode('utf-8')
                if '<' in txt:
                    print(f'  ZSTD-XML: {e.filename}')
            except:
                print(f'  BINARY: {e.filename}')

zf.close()
