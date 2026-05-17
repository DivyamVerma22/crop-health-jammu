"""Download the trained Crop Health Score model from external storage.

This script keeps the repository slim by hosting the ~228 MB
``Best_model.pkl`` artefact outside of Git.  Edit ``MODEL_URL`` below
to point at your chosen host (Zenodo, Hugging Face Hub, Google
Drive direct-download link, S3 pre-signed URL, etc.) before sharing
the repository publicly.

The SHA-256 checksum is the authoritative fingerprint of the
artefact produced by ``notebooks/03_model_building.ipynb``.  Do not
change it unless you have re-trained the model.

Usage
-----
    python scripts/download_model.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import requests
from tqdm import tqdm

# ---------------------------------------------------------------
# Configuration — edit MODEL_URL before publishing.
#
# Recommended hosts (any one is fine):
#
#   Zenodo:        https://zenodo.org/records/XXXXXXX/files/Best_model.pkl
#   Hugging Face:  https://huggingface.co/<user>/<repo>/resolve/main/Best_model.pkl
#   Google Drive:  use a "direct download" URL, not a sharing link
# ---------------------------------------------------------------
MODEL_URL: str = "https://example.com/replace-with-your-hosted-model.pkl"

# Pre-computed SHA-256 of the canonical Best_model.pkl produced by
# notebooks/03_model_building.ipynb.  Do not modify unless you re-train.
EXPECTED_SHA256: str | None = (
    "a17137b14aa51b8e9159967a538da76487886968914f97aaf03a951f4dabe713"
)
EXPECTED_SIZE_BYTES: int = 239_136_215  # ~228 MB

MODEL_PATH: Path = Path(__file__).resolve().parent.parent / "models" / "Best_model.pkl"
CHUNK_SIZE: int = 1024 * 1024  # 1 MiB


def _sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> None:
    """Download :data:`MODEL_URL` to :data:`MODEL_PATH`."""
    if MODEL_URL.startswith("https://example.com"):
        sys.exit(
            "[download_model] ERROR: MODEL_URL is still the placeholder.\n"
            "Edit scripts/download_model.py and set MODEL_URL to your\n"
            "hosted artefact (Zenodo / Hugging Face / Drive / S3)."
        )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    if MODEL_PATH.exists():
        print(f"[download_model] {MODEL_PATH} already exists. Skipping.")
        return

    print(f"[download_model] Fetching model from: {MODEL_URL}")
    with requests.get(MODEL_URL, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("Content-Length", 0)) or EXPECTED_SIZE_BYTES

        with MODEL_PATH.open("wb") as fh, tqdm(
            total=total, unit="B", unit_scale=True, desc="Best_model.pkl"
        ) as bar:
            for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    fh.write(chunk)
                    bar.update(len(chunk))

    if EXPECTED_SHA256:
        actual = _sha256(MODEL_PATH)
        if actual != EXPECTED_SHA256:
            MODEL_PATH.unlink(missing_ok=True)
            sys.exit(
                f"[download_model] ERROR: checksum mismatch.\n"
                f"  expected: {EXPECTED_SHA256}\n"
                f"  actual  : {actual}\n"
                f"The downloaded file has been removed."
            )
        print("[download_model] Checksum OK.")

    print(f"[download_model] Saved to {MODEL_PATH}")


if __name__ == "__main__":
    download()
