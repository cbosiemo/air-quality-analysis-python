# Processed Data

This folder contains analysis-ready datasets generated from the original AirQualityUCI dataset.

## Files

- `airquality_clean.csv` – Cleaned hourly air-quality and meteorological observations used in the main analysis.
- `airquality_daily.csv` – Daily aggregated pollutant and meteorological measurements.
- `airquality_monthly.csv` – Monthly aggregated pollutant and meteorological measurements.

## Processing

The original dataset was cleaned and prepared using Python and pandas. Key preprocessing steps included:

- Removing empty rows and columns.
- Replacing the dataset's `-200` sentinel values with missing values.
- Combining the original date and time fields into a datetime index.
- Assessing missingness across variables.
- Excluding NMHC due to more than 90% missing observations.
- Handling short gaps in the remaining time-series variables.
- Generating daily and monthly aggregates for temporal analysis.

The complete and reproducible data-cleaning workflow is available in the project Jupyter notebook.

## Source

The processed datasets are derived from the **Air Quality dataset** available through the UCI Machine Learning Repository.

These files are provided to support transparency and reproducibility of the analysis.
