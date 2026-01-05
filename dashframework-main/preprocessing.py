import pandas as pd
import numpy as np
from pathlib import Path

# =========================================
# CONFIG (paths + output names)
# =========================================
RAW_DIR = Path("data_sets/raw")
OUT_DIR = Path("data_sets/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PATHS = {
    "economy": RAW_DIR / "economy_data.csv",
    "demographics": RAW_DIR / "demographics_data.csv",
    "energy": RAW_DIR / "energy_data.csv",
    "transportation": RAW_DIR / "transportation_data.csv",
    "geography": RAW_DIR / "geography_data.csv",
}
OUT_CLEAN = "data_sets/processed/countries_processed.csv"
OUT_REPORT = OUT_DIR / "data_quality_report.csv"

WINSOR_Q = (0.01, 0.99)  # 1st–99th percentile clipping



# Organizing functions for preprocessing steps

def coerce_numeric(s: pd.Series) -> pd.Series:
    """Convert messy numeric strings to float; keep NaN for non-parsable."""
    if s.dtype.kind in "biufc":
        return s.astype(float)

    cleaned = (
        s.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("nan", "", regex=False)
        .str.replace("None", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def censor_range(df: pd.DataFrame, col: str, lo=None, hi=None, ge0=False, gt0=False) -> pd.DataFrame:
    """Censor invalid values by setting them to NaN (do not drop rows)."""
    if col not in df.columns:
        return df

    x = df[col]
    mask = pd.Series(False, index=df.index)

    if lo is not None:
        mask |= x < lo
    if hi is not None:
        mask |= x > hi
    if ge0:
        mask |= x < 0
    if gt0:
        mask |= x <= 0

    df.loc[mask, col] = np.nan
    return df


def winsorize(df: pd.DataFrame, col: str, q=WINSOR_Q) -> pd.DataFrame:
    """Clip extreme values (winsorization) to reduce dominance."""
    if col not in df.columns:
        return df

    x = df[col].dropna()
    if x.empty:
        return df

    lo, hi = x.quantile(q[0]), x.quantile(q[1])
    df[col] = df[col].clip(lo, hi)
    return df


def minmax01(df: pd.DataFrame, col: str, out_col: str, invert: bool = False) -> pd.DataFrame:
    """Normalize to [0,1]. Optionally invert so higher=better."""
    if col not in df.columns:
        df[out_col] = np.nan
        return df

    x = df[col].astype(float)
    mn, mx = x.min(skipna=True), x.max(skipna=True)

    if pd.isna(mn) or pd.isna(mx) or mn == mx:
        df[out_col] = np.nan
        return df

    scaled = (x - mn) / (mx - mn)
    if invert:
        scaled = 1.0 - scaled

    df[out_col] = scaled
    return df


def safe_div(a: pd.Series, b: pd.Series) -> np.ndarray:
    """Safe division that returns NaN when divisor is 0/NaN."""
    a = a.astype(float)
    b = b.astype(float)
    return np.where((b == 0) | np.isnan(b), np.nan, a / b)


# load raw datasets
dfs = {}
for name, path in PATHS.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    dfs[name] = pd.read_csv(path)

for name, df in dfs.items():
    if "Country" not in df.columns:
        raise ValueError(f"'{name}' dataset is missing a 'Country' column.")

processed_countries = dfs["economy"].copy()
for k in ["demographics", "energy", "transportation", "geography"]:
    processed_countries = processed_countries.merge(dfs[k], on="Country", how="outer", suffixes=("", f"_{k}"))


# numeric columns

NUM_COLS = [
    # GLOBAL metrics
    "Unemployment_Rate_percent",
    "Youth_Unemployment_Rate_percent",
    "Real_GDP_PPP_billion_USD",
    "Population_Growth_Rate",
    "electricity_access_percent",
    "electricity_generating_capacity_kW",

    # DERIVED metric inputs
    "Total_Literacy_Rate",
    "Total_Population",
    "airports_paved_runways_count",
    "airports_unpaved_runways_count",
    "railways_km",
    "waterways_km",
    "Real_GDP_per_Capita_USD",

    # OPTIONAL / if available
    "Inflation_Rate_percent",
    "Public_Debt_percent_of_GDP",
]

for c in NUM_COLS:
    if c in processed_countries.columns:
        processed_countries[c] = coerce_numeric(processed_countries[c])


# Censoring invalid values (do not delete)

# Percentages must be within [0,100]
PCT_COLS = [
    "Unemployment_Rate_percent",
    "Youth_Unemployment_Rate_percent",
    "electricity_access_percent",
    "Total_Literacy_Rate",
    "Public_Debt_percent_of_GDP",
]
for c in PCT_COLS:
    processed_countries = censor_range(processed_countries, c, lo=0, hi=100)

# Population growth: allow negative, censor extreme
if "Population_Growth_Rate" in processed_countries.columns:
    processed_countries = censor_range(processed_countries, "Population_Growth_Rate", lo=-10, hi=10)

# Inflation: allow deflation, censor extreme (only if present)
if "Inflation_Rate_percent" in processed_countries.columns:
    processed_countries["Inflation_Rate_percent"] = coerce_numeric(processed_countries["Inflation_Rate_percent"])
    processed_countries = censor_range(processed_countries, "Inflation_Rate_percent", lo=-20, hi=200)

# Positive-only quantities
POS_ONLY = [
    "Real_GDP_PPP_billion_USD",
    "electricity_generating_capacity_kW",
    "Total_Population",
    "Real_GDP_per_Capita_USD",
]
for c in POS_ONLY:
    processed_countries = censor_range(processed_countries, c, gt0=True)

# Non-negative transport lengths/counts
NONNEG = ["airports_paved_runways_count", "airports_unpaved_runways_count", "railways_km", "waterways_km"]
for c in NONNEG:
    processed_countries = censor_range(processed_countries, c, ge0=True)



# 2) OUTLIERS: winsorize heavy-tailed metrics

HEAVY_TAIL = [
    "Real_GDP_PPP_billion_USD",
    "electricity_generating_capacity_kW",
    "railways_km",
    "waterways_km",
    "Real_GDP_per_Capita_USD",
]
for c in HEAVY_TAIL:
    processed_countries = winsorize(processed_countries, c)


# derived metrics
#  Available Skilled Workforce
if {"Total_Literacy_Rate", "Unemployment_Rate_percent"}.issubset(processed_countries.columns):
    processed_countries["Available_Skilled_Workforce"] = (
        processed_countries["Total_Literacy_Rate"]
        * (100.0 - processed_countries["Unemployment_Rate_percent"]) / 100.0
    )

#  Industrial Energy Capacity
if {"electricity_generating_capacity_kW", "Total_Population", "electricity_access_percent"}.issubset(processed_countries.columns):
    cap_per_capita = safe_div(processed_countries["electricity_generating_capacity_kW"], processed_countries["Total_Population"])
    processed_countries["Industrial_Energy_Capacity"] = cap_per_capita * (processed_countries["electricity_access_percent"] / 100.0)

# Supply Chain Connectivity Score
if {"airports_paved_runways_count", "airports_unpaved_runways_count"}.issubset(processed_countries.columns):
    processed_countries["airports_total"] = (
        processed_countries["airports_paved_runways_count"].fillna(0)
        + processed_countries["airports_unpaved_runways_count"].fillna(0)
    )

# Normalize components first
processed_countries = minmax01(processed_countries, "airports_total", "airports_total__norm", invert=False)
processed_countries = minmax01(processed_countries, "railways_km", "railways_km__norm", invert=False)
processed_countries = minmax01(processed_countries, "waterways_km", "waterways_km__norm", invert=False)

if {"airports_total__norm", "railways_km__norm", "waterways_km__norm"}.issubset(processed_countries.columns):
    processed_countries["Supply_Chain_Connectivity_Score"] = (
        0.4 * processed_countries["airports_total__norm"]
        + 0.3 * processed_countries["railways_km__norm"]
        + 0.3 * processed_countries["waterways_km__norm"]
    )

#  Wage Sustainability Index (only if inflation exists)
if {"Real_GDP_per_Capita_USD", "Inflation_Rate_percent"}.issubset(processed_countries.columns):
    processed_countries["Wage_Sustainability_Index"] = (
        processed_countries["Real_GDP_per_Capita_USD"] / (1.0 + processed_countries["Inflation_Rate_percent"] / 100.0)
    )

# Economic Resilience Score (simple proxy if debt + inflation exist)
if {"Public_Debt_percent_of_GDP", "Inflation_Rate_percent"}.issubset(processed_countries.columns):
    processed_countries = minmax01(processed_countries, "Public_Debt_percent_of_GDP", "Debt__norm_inv", invert=True)

    target = 2.5  # “ideal” inflation zone ~2–3%
    processed_countries["Inflation_Distance"] = (processed_countries["Inflation_Rate_percent"] - target).abs()
    processed_countries = minmax01(processed_countries, "Inflation_Distance", "Inflation_Control__norm_inv", invert=True)

    processed_countries["Economic_Resilience_Score"] = (
        0.5 * processed_countries["Debt__norm_inv"]
        + 0.5 * processed_countries["Inflation_Control__norm_inv"]
    )


# normalize global metrics to [0,1]
processed_countries = minmax01(processed_countries, "Unemployment_Rate_percent", "Unemployment__norm_inv", invert=True)
processed_countries = minmax01(processed_countries, "Real_GDP_PPP_billion_USD", "GDP__norm", invert=False)
processed_countries = minmax01(processed_countries, "Youth_Unemployment_Rate_percent", "Youth_Unemp__norm_inv", invert=True)
processed_countries = minmax01(processed_countries, "Population_Growth_Rate", "Pop_Growth__norm", invert=False)
processed_countries = minmax01(processed_countries, "electricity_access_percent", "Elec_Access__norm", invert=False)
processed_countries = minmax01(processed_countries, "electricity_generating_capacity_kW", "Elec_Capacity__norm", invert=False)

# Normalize derived metrics too (useful for composites / UI)
DERIVED_TO_NORM = [
    "Available_Skilled_Workforce",
    "Industrial_Energy_Capacity",
    "Supply_Chain_Connectivity_Score",
    "Wage_Sustainability_Index",
    "Economic_Resilience_Score",
]
for c in DERIVED_TO_NORM:
    if c in processed_countries.columns:
        processed_countries = minmax01(processed_countries, c, f"{c}__norm", invert=False)


# quality report
report_rows = []
for col in [c for c in NUM_COLS if c in processed_countries.columns]:
    total = len(processed_countries)
    missing = processed_countries[col].isna().sum()
    report_rows.append({
        "metric": col,
        "total_rows": int(total),
        "missing_rows": int(missing),
        "missing_percent": float(missing) / float(total) * 100.0
    })

quality_report = pd.DataFrame(report_rows).sort_values("missing_percent", ascending=False)

# output saving
processed_countries.to_csv(OUT_CLEAN, index=False)
quality_report.to_csv(OUT_REPORT, index=False)

print(f"Saved: {OUT_CLEAN}")    
print(f"Saved: {OUT_REPORT}")   