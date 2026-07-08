#!/usr/bin/env python3
"""
strip_verification.py
---------------------
Vô hiệu hoá verification entry của CommonActions.pkg.bytes
trong resourceverificationinfosetall.assetbundle.

Cơ chế (Bypass v3 - path corruption):
  Thay vì XOÁ entry (gây lệch cấu trúc serialized data),
  chỉ SỬA 1 byte trong path để game không tìm thấy file.

  Game đọc danh sách verification tuần tự. Khi gặp entry có path
  "...Commonactions.pkg.bytes" (chữ 'a' thường thay vì 'A'),
  game sẽ không tìm thấy file đó → bỏ qua.
  File thật "CommonActions.pkg.bytes" không có trong danh sách → không bị check hash.

Ưu điểm:
  - Chỉ thay 1 byte, KHÔNG shift, KHÔNG đổi count, KHÔNG đổi cấu trúc.
  - 100% giữ nguyên cấu trúc Unity SerializedFile.
  - Không gây lệch sequential reader.
  - File size giữ nguyên.
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

_CA_PATH_ORIGINAL = b"CommonActions"
_CA_PATH_CORRUPTED = b"Commonactions"
_SEARCH_PATTERN = b"Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"


# ------------------------------------------------------------------ #
#  Bypass logic                                                       #
# ------------------------------------------------------------------ #

def _corrupt_common_actions_path(data: bytearray) -> tuple[bytearray, bool, str]:
    """
    Tìm entry CommonActions trong raw file bytes và sửa 1 byte trong path.
    Đổi 'CommonActions' → 'Commonactions' (chữ 'A' → 'a').
    """
    idx = data.find(_SEARCH_PATTERN)

    if idx < 0:
        corrupted_pattern = _SEARCH_PATTERN.replace(_CA_PATH_ORIGINAL, _CA_PATH_CORRUPTED)
        if data.find(corrupted_pattern) >= 0:
            return data, False, "✅  File đã được bypass trước đó — không cần xử lý."

        if b"CommonActions" in data:
            return data, False, (
                "⚠️  Tìm thấy tên 'CommonActions' nhưng không khớp format chuẩn.\n"
                "    Có thể phiên bản game đã thay đổi cấu trúc."
            )
        return data, False, "✅  Không tìm thấy CommonActions — file đã sạch."

    # Vị trí chữ 'A' trong 'Actions'
    ca_offset_in_pattern = _SEARCH_PATTERN.find(_CA_PATH_ORIGINAL)
    target_byte_offset = idx + ca_offset_in_pattern + len(b"Common")

    if data[target_byte_offset] != ord('A'):
        return data, False, (
            f"⚠️  Byte tại offset 0x{target_byte_offset:X} không phải 'A'. "
            f"Cấu trúc bất thường."
        )

    # Sửa 1 byte: 'A' (0x41) → 'a' (0x61)
    data[target_byte_offset] = ord('a')

    msg = (
        f"✅  Đã bypass verification cho CommonActions.\n"
        f"    Sửa 1 byte tại offset 0x{target_byte_offset:X}: 'A' → 'a'\n"
        f"    Path: ...Commonactions.pkg.bytes\n"
        f"    Cấu trúc file 100% nguyên vẹn."
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
    CommonActions bằng cách sửa 1 byte trong path, lưu ra output_path.
    """
    try:
        data = bytearray(input_path.read_bytes())
    except Exception as e:
        return StripResult(False, f"Không đọc được file: {e}")

    if data[:8] != b"UnityFS\x00":
        return StripResult(False, "Không phải file UnityFS hợp lệ.")

    data, modified, msg = _corrupt_common_actions_path(data)

    if not modified:
        return StripResult(
            success="đã sạch" in msg or "đã được bypass" in msg,
            message=msg,
            output_path=None,
        )

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data)
    except Exception as e:
        return StripResult(False, f"Không lưu được file: {e}")

    return StripResult(success=True, message=msg, output_path=output_path)


# ------------------------------------------------------------------ #
#  CLI                                                                #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Dùng: python strip_verification.py <input> <output>")
        sys.exit(1)
    result = strip_common_actions_from_bundle(Path(sys.argv[1]), Path(sys.argv[2]))
    print(result.message)
    sys.exit(0 if result.success else 1)
