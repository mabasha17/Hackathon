"""
Main Pipeline - Orchestrate the complete automated insight engine
"""
import argparse
import sys
from pathlib import Path
import pandas as pd

# Import all modules
from src.config import INPUT_DIR, OUTPUT_DIR
from src.kaggle_downloader import download_kaggle_dataset
from src.ingestion import load_from_directory
from src.preprocessing import clean_data, engineer_features
from src.metrics import calculate_summary_metrics
from src.visualization import create_comprehensive_dashboard
from src.insight_engine import generate_detailed_analysis, generate_ai_insights
from src.report_pdf import create_pdf_report
from src.report_pptx import create_pptx_report


def create_sample_dataset():
    """Create a sample marketing campaign dataset for testing."""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    print("\n" + "="*60)
    print("CREATING SAMPLE DATASET")
    print("="*60)
    
    np.random.seed(42)
    
    # Generate 30 days of data
    start_date = datetime(2024, 11, 1)
    dates = [start_date + timedelta(days=i) for i in range(30)]
    
    data = []
    campaign_ids = [f'CMP_{i:03d}' for i in range(1, 7)]
    ad_ids = [f'AD_{i:03d}' for i in range(1, 11)]
    genders = ['Male', 'Female']
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    interests = ['Technology', 'Fashion', 'Sports', 'Travel', 'Food']
    
    for date in dates:
        for _ in range(np.random.randint(10, 20)):
            impressions = np.random.randint(1000, 10000)
            clicks = int(impressions * np.random.uniform(0.01, 0.08))
            spent = clicks * np.random.uniform(0.10, 1.50)
            conversions = int(clicks * np.random.uniform(0.01, 0.06))
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'campaign_id': np.random.choice(campaign_ids),
                'ad_id': np.random.choice(ad_ids),
                'gender': np.random.choice(genders),
                'age': np.random.choice(age_groups),
                'interest': np.random.choice(interests),
                'impressions': impressions,
                'clicks': clicks,
                'spent': round(spent, 2),
                'conversions': conversions
            })
    
    df = pd.DataFrame(data)
    output_path = INPUT_DIR / 'sample_campaign_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✓ Created sample dataset: {len(df)} rows")
    print(f"✓ Saved to: {output_path}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Campaigns: {df['campaign_id'].nunique()}")
    print(f"  Ads: {df['ad_id'].nunique()}")
    
    return output_path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Automated Marketing Insight Engine')
    
    parser.add_argument('--download', action='store_true',
                       help='Download dataset from Kaggle')
    parser.add_argument('--dataset', type=str,
                       help='Kaggle dataset identifier (e.g., username/dataset-name)')
    parser.add_argument('--input', type=str,
                       help='Path to input data file or directory')
    parser.add_argument('--output-format', type=str, choices=['pdf', 'pptx', 'both'],
                       default='both', help='Output report format')
    parser.add_argument('--sample', action='store_true',
                       help='Use sample dataset (for testing)')
    
    return parser.parse_args()


def main():
    """Main pipeline execution."""
    print("\n" + "="*60)
    print("AUTOMATED INSIGHT ENGINE - STARTING")
    print("="*60)
    
    args = parse_arguments()
    
    # Step 1: Data Acquisition
    print("\n[STEP 1/7] DATA ACQUISITION")
    
    if args.sample:
        # Create sample dataset
        data_path = create_sample_dataset()
    elif args.download or args.dataset:
        # Download from Kaggle
        dataset_name = args.dataset if args.dataset else None
        data_path = download_kaggle_dataset(dataset_name)
        
        if not data_path:
            print("⚠ Kaggle download failed, creating sample dataset instead...")
            data_path = create_sample_dataset()
    elif args.input:
        # Use provided input
        data_path = Path(args.input)
        if not data_path.exists():
            print(f"Error: Input path not found: {data_path}")
            sys.exit(1)
    else:
        # Try to load existing data, or create sample
        existing_files = list(INPUT_DIR.glob("*.csv"))
        if existing_files:
            print(f"✓ Found existing data files: {len(existing_files)}")
            data_path = INPUT_DIR
        else:
            print("No existing data found, creating sample dataset...")
            data_path = create_sample_dataset()
    
    # Step 2: Data Ingestion
    print("\n[STEP 2/7] DATA INGESTION")
    if data_path.is_dir():
        df = load_from_directory(data_path)
    else:
        from ingestion import load_data
        df = load_data(data_path)
    
    # Step 3: Data Cleaning
    print("\n[STEP 3/7] DATA PREPROCESSING")
    df_clean = clean_data(df)
    df_processed = engineer_features(df_clean)
    
    # Step 4: Metrics Calculation
    print("\n[STEP 4/7] METRICS CALCULATION")
    summary_metrics = calculate_summary_metrics(df_processed)
    
    print("\nSummary Metrics:")
    for key, value in summary_metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    # Step 5: Visualization
    print("\n[STEP 5/7] CREATING COMPREHENSIVE VISUALIZATIONS")
    chart_paths = create_comprehensive_dashboard(df_processed)
    
    # Step 6: AI Insights
    print("\n[STEP 6/7] GENERATING AI-POWERED INSIGHTS")
    detailed_analysis = generate_detailed_analysis(df_processed, summary_metrics)
    insights = generate_ai_insights(df_processed, summary_metrics)
    
    print("\n" + insights)
    
    # Step 7: Report Generation
    print("\n[STEP 7/7] GENERATING COMPREHENSIVE REPORTS")
    
    reports_generated = []
    
    if args.output_format in ['pdf', 'both']:
        pdf_path = create_pdf_report(summary_metrics, detailed_analysis, chart_paths)
        reports_generated.append(pdf_path)
    
    if args.output_format in ['pptx', 'both']:
        pptx_path = create_pptx_report(summary_metrics, detailed_analysis, chart_paths)
        reports_generated.append(pptx_path)
    
    # Final Summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n✓ Processed {len(df_processed)} records")
    print(f"✓ Generated {len(chart_paths)} visualizations")
    print(f"✓ Created {len(reports_generated)} report(s)")
    
    print("\nGenerated Reports:")
    for report in reports_generated:
        print(f"  - {report}")
    
    print("\nCharts saved to:")
    print(f"  {chart_paths[0].parent if chart_paths else 'N/A'}")
    
    print("\n" + "="*60)
    print("Thank you for using Automated Insight Engine!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
