"""
Data Preprocessing Module - Clean and transform data
"""
import pandas as pd
import numpy as np


def clean_data(df):
    """
    Clean the dataset: handle missing values, remove duplicates, fix data types.
    
    Args:
        df: Raw pandas DataFrame
    
    Returns:
        Cleaned pandas DataFrame
    """
    print("\n" + "="*50)
    print("DATA CLEANING")
    print("="*50)
    
    original_rows = len(df)
    print(f"Original rows: {original_rows}")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # 1. Remove duplicates
    duplicates = df_clean.duplicated().sum()
    if duplicates > 0:
        df_clean = df_clean.drop_duplicates()
        print(f"✓ Removed {duplicates} duplicate rows")
    
    # 2. Handle missing values
    missing_before = df_clean.isnull().sum().sum()
    if missing_before > 0:
        print(f"\nMissing values detected: {missing_before}")
        
        # Strategy: Fill numeric columns with 0, categorical with 'Unknown'
        for col in df_clean.columns:
            if df_clean[col].isnull().any():
                if df_clean[col].dtype in ['float64', 'int64']:
                    df_clean[col].fillna(0, inplace=True)
                    print(f"  - {col}: Filled with 0")
                else:
                    df_clean[col].fillna('Unknown', inplace=True)
                    print(f"  - {col}: Filled with 'Unknown'")
    
    # 3. Convert date columns if present
    date_columns = [col for col in df_clean.columns if 'date' in col.lower()]
    for col in date_columns:
        try:
            df_clean[col] = pd.to_datetime(df_clean[col])
            print(f"✓ Converted {col} to datetime")
        except:
            print(f"⚠ Could not convert {col} to datetime")
    
    # 4. Remove rows with invalid numeric values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        invalid = df_clean[col] < 0
        if invalid.any():
            df_clean = df_clean[~invalid]
            print(f"✓ Removed {invalid.sum()} rows with negative {col}")
    
    final_rows = len(df_clean)
    print(f"\nFinal rows: {final_rows} ({original_rows - final_rows} removed)")
    
    return df_clean


def engineer_features(df):
    """
    Create derived features for analysis.
    
    Args:
        df: Cleaned pandas DataFrame
    
    Returns:
        DataFrame with additional features
    """
    print("\n" + "="*50)
    print("FEATURE ENGINEERING")
    print("="*50)
    
    df_enhanced = df.copy()
    
    # Common marketing metrics
    if 'clicks' in df_enhanced.columns and 'impressions' in df_enhanced.columns:
        df_enhanced['CTR'] = (df_enhanced['clicks'] / df_enhanced['impressions'] * 100).fillna(0)
        print("✓ Created CTR (Click-Through Rate)")
    
    if 'spent' in df_enhanced.columns and 'clicks' in df_enhanced.columns:
        df_enhanced['CPC'] = (df_enhanced['spent'] / df_enhanced['clicks']).replace([np.inf, -np.inf], 0).fillna(0)
        print("✓ Created CPC (Cost Per Click)")
    
    if 'spent' in df_enhanced.columns and 'impressions' in df_enhanced.columns:
        df_enhanced['CPM'] = (df_enhanced['spent'] / df_enhanced['impressions'] * 1000).fillna(0)
        print("✓ Created CPM (Cost Per Mille)")
    
    if 'conversions' in df_enhanced.columns and 'clicks' in df_enhanced.columns:
        df_enhanced['conversion_rate'] = (df_enhanced['conversions'] / df_enhanced['clicks'] * 100).fillna(0)
        print("✓ Created conversion_rate")
    
    if 'conversions' in df_enhanced.columns and 'spent' in df_enhanced.columns:
        df_enhanced['cost_per_conversion'] = (df_enhanced['spent'] / df_enhanced['conversions']).replace([np.inf, -np.inf], 0).fillna(0)
        print("✓ Created cost_per_conversion")
    
    # Time-based features
    date_col = next((col for col in df_enhanced.columns if 'date' in col.lower()), None)
    if date_col and pd.api.types.is_datetime64_any_dtype(df_enhanced[date_col]):
        df_enhanced['day_of_week'] = df_enhanced[date_col].dt.dayofweek
        df_enhanced['is_weekend'] = df_enhanced['day_of_week'].isin([5, 6]).astype(int)
        df_enhanced['week_of_year'] = df_enhanced[date_col].dt.isocalendar().week
        print("✓ Created time-based features")
    
    print(f"\nTotal features: {len(df_enhanced.columns)}")
    
    return df_enhanced


if __name__ == "__main__":
    from src.ingestion import load_from_directory
    from src.config import INPUT_DIR
    
    # Test preprocessing
    try:
        df = load_from_directory(INPUT_DIR)
        df_clean = clean_data(df)
        df_final = engineer_features(df_clean)
        
        print("\n" + "="*50)
        print("FINAL DATASET PREVIEW:")
        print("="*50)
        print(df_final.head())
        print(f"\nShape: {df_final.shape}")
    except Exception as e:
        print(f"Error: {e}")
