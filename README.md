<<<<<<< HEAD
# H-001 Automated Insight Engine

A complete local pipeline that downloads marketing/adtech data from Kaggle, performs comprehensive analytics, generates professional visualizations, produces AI-powered insights, and outputs polished PDF & PowerPoint reports automatically.

## 🎯 Features

- **Automated Kaggle Integration**: Download datasets directly from Kaggle using the API
- **Multi-Format Data Support**: CSV, XLSX, and JSON file formats
- **Comprehensive Analytics**: CTR, CPC, CPM, ROAS, conversion rates, and more
- **Professional Visualizations**: Auto-generated charts and plots
- **AI-Powered Insights**: Google Gemini integration with rule-based fallback
- **Multi-Format Reports**: PDF and PowerPoint presentations
- **Hackathon-Ready**: Runs on normal laptops without GPU requirements

## 📊 Dataset

This project uses marketing campaign datasets from multiple sources:

### Primary Dataset (Used in Testing)

**[Social Media Ad Campaign Dataset](https://www.kaggle.com/datasets/programmer3/social-media-ad-campaign-dataset)** from Kaggle

**Dataset Details:**

- **Rows**: 500 campaign records
- **Columns**: 16 attributes including:
  - `user_id`, `age`, `gender`, `location`, `interests`
  - `ad_id`, `ad_category`, `ad_platform`, `ad_type`
  - `impressions`, `clicks`, `conversion`, `time_spent_on_ad`
  - `day_of_week`, `device_type`, `engagement_score`

**Platforms Covered**: Facebook, Instagram, Google, Twitter  
**Ad Categories**: Electronics, Fashion, Food, Sports, Travel  
**Device Types**: Mobile, Desktop, Tablet  
**Perfect For**: CTR, conversion rate, engagement analysis, demographic segmentation

### Alternative: Sample Dataset (Included)

For quick testing without Kaggle download, a sample dataset (`sample_marketing_data.csv`) is auto-generated with:

- **Rows**: 443 marketing records
- **Impressions**: 2,295,626 total
- **Clicks**: 113,305 total
- **Columns**: Same 16 attributes as Kaggle dataset
- **Use Case**: Offline testing, demo purposes

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9 or higher
- Kaggle account and API credentials
- Internet connection for Kaggle downloads

### 2. Installation

```bash
# Clone or download this project
cd automated-insight-engine

# Install dependencies
pip install -r requirements.txt
```

### 3. Kaggle Configuration

To download datasets from Kaggle, you need to set up your API credentials:

#### Step 1: Get Your Kaggle API Key

1. Go to [Kaggle](https://www.kaggle.com/)
2. Click on your profile picture → **Account**
3. Scroll to **API** section
4. Click **Create New API Token**
5. This downloads `kaggle.json` to your computer

#### Step 2: Place kaggle.json

**Windows:**

```
C:\Users\<YOUR_USERNAME>\.kaggle\kaggle.json
```

**Linux/Mac:**

```
~/.kaggle/kaggle.json
```

**Manual Setup (if auto-detection fails):**

```bash
# Create .kaggle directory
mkdir -p ~/.kaggle  # Linux/Mac
mkdir %USERPROFILE%\.kaggle  # Windows

# Copy kaggle.json to the directory
cp kaggle.json ~/.kaggle/  # Linux/Mac
copy kaggle.json %USERPROFILE%\.kaggle\  # Windows

# Set permissions (Linux/Mac only)
chmod 600 ~/.kaggle/kaggle.json
```

### 4. Optional: Google Gemini API (for AI Insights)

If you want AI-powered insights:

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   USE_GEMINI=true
   ```

**Note:** If you skip this, the engine will use rule-based insights (still very useful!).

## 📖 Usage

### Basic Usage (Download from Kaggle)

```bash
cd src
python main.py --download-kaggle --output-format both
```

This will:

1. Download the Facebook Ad Campaign dataset from Kaggle
2. Clean and preprocess the data
3. Calculate all marketing metrics
4. Generate visualizations
5. Create AI insights
6. Generate both PDF and PowerPoint reports

### Use Existing Dataset

If you already have a dataset in `data/input/`:

```bash
python main.py --output-format both
```

### Generate Specific Report Types

```bash
# PDF only
python main.py --output-format pdf

# PowerPoint only
python main.py --output-format pptx
```

### Use Custom Dataset

```bash
python main.py --input-file path/to/your/dataset.csv --output-format both
```

### Enable AI Insights with Gemini

```bash
python main.py --use-gemini --output-format both
```

### Save Cleaned Dataset

```bash
python main.py --save-cleaned --output-format both
```

### All Options

```bash
python main.py --help
```

## 📁 Project Structure

```
automated-insight-engine/
├── data/
│   ├── input/              # Raw datasets (CSV, XLSX, JSON)
│   └── output/             # Cleaned datasets
├── reports/
│   ├── pdf/                # Generated PDF reports
│   ├── pptx/               # Generated PowerPoint presentations
│   └── plots/              # Chart images (PNG)
├── src/
│   ├── config.py           # Configuration and paths
│   ├── kaggle_downloader.py # Kaggle dataset downloader
│   ├── ingestion.py        # Data loading module
│   ├── preprocessing.py    # Data cleaning and preparation
│   ├── metrics.py          # KPI calculation
│   ├── visualization.py    # Chart generation
│   ├── insight_engine.py   # AI/rule-based insights
│   ├── report_pdf.py       # PDF report generation
│   ├── report_pptx.py      # PowerPoint generation
│   └── main.py             # Main orchestration pipeline
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 📊 Metrics Calculated

The engine automatically calculates:

- **CTR (Click-Through Rate)**: `(Clicks / Impressions) × 100`
- **CPC (Cost Per Click)**: `Spend / Clicks`
- **CPM (Cost Per Mille)**: `(Spend / Impressions) × 1000`
- **Conversion Rate**: `(Conversions / Clicks) × 100`
- **Cost Per Conversion**: `Spend / Conversions`
- **ROAS (Return on Ad Spend)**: `Revenue / Spend` (if revenue data available)

## 📈 Visualizations Generated

1. **CTR Trend Over Time** - Line chart with trend analysis
2. **Spend vs Clicks** - Dual-axis comparison
3. **CPC & CPM Distribution** - Histograms with averages
4. **Conversion Funnel** - Impressions → Clicks → Conversions
5. **Performance by Gender** - Multi-metric comparison
6. **Performance by Age Group** - Demographic analysis

## 🤖 AI Insights

When enabled, the Gemini AI provides:

1. **Executive Summary** - C-suite ready overview
2. **Key Performance Shifts** - Important trends and changes
3. **Root-Cause Analysis** - Why metrics perform as they do
4. **Actionable Recommendations** - Specific, data-driven suggestions

If Gemini is not configured, the engine falls back to intelligent rule-based insights.

## 🎓 Example Commands

### Hackathon Quick Start

```bash
# Complete pipeline in one command
python main.py --download-kaggle --use-gemini --output-format both --save-cleaned
```

### Demo with Existing Data

```bash
# Use pre-downloaded data, skip AI, generate PDF
python main.py --output-format pdf
```

### Custom Dataset Analysis

```bash
# Analyze your own marketing data
python main.py --input-file ../data/my_campaign.csv --output-format both
```

## 🔧 Troubleshooting

### Kaggle Download Fails

**Error: "kaggle.json not found"**

- Ensure `kaggle.json` is in the correct location
- Check file permissions (Linux/Mac: `chmod 600 ~/.kaggle/kaggle.json`)

**Error: "kaggle command not found"**

```bash
pip install kaggle
```

### Matplotlib/Visualization Errors

```bash
# Windows users may need:
pip install --upgrade matplotlib pillow

# Linux users may need:
sudo apt-get install python3-tk
```

### ReportLab PDF Issues

```bash
pip install --upgrade reportlab
```

### Google Gemini API Errors

- Verify your API key in `.env`
- Check your API quota at [Google AI Studio](https://makersuite.google.com/)
- The system will automatically fall back to rule-based insights if Gemini fails

## 📝 Dependencies

See `requirements.txt` for full list. Key libraries:

- **pandas** - Data manipulation
- **matplotlib** - Visualizations
- **reportlab** - PDF generation
- **python-pptx** - PowerPoint generation
- **kaggle** - Kaggle API
- **google-generativeai** - AI insights (optional)
=======

>>>>>>> 0474efb66b464719bf2c79697c475f8b46ecb450
