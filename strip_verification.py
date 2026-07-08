#!/usr/bin/env python3
"""
strip_verification.py
---------------------
Tìm và xoá entry CommonActions.pkg.bytes khỏi resourceverificationinfosetall.assetbundle.

Cơ chế (Bypass):
  Rút thẻ CommonActions ra khỏi danh sách kiểm soát.
  Game đọc danh sách, không thấy CommonActions, nên không kiểm tra và không restore.

Format mỗi entry trong verification list:
  [4 bytes LE: độ dài chuỗi] [chuỗi path] [null + padding align 4] [8 bytes hash ID]

Phương pháp (v2 - direct raw bytes):
  1. Tìm entry CommonActions trực tiếp trong RAW FILE bytes (không cần parse UnityFS payload).
  2. Tìm ranh giới mảng chứa entry (scan entries liên tiếp trước/sau CA).
  3. Shift CHỈ trong phạm vi mảng đó (không đụng data ngoài mảng).
  4. Giảm array count đi 1.
  5. Giữ nguyên file size (zero-fill phần cuối mảng).

Kết quả: File mới có cùng kích thước, chỉ mảng chứa CA bị sửa, mọi data khác nguyên vẹn.
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
#  Hằng số / Pattern                                                  #
# ------------------------------------------------------------------ #

# Path của CommonActions trong verification list
_CA_PATH = b"Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
_CA_PATH_LEN = len(_CA_PATH)   # 58

# Mỗi entry = 4B length_prefix + 58B path + 2B null/pad + 8B hash = 72 bytes
_CA_ENTRY_SIZE = 4 + _CA_PATH_LEN + 2 + 8   # 72


def _build_ca_prefix() -> bytes:
    """Trả về pattern tìm kiếm: length_prefix + path."""
    return struct.pack("<I", _CA_PATH_LEN) + _CA_PATH


# ------------------------------------------------------------------ #
#  Entry scanning helpers                                             #
# ------------------------------------------------------------------ #

def _entry_size_at(data: bytes, pos: int) -> int | None:
    """
    Tại vị trí pos, kiểm tra xem có phải 1 entry hợp lệ không.
    Trả về kích thước entry nếu hợp lệ, None nếu không.
    Entry format: [4B LE length] [path bytes] [null+pad align 4] [8B hash]
    """
    if pos + 4 > len(data):
        return None
    str_len = struct.unpack_from("<I", data, pos)[0]
    if str_len < 1 or str_len > 300:
        return None
    path_start = pos + 4
    if path_start + str_len > len(data):
        return None
    path_bytes = data[path_start:path_start + str_len]
    # Path phải là printable ASCII
    if not all(32 <= b < 128 for b in path_bytes):
        return None
    # Phải có dấu chấm (tên file)
    if b"." not in path_bytes:
        return None
    # Null padding: align (str_len + 1) lên bội 4
    padded = ((str_len + 1 + 3) // 4) * 4
    null_pad_size = padded - str_len
    hash_start = path_start + str_len + null_pad_size
    entry_end = hash_start + 8
    if entry_end > len(data):
        return None
    # Verify null terminator
    if data[path_start + str_len] != 0x00:
        return None
    return entry_end - pos


def _scan_array_bounds(data: bytes, ca_offset: int) -> tuple[int, int, int]:
    """
    Từ vị trí entry CommonActions (ca_offset), tìm:
    - array_start: offset bắt đầu entry đầu tiên của mảng
    - array_end: offset cuối cùng entry cuối cùng của mảng
    - count_offset: offset của int32 array count (ngay trước array_start)

    Scan backward từ ca_offset để tìm entry đầu tiên, scan forward để tìm entry cuối.
    """
    # --- Scan backward: tìm entry đầu tiên của mảng ---
    array_start = ca_offset
    pos = ca_offset
    while True:
        # Thử lùi: scan từng byte backward tìm entry hợp lệ ngay trước pos
        found_prev = False
        # Thử mỗi khoảng cách possible (entry sizes từ 12 đến 320 bytes)
        for try_back in range(12, 320):
            prev_pos = pos - try_back
            if prev_pos < 0:
                break
            entry_sz = _entry_size_at(data, prev_pos)
            if entry_sz is not None and prev_pos + entry_sz == pos:
                # Entry trước kết thúc ngay tại pos → liên tiếp
                array_start = prev_pos
                pos = prev_pos
                found_prev = True
                break
        if not found_prev:
            break

    # --- Scan forward: tìm entry cuối cùng của mảng ---
    array_end = ca_offset + _CA_ENTRY_SIZE
    pos = array_end
    while True:
        entry_sz = _entry_size_at(data, pos)
        if entry_sz is None:
            break
        pos += entry_sz
        array_end = pos

    # --- Tìm array count: int32 LE ngay trước array_start ---
    count_offset = array_start - 4
    if count_offset < 0:
        count_offset = -1

    return array_start, array_end, count_offset


# ------------------------------------------------------------------ #
#  Strip CommonActions (v2 - chỉ shift trong mảng)                    #
# ------------------------------------------------------------------ #

def _strip_common_actions_v2(data: bytearray) -> tuple[bytearray, bool, str]:
    """
    Tìm và xoá entry CommonActions trực tiếp trong raw file bytes.
    Chỉ shift bytes TRONG mảng chứa CA, không đụng data ngoài mảng.
    Trả về (data_mới, đã_xoá, thông_báo).
    """
    prefix = _build_ca_prefix()
    ca_idx = data.find(prefix)

    if ca_idx < 0:
        if b"CommonActions" in data:
            return data, False, (
                "⚠️  Tìm thấy tên 'CommonActions' nhưng không khớp format entry chuẩn.\n"
                "    Có thể phiên bản game này đã thay đổi cấu trúc.\n"
                "    Cần can thiệp thủ công hoặc AI để phân tích."
            )
        return data, False, "✅  Không tìm thấy CommonActions trong danh sách — file đã sạch, không cần xử lý."

    # Verify entry structure
    str_end_pos = ca_idx + 4 + _CA_PATH_LEN
    if str_end_pos >= len(data) or data[str_end_pos] != 0x00:
        return data, False, (
            "⚠️  Tìm thấy entry CommonActions nhưng cấu trúc bất thường.\n"
            "    Cần can thiệp thủ công hoặc AI."
        )

    entry_start = ca_idx
    entry_end = entry_start + _CA_ENTRY_SIZE
    if entry_end > len(data):
        return data, False, (
            "⚠️  Entry CommonActions bị cắt ngắn ở cuối file.\n"
            "    Cần can thiệp thủ công hoặc AI."
        )

    # Tìm ranh giới mảng
    array_start, array_end, count_offset = _scan_array_bounds(data, entry_start)
    array_size = array_end - array_start

    if count_offset < 0:
        return data, False, (
            "⚠️  Không tìm được array count.\n"
            "    Cần can thiệp thủ công hoặc AI."
        )

    old_count = struct.unpack_from("<I", data, count_offset)[0]
    new_count = old_count - 1

    # --- Thực hiện xoá: shift CHỈ trong phạm vi mảng ---
    # Phần bytes sau entry CA đến hết mảng
    after_ca_in_array = bytes(data[entry_end:array_end])
    # Ghi đè: bắt đầu từ entry_start
    data[entry_start:entry_start + len(after_ca_in_array)] = after_ca_in_array
    # Zero-fill phần cuối mảng (72 bytes cuối)
    new_array_tail = entry_start + len(after_ca_in_array)
    data[new_array_tail:array_end] = b"\x00" * (array_end - new_array_tail)

    # Cập nhật array count
    struct.pack_into("<I", data, count_offset, new_count)

    msg = (
        f"✅  Đã xoá entry CommonActions ({_CA_ENTRY_SIZE} bytes).\n"
        f"    Array count: {old_count} → {new_count}\n"
        f"    Array range: [0x{array_start:X}, 0x{array_end:X}] ({array_size} bytes)\n"
        f"    Chỉ shift {len(after_ca_in_array)} bytes trong mảng, data ngoài mảng NGUYÊN VẸN."
    )
    return data, True, msg


# ------------------------------------------------------------------ #
#  Hàm public chính                                                   #
# ------------------------------------------------------------------ #

def strip_common_actions_from_bundle(
    input_path: Path,
    output_path: Path,
) -> StripResult:
    """
    Đọc resourceverificationinfosetall.assetbundle, xoá CommonActions,
    lưu file mới ra output_path.

    Returns StripResult với success=True nếu thành công.
    """
    try:
        data = bytearray(input_path.read_bytes())
    except Exception as e:
        return StripResult(False, f"Không đọc được file: {e}")

    # Verify đây là UnityFS
    if data[:8] != b"UnityFS\x00":
        return StripResult(False, "Không phải file UnityFS hợp lệ (magic bytes sai).")

    # Tìm và xoá CommonActions trực tiếp trên raw bytes
    data, stripped, msg = _strip_common_actions_v2(data)

    if not stripped:
        return StripResult(
            success=b"CommonActions" not in data,
            message=msg,
            output_path=None,
        )

    # Lưu file (giữ nguyên kích thước)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data)
    except Exception as e:
        return StripResult(False, f"Không lưu được file: {e}")

    return StripResult(
        success=True,
        message=msg,
        output_path=output_path,
    )


# ------------------------------------------------------------------ #
#  CLI test                                                           #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Dùng: python strip_verification.py <input.assetbundle> <output.assetbundle>")
        sys.exit(1)

    result = strip_common_actions_from_bundle(Path(sys.argv[1]), Path(sys.argv[2]))
    print(result.message)
    if result.output_path:
        print(f"Output: {result.output_path}")
    sys.exit(0 if result.success else 1)
