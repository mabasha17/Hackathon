"""
Kaggle Dataset Downloader with automatic authentication
"""
import shutil
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from src.config import KAGGLE_JSON_PATHS, INPUT_DIR, KAGGLE_DATASET


def setup_kaggle_auth():
    """Locate and copy kaggle.json to the standard location."""
    standard_location = Path.home() / ".kaggle" / "kaggle.json"
    
    # If already at standard location, we're done
    if standard_location.exists():
        print(f"✓ Kaggle credentials found at: {standard_location}")
        return True
    
    # Search alternate paths
    for path in KAGGLE_JSON_PATHS:
        if path and path.exists():
            print(f"Found kaggle.json at: {path}")
            standard_location.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, standard_location)
            standard_location.chmod(0o600)  # Secure permissions
            print(f"✓ Copied to standard location: {standard_location}")
            return True
    
    print("❌ kaggle.json not found. Please place it in one of these locations:")
    for path in KAGGLE_JSON_PATHS:
        if path:
            print(f"   - {path}")
    return False


def download_kaggle_dataset(dataset_name=None, output_path=None):
    """
    Download dataset from Kaggle.
    
    Args:
        dataset_name: Kaggle dataset identifier (e.g., 'username/dataset-name')
        output_path: Directory to save the dataset
    
    Returns:
        Path to downloaded CSV file or None if failed
    """
    if not setup_kaggle_auth():
        return None
    
    dataset_name = dataset_name or KAGGLE_DATASET
    output_path = Path(output_path) if output_path else INPUT_DIR
    
    try:
        print(f"\nDownloading dataset: {dataset_name}")
        api = KaggleApi()
        api.authenticate()
        
        api.dataset_download_files(
            dataset_name,
            path=output_path,
            unzip=True
        )
        
        print(f"✓ Dataset downloaded to: {output_path}")
        
        # Find the CSV file
        csv_files = list(output_path.glob("*.csv"))
        if csv_files:
            print(f"✓ Found CSV file: {csv_files[0].name}")
            return csv_files[0]
        else:
            print("⚠ No CSV file found in downloaded dataset")
            return None
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None


if __name__ == "__main__":
    csv_path = download_kaggle_dataset()
    if csv_path:
        print(f"\n✓ Success! Dataset ready at: {csv_path}")
    else:
        print("\n❌ Download unsuccessful")
