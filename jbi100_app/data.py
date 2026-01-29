"""
Data loading and preprocessing module.
Handles CSV imports, data cleaning, and metric calculations for the visualization.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from functools import reduce

# Standardized country column name used across all metrics
COUNTRY_COL = 'Country'

# Cached dataframe to avoid reloading from disk on every callback
DATA_DF = None

# Load and cache the global dataset, filtering out small countries.
# min_pop: Minimum population threshold (default 5 million)
def ensure_data_loaded(min_pop = 5000000):
    global DATA_DF
    if DATA_DF is None:
        DATA_DF = get_data()
        # Filter out countries with small populations to focus on major economies
        DATA_DF = DATA_DF[DATA_DF['Total_Population'] >= min_pop].reset_index(drop=True)
    return DATA_DF

# Load and merge all CSV files from the data_sets directory.
# Performs data cleaning and type conversion.
def get_data():
    # Locate CSV files in the package data directory
    data_dir = Path(__file__).parent / "data_sets"
    all_files = [str(p) for p in data_dir.glob("*.csv")]
    
    # Read each CSV into its own DataFrame
    dfs = [pd.read_csv(f) for f in all_files]
    
    # Merge all DataFrames on 'Country' column using outer join
    # This preserves all countries even if they don't appear in all datasets
    df = reduce(lambda left, right: pd.merge(left, right, on='Country', how='outer'), dfs)
    
    # Remove columns not needed for the analysis
    df = df.drop(columns=['coal_metric_tons', 'petroleum_bbl_per_day', 'refined_petroleum_products_bbl_per_day', 
                          'refined_petroleum_exports_bbl_per_day', 'refined_petroleum_imports_bbl_per_day', 
                          'natural_gas_cubic_meters', 'Geographic_Coordinates', 'Highest_Elevation', 'Lowest_Elevation', 
                          'airports_unpaved_runways_count', 'heliports_count', 'Water_Area', 'gas_pipelines_km',
                          'oil_pipelines_km', 'refined_products_pipelines', 'water_pipelines_km', 'Forest_Land',
                          'Male_Literacy_Rate', 'Female_Literacy_Rate', 'Sex_Ratio', 'Death_Rate',
                          'Land_Boundaries', 'Coastline', 'Ohter_Land', 'Agricultural_Land', 'Arable_Land (%% of Total Agricultural Land)',
                          'Permanent_Crops (%% of Total Agricultural Land)', 'Permanent_Pasture (%% of Total Agricultural Land)', 
                          'refined_products_pipelines_km', 'Irrigated_Land', 'Other_Land', 'Infant_Mortality_Rate', 
                          'Total_Fertility_Rate', 'Net_Migration_Rate', 'Exchange_Rate_per_USD', 
                          'carbon_dioxide_emissions_Mt'], errors='ignore')
    
    # Columns that should remain as strings (not converted to numeric)
    text_columns = ['Country', 'Fiscal_Year']
    
    # Clean and convert numeric columns
    for col in df.columns:
        if col in text_columns:
            continue  # Skip text columns
            
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '', regex=True)
            
            # million sq km is handled differently, otherwise we couldnt multiply
            million_mask = df[col].str.contains('million sq km', na=False)
            df.loc[million_mask, col] = df.loc[million_mask, col].str.replace(' million sq km', '', regex=True)
            df.loc[million_mask, col] = pd.to_numeric(df.loc[million_mask, col], errors='coerce') * 1_000_000
            
            # clean regular sq km
            sq_km_mask = df[col].str.contains(' sq km', na=False) & ~million_mask
            df.loc[sq_km_mask, col] = df.loc[sq_km_mask, col].str.replace(' sq km', '', regex=True)
            
            # clean the rest
            df[col] = df[col].astype(str).str.replace('km', '', regex=True)
            df[col] = df[col].str.replace('%', '', regex=True)
            df[col] = df[col].str.strip()
            
            # convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# Robust normalization for global datasets:
# 1. Log-transforms the data to reduce skew
# 2. Clips outliers at a specific percentile (default 90th)
# 3. Min-Max scales the result to [0, 1]
def normalize_series(series, clip_percentile=0.90):
    if series.empty or series.max() == series.min():
        return series * 0
    
    # Work on a copy to avoid warnings
    s = series.copy()

    # Log Transformation (for 'Density' and 'Population' metrics)
    if s.min() < 0:
        s = s - s.min()
    s = np.log1p(s)

    # Percentile Clipping
    # This caps the 'Max' at the 90th percentile so the top 10% of outliers don't skew the scale
    upper_bound = s.quantile(clip_percentile)
    s = s.clip(upper=upper_bound)

    # Standard Min-Max of the clipped/log data
    denom = s.max() - s.min()
    if denom == 0:
        return s * 0
        
    return (s - s.min()) / denom

# Calculate workforce availability score based on literacy, unemployment, and population
def available_skilled_workforce():
    df = ensure_data_loaded()
    required = [COUNTRY_COL, 'Total_Literacy_Rate', 'Unemployment_Rate_percent', 'Total_Population']
    sub = df[required].copy().set_index(COUNTRY_COL)
    sub = sub.dropna()
    
    # Calculate the 'Quality' of the workforce
    quality_score = (sub['Total_Literacy_Rate'] / 100) * (sub['Unemployment_Rate_percent'] / 100)
    
    # Apply Scale Factor.
    scale_factor = np.log10(sub['Total_Population'])

    metric = quality_score * scale_factor
    return normalize_series(metric)

# Calculate industrial energy capacity based on per-capita generation and grid scale
def industrial_energy_capacity():
    df = ensure_data_loaded()
    required = [COUNTRY_COL, 'electricity_generating_capacity_kW', 'Total_Population', 'electricity_access_percent']
    sub = df[required].copy().set_index(COUNTRY_COL)
    sub = sub.dropna()
    
    # Base Capacity: How much power per person with access?
    pop_with_access = sub['Total_Population'] * (sub['electricity_access_percent'] / 100)
    per_capita_capacity = sub['electricity_generating_capacity_kW'] / pop_with_access.replace(0, np.nan)
    
    # Scale Factor: Log of Total generating capacity. 
    grid_scale = np.log10(sub['electricity_generating_capacity_kW'].clip(lower=1))
    
    metric = per_capita_capacity * grid_scale
    
    return normalize_series(metric.dropna())

# Measure infrastructure density (airports, railways, waterways relative to land area)
def supply_chain_connectivity_score():
    df = ensure_data_loaded()
    required = [COUNTRY_COL, 'airports_paved_runways_count', 'railways_km', 'waterways_km', 'Land_Area']
    sub = df[required].copy().set_index(COUNTRY_COL)
    sub = sub.dropna()
    
    # Calculate Density
    area_factor = sub['Land_Area'] + 1
    
    air_density = sub['airports_paved_runways_count'] / area_factor
    rail_density = sub['railways_km'] / area_factor
    water_density = sub['waterways_km'] / area_factor
    
    # Normalize the densities
    airports_norm = normalize_series(air_density)
    railways_norm = normalize_series(rail_density)
    waterways_norm = normalize_series(water_density)
    
    # Apply weights 
    metric = (0.35 * airports_norm) + (0.3 * railways_norm) + (0.35 * waterways_norm)
    
    return normalize_series(metric)


# Calculate wage sustainability using GDP per capita adjusted for fiscal risk
# Index = Real_GDP_per_Capita_USD * (1 + |Budget_Deficit|/100 + Public_Debt/200)
def wage_sustainability_index():
    df = ensure_data_loaded()
    sub = df[[COUNTRY_COL, 'Real_GDP_per_Capita_USD', 'Budget_Deficit_percent_of_GDP', 
        'Public_Debt_percent_of_GDP']].copy().set_index(COUNTRY_COL)
    sub = sub.dropna()
    
    budget_risk = sub['Budget_Deficit_percent_of_GDP'].abs() / 100.0
    debt_risk = sub['Public_Debt_percent_of_GDP'] / 200.0
    risk_multiplier = 1.0 + budget_risk + debt_risk

    # This reflects the "True" cost of labor when accounting for fiscal instability.
    metric = sub['Real_GDP_per_Capita_USD'] * risk_multiplier
    
    return 1.0 - normalize_series(metric)

# Calculate economic resilience combining GDP growth, budget stability, and debt management
# Weighted: 0.4 * GDP Growth + 0.3 * Budget Stability + 0.3 * Debt Management
def economic_resilience_score():
    df = ensure_data_loaded()
    sub = df[[COUNTRY_COL, 'Real_GDP_Growth_Rate_percent', 
        'Budget_Deficit_percent_of_GDP', 
        'Public_Debt_percent_of_GDP']].copy().set_index(COUNTRY_COL)
    sub = sub.dropna()
    
    gdp_growth_norm = normalize_series(sub['Real_GDP_Growth_Rate_percent'])
    
    budget_stability = -sub['Budget_Deficit_percent_of_GDP'].abs()
    budget_norm = normalize_series(budget_stability)
    
    debt_inverted = -sub['Public_Debt_percent_of_GDP']
    debt_norm = normalize_series(debt_inverted)
    
    metric = (0.4 * gdp_growth_norm) + (0.3 * budget_norm) + (0.3 * debt_norm)
    
    return normalize_series(metric)