# Notebooks

This directory contains the six numbered notebooks that constitute the full research pipeline. Each notebook is self-contained and can be executed in order on a fresh kernel after the environment is set up (see `docs/SETUP.md`).

| # | Notebook | Stage |
|---|----------|-------|
| 1 | `01_data_extraction.ipynb` | Earth Engine authentication, AOI definition, sampling points, feature export. |
| 2 | `02_preprocessing_pca.ipynb` | Cleaning, lag engineering, CHS target construction, PCA. |
| 3 | `03_model_building.ipynb` | Sequence construction, model benchmarking, selection of the production Random Forest. |
| 4 | `04_validation_shap.ipynb` | Temporal hold-out evaluation and SHAP interpretability. |
| 5 | `05_multi_step_forecasting.ipynb` | Recursive N-step forecasting. |
| 6 | `06_coordinate_prediction.ipynb` | Single-coordinate prediction prototype that became `app/app.py`. |

Notebooks 2–5 can be run directly against the small sample CSVs in `data/sample/`. Notebook 1 additionally requires Earth Engine access.
