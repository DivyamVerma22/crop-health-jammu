# Methodology

This document records the scientific methodology behind the repository so that the work is fully reproducible and so that examiners or downstream researchers can audit each step without having to read every notebook in detail.

## 1. Study Area and Sampling Design

The study targets the cultivated landscape of the Jammu region in the Union Territory of Jammu &amp; Kashmir, India. The administrative boundary of the region is loaded inside `notebooks/01_data_extraction.ipynb`, and one hundred and fifty fixed spatial sampling points are generated within it using a reproducible random seed. The points are persisted as an Earth Engine `FeatureCollection` so that every downstream extraction operates on exactly the same coordinates, which preserves comparability across the multi-year time series.

## 2. Earth Observation Inputs

Three open archives provide the raw observations. Sentinel-2 surface reflectance from the `COPERNICUS/S2_SR` collection contributes the optical bands required to derive vegetation and moisture indices. MODIS `MOD11A2` provides eight-day composite daytime land-surface temperature, converted from kelvin to Celsius after applying the standard scale factor of 0.02. CHIRPS daily precipitation contributes monthly rainfall totals and a one-month lag covering the preceding October–December window so that residual soil moisture from the previous wet season can be represented as an explicit predictor.

A cloud-cover threshold of 10 % is applied to Sentinel-2 prior to median compositing. The pipeline therefore favours cleaner pixels at the cost of occasionally missing dates in the monsoon months; this trade-off is discussed in `docs/SETUP.md` under *Known Caveats*.

## 3. Feature Engineering

Seven features are derived per sampling point per month. The Normalised Difference Vegetation Index, NDVI, is computed from near-infrared and red reflectance. The Enhanced Vegetation Index, EVI, applies the standard MODIS formulation with soil and atmosphere adjustment terms. The Normalised Difference Moisture Index, NDMI, uses near-infrared and short-wave infrared to quantify canopy moisture, while the Normalised Difference Water Index, NDWI, uses green and near-infrared to highlight open water and waterlogged areas. Land-surface temperature, LST, comes from MODIS as described above. Rainfall is the monthly CHIRPS sum, and Rainfall_lag1 is the antecedent-season sum.

The composite Crop Health Score, CHS, is constructed in `notebooks/02_preprocessing_pca.ipynb`. A raw signal is built from the vegetation and moisture indices and then min-max normalised into a 0–1 range so that downstream models receive a bounded, dimensionless target. The intermediate quantity is preserved in the dataset as `CHS_raw` for transparency.

## 4. Dataset Construction

The long-format feature table is sorted by point identifier, year, and month — in that order — before any sequence construction, to guarantee that temporal ordering within each point is preserved through every subsequent transformation. A six-month sliding window is then built per point: each training example consists of the seven features stacked over six consecutive months, with the CHS of the seventh month as the target. Classical learners receive these examples as flat 42-dimensional vectors, while the LSTM ingests them in their native `(6, 7)` tensor form.

A strict temporal hold-out is enforced. All observations up to and including the 2023 calendar year are assigned to the training set, and observations from 2024 onwards form the test set. This design avoids any optimistic bias that would arise from random shuffling of an autocorrelated time series.

## 5. Model Benchmarking

Four candidate regressors are benchmarked in `notebooks/03_model_building.ipynb`: a baseline Linear Regression, a Random Forest with four hundred trees, an XGBoost regressor with shallow tuning, and a single-layer LSTM with sixty-four hidden units, dropout, and a dense regression head. All four are trained on the same windowed dataset, evaluated on the same temporal hold-out, and compared on the coefficient of determination, the root-mean-squared error, and the mean absolute error. The Random Forest emerged as the best generalising model and is serialised as `Best_model.pkl` for downstream use.

## 6. Validation and Interpretability

Notebook 4 re-loads the saved Random Forest, reproduces the test predictions, and explains them with SHAP. Per-feature mean absolute SHAP values quantify global feature importance, beeswarm summaries reveal the direction and density of each feature's contribution, and dependence plots expose any non-linear interactions. The SHAP analysis is the basis for the discussion of agronomic plausibility in the dissertation.

## 7. Multi-Step Forecasting

Notebook 5 extends the trained model to recursive *N*-step forecasting. For each test window the model predicts the next CHS value, that prediction is appended to the input sequence in place of the oldest month, and the procedure is repeated *N* times. The notebook reports RMSE and MAE as a function of forecast horizon, which is the standard way to characterise error accumulation in autoregressive forecasting.

## 8. Operational Deployment

Notebook 6 prototypes single-coordinate inference, and `app/app.py` productionises that prototype as a Streamlit application. The app accepts any latitude–longitude pair within the study area, buffers it to a 500 m disc to stabilise the reduction step, pulls the same seven features for the requested month from Earth Engine, scores them with the saved Random Forest, and classifies the result into a *Low / Moderate / High* category using the thresholds 0.30 and 0.60. The classification thresholds are deliberately kept simple and transparent so that they can be tuned by domain experts.

## 9. Limitations and Future Work

The model treats each point in isolation, ignoring spatial autocorrelation between neighbouring sampling locations. Convolutional or graph-based extensions are natural next steps. The CHS target is a composite, not a directly observed agronomic quantity, and would benefit from validation against field-measured yields or biomass where ground truth is available. Finally, as noted in the setup document, the Streamlit prototype currently approximates the six-month input window with a single snapshot for responsiveness; a production deployment should replace this with a true rolling window.
