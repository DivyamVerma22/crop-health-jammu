# Setup &amp; Reproducibility Guide

This document explains, in full, how to bring the project to a runnable state on a fresh machine. It complements the *Quickstart* section of the main `README.md`.

## 1. Environment

The project targets **Python 3.10 or newer**. A clean virtual environment is strongly recommended because the geospatial and deep-learning dependencies pull a large set of transitive packages.

```bash
python -m venv .venv
source .venv/bin/activate            # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

If you do not intend to retrain or re-benchmark the LSTM model from notebook 3, you may comment out the `tensorflow` line in `requirements.txt` to keep the install lean. Every other notebook, including the Streamlit app, will continue to work without TensorFlow because the production model is a scikit-learn Random Forest.

## 2. Google Earth Engine Authentication

The data extraction notebook and the Streamlit app both call the Earth Engine API and therefore require an authenticated, project-scoped session.

The first time you use Earth Engine on a machine, run:

```bash
earthengine authenticate
```

This opens a browser, prompts you to sign in with the Google account that holds the access, and stores a refresh token under `~/.config/earthengine/`. Subsequent runs read that token automatically.

You will also need a **Cloud project** with the Earth Engine API enabled. In the reference implementation this project is named `gee-jammu-dissertation`, and the identifier appears in two places:

- `notebooks/01_data_extraction.ipynb`, in the cell that calls `ee.Initialize(project=...)`.
- `app/app.py`, inside the `init_gee()` function.

Replace this string with your own project ID before running. A safer pattern, recommended for any public deployment, is to read it from an environment variable, for example:

```python
import os
ee.Initialize(project=os.environ["GEE_PROJECT"])
```

The `python-dotenv` package is already in `requirements.txt`, so you can place `GEE_PROJECT=...` in a local `.env` file (which is ignored by Git through `*.json` and the project rules in `.gitignore`).

## 3. Obtaining the Trained Model

The serialised Random Forest, `Best_model.pkl`, is roughly 229 MB and therefore not stored directly in Git. Two retrieval paths are supported.

**Option A — Git LFS (recommended when the model is hosted in this repository).** Install Git LFS, run `git lfs install`, and ensure `models/*.pkl` is tracked through the supplied `.gitattributes` file. A normal `git clone` will then transparently fetch the file from LFS.

**Option B — External host (recommended when the model is hosted on Hugging Face, Zenodo, or Google Drive).** Edit `scripts/download_model.py` and replace the placeholder URL with the public download link for your hosted artefact, then run:

```bash
python scripts/download_model.py
```

The script verifies the file size, places the result in `models/Best_model.pkl`, and exits with a clear error message if anything is missing.

## 4. Sample Data

Three small CSVs are committed under `data/sample/` for quick verification:

- `final.csv` — the monthly, point-indexed feature table with the CHS target.
- `wp1_features_pointid.csv` — the raw extracted features prior to target construction.
- `wp1_ndvi_ndmi_2017_2025.csv` — a long historical record of NDVI and NDMI used in exploratory analysis.

These are sufficient to run notebooks 2 through 5 end-to-end. To regenerate the full feature table from satellite sources, execute notebook 1 after configuring Earth Engine.

## 5. Running the Streamlit App

From the repository root, simply run:

```bash
streamlit run app/app.py
```

The app loads the Random Forest from `models/Best_model.pkl`, exposes a Folium map and a sidebar control panel, and triggers a fresh GEE extraction for each predicted point. Network access to Earth Engine endpoints is required at inference time.

## 6. Verifying the Installation

A minimal sanity check is provided as `scripts/check_environment.py`. Running this script prints the resolved Python, NumPy, scikit-learn, Earth Engine, and Streamlit versions, attempts a `ee.Initialize()` call, and confirms that `models/Best_model.pkl` is present and loadable. Use it as the first step when triaging installation issues.

## 7. Known Caveats

The Streamlit prototype currently fills the six-month input window with a single snapshot of features (`np.repeat(...)`), which is a deliberate simplification to make on-demand inference responsive. For dissertation-grade rigour, replace this with a true six-month rolling window — pull the previous six months of imagery, compute the seven features per month, and feed the resulting `(6, 7)` sequence into the model. The notebook pipeline already builds proper rolling sequences and can be reused.

Cloud-cover filtering in the app is fixed at &lt; 10 %. In dry months over Jammu this is usually sufficient, but during the monsoon you may receive empty composites; the app handles this gracefully by returning `None` and skipping the point. Loosening the threshold or widening the date range remediates this in practice.
