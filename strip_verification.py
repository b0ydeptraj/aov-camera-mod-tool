#!/usr/bin/env python3
"""
strip_verification.py
---------------------
Tìm và xoá entry CommonActions.pkg.bytes khỏi resourceverificationinfosetall.assetbundle.

Cơ chế (Bypass):
  Thay vì trình thẻ giả, ta rút thẻ CommonActions ra khỏi danh sách kiểm soát.
  Game đọc danh sách, không thấy CommonActions, nên không kiểm tra và không restore.

Format mỗi entry trong verification list:
  [4 bytes LE: độ dài chuỗi] [chuỗi path] [null + padding align 4] [8 bytes hash ID]

Phương pháp:
  1. Parse UnityFS header và block info.
  2. Decompress block info (LZ4) để lấy block storage metadata.
  3. Trích payload (data block - thường uncompressed).
  4. Tìm entry CommonActions bằng pattern chuỗi.
  5. Xoá 72 bytes của entry, shift các byte còn lại lên và pad 72 byte zeros ở cuối payload.
  6. Giảm array count đi 1.
  7. Cập nhật SerializedFile file_size trong header.
  8. Recompress block info và rebuild file UnityFS.

Kết quả: File mới có cùng kích thước, cấu trúc còn nguyên, không còn CommonActions.
"""

import struct
from dataclasses import dataclass
from pathlib import Path

try:
    import lz4.block as _lz4_block
    _HAS_LZ4 = True
except ImportError:
    _HAS_LZ4 = False

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

# Padding sau chuỗi (null + 1 byte pad để align 4: (58+1)=59 -> next multiple of 4 is 60)
_CA_NULL_PAD = b"\x00\x00"

# Mỗi entry = 4B length_prefix + 58B path + 2B null/pad + 8B hash = 72 bytes
_CA_ENTRY_SIZE = 4 + _CA_PATH_LEN + 2 + 8


def _build_ca_prefix() -> bytes:
    """Trả về pattern tìm kiếm: length_prefix + path (không bao gồm null/pad/hash vì hash thay đổi)."""
    return struct.pack("<I", _CA_PATH_LEN) + _CA_PATH


# ------------------------------------------------------------------ #
#  Parse UnityFS header                                               #
# ------------------------------------------------------------------ #

class _ParseError(Exception):
    pass


def _parse_unityfs_header(data: bytes) -> dict:
    """
    Parse header UnityFS, trả về dict với các trường cần thiết.
    Raises _ParseError nếu không phải UnityFS hợp lệ.
    """
    if data[:8] != b"UnityFS\x00":
        raise _ParseError("Không phải file UnityFS hợp lệ (magic bytes sai).")

    pos = 8
    fmt_ver = struct.unpack_from(">I", data, pos)[0]; pos += 4
    # unity_ver string
    end = data.index(b"\x00", pos); pos = end + 1
    # unity_rev string
    end = data.index(b"\x00", pos); pos = end + 1

    file_size = struct.unpack_from(">Q", data, pos)[0]; pos += 8
    comp_info_size = struct.unpack_from(">I", data, pos)[0]; pos += 4
    uncomp_info_size = struct.unpack_from(">I", data, pos)[0]; pos += 4
    flags = struct.unpack_from(">I", data, pos)[0]; pos += 4

    header_end = pos
    compression = flags & 0x3F
    block_info_at_end = bool(flags & 0x80)
    block_info_aligned = bool(flags & 0x200)

    if block_info_at_end:
        info_start = len(data) - comp_info_size
    else:
        info_start = header_end
        if block_info_aligned:
            info_start = (info_start + 15) & ~15

    return {
        "fmt_ver": fmt_ver,
        "file_size": file_size,
        "comp_info_size": comp_info_size,
        "uncomp_info_size": uncomp_info_size,
        "flags": flags,
        "compression": compression,
        "block_info_at_end": block_info_at_end,
        "info_start": info_start,
        "header_end": header_end,
    }


# ------------------------------------------------------------------ #
#  Parse block info                                                   #
# ------------------------------------------------------------------ #

def _decompress_block_info(data: bytes, hdr: dict) -> bytes:
    """Decompress block info từ file data."""
    comp_data = data[hdr["info_start"]: hdr["info_start"] + hdr["comp_info_size"]]
    compression = hdr["compression"]

    if compression == 0:
        return comp_data
    elif compression == 2:  # LZMA
        raise _ParseError(
            "Block info dùng LZMA - file có thể bị mã hoá hoặc dùng build pipeline tuỳ chỉnh.\n"
            "Không thể tự động xử lý. Cần can thiệp thủ công hoặc AI."
        )
    elif compression == 3:  # LZ4
        if not _HAS_LZ4:
            raise _ParseError("Thiếu thư viện lz4. Hãy cài: pip install lz4")
        return _lz4_block.decompress(comp_data, uncompressed_size=hdr["uncomp_info_size"])
    else:
        raise _ParseError(
            f"Block info dùng compression không xác định (0x{compression:02x}).\n"
            "Không thể tự động xử lý. Cần can thiệp thủ công hoặc AI."
        )


def _parse_blocks_only(raw: bytes) -> tuple[list[tuple], int]:
    """
    Parse chỉ danh sách storage blocks từ block_info (bỏ qua nodes).
    Trả về (blocks, data_size_total).
    blocks = [(uncomp, comp, flags), ...]
    """
    pos = 16  # Skip 16-byte hash
    num_blocks = struct.unpack_from(">I", raw, pos)[0]; pos += 4
    blocks = []
    total_comp = 0
    for _ in range(num_blocks):
        b_uncomp = struct.unpack_from(">I", raw, pos)[0]; pos += 4
        b_comp = struct.unpack_from(">I", raw, pos)[0]; pos += 4
        b_flags = struct.unpack_from(">H", raw, pos)[0]; pos += 2
        blocks.append((b_uncomp, b_comp, b_flags))
        total_comp += b_comp
    return blocks, total_comp


# ------------------------------------------------------------------ #
#  Đọc data payload                                                   #
# ------------------------------------------------------------------ #

def _read_data_payload(data: bytes, hdr: dict, blocks: list[tuple]) -> tuple[bytearray, int]:
    """
    Đọc toàn bộ data blocks, decompress nếu cần.
    Trả về (payload_bytearray, data_start_offset_in_file).
    """
    data_start = hdr["info_start"] + hdr["comp_info_size"]
    full_data = bytearray()
    off = data_start

    for b_uncomp, b_comp, b_flags in blocks:
        raw_block = data[off: off + b_comp]
        b_compression = b_flags & 0x3F

        if b_compression == 0:
            full_data += raw_block
        elif b_compression == 2:
            raise _ParseError(
                "Data block dùng LZMA - file có thể bị mã hoá hoặc dùng build pipeline tuỳ chỉnh.\n"
                "Không thể tự động xử lý. Cần can thiệp thủ công hoặc AI."
            )
        elif b_compression == 3:
            if not _HAS_LZ4:
                raise _ParseError("Thiếu thư viện lz4. Hãy cài: pip install lz4")
            full_data += _lz4_block.decompress(raw_block, uncompressed_size=b_uncomp)
        else:
            raise _ParseError(
                f"Data block dùng compression không xác định (0x{b_compression:02x}).\n"
                "Không thể tự động xử lý. Cần can thiệp thủ công hoặc AI."
            )
        off += b_comp

    # Nối thêm bất kỳ bytes thừa nào ở cuối file (không nằm trong blocks)
    # Điều này đảm bảo khi ta shift payload, phần đuôi thừa (ví dụ 15 bytes) cũng được shift theo.
    if off < len(data):
        full_data += data[off:]

    return full_data, data_start


# ------------------------------------------------------------------ #
#  Tìm và xoá CommonActions                                           #
# ------------------------------------------------------------------ #

def _strip_common_actions(payload: bytearray) -> tuple[bytearray, bool, str]:
    """
    Tìm và xoá entry CommonActions trong payload.
    Trả về (payload_mới, đã_xoá, thông_báo).
    """
    prefix = _build_ca_prefix()
    ca_idx = payload.find(prefix)

    if ca_idx < 0:
        # Kiểm tra có tồn tại chuỗi CommonActions không (có thể format khác)
        if b"CommonActions" in payload:
            return payload, False, (
                "⚠️  Tìm thấy tên 'CommonActions' nhưng không khớp format entry chuẩn.\n"
                "    Có thể phiên bản game này đã thay đổi cấu trúc.\n"
                "    Cần can thiệp thủ công hoặc AI để phân tích."
            )
        # Không có CommonActions gì cả
        return payload, False, "✅  Không tìm thấy CommonActions trong danh sách — file đã sạch, không cần xử lý."

    # Xác định vị trí entry: ca_idx đã trỏ vào length prefix (4 bytes)
    # Verify null terminator ngay sau path (tại ca_idx + 4 + 58 = ca_idx + 62)
    str_end = ca_idx + 4 + _CA_PATH_LEN  # vị trí null terminator
    if payload[str_end] != 0x00:
        return payload, False, (
            "⚠️  Tìm thấy entry CommonActions nhưng không có null terminator đúng vị trí.\n"
            "    Cấu trúc file bất thường. Cần can thiệp thủ công hoặc AI."
        )

    entry_start_actual = ca_idx           # ca_idx đã là vị trí length prefix
    entry_end = entry_start_actual + _CA_ENTRY_SIZE  # = ca_idx + 72

    if entry_end > len(payload):
        return payload, False, (
            "⚠️  Entry CommonActions bị cắt ngắn ở cuối file — cấu trúc bất thường.\n"
            "    Cần can thiệp thủ công hoặc AI."
        )

    # --- Tìm và cập nhật array count (nằm 4 bytes ngay trước entry đầu tiên của mảng)
    # Mảng này là danh sách path+hash trong MonoBehaviour serialized.
    # Count là int32 LE ngay trước toàn bộ mảng.
    # Chúng ta tìm backwards từ vị trí entry đầu tiên (entry_start_actual)
    # bằng cách tìm count hiện tại (>= số entry thực tế).
    # Cách an toàn: dùng pattern "scan backward" tìm int32 có giá trị hợp lý (200–500).
    count_offset = _find_array_count(payload, entry_start_actual)
    if count_offset < 0:
        return payload, False, (
            "⚠️  Không tìm được vị trí array count trong serialized data.\n"
            "    Cần can thiệp thủ công hoặc AI."
        )

    old_count = struct.unpack_from("<I", payload, count_offset)[0]
    new_count = old_count - 1

    # --- Thực hiện xoá entry: shift bytes lên trái ---
    # Lưu phần bytes từ entry_end đến cuối payload (sẽ được dịch lên)
    size = len(payload)
    after_entry = bytes(payload[entry_end:])   # bytes sau entry (sẽ shift lên)
    # Dịch lên: ghi after_entry bắt đầu từ entry_start_actual
    payload[entry_start_actual: entry_start_actual + len(after_entry)] = after_entry
    # Pad zeros cho phần còn lại (phần đã shift đi, kích thước = entry_size)
    new_tail_start = entry_start_actual + len(after_entry)
    payload[new_tail_start:size] = b"\x00" * (size - new_tail_start)

    # --- Cập nhật count (vị trí không đổi sau khi shift vì nó nằm TRƯỚC entry) ---
    struct.pack_into("<I", payload, count_offset, new_count)

    msg = (
        f"✅  Đã xoá entry CommonActions ({_CA_ENTRY_SIZE} bytes).\n"
        f"    Array count: {old_count} → {new_count}\n"
        f"    Payload size giữ nguyên: {size} bytes (đã pad {_CA_ENTRY_SIZE} zeros ở đuôi)."
    )
    return payload, True, msg


def _find_array_count(payload: bytearray, first_entry_offset: int) -> int:
    """
    Tìm vị trí array count trong serialized data bằng cách scan backward.
    Tìm int32 LE có giá trị 100–1000 trong 200 byte trước first_entry_offset.
    Ưu tiên vị trí gần nhất.
    """
    search_start = max(0, first_entry_offset - 200)
    candidates = []

    for i in range(first_entry_offset - 4, search_start - 1, -4):
        val = struct.unpack_from("<I", payload, i)[0]
        if 100 <= val <= 1000:
            candidates.append(i)

    # Chọn vị trí gần first_entry_offset nhất
    return candidates[0] if candidates else -1


def _update_sf_file_size(payload: bytearray, removed_bytes: int) -> None:
    """
    Cập nhật trường file_size bên trong SerializedFile header.
    SerializedFile lưu file_size tại một offset cụ thể (big-endian Q).
    Scan tìm giá trị phù hợp với payload size và giảm đi removed_bytes.
    """
    orig_size = len(payload)  # payload đã bị shift nhưng giữ size (vì pad zeros)
    expected_old = orig_size   # old file_size = current payload size (before strip)
    # Scan các offset thường gặp
    for try_offset in [39, 43, 31, 27, 35]:
        if try_offset + 8 > len(payload):
            continue
        val = struct.unpack_from(">Q", payload, try_offset)[0]
        # Giá trị file_size gốc nên bằng kích thước payload (vì block là uncompressed)
        if abs(val - orig_size) <= 256:  # cho phép sai số nhỏ do header metadata
            struct.pack_into(">Q", payload, try_offset, val - removed_bytes)
            return


# ------------------------------------------------------------------ #
#  Rebuild UnityFS file                                               #
# ------------------------------------------------------------------ #

def _rebuild_unityfs(
    orig_data: bytes,
    hdr: dict,
    payload: bytearray,
) -> bytes:
    """
    Rebuild file UnityFS từ payload đã sửa.
    Kích thước payload giữ nguyên → giữ nguyên TOÀN BỘ header + block_info gốc.
    Chỉ thay phần data payload, đảm bảo file size y hệt bản gốc.
    """
    # data_start = vị trí bắt đầu của payload trong file gốc
    data_start = hdr["info_start"] + hdr["comp_info_size"]

    # Giữ nguyên tất cả bytes trước payload (header + block_info_compressed)
    before = orig_data[:data_start]

    # payload đã được shift và pad zeros — kích thước bằng len(orig_data) - data_start
    return bytes(before) + bytes(payload)


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
        data = input_path.read_bytes()
    except Exception as e:
        return StripResult(False, f"Không đọc được file: {e}")

    # 1. Parse UnityFS header
    try:
        hdr = _parse_unityfs_header(data)
    except _ParseError as e:
        return StripResult(False, str(e))
    except Exception as e:
        return StripResult(False, f"Lỗi parse header: {e}\nCó thể file bị mã hoá. Cần can thiệp thủ công hoặc AI.")

    # 2. Decompress block info
    try:
        block_info_raw = _decompress_block_info(data, hdr)
    except _ParseError as e:
        return StripResult(False, str(e))
    except Exception as e:
        return StripResult(False, f"Lỗi decompress block info: {e}\nCó thể file bị mã hoá. Cần can thiệp thủ công hoặc AI.")

    # 3. Parse blocks (bỏ qua nodes — không cần để patch payload)
    try:
        blocks, _ = _parse_blocks_only(block_info_raw)
    except Exception as e:
        return StripResult(False, f"Lỗi parse block info structure: {e}\nCần can thiệp thủ công hoặc AI.")

    # 4. Kiểm tra block nén để đảm bảo data accessible
    for i, (b_uncomp, b_comp, b_flags) in enumerate(blocks):
        b_compression = b_flags & 0x3F
        if b_compression not in (0, 3):
            return StripResult(
                False,
                f"Data block #{i} dùng compression type 0x{b_compression:02x} không hỗ trợ.\n"
                "Có thể file bị mã hoá bằng key tuỳ chỉnh.\nCần can thiệp thủ công hoặc AI."
            )

    # 5. Đọc payload
    try:
        payload, data_start = _read_data_payload(data, hdr, blocks)
    except _ParseError as e:
        return StripResult(False, str(e))
    except Exception as e:
        return StripResult(False, f"Lỗi đọc data block: {e}\nCần can thiệp thủ công hoặc AI.")

    # 6. Tìm và xoá CommonActions
    payload, stripped, msg = _strip_common_actions(payload)

    if not stripped:
        # Trả về thông báo (có thể là "đã sạch" hoặc cảnh báo)
        return StripResult(
            success=b"CommonActions" not in payload,  # True nếu đã sạch
            message=msg,
            output_path=None,
        )

    # 7. Rebuild UnityFS (giữ nguyên header + block_info gốc, chỉ thay payload)
    try:
        new_data = _rebuild_unityfs(data, hdr, payload)
    except Exception as e:
        return StripResult(False, f"Lỗi rebuild UnityFS: {e}")

    # 8. Lưu file
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(new_data)
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
