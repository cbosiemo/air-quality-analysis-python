# Analysis Figures

This folder contains visual outputs generated from the historical air-quality analysis using the UCI Air Quality dataset.

The figures support the exploratory, temporal, correlation, and predictive modelling components of the project.

## Figures

### `daily_pollutant_trends.png`
Daily concentrations of CO, benzene, NOx, and NO₂ with seven-day rolling means, used to examine temporal and seasonal variation across the study period.

### `diurnal_cycle.png`
Average normalised pollutant concentrations by hour of day, highlighting systematic variation in pollution levels across the daily cycle.

### `correlation_matrix.png`
Pearson correlation matrix showing relationships among the major pollutants and meteorological variables used in the analysis.

### `weekday_weekend.png`
Comparison of pollutant distributions between weekdays and weekends, used to explore differences associated with weekly activity patterns.

### `benzene_actual_vs_predicted.png`
Actual versus predicted benzene concentrations for the chronologically held-out test period using the Random Forest model.

### `random_forest_feature_importance.png`
Relative feature importance from the Random Forest model, showing which pollutant, meteorological, and temporal variables contributed most strongly to model predictions.

## Reproducibility

These figures are generated from the analysis contained in:

- `../../notebooks/AirQuality_Analysis.ipynb`
- `../../src/analysis.py`

The underlying raw dataset is stored in `../../data/raw/`, while processed datasets and statistical outputs are maintained elsewhere in the repository.

For the full methodology, findings, limitations, and interpretation, see the main project `README.md`.
