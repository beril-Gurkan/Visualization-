from pathlib import Path
import pandas as pd
from functools import reduce


def get_data():
    # Read all CSV files from the package-local data_sets folder
    data_dir = Path(__file__).parent / "data_sets"
    all_files = [str(p) for p in data_dir.glob("*.csv")]
    
    # Read each CSV into a list of DataFrames
    dfs = [pd.read_csv(f) for f in all_files]
    
    # Merge all DataFrames on 'Country' column
    df = reduce(lambda left, right: pd.merge(left, right, on='Country', how='outer'), dfs)
    
    # Drop unnecessary columns
    df = df.drop(columns=['coal_metric_tons', 'petroleum_bbl_per_day', 'refined_petroleum_products_bbl_per_day', 
                          'refined_petroleum_exports_bbl_per_day', 'refined_petroleum_imports_bbl_per_day', 
                          'natural_gas_cubic_meters', 'Geographic_Coordinates', 'Highest_Elevation', 'Lowest_Elevation', 
                          'airports_unpaved_runways_count', 'heliports_count'])
    
    # columns that should stay as strings
    text_columns = ['Country', 'Fiscal_Year']
    
    # Clean and convert columns to numeric
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