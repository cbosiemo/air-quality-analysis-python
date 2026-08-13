# Historical Air Quality Analysis in Python

A reproducible exploratory and predictive analysis of the **UCI Air Quality** dataset, using hourly pollution and meteorological measurements from an Italian city. The project examines temporal patterns, pollutant relationships, data-quality challenges, and the predictive signal available for benzene concentrations.

## Why this project

Air-quality monitoring data are messy, time-dependent, and closely linked to public-health and environmental decisions. This project was developed as an academic mini-project and expanded into a portfolio analysis to demonstrate practical skills in:

- cleaning and structuring environmental sensor data;
- working with hourly time-series observations;
- analysing daily, monthly, diurnal, and weekday/weekend patterns;
- exploring pollutant-weather relationships;
- producing reproducible visualisations and statistical summaries; and
- comparing simple predictive models using a chronological train/test split.

## Dataset

The analysis uses the **Air Quality** dataset from the UCI Machine Learning Repository. It contains roughly 9,300 hourly records from a multisensor device deployed at road level in a polluted Italian urban area, alongside reference measurements for pollutants including carbon monoxide (CO), benzene (C₆H₆), nitrogen oxides (NOx), and nitrogen dioxide (NO₂), plus meteorological variables.

- UCI dataset: https://archive.ics.uci.edu/dataset/360/air+quality
- DOI: https://doi.org/10.24432/C59K5F
- Citation: De Vito, S. et al., *Air Quality*, UCI Machine Learning Repository.

Missing readings in the source file are encoded as `-200`.

## Research questions

1. How do major pollutant concentrations vary over time?
2. What daily, seasonal, and weekday/weekend patterns are visible?
3. How strongly are pollutants related to one another and to temperature and humidity?
4. Can benzene concentrations be estimated from co-located pollutant, weather, and time-of-day variables?

## Data cleaning

The workflow:

1. converts source `-200` sentinel values to missing values;
2. combines date and time into a proper datetime index;
3. removes empty trailing columns and blank rows;
4. drops NMHC from the analytical dataset because more than 90% of its observations are missing; and
5. uses time-based interpolation only for short gaps of up to six hours, while leaving longer gaps missing.

The treatment of NMHC is a deliberate data-quality decision rather than an attempt to impute a largely unavailable variable.

## Analysis

The project includes:

- descriptive statistics;
- daily and monthly aggregation;
- seven-day rolling trends;
- mean diurnal pollution profiles;
- weekday versus weekend comparisons;
- Pearson correlation analysis;
- pollutant-weather scatter analysis; and
- linear regression and Random Forest models for contemporaneous benzene prediction.

The predictive component is **not a future forecasting model**. It estimates benzene using co-located pollutant, meteorological, and temporal features. A chronological 80/20 split is used so that later observations are held out for evaluation.

## Selected findings

- CO, benzene, NOx, and NO₂ show strong positive correlations, a pattern consistent with shared combustion-related sources such as road traffic.
- Average pollutant profiles show pronounced morning and evening peaks, consistent with commuting-hour activity.
- NOx levels are lower at weekends than on weekdays, again consistent with changing traffic activity. This is an observational association and is not treated as a causal policy estimate.
- NOx and NO₂ increase during colder months in this dataset, while CO and benzene show a late-summer dip.
- Linear Regression and Random Forest models both capture substantial predictive signal for benzene on the held-out period; the Random Forest achieves lower mean absolute error in the project results.

## Limitations

This is an exploratory analysis of a single monitoring site covering about 13 months. Results should not be generalized to other cities without validation. The analysis does not establish causal effects of traffic or environmental policy, and weather, seasonality, and human activity may be confounded. NMHC is excluded because the source variable is more than 90% missing.

## Repository structure

```text
air-quality-analysis-python/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                    # download AirQualityUCI.csv here
│   └── processed/              # cleaned, daily, and monthly datasets
├── notebooks/
│   └── AirQuality_Analysis.ipynb
├── src/
│   └── analysis.py
├── outputs/
│   ├── figures/
│   ├── correlation.csv
│   ├── model_results.csv
│   └── summary_stats.csv
└── reports/
    ├── Air_Quality_Report.docx
    └── Air_Quality_Presentation.pptx
```

## How to reproduce the analysis

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/air-quality-analysis-python.git
cd air-quality-analysis-python
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the raw dataset

Download `AirQualityUCI.csv` from UCI and save it as:

```text
data/raw/AirQualityUCI.csv
```

### 5. Run the analysis

```bash
python src/analysis.py
```

Or open the Jupyter notebook:

```bash
jupyter notebook notebooks/AirQuality_Analysis.ipynb
```

## Tools

Python · pandas · NumPy · Matplotlib · Seaborn · scikit-learn · Jupyter Notebook

## Author

**Cynthia Osiemo**  
Economics, Statistics & Data Science  
GitHub: https://github.com/cbosiemo

## Acknowledgement

This project uses the UCI Machine Learning Repository Air Quality dataset. Dataset creators and UCI retain attribution for the underlying data. The analysis, code, interpretation, and portfolio presentation in this repository are the author's work.
