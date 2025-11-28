import pandas as pd
import glob
from functools import reduce


def get_data():
    # Read all CSV files from the data_sets folder
    all_files = glob.glob("data_sets/*.csv")
    
    # Read each CSV into a list of DataFrames
    dfs = [pd.read_csv(f) for f in all_files]
    
    # Merge all DataFrames on 'Country' column
    df = reduce(lambda left, right: pd.merge(left, right, on='Country', how='outer'), dfs)
    
    # Drop unnecessary columns
    df = df.drop(columns=['coal_metric_tons', 'petroleum_bbl_per_day', 'refined_petroleum_products_bbl_per_day', 
                          'refined_petroleum_exports_bbl_per_day', 'refined_petroleum_imports_bbl_per_day', 
                          'natural_gas_cubic_meters', 'Geographic_Coordinates', 'Highest_Elevation', 'Lowest_Elevation', 
                          'airports_unpaved_runways_count', 'heliports_count'])
    
    # Columns that should stay as strings
    text_columns = ['Country', 'Fiscal_Year']
    
    # Clean and convert columns to numeric
    for col in df.columns:
        if col in text_columns:
            continue  # Skip text columns
            
        if df[col].dtype == 'object':  # Process string columns
            # Clean the values
            df[col] = df[col].astype(str).str.replace(',', '', regex=True)
            df[col] = df[col].str.replace(' million sq km', '', regex=True)
            df[col] = df[col].str.replace(' sq km', '', regex=True)
            df[col] = df[col].str.replace('km', '', regex=True)
            df[col] = df[col].str.replace('%', '', regex=True)
            df[col] = df[col].str.strip()
            
            # Convert to numeric (non-numeric values become NaN)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
