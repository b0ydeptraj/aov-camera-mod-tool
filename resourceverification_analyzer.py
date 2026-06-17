#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


RESOURCEVERIFICATION_NAME = "resourceverificationinfosetall.assetbundle"
COMMONACTIONS_NAME = b"CommonActions.pkg.bytes"
COMMONACTIONS_PATH_SLASH = b"Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
COMMONACTIONS_PATH_BACKSLASH = b"Ages\\Prefab_Characters\\Prefab_Hero\\CommonActions.pkg.bytes"
COMMONACTIONS_RESOURCE_ID = bytes.fromhex("c9cc946d3f89f32e")


def resolve_resourceverification(path: Path) -> Path:
    path = Path(path)
    if path.is_file():
        return path

    direct = path / "assetbundle" / RESOURCEVERIFICATION_NAME
    if direct.exists():
        return direct

    direct = path / RESOURCEVERIFICATION_NAME
    if direct.exists():
        return direct

    candidates = sorted(path.rglob(RESOURCEVERIFICATION_NAME), key=lambda p: (len(p.parts), str(p).lower()))
    if not candidates:
        raise FileNotFoundError(f"Cannot find {RESOURCEVERIFICATION_NAME} under: {path}")
    return candidates[0]


def contains_commonactions(data: bytes) -> bool:
    return (
        COMMONACTIONS_NAME in data
        or COMMONACTIONS_PATH_SLASH in data
        or COMMONACTIONS_PATH_BACKSLASH in data
        or COMMONACTIONS_RESOURCE_ID in data
    )


def analyze_resourceverification(path: Path) -> dict[str, Any]:
    resolved = resolve_resourceverification(path)
    data = resolved.read_bytes()
    contains_name_or_path = (
        COMMONACTIONS_NAME in data
        or COMMONACTIONS_PATH_SLASH in data
        or COMMONACTIONS_PATH_BACKSLASH in data
    )
    contains_resource_id = COMMONACTIONS_RESOURCE_ID in data
    return {
        "path": str(resolved),
        "size": len(data),
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "contains_commonactions_name_or_path": contains_name_or_path,
        "contains_commonactions_resource_id": contains_resource_id,
        "contains_commonactions": contains_name_or_path or contains_resource_id,
    }


def format_report(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"resourceverification: {report['path']}",
            f"size: {report['size']}",
            f"MD5: {report['md5']}",
            f"SHA1: {report['sha1']}",
            f"SHA256: {report['sha256']}",
            f"Co ten/path CommonActions: {report['contains_commonactions_name_or_path']}",
            f"Co resource id CommonActions: {report['contains_commonactions_resource_id']}",
            f"Ket luan co chua CommonActions: {report['contains_commonactions']}",
        ]
    )
