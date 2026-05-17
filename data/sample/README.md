# Sample Data

These three CSVs are committed to make the repository runnable out of the box. They are sufficient to execute notebooks 2 through 5 end-to-end and to drive the validation and forecasting analyses without re-running the Earth Engine extraction.

`final.csv` is the master modelling table. Each row represents one sampling point in one calendar month and contains the seven features (`NDVI`, `EVI`, `NDMI`, `NDWI`, `LST`, `Rainfall`, `Rainfall_lag1`) together with the raw and normalised Crop Health Score (`CHS_raw`, `CHS`). The point identifier (`point_id`) and the temporal index columns (`Year`, `Month`) uniquely key every row.

`wp1_features_pointid.csv` is an earlier version of the same table from before the CHS target was engineered. It is retained as a checkpoint so that the target-construction step in notebook 2 can be re-executed against the original features without rerunning the GEE pipeline.

`wp1_ndvi_ndmi_2017_2025.csv` is a long historical record of NDVI and NDMI between 2017 and 2025 used for exploratory time-series visualisation. It includes the latitude and longitude of each observation alongside the year-month index.

The full dataset across all 150 points and the complete temporal range can be regenerated from `notebooks/01_data_extraction.ipynb` once Earth Engine access is configured.
