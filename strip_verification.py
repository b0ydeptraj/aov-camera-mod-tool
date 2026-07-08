#!/usr/bin/env python3
"""
strip_verification.py
---------------------
Xoá entry CommonActions.pkg.bytes khỏi
resourceverificationinfosetall.assetbundle.

Cơ chế:
  1. Tìm path string "Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
     trong raw file bytes.
  2. Xác định entry boundary: [4B path_len] [path] [align pad] [8B hash]
  3. Dịch toàn bộ data sau entry lên, lấp chỗ trống bằng 0x00 ở cuối.
  4. Giảm array count đi 1.
  5. File size giữ nguyên (pad zeros ở cuối data region).

Đây là cách tool cũ hoạt động thành công ở các mùa trước.
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
#  Tìm entry và xoá                                                   #
# ------------------------------------------------------------------ #

def _find_entry_bounds(data: bytearray) -> tuple[int, int, int] | None:
    """
    Tìm entry CommonActions trong data.
    Entry format: [4B path_len LE] [path bytes] [align to 4] [8B hash]

    Returns: (entry_start, entry_end, path_len_value) hoặc None nếu không tìm thấy.
    """
    idx = data.find(_SEARCH_PATTERN)
    if idx < 0:
        return None

    # path_len nằm 4 bytes trước path string
    path_len_off = idx - 4
    if path_len_off < 0:
        return None

    path_len = struct.unpack_from("<I", data, path_len_off)[0]
    expected_len = len(_SEARCH_PATTERN)

    if path_len != expected_len:
        # Có thể path string bắt đầu trước "Ages/..." (ví dụ có prefix)
        # Thử tìm path_len phù hợp bằng cách scan ngược
        for back in range(5, 80):
            test_off = idx - back
            if test_off < 4:
                break
            test_len = struct.unpack_from("<I", data, test_off)[0]
            if test_len == back:
                path_len_off = test_off
                path_len = test_len
                break
        else:
            return None

    # Entry start = path_len field
    entry_start = path_len_off

    # After path: align to 4 bytes, then 8 bytes hash
    align_pad = (4 - (path_len % 4)) % 4
    hash_end = entry_start + 4 + path_len + align_pad + 8
    entry_end = hash_end

    return entry_start, entry_end, path_len


def _find_array_count_offset(data: bytearray, entry_start: int) -> int | None:
    """
    Tìm array count field (4 bytes LE) nằm trước entry đầu tiên trong mảng.
    Count nằm trước Behaviac entry (entry đầu tiên), không phải trước CommonActions.
    Scan ngược từ entry_start tới 200 bytes để tìm uint32 hợp lý.
    """
    for back in range(4, 200, 4):
        test_off = entry_start - back
        if test_off < 0:
            break
        val = struct.unpack_from("<I", data, test_off)[0]
        # Array count phải > 0 và hợp lý (khoảng 100-1000 entries)
        if 50 < val < 10000:
            return test_off
    return None


def _strip_entry(data: bytearray) -> tuple[bytearray, bool, str]:
    """
    Xoá entry CommonActions bằng cách dịch bytes và giảm count.
    """
    bounds = _find_entry_bounds(data)
    if bounds is None:
        # Kiểm tra đã xoá trước đó chưa
        if b"CommonActions" not in data:
            return data, False, "✅  Không tìm thấy CommonActions — file đã sạch."
        return data, False, (
            "⚠️  Tìm thấy 'CommonActions' nhưng không xác định được entry boundary.\n"
            "    Có thể cấu trúc file đã thay đổi."
        )

    entry_start, entry_end, path_len = bounds
    entry_size = entry_end - entry_start

    # Tìm data region boundary
    # Block info nằm ở cuối file (flag 0x40 trong UnityFS header)
    # Đọc compressed block info size từ header
    pos = 12
    while pos < len(data) and data[pos] != 0:
        pos += 1
    pos += 1  # skip null
    while pos < len(data) and data[pos] != 0:
        pos += 1
    pos += 1  # skip null

    comp_info_size = struct.unpack_from(">I", data, pos + 8)[0]
    flags = struct.unpack_from(">I", data, pos + 16)[0]

    has_dir_at_end = (flags & 0x40) != 0
    if has_dir_at_end:
        data_region_end = len(data) - comp_info_size
    else:
        data_region_end = len(data)

    # Dịch bytes: mọi thứ sau entry dịch lên entry_size bytes
    shift_src = entry_end
    shift_dst = entry_start
    shift_len = data_region_end - entry_end

    if shift_len > 0:
        data[shift_dst:shift_dst + shift_len] = data[shift_src:shift_src + shift_len]

    # Pad zeros ở cuối data region
    pad_start = shift_dst + shift_len
    data[pad_start:pad_start + entry_size] = b"\x00" * entry_size

    # Giảm array count
    count_off = _find_array_count_offset(data, entry_start)
    count_msg = ""
    if count_off is not None:
        old_count = struct.unpack_from("<I", data, count_off)[0]
        struct.pack_into("<I", data, count_off, old_count - 1)
        count_msg = (
            f"    Array count: {old_count} → {old_count - 1} "
            f"(offset 0x{count_off:X})\n"
        )
    else:
        count_msg = "    ⚠️  Không tìm thấy array count — chỉ dịch bytes.\n"

    # Verify
    still_found = data.find(b"CommonActions")

    msg = (
        f"✅  Đã xoá entry CommonActions khỏi verification.\n"
        f"    Entry: offset 0x{entry_start:X}–0x{entry_end:X} ({entry_size} bytes)\n"
        f"    Dịch {shift_len} bytes lên, pad {entry_size} bytes zeros.\n"
        f"{count_msg}"
    )

    if still_found >= 0:
        msg += f"    ⚠️  Vẫn còn 'CommonActions' tại 0x{still_found:X} — có thể có nhiều entry.\n"
    else:
        msg += "    ✓  Xác nhận: CommonActions đã bị xoá hoàn toàn.\n"

    return data, True, msg


# ------------------------------------------------------------------ #
#  Hàm public                                                         #
# ------------------------------------------------------------------ #

def strip_common_actions_from_bundle(
    input_path: Path,
    output_path: Path,
) -> StripResult:
    """
    Đọc resourceverificationinfosetall.assetbundle, xoá entry
    CommonActions, lưu ra output_path.
    """
    try:
        data = bytearray(input_path.read_bytes())
    except Exception as e:
        return StripResult(False, f"Không đọc được file: {e}")

    if data[:8] != _UNITYFS_MAGIC:
        return StripResult(False, "Không phải file UnityFS hợp lệ.")

    data, modified, msg = _strip_entry(data)

    if not modified:
        return StripResult(
            success="đã sạch" in msg or "đã được" in msg,
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
