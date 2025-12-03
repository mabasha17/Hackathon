"""
Central Configuration for Automated Insight Engine
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add D drive Python libraries to path FIRST
D_DRIVE_LIBS = r"D:\python_libs"
if D_DRIVE_LIBS not in sys.path:
    sys.path.insert(0, D_DRIVE_LIBS)

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"
PDF_DIR = REPORTS_DIR / "pdf"
PPTX_DIR = REPORTS_DIR / "pptx"
PLOTS_DIR = REPORTS_DIR / "plots"

# Create directories if they don't exist
for directory in [INPUT_DIR, OUTPUT_DIR, PDF_DIR, PPTX_DIR, PLOTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Kaggle configuration
KAGGLE_JSON_PATHS = [
    Path(r"C:\Users\HARSHA VARDHAN\Downloads\kaggle.json"),  # User's Downloads folder
    Path.home() / ".kaggle" / "kaggle.json",
    Path(os.getenv("KAGGLE_CONFIG_DIR", "")) / "kaggle.json" if os.getenv("KAGGLE_CONFIG_DIR") else None,
]

KAGGLE_DATASET = os.getenv("KAGGLE_DATASET", "programmer3/social-media-ad-campaign-dataset")

# Gemini AI configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "true").lower() == "true"

# Visualization settings
CHART_DPI = 100
CHART_FIGSIZE = (10, 6)
COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Report settings
COMPANY_NAME = os.getenv("COMPANY_NAME", "Marketing Analytics Inc.")
REPORT_AUTHOR = os.getenv("REPORT_AUTHOR", "Automated Insight Engine")
