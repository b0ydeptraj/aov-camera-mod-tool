"""
Kiem tra:
1. CommonActions patch co tao XML hop le khong
2. File patched co bi loi gi khong
3. Game co co che kiem tra hash khac ngoai resourceverification khong
"""
import sys, zipfile, io, struct, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
import zstandard as zstd

PKG_MAGIC = b'\x22\x4a\x00\xef'

orig_ca = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions.pkg.bytes')
patched_ca = Path(r'C:\Users\b0ydeptrai\Downloads\zin\CommonActions_patched.pkg.bytes')
res_assets = Path(r'C:\Users\b0ydeptrai\Downloads\zin\resources.assets')

if not patched_ca.exists():
    print("Patched file chua co, chay patch truoc...")
    from patch_aov_camera import patch_package
    patch_package(
        pkg_path=orig_ca,
        height_rate=1.5,
        level=17,
        backup=False,
        output_path=patched_ca,
        game_assets_path=res_assets,
    )

print(f"Original:  {orig_ca.stat().st_size} bytes")
print(f"Patched:   {patched_ca.stat().st_size} bytes")
print(f"Size diff: {patched_ca.stat().st_size - orig_ca.stat().st_size}")

# Load dict
res_data = res_assets.read_bytes()
dict_magic = b'\x37\xa4\x30\xec'
target_id = 188962279
for m in re.finditer(re.escape(dict_magic), res_data):
    d_id = int.from_bytes(res_data[m.start()+4:m.start()+8], 'little')
    if d_id == target_id:
        dict_data = res_data[m.start():m.start()+112640]
        zstd_dict = zstd.ZstdCompressionDict(dict_data)
        break

dec = zstd.ZstdDecompressor(dict_data=zstd_dict)

# Verify ALL entries in patched ZIP can be decoded
print("\n=== Verifying patched ZIP integrity ===")
patched_data = patched_ca.read_bytes()
zf = zipfile.ZipFile(io.BytesIO(patched_data))
errors = 0
target_entries = ["commonresource/Dance.xml", "PassiveResource/junglemark.xml"]

for entry in zf.infolist():
    raw = zf.read(entry.filename)
    if raw[:4] == PKG_MAGIC:
        expected = struct.unpack('<I', raw[4:8])[0]
        try:
            xml_b = dec.decompress(raw[8:])
            if len(xml_b) != expected:
                print(f"  [WARN] {entry.filename}: size mismatch {len(xml_b)} vs {expected}")
            xml = xml_b.decode('utf-8-sig')
            if entry.filename in target_entries:
                # Verify XML validity
                if '<?xml' not in xml:
                    print(f"  [ERROR] {entry.filename}: NO XML header!")
                    errors += 1
                elif '</Project>' not in xml:
                    print(f"  [ERROR] {entry.filename}: NO </Project> closing tag!")
                    errors += 1
                elif 'SetCameraHeightDuration' not in xml:
                    print(f"  [WARN] {entry.filename}: NO camera track found after patching")
                else:
                    # Find and print the camera track
                    match = re.search(r'<Track trackName="SetCameraHeightDuration0".*?</Track>', xml, re.DOTALL)
                    if match:
                        print(f"  [OK] {entry.filename}: Camera track injected correctly")
                        # Print heightRate value
                        hr = re.search(r'name="heightRate" value="([^"]+)"', match.group())
                        if hr:
                            print(f"       heightRate = {hr.group(1)}")
                    else:
                        print(f"  [WARN] {entry.filename}: has SetCameraHeightDuration text but no Track node")
        except Exception as e:
            print(f"  [ERROR] {entry.filename}: decode failed: {e}")
            errors += 1
    elif raw[:4] == b'PK\x03\x04':
        # Nested ZIP?
        print(f"  [INFO] {entry.filename}: nested ZIP")
    # Non-PKG entries are OK (plain text or other format)

# Compare original and patched entry by entry
print(f"\n=== Comparing original vs patched entries ===")
orig_data = orig_ca.read_bytes()
zf_orig = zipfile.ZipFile(io.BytesIO(orig_data))

orig_names = set(zf_orig.namelist())
patch_names = set(zf.namelist())

if orig_names != patch_names:
    added = patch_names - orig_names
    removed = orig_names - patch_names
    if added: print(f"  Added entries: {added}")
    if removed: print(f"  REMOVED entries: {removed}")
    errors += 1
else:
    print(f"  Entry count: {len(orig_names)} (same)")

# For non-target entries, verify they are IDENTICAL
changed = []
for name in orig_names:
    if name not in patch_names:
        continue
    orig_raw = zf_orig.read(name)
    patch_raw = zf.read(name)
    if orig_raw != patch_raw:
        changed.append(name)

print(f"  Changed entries: {len(changed)}")
for name in changed:
    print(f"    - {name}")
    if name not in target_entries:
        print(f"      !!! UNEXPECTED CHANGE - entry should not be modified !!!")
        errors += 1

zf.close()
zf_orig.close()

# Check test 3: is the game checking the hash of CommonActions independently?
print(f"\n=== Checking hash in verification entries ===")
# The hash of CommonActions in the verification file should match the ORIGINAL hash
# If we change CommonActions, its hash changes, and the verification file still has the old hash
# When game checks: verification says hash should be X, but actual file has hash Y -> CRASH

import hashlib
orig_md5 = hashlib.md5(orig_data).hexdigest()
patched_md5 = hashlib.md5(patched_data).hexdigest()
print(f"Original CommonActions MD5:  {orig_md5}")
print(f"Patched CommonActions MD5:   {patched_md5}")
print(f"Hashes different: {orig_md5 != patched_md5}")

print(f"\nNOTE: Neu game dung verification de check hash cua CommonActions.pkg.bytes,")
print(f"thi sau khi mod, hash khong khop -> game crash.")
print(f"Cach giai quyet: PHAI xoa entry CommonActions khoi verification TRUOC")
print(f"de game khong check hash cua file do nua.")

if errors > 0:
    print(f"\n=== {errors} LOI TIM THAY ===")
else:
    print(f"\n=== KHONG CO LOI - Patching OK ===")
    print("Neu game van crash, co the do:")
    print("1. User chua replace CA DONG THOI voi verification stripped")
    print("2. Game co co che bao ve KHAC ngoai resourceverification")
    print("3. File size thay doi khien game nghi ngam")
