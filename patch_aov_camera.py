#!/usr/bin/env python3
import argparse
import datetime as _dt
import os
import re
import shutil
import struct
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

try:
    import zstandard as zstd
except ImportError:
    print("Missing Python package: zstandard")
    print("Install it with: python -m pip install zstandard")
    sys.exit(1)


TARGET_ENTRIES = (
    "commonresource/Dance.xml",
    "PassiveResource/junglemark.xml",
)

PKG_MAGIC = b"\x22\x4a\x00\xef"
ZSTD_DICT_MAGIC = b"\x37\xa4\x30\xec"
MIN_DICT_SCAN_SIZE = 1024
MAX_DICT_SCAN_SIZE = 1024 * 1024
CAMERA_TRACK_RE = re.compile(
    r"\s*<Track\s+trackName=\"SetCameraHeightDuration0\"[^>]*>.*?</Track>",
    re.DOTALL,
)


@dataclass(frozen=True)
class ExtractedDictionary:
    data: bytes
    source_path: Path
    offset: int
    size: int
    dict_id: int


def build_camera_track(height_rate: float) -> str:
    rate = f"{height_rate:g}"
    return (
        '<Track trackName="SetCameraHeightDuration0" '
        'eventType="SetCameraHeightDuration" '
        'guid="9489c796-894b-4c2e-9a95-acf27873964a" enabled="true" '
        'useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" '
        'execOnForceStopped="false" execOnActionCompleted="false" '
        'stopAfterLastEvent="true"><Event eventName="SetCameraHeightDuration" '
        'time="0.000" length="1.000" isDuration="true" '
        'guid="422a1ed9-a12c-44b3-a9c5-3fe899d689dd">'
        '<int name="slerpTick" value="0" refParamName="" useRefParam="false" />'
        f'<float name="heightRate" value="{rate}" refParamName="" useRefParam="false" />'
        '<bool name="bOverride" value="true" refParamName="" useRefParam="false" />'
        '<bool name="leftTimeSlerpBack" value="true" refParamName="" useRefParam="false" />'
        '<String name="refParamName" value="" refParamName="" useRefParam="false" />'
        "</Event></Track>"
    )


def resolve_common_actions(path: Path) -> Path:
    if path.is_file():
        name = path.name.lower()
        if not (name == "commonactions.pkg.bytes" or (name.startswith("commonactions") and name.endswith(".bytes"))):
            raise SystemExit(f"Input file is not CommonActions*.bytes: {path}")
        return path

    candidates = [
        p for p in path.rglob("CommonActions.pkg.bytes")
        if "Prefab_Hero" in [part for part in p.parts]
    ]
    if not candidates:
        raise SystemExit(f"Cannot find CommonActions.pkg.bytes under: {path}")

    candidates.sort(key=lambda p: (len(p.parts), str(p).lower()))
    return candidates[0]


def resolve_game_assets(path: Path) -> Path:
    if path.is_file():
        return path

    direct = path / "Data" / "resources.assets"
    if direct.exists():
        return direct

    direct = path / "resources.assets"
    if direct.exists():
        return direct

    candidates = sorted(path.rglob("resources.assets"), key=lambda p: (len(p.parts), str(p).lower()))
    if not candidates:
        raise FileNotFoundError(f"Cannot find resources.assets under: {path}")
    return candidates[0]


def read_target_entry_data(pkg_path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(pkg_path, "r") as zin:
        names = set(zin.namelist())
        missing = [name for name in TARGET_ENTRIES if name not in names]
        if missing:
            raise SystemExit("Missing required entries: " + ", ".join(missing))
        return {name: zin.read(name) for name in TARGET_ENTRIES}


def read_entry_dict_ids_from_data(entry_data: dict[str, bytes]) -> dict[str, int]:
    ids: dict[str, int] = {}
    for name in TARGET_ENTRIES:
        data = entry_data[name]
        if not data.startswith(PKG_MAGIC):
            raise ValueError(f"{name} does not start with AoV zstd magic 22 4A 00 EF")
        ids[name] = zstd.get_frame_parameters(data[8:]).dict_id
    return ids


def looks_like_target_xml(raw: bytes) -> bool:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    stripped = text.lstrip()
    return (
        stripped.startswith("<?xml")
        and "<Project" in text
        and "</Project>" in text
        and "<Action" in text
    )


def candidate_decodes_target_entries(candidate: bytes, entry_data: dict[str, bytes]) -> bool:
    try:
        zdict = zstd.ZstdCompressionDict(candidate)
    except zstd.ZstdError:
        return False
    decompressor = zstd.ZstdDecompressor(dict_data=zdict)
    for name, data in entry_data.items():
        if not data.startswith(PKG_MAGIC):
            return False
        expected_size = struct.unpack("<I", data[4:8])[0]
        try:
            raw = decompressor.decompress(data[8:])
        except zstd.ZstdError:
            return False
        if len(raw) != expected_size or not looks_like_target_xml(raw):
            return False
    return True


def extract_raw_dict_from_assets(
    game_assets_path: Path,
    required_ids: dict[str, int] | None = None,
    entry_data: dict[str, bytes] | None = None,
) -> ExtractedDictionary:
    source_path = resolve_game_assets(game_assets_path)
    asset_data = source_path.read_bytes()
    required = sorted({dict_id for dict_id in (required_ids or {}).values() if dict_id})
    if entry_data is None:
        raise ValueError("CommonActions entry data is required when extracting from resources.assets.")

    start = 0
    while True:
        offset = asset_data.find(ZSTD_DICT_MAGIC, start)
        if offset < 0:
            break
        start = offset + 1
        if required and len(asset_data) >= offset + 8:
            header_dict_id = struct.unpack("<I", asset_data[offset + 4:offset + 8])[0]
            if header_dict_id not in required:
                continue

        max_size = min(MAX_DICT_SCAN_SIZE, len(asset_data) - offset)
        sizes = range(MIN_DICT_SCAN_SIZE, max_size + 1)

        for size in sizes:
            end = offset + size
            if end > len(asset_data):
                continue

            candidate = asset_data[offset:end]
            try:
                dict_id = zstd.ZstdCompressionDict(candidate).dict_id()
            except zstd.ZstdError:
                continue

            if required and dict_id not in required:
                continue

            if entry_data is not None and not candidate_decodes_target_entries(candidate, entry_data):
                continue

            return ExtractedDictionary(
                data=candidate,
                source_path=source_path,
                offset=offset,
                size=size,
                dict_id=dict_id,
            )

    required_text = ", ".join(str(dict_id) for dict_id in required) if required else "any"
    raise ValueError(
        f"Cannot extract matching raw zstd dictionary from {source_path}. "
        f"auto-scan <= {MAX_DICT_SCAN_SIZE}, required dict id={required_text}."
    )


def load_dict_from_assets(
    game_assets_path: Path,
    required_ids: dict[str, int],
    entry_data: dict[str, bytes],
) -> zstd.ZstdCompressionDict:
    extracted = extract_raw_dict_from_assets(game_assets_path, required_ids, entry_data)
    print(f"Extracted raw dictionary from: {extracted.source_path}")
    print(
        f"Dictionary offset={extracted.offset}, size={extracted.size}, "
        f"dict id={extracted.dict_id}"
    )
    return zstd.ZstdCompressionDict(extracted.data)


def read_entry_dict_ids(pkg_path: Path) -> dict[str, int]:
    return read_entry_dict_ids_from_data(read_target_entry_data(pkg_path))


def ensure_dict_matches_package(zdict: zstd.ZstdCompressionDict, required_ids: dict[str, int]) -> None:
    required = sorted({dict_id for dict_id in required_ids.values() if dict_id})
    actual = zdict.dict_id()
    if required:
        print("CommonActions required dictionary id(s): " + ", ".join(str(dict_id) for dict_id in required))
        if actual not in required:
            raise ValueError(
                f"Raw dictionary id {actual} does not match CommonActions required dict id(s): "
                + ", ".join(str(dict_id) for dict_id in required)
                + ". This looks like a new game dictionary; refusing to use an old dictionary."
            )
        print(f"Dictionary id OK: {actual}")
    else:
        print("Warning: CommonActions entries do not advertise a zstd dictionary id")


def decode_entry(data: bytes, zdict: zstd.ZstdCompressionDict) -> str:
    if not data.startswith(PKG_MAGIC):
        raise ValueError("entry does not start with AoV zstd magic 22 4A 00 EF")

    expected_size = struct.unpack("<I", data[4:8])[0]
    raw = zstd.ZstdDecompressor(dict_data=zdict).decompress(data[8:])
    if expected_size != len(raw):
        print(f"Warning: decompressed size {len(raw)} != header size {expected_size}")
    return raw.decode("utf-8-sig")


def encode_entry(xml_text: str, zdict: zstd.ZstdCompressionDict, level: int) -> bytes:
    raw = xml_text.encode("utf-8")
    compressed = zstd.ZstdCompressor(
        level=level,
        dict_data=zdict,
        write_content_size=True,
        write_dict_id=True,
    ).compress(raw)
    return PKG_MAGIC + struct.pack("<I", len(raw)) + compressed


def patch_xml(xml_text: str, height_rate: float) -> tuple[str, str]:
    line_ending = "\r\n" if "\r\n" in xml_text else "\n"
    track = "    " + build_camera_track(height_rate)

    if CAMERA_TRACK_RE.search(xml_text):
        patched = CAMERA_TRACK_RE.sub(line_ending + track, xml_text, count=1)
        return patched, "updated existing camera track"

    replacement = f"{line_ending}{track}{line_ending}  </Action>{line_ending}</Project>"
    patched, count = re.subn(
        r"\s*</Action>\s*</Project>\s*$",
        replacement,
        xml_text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError("cannot find final </Action></Project> block")
    return patched, "inserted camera track"


def patch_package(
    pkg_path: Path,
    height_rate: float,
    level: int,
    backup: bool,
    output_path: Path | None = None,
    game_assets_path: Path | None = None,
) -> None:
    entry_data = read_target_entry_data(pkg_path)
    required_ids = read_entry_dict_ids_from_data(entry_data)
    if game_assets_path is not None:
        zdict = load_dict_from_assets(game_assets_path, required_ids, entry_data)
    else:
        raise ValueError("kgvn.app or resources.assets is required.")
    ensure_dict_matches_package(zdict, required_ids)

    statuses: list[str] = []
    tmp_fd, tmp_name = tempfile.mkstemp(prefix="commonactions_", suffix=".pkg.bytes")
    os.close(tmp_fd)
    tmp = Path(tmp_name)

    with zipfile.ZipFile(pkg_path, "r") as zin:
        names = set(zin.namelist())
        missing = [name for name in TARGET_ENTRIES if name not in names]
        if missing:
            raise SystemExit("Missing required entries: " + ", ".join(missing))

        patched_entries: dict[str, bytes] = {}
        for name in TARGET_ENTRIES:
            xml_text = decode_entry(zin.read(name), zdict)
            patched_xml, status = patch_xml(xml_text, height_rate)
            patched_entries[name] = encode_entry(patched_xml, zdict, level)
            statuses.append(f"{name}: {status}")

        try:
            with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_STORED) as zout:
                for item in zin.infolist():
                    data = b"" if item.is_dir() else zin.read(item.filename)
                    if item.filename in patched_entries:
                        data = patched_entries[item.filename]

                    out_info = zipfile.ZipInfo(item.filename, date_time=item.date_time)
                    out_info.external_attr = item.external_attr
                    out_info.comment = item.comment
                    out_info.create_system = item.create_system
                    out_info.compress_type = zipfile.ZIP_STORED
                    zout.writestr(out_info, data)
        except Exception:
            if tmp.exists():
                tmp.unlink()
            raise

    if output_path is None:
        output_path = pkg_path

    if output_path != pkg_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tmp), output_path)
        print(f"Input: {pkg_path}")
        print(f"Output: {output_path}")
    else:
        if backup:
            stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = pkg_path.with_name(pkg_path.name + f".bak_{stamp}")
            shutil.copy2(pkg_path, backup_path)
            print(f"Backup: {backup_path}")

        shutil.move(str(tmp), pkg_path)
        print(f"Patched: {pkg_path}")

    for status in statuses:
        print(status)
    print(f"heightRate={height_rate:g}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch AoV/Lien Quan CommonActions.pkg.bytes camera height.",
    )
    parser.add_argument(
        "input",
        help="CommonActions.pkg.bytes, Ages folder, or Resources/<version> folder",
    )
    parser.add_argument(
        "--game-assets",
        required=True,
        help="kgvn.app folder or Data/resources.assets file to extract raw zstd dictionary",
    )
    parser.add_argument(
        "--height",
        type=float,
        default=1.5,
        help="camera heightRate value, default 1.5",
    )
    parser.add_argument(
        "--level",
        type=int,
        default=17,
        help="zstd compression level, default 17",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="overwrite without creating .bak_TIMESTAMP",
    )
    parser.add_argument(
        "--output",
        help="write patched package to this path instead of overwriting input",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    game_assets_path = Path(args.game_assets).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input does not exist: {input_path}")
    if not game_assets_path.exists():
        raise SystemExit(f"Game assets path does not exist: {game_assets_path}")

    pkg_path = resolve_common_actions(input_path)
    patch_package(
        pkg_path=pkg_path,
        height_rate=args.height,
        level=args.level,
        backup=not args.no_backup,
        output_path=Path(args.output).expanduser().resolve() if args.output else None,
        game_assets_path=game_assets_path,
    )


if __name__ == "__main__":
    main()
