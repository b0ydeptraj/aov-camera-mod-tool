#!/usr/bin/env python3
"""
strip_verification.py
---------------------
Vô hiệu hoá entry CommonActions.pkg.bytes trong
resourceverificationinfosetall.assetbundle.

Cơ chế (v4 - zero path, giữ nguyên cấu trúc):
  1. Tìm path string "Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
  2. Zero toàn bộ path bytes + hash → path rỗng, game không match → bỏ qua
  3. KHÔNG dịch bytes, KHÔNG đổi count, KHÔNG đổi size
  4. File size giữ nguyên, cấu trúc SerializedFile 100% nguyên vẹn
"""

import struct
from dataclasses import dataclass
from pathlib import Path


# ------------------------------------------------------------------ #
#  Kết quả trả về                                                     #
# ------------------------------------------------------------------ #

@dataclass
class StripResult:
    success: bool
    message: str        # Hiển thị cho người dùng
    output_path: Path | None = None


# ------------------------------------------------------------------ #
#  Hằng số                                                            #
# ------------------------------------------------------------------ #

_SEARCH_PATTERN = b"Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
_UNITYFS_MAGIC = b"UnityFS\x00"


# ------------------------------------------------------------------ #
#  Tìm entry và vô hiệu hoá                                          #
# ------------------------------------------------------------------ #

def _find_hash_offset(data: bytearray, path_idx: int, path_len: int) -> int:
    """Tính offset của hash (8 bytes) sau path string + align pad."""
    align_pad = (4 - (path_len % 4)) % 4
    return path_idx + path_len + align_pad


def _nullify_entry(data: bytearray) -> tuple[bytearray, bool, str]:
    """
    Vô hiệu hoá entry CommonActions bằng cách zero path + hash.
    Không dịch bytes, không đổi count, không phá cấu trúc.
    """
    idx = data.find(_SEARCH_PATTERN)

    if idx < 0:
        # Kiểm tra đã xử lý trước đó chưa
        if b"CommonActions" not in data:
            return data, False, "Da xu ly roi — CommonActions khong con trong file."
        return data, False, (
            "Tim thay 'CommonActions' nhung khong khop pattern chuan.\n"
            "    Co the phien ban game da thay doi cau truc."
        )

    # path_len nằm 4 bytes trước path string
    path_len_off = idx - 4
    if path_len_off < 0:
        return data, False, "Khong xac dinh duoc path_len offset."

    path_len = struct.unpack_from("<I", data, path_len_off)[0]

    # Verify path_len khớp
    if path_len != len(_SEARCH_PATTERN):
        # Thử tìm path_len field chính xác
        found = False
        for back in range(5, 80):
            test_off = idx - back
            if test_off < 4:
                break
            test_len = struct.unpack_from("<I", data, test_off)[0]
            if test_len == back:
                path_len_off = test_off
                path_len = test_len
                idx = test_off + 4  # path starts after len field
                found = True
                break
        if not found:
            return data, False, "Khong xac dinh duoc entry boundary."

    hash_off = _find_hash_offset(data, idx, path_len)

    # Lưu hash cũ để log
    old_hash = data[hash_off:hash_off + 8].hex()

    # === ZERO PATH + HASH ===
    # Zero path_len field (4 bytes)
    data[path_len_off:path_len_off + 4] = b"\x00" * 4

    # Zero path bytes
    data[idx:idx + path_len] = b"\x00" * path_len

    # Zero hash (8 bytes)
    data[hash_off:hash_off + 8] = b"\x00" * 8

    total_zeroed = 4 + path_len + 8  # path_len field + path + hash
    # align pad bytes between path and hash are already padding, leave them

    msg = (
        f"Da vo hieu hoa entry CommonActions trong verification.\n"
        f"    Zero {total_zeroed} bytes: path_len(4) + path({path_len}) + hash(8)\n"
        f"    Hash cu: {old_hash}\n"
        f"    Offset: 0x{path_len_off:X}–0x{hash_off + 8:X}\n"
        f"    Cau truc file 100% nguyen ven, khong dich bytes."
    )

    return data, True, msg


# ------------------------------------------------------------------ #
#  Hàm public                                                         #
# ------------------------------------------------------------------ #

def strip_common_actions_from_bundle(
    input_path: Path,
    output_path: Path,
) -> StripResult:
    """
    Đọc resourceverificationinfosetall.assetbundle, vô hiệu hoá entry
    CommonActions bằng cách zero path+hash, lưu ra output_path.
    """
    try:
        data = bytearray(input_path.read_bytes())
    except Exception as e:
        return StripResult(False, f"Khong doc duoc file: {e}")

    if data[:8] != _UNITYFS_MAGIC:
        return StripResult(False, "Khong phai file UnityFS hop le.")

    data, modified, msg = _nullify_entry(data)

    if not modified:
        return StripResult(
            success="Da xu ly" in msg,
            message=msg,
            output_path=None,
        )

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data)
    except Exception as e:
        return StripResult(False, f"Khong luu duoc file: {e}")

    return StripResult(success=True, message=msg, output_path=output_path)


# ------------------------------------------------------------------ #
#  CLI                                                                #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Dung: python strip_verification.py <input> <output>")
        sys.exit(1)
    result = strip_common_actions_from_bundle(Path(sys.argv[1]), Path(sys.argv[2]))
    print(result.message)
    sys.exit(0 if result.success else 1)
