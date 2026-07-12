#!/usr/bin/env python3
"""
strip_verification.py
---------------------
Vô hiệu hoá entry CommonActions.pkg.bytes trong
resourceverificationinfosetall.assetbundle.

Cơ chế (v5 - rename path, giữ nguyên 100% cấu trúc):
  1. Tìm path string "Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
  2. Thay NỘI DUNG path bằng chuỗi cùng độ dài nhưng khác tên
     "Ages/Prefab_Characters/Prefab_Hero/_ommonActions.pkg.bytes"
     (Thay 'C' đầu thành '_' — ký tự hợp lệ nhưng không tồn tại)
  3. KHÔNG zero path_len, KHÔNG dịch bytes, KHÔNG đổi count
  4. Cấu trúc SerializedFile 100% nguyên vẹn, Unity reader parse bình thường
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
    message: str
    output_path: Path | None = None


# ------------------------------------------------------------------ #
#  Hằng số                                                            #
# ------------------------------------------------------------------ #

_SEARCH_PATTERN = b"Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
_UNITYFS_MAGIC = b"UnityFS\x00"

# Thay 'C' trong 'CommonActions' thành '_'
# → "_ommonActions.pkg.bytes" — file không tồn tại trên bất kỳ OS
_REPLACE_OFFSET = _SEARCH_PATTERN.index(b"CommonActions")
_ORIGINAL_CHAR = ord('C')   # 0x43
_REPLACE_CHAR  = ord('_')   # 0x5F


# ------------------------------------------------------------------ #
#  Logic                                                               #
# ------------------------------------------------------------------ #

def _rename_entry(data: bytearray) -> tuple[bytearray, bool, str]:
    """
    Rename path CommonActions → _ommonActions trong verification list.
    Chỉ thay 1 byte, giữ nguyên tuyệt đối mọi thứ khác.
    """
    idx = data.find(_SEARCH_PATTERN)

    if idx < 0:
        # Kiểm tra đã rename trước đó chưa
        renamed = bytearray(_SEARCH_PATTERN)
        renamed[_REPLACE_OFFSET] = _REPLACE_CHAR
        if bytes(renamed) in data:
            return data, False, "Da xu ly truoc do — entry da duoc rename thanh _ommonActions."

        if b"CommonActions" not in data:
            return data, False, "Khong tim thay CommonActions trong file."

        return data, False, (
            "Tim thay 'CommonActions' nhung khong khop pattern day du.\n"
            "    Co the phien ban game da thay doi cau truc."
        )

    # Vị trí byte 'C' cần thay
    target_offset = idx + _REPLACE_OFFSET

    if data[target_offset] != _ORIGINAL_CHAR:
        return data, False, (
            f"Byte tai offset 0x{target_offset:X} khong phai 'C' "
            f"(la 0x{data[target_offset]:02X}). Cau truc bat thuong."
        )

    # Thay 1 byte: 'C' (0x43) → '_' (0x5F)
    data[target_offset] = _REPLACE_CHAR

    msg = (
        f"Da vo hieu hoa entry CommonActions trong verification.\n"
        f"    Doi 1 byte tai offset 0x{target_offset:X}: "
        f"'C' (0x{_ORIGINAL_CHAR:02X}) -> '_' (0x{_REPLACE_CHAR:02X})\n"
        f"    Path moi: ..._ommonActions.pkg.bytes\n"
        f"    File nay khong ton tai -> game bo qua verification.\n"
        f"    Cau truc file 100% nguyen ven, chi khac 1 byte."
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
    Đọc resourceverificationinfosetall.assetbundle, rename entry
    CommonActions → _ommonActions, lưu ra output_path.
    """
    try:
        data = bytearray(input_path.read_bytes())
    except Exception as e:
        return StripResult(False, f"Khong doc duoc file: {e}")

    if data[:8] != _UNITYFS_MAGIC:
        return StripResult(False, "Khong phai file UnityFS hop le.")

    data, modified, msg = _rename_entry(data)

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
