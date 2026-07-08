import sys, struct
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

data = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle').read_bytes()

# Tim TAT CA vi tri chua 'CommonActions' trong file
needle = b'CommonActions'
positions = []
start = 0
while True:
    idx = data.find(needle, start)
    if idx < 0:
        break
    positions.append(idx)
    start = idx + 1

print(f"Tim thay {len(positions)} vi tri chua 'CommonActions':")
for pos in positions:
    ctx_start = max(0, pos - 40)
    ctx_end = min(len(data), pos + 80)
    ctx = data[ctx_start:ctx_end]
    ascii_ctx = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
    print(f"\n  === File offset 0x{pos:05X} ({pos}) ===")
    print(f"  ASCII: {ascii_ctx}")
    for i in range(0, len(ctx), 16):
        c = ctx[i:i+16]
        h = ' '.join(f'{c[j]:02x}' for j in range(len(c)))
        a = ''.join(chr(c[j]) if 32 <= c[j] < 127 else '.' for j in range(len(c)))
        print(f"  {ctx_start+i:05X}: {h:<48}  {a}")

# Tim trong file DA STRIP
print("\n\n========== FILE DA STRIP ==========")
from strip_verification import strip_common_actions_from_bundle
import tempfile
out = Path(tempfile.mktemp(suffix='.assetbundle'))
result = strip_common_actions_from_bundle(Path(r'C:\Users\b0ydeptrai\Downloads\zin\resourceverificationinfosetall.assetbundle'), out)
print(f"Strip: {result.message}")

stripped = out.read_bytes()
positions2 = []
start = 0
while True:
    idx = stripped.find(needle, start)
    if idx < 0:
        break
    positions2.append(idx)
    start = idx + 1

print(f"\nSau strip: {len(positions2)} vi tri chua 'CommonActions':")
for pos in positions2:
    ctx_start = max(0, pos - 20)
    ctx_end = min(len(stripped), pos + 80)
    ctx = stripped[ctx_start:ctx_end]
    ascii_ctx = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
    print(f"  0x{pos:05X}: {ascii_ctx}")

out.unlink()
