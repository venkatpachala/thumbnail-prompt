from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime


_STORAGE_ROOT = Path(__file__).resolve().parent.parent / "storage"


def storage_root() -> Path:
    """Return storage root path."""
    return _STORAGE_ROOT


def ensure_dirs() -> None:
    """Create required storage sub-directories."""
    for sub in ["uploads", "backgrounds", "cutouts", "thumbnails"]:
        (storage_root() / sub).mkdir(parents=True, exist_ok=True)


def safe_filename(base: str, ext: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    base = "".join(c for c in base if c.isalnum() or c in ("_", "-"))
    return f"{base}_{timestamp}.{ext}"


def file_path(subdir: str, filename: str) -> Path:
    return storage_root() / subdir / filename


def public_url(subdir: str, filename: str) -> str:
    return f"/files/{subdir}/{filename}"
