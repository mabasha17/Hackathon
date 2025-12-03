"""
Data Ingestion Module - Load data from multiple sources
"""
import pandas as pd
from pathlib import Path


def load_data(file_path):
    """
    Load data from CSV, Excel, or JSON file.
    
    Args:
        file_path: Path to the data file
    
    Returns:
        pandas DataFrame
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    print(f"Loading data from: {file_path.name}")
    
    # Determine file type and load accordingly
    suffix = file_path.suffix.lower()
    
    if suffix == '.csv':
        df = pd.read_csv(file_path)
    elif suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    elif suffix == '.json':
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
    
    print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {', '.join(df.columns.tolist())}")
    
    return df


def load_from_directory(directory_path, pattern="*.csv"):
    """
    Load and combine multiple files from a directory.
    
    Args:
        directory_path: Path to directory containing data files
        pattern: File pattern to match (default: *.csv)
    
    Returns:
        Combined pandas DataFrame
    """
    directory_path = Path(directory_path)
    files = list(directory_path.glob(pattern))
    
    if not files:
        raise FileNotFoundError(f"No files matching '{pattern}' found in {directory_path}")
    
    print(f"Found {len(files)} file(s) matching '{pattern}'")
    
    dfs = []
    for file in files:
        print(f"Loading: {file.name}")
        df = load_data(file)
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"\n✓ Combined data: {len(combined_df)} total rows")
    
    return combined_df


if __name__ == "__main__":
    from src.config import INPUT_DIR
    
    # Test loading
    try:
        df = load_from_directory(INPUT_DIR)
        print("\n" + "="*50)
        print("DATA PREVIEW:")
        print("="*50)
        print(df.head())
        print(f"\nShape: {df.shape}")
        print(f"Data types:\n{df.dtypes}")
    except Exception as e:
        print(f"Error: {e}")
