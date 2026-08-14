"""Historical Air Quality Analysis using the UCI Air Quality dataset.

Run from the repository root:
    python src/analysis.py

The raw dataset must be saved as:
    data/raw/AirQualityUCI.csv
"""
from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "AirQualityUCI.csv"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"

for folder in (PROCESSED, OUTPUTS, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

if not SRC.exists():
    raise FileNotFoundError(
        "Missing data/raw/AirQualityUCI.csv. Download the Air Quality dataset "
        "from the UCI Machine Learning Repository and place AirQualityUCI.csv "
        "in data/raw/ before running this script."
    )

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.dpi"] = 140
plt.rcParams["savefig.bbox"] = "tight"

# 1. Load
df = pd.read_csv(SRC, sep=";", decimal=",", na_values=["-200", "-200,0"])
df = df.loc[:, ~df.columns.str.match(r"^Unnamed")]
df = df.dropna(how="all").reset_index(drop=True)
df = df.replace(-200, np.nan)

# 2. Clean and structure time series
df["Datetime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"].str.replace(".", ":", regex=False),
    format="%d/%m/%Y %H:%M:%S",
)
df = df.drop(columns=["Date", "Time"]).set_index("Datetime").sort_index()

rename = {
    "CO(GT)": "CO_mgm3", "PT08.S1(CO)": "S1_CO",
    "NMHC(GT)": "NMHC_ugm3", "C6H6(GT)": "C6H6_ugm3",
    "PT08.S2(NMHC)": "S2_NMHC", "NOx(GT)": "NOx_ppb",
    "PT08.S3(NOx)": "S3_NOx", "NO2(GT)": "NO2_ugm3",
    "PT08.S4(NO2)": "S4_NO2", "PT08.S5(O3)": "S5_O3",
    "T": "Temp_C", "RH": "RH_pct", "AH": "AbsHum",
}
df = df.rename(columns=rename)

missing_before = df.isna().mean().mul(100).round(1).sort_values(ascending=False)
missing_before.to_csv(OUTPUTS / "missingness_before_cleaning.csv", header=["missing_pct"])

# NMHC is >90% missing in this dataset, so it is excluded from analysis.
df = df.drop(columns=["NMHC_ugm3"])

# Apply time-based interpolation with a six-observation limit in each direction.
df_clean = df.interpolate(method="time", limit=6, limit_direction="both")

pollutants = ["CO_mgm3", "C6H6_ugm3", "NOx_ppb", "NO2_ugm3"]
weather = ["Temp_C", "RH_pct", "AbsHum"]
analysis_cols = pollutants + weather

# 3. Aggregate and save tables
daily = df_clean[analysis_cols].resample("D").mean()
monthly = df_clean[analysis_cols].resample("MS").mean()
summary = df_clean[analysis_cols].describe().round(2)
corr = df_clean[analysis_cols].corr().round(2)

df_clean.to_csv(PROCESSED / "airquality_clean.csv")
daily.to_csv(PROCESSED / "airquality_daily.csv")
monthly.to_csv(PROCESSED / "airquality_monthly.csv")
summary.to_csv(OUTPUTS / "summary_stats.csv")
corr.to_csv(OUTPUTS / "correlation.csv")

pretty = {
    "CO_mgm3": "CO (mg/m³)", "C6H6_ugm3": "Benzene C₆H₆ (µg/m³)",
    "NOx_ppb": "NOx (ppb)", "NO2_ugm3": "NO₂ (µg/m³)",
    "Temp_C": "Temperature (°C)", "RH_pct": "Relative Humidity (%)",
    "AbsHum": "Absolute Humidity",
}

# 4. Figures
fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
for ax, col, color in zip(axes, pollutants, sns.color_palette("rocket", 4)):
    ax.plot(daily.index, daily[col], color=color, alpha=0.35, lw=0.8, label="Daily mean")
    ax.plot(daily.index, daily[col].rolling(7, min_periods=3).mean(), color=color, lw=2, label="7-day rolling")
    ax.set_ylabel(pretty[col]); ax.legend(fontsize=8)
axes[0].set_title("Daily pollutant trends, March 2004 – April 2005", fontweight="bold")
axes[-1].set_xlabel("Date")
plt.tight_layout(); plt.savefig(FIGURES / "daily_pollutant_trends.png"); plt.close()

monthly_norm = monthly[pollutants] / monthly[pollutants].max()
fig, ax = plt.subplots(figsize=(11, 5))
monthly_norm.index = [d.strftime("%b %Y") for d in monthly_norm.index]
monthly_norm.plot(kind="bar", ax=ax, width=0.8, color=sns.color_palette("rocket", 4))
ax.set_xticklabels(monthly_norm.index, rotation=45, ha="right")
ax.set_ylabel("Normalised monthly mean (0–1)")
ax.set_title("Monthly pollutant levels (normalised within pollutant)", fontweight="bold")
ax.legend([pretty[c] for c in pollutants], fontsize=8)
plt.tight_layout(); plt.savefig(FIGURES / "monthly_pollutant_levels.png"); plt.close()

fig, ax = plt.subplots(figsize=(8, 6.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1, square=True, ax=ax)
ax.set_title("Pearson correlation: pollutants & weather", fontweight="bold")
plt.tight_layout(); plt.savefig(FIGURES / "correlation_matrix.png"); plt.close()

hourly_profile = df_clean.groupby(df_clean.index.hour)[pollutants].mean()
fig, ax = plt.subplots(figsize=(10, 5))
for col, color in zip(pollutants, sns.color_palette("rocket", 4)):
    series = hourly_profile[col] / hourly_profile[col].max()
    ax.plot(series.index, series.values, marker="o", lw=2, color=color, label=pretty[col])
ax.set(xticks=range(0, 24, 2), xlabel="Hour of day", ylabel="Normalised concentration")
ax.set_title("Diurnal cycle — hourly pollutant patterns", fontweight="bold")
ax.legend(fontsize=9)
plt.tight_layout(); plt.savefig(FIGURES / "diurnal_cycle.png"); plt.close()

sample = df_clean.sample(min(2000, len(df_clean)), random_state=0)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
sns.scatterplot(data=sample, x="Temp_C", y="CO_mgm3", ax=axes[0], alpha=0.4, s=15)
sns.regplot(data=sample, x="Temp_C", y="CO_mgm3", ax=axes[0], scatter=False, line_kws={"lw": 1.5})
axes[0].set(xlabel="Temperature (°C)", ylabel="CO (mg/m³)", title="CO vs Temperature")
sns.scatterplot(data=sample, x="RH_pct", y="NO2_ugm3", ax=axes[1], alpha=0.4, s=15)
sns.regplot(data=sample, x="RH_pct", y="NO2_ugm3", ax=axes[1], scatter=False, line_kws={"lw": 1.5})
axes[1].set(xlabel="Relative Humidity (%)", ylabel="NO₂ (µg/m³)", title="NO₂ vs Relative Humidity")
plt.tight_layout(); plt.savefig(FIGURES / "pollutant_weather_scatter.png"); plt.close()

tmp = df_clean.copy(); tmp["DayType"] = np.where(tmp.index.dayofweek < 5, "Weekday", "Weekend")
fig, axes = plt.subplots(1, 4, figsize=(14, 4))
for ax, col in zip(axes, pollutants):
    sns.boxplot(data=tmp, x="DayType", y=col, ax=ax, showfliers=False)
    ax.set_title(pretty[col], fontsize=10); ax.set_xlabel("")
plt.suptitle("Weekday vs weekend pollutant distributions", fontweight="bold", y=1.02)
plt.tight_layout(); plt.savefig(FIGURES / "weekday_weekend.png"); plt.close()

# 5. Predictive modelling: contemporaneous benzene estimation, not future forecasting.
model_df = df_clean.dropna(subset=analysis_cols).copy()
model_df["hour"] = model_df.index.hour
model_df["dayofweek"] = model_df.index.dayofweek
model_df["month"] = model_df.index.month
features = ["CO_mgm3", "NOx_ppb", "NO2_ugm3", "Temp_C", "RH_pct", "AbsHum", "hour", "dayofweek", "month"]
target = "C6H6_ugm3"
X, y = model_df[features], model_df[target]
split = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

models = [
    ("Linear Regression", LinearRegression()),
    ("Random Forest", RandomForestRegressor(n_estimators=120, random_state=0, n_jobs=-1)),
]
results = []
for name, model in models:
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    results.append({"Model": name, "MAE": round(mean_absolute_error(y_test, pred), 3), "R2": round(r2_score(y_test, pred), 3)})

results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUTS / "model_results.csv", index=False)

rf = RandomForestRegressor(n_estimators=120, random_state=0, n_jobs=-1).fit(X_train, y_train)
pred = rf.predict(X_test)
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(model_df.index[split:], y_test.values, lw=1, alpha=0.8, label="Actual")
ax.plot(model_df.index[split:], pred, lw=1, alpha=0.8, label="Predicted")
ax.set_title(f"Benzene — actual vs predicted (Random Forest, R²={r2_score(y_test, pred):.3f})", fontweight="bold")
ax.set_ylabel("C₆H₆ (µg/m³)"); ax.legend()
plt.tight_layout(); plt.savefig(FIGURES / "benzene_actual_vs_predicted.png"); plt.close()

importance = pd.Series(rf.feature_importances_, index=features).sort_values()
fig, ax = plt.subplots(figsize=(8, 4.5))
importance.plot(kind="barh", ax=ax)
ax.set_title("Random Forest feature importance for benzene prediction", fontweight="bold")
ax.set_xlabel("Relative importance")
plt.tight_layout(); plt.savefig(FIGURES / "random_forest_feature_importance.png"); plt.close()

print("Analysis complete.")
print(f"Processed data: {PROCESSED}")
print(f"Tables and model outputs: {OUTPUTS}")
print(f"Figures: {FIGURES}")
