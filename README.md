# Automated Insight Engine (H-001)

**Track:** Data Engineering & Analytics  
**Hackathon Project:** Automated Insight Engine

## Overview

The Automated Insight Engine is a Python-based pipeline that transforms raw AdTech CSV data into executive-ready PowerPoint presentations with AI-driven insights. The system automatically:

1. **Ingests** CSV data from various sources
2. **Processes** data using pandas to calculate summary statistics
3. **Generates** AI-powered insights using LLMs (OpenAI/Gemini)
4. **Visualizes** trends with matplotlib charts
5. **Outputs** formatted PowerPoint presentations (.pptx)

## Features

- ✅ Automated data processing and statistics calculation
- ✅ LLM integration (OpenAI GPT-4o/Gemini) for intelligent insights
- ✅ Unstructured data support (client emails/complaints)
- ✅ Automatic chart generation (Clicks over Time)
- ✅ Professional PowerPoint output
- ✅ CLI-based execution (no web dashboard)
- ✅ Fallback heuristic summaries when LLM APIs are unavailable
- ✅ Support for custom CSV datasets via command-line arguments

## Project Structure

```
Hackathon/
├── main.py                      # Main orchestrator script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── data/                        # Data directory
│   ├── adtech_data.csv         # Input CSV file (auto-generated if missing)
│   └── email.txt               # Unstructured client feedback
│
├── charts/                      # Generated chart images
│   └── clicks_over_time.png    # Auto-generated visualization
│
├── reports/                     # Output directory
│   └── weekly_performance_report.pptx  # Generated PowerPoint
│
├── llm/                         # LLM integration module
│   ├── __init__.py
│   └── client.py               # OpenAI/Gemini client with fallback
│
├── ppt/                         # PowerPoint generation module
│   ├── __init__.py
│   └── pptx_generator.py       # Presentation builder
│
└── scripts/                     # Utility scripts
    └── generate_dummy_data.py  # CSV data generator for testing
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory:**

   ```bash
   cd Hackathon
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys (Optional):**

   **Option A: Using .env file (Recommended)**

   Create a `.env` file in the project root:

   ```bash
   # Create .env file
   # Windows PowerShell
   New-Item -Path .env -ItemType File

   # Linux/Mac
   touch .env
   ```

   Add your API keys to `.env`:

   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

   **Option B: Using System Environment Variables**

   For **OpenAI**:

   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-openai-api-key-here"

   # Linux/Mac
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

   For **Google Gemini**:

   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-gemini-api-key-here"

   # Linux/Mac
   export GEMINI_API_KEY="your-gemini-api-key-here"
   ```

   **Note:**

   - The `.env` file method is recommended as it's easier to manage
   - The `.env` file is automatically ignored by git (see `.gitignore`)
   - If no API keys are configured, the system will use a heuristic fallback summary generator

## Usage

### Basic Usage

Run the main script to process data and generate a PowerPoint:

```bash
python main.py
```

This will:

1. Load or generate `data/adtech_data.csv` (if missing)
2. Calculate summary statistics
3. Read unstructured data from `data/email.txt`
4. Generate a chart (`charts/clicks_over_time.png`)
5. Get AI insights (or use fallback)
6. Create PowerPoint (`reports/weekly_performance_report.pptx`)

### Using Custom Datasets

Process your own CSV file:

```bash
python main.py --input path/to/your/dataset.csv
```

**With custom output filename:**

```bash
python main.py --input my_data.csv --output my_custom_report.pptx
```

**With custom email context:**

```bash
python main.py --input my_data.csv --email my_emails.txt
```

**CSV Format Requirements:**
Your CSV must contain these columns:

- `Date` - Date column (will be parsed automatically)
- `Clicks` - Number of clicks (integer)
- `Impressions` - Number of impressions (integer)
- `Spend` - Amount spent (float)
- `Platform` - Platform name (e.g., "Google", "Facebook")
- `Campaign_ID` - Campaign identifier (optional but recommended)

### Custom Output Path

Specify a custom output file:

```bash
python main.py --output my_custom_report.pptx
```

### Generate Test Data

If you need to regenerate the test CSV file:

```bash
python scripts/generate_dummy_data.py
```

This creates `data/adtech_data.csv` with 500 rows of realistic AdTech data.

