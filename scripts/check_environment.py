"""Lightweight environment sanity check.

Run this immediately after ``pip install -r requirements.txt`` to
confirm that every critical dependency is importable, that Earth
Engine can authenticate, and that the trained model is reachable.

Usage
-----
    python scripts/check_environment.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

REQUIRED = [
    "numpy",
    "pandas",
    "sklearn",
    "joblib",
    "ee",
    "geemap",
    "folium",
    "streamlit",
    "shap",
    "matplotlib",
]

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "Best_model.pkl"


def _check_imports() -> int:
    print("Checking imports ...")
    failures = 0
    for name in REQUIRED:
        try:
            mod = importlib.import_module(name)
            version = getattr(mod, "__version__", "n/a")
            print(f"  [OK] {name:<12} {version}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  [FAIL] {name:<12} {exc}")
    return failures


def _check_earth_engine() -> int:
    print("\nChecking Earth Engine ...")
    try:
        import ee
        try:
            ee.Initialize()
        except Exception:
            print("  [WARN] ee.Initialize() failed without a project. "
                  "Run `earthengine authenticate` and set GEE_PROJECT.")
            return 1
        print("  [OK] Earth Engine initialised.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] {exc}")
        return 1


def _check_model() -> int:
    print("\nChecking model artefact ...")
    if not MODEL_PATH.exists():
        print(f"  [WARN] {MODEL_PATH} not found. "
              "Run `python scripts/download_model.py`.")
        return 1
    try:
        import joblib
        joblib.load(MODEL_PATH)
        print(f"  [OK] {MODEL_PATH.name} loaded successfully.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] Could not load {MODEL_PATH}: {exc}")
        return 1


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    failures = _check_imports() + _check_earth_engine() + _check_model()
    print()
    if failures == 0:
        print("All checks passed. You are ready to run the pipeline.")
    else:
        print(f"{failures} check(s) need attention. See messages above.")
    return failures


if __name__ == "__main__":
    sys.exit(main())
