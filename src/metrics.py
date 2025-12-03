"""
Metrics Calculation Module - Calculate KPIs and performance indicators
"""
import pandas as pd
import numpy as np


def calculate_summary_metrics(df):
    """
    Calculate overall campaign performance metrics.
    
    Args:
        df: Processed pandas DataFrame
    
    Returns:
        Dictionary of summary metrics
    """
    metrics = {}
    
    # Basic counts
    if 'campaign_id' in df.columns:
        metrics['total_campaigns'] = df['campaign_id'].nunique()
    if 'ad_id' in df.columns:
        metrics['total_ads'] = df['ad_id'].nunique()
    
    # Totals
    for col in ['impressions', 'clicks', 'spent', 'conversions']:
        if col in df.columns:
            metrics[f'total_{col}'] = df[col].sum()
    
    # Averages
    if 'CTR' in df.columns:
        metrics['avg_CTR'] = df['CTR'].mean()
    if 'CPC' in df.columns:
        metrics['avg_CPC'] = df[df['CPC'] > 0]['CPC'].mean() if (df['CPC'] > 0).any() else 0
    if 'CPM' in df.columns:
        metrics['avg_CPM'] = df[df['CPM'] > 0]['CPM'].mean() if (df['CPM'] > 0).any() else 0
    if 'conversion_rate' in df.columns:
        metrics['avg_conversion_rate'] = df['conversion_rate'].mean()
    if 'cost_per_conversion' in df.columns:
        metrics['avg_cost_per_conversion'] = df[df['cost_per_conversion'] > 0]['cost_per_conversion'].mean() if (df['cost_per_conversion'] > 0).any() else 0
    
    # ROAS (Return on Ad Spend) - if revenue data available
    if 'revenue' in df.columns and 'spent' in df.columns:
        total_revenue = df['revenue'].sum()
        total_spent = df['spent'].sum()
        metrics['ROAS'] = (total_revenue / total_spent) if total_spent > 0 else 0
    
    return metrics


def calculate_segment_performance(df, segment_by='campaign_id'):
    """
    Calculate performance metrics by segment (campaign, ad, demographic, etc.).
    
    Args:
        df: Processed DataFrame
        segment_by: Column to segment by
    
    Returns:
        DataFrame with segment-level metrics
    """
    if segment_by not in df.columns:
        print(f"Warning: Column '{segment_by}' not found")
        return pd.DataFrame()
    
    agg_dict = {}
    
    # Count metrics
    agg_dict['count'] = (segment_by, 'count')
    
    # Sum metrics
    for col in ['impressions', 'clicks', 'spent', 'conversions']:
        if col in df.columns:
            agg_dict[f'total_{col}'] = (col, 'sum')
    
    # Average metrics
    for col in ['CTR', 'CPC', 'CPM', 'conversion_rate', 'cost_per_conversion']:
        if col in df.columns:
            agg_dict[f'avg_{col}'] = (col, 'mean')
    
    # Group and aggregate
    segment_df = df.groupby(segment_by).agg(**agg_dict).reset_index()
    
    # Sort by spent (highest first)
    if 'total_spent' in segment_df.columns:
        segment_df = segment_df.sort_values('total_spent', ascending=False)
    
    return segment_df


def calculate_time_series_metrics(df, date_column='date', freq='D'):
    """
    Calculate metrics over time.
    
    Args:
        df: DataFrame with date column
        date_column: Name of date column
        freq: Frequency for aggregation ('D'=daily, 'W'=weekly, 'M'=monthly)
    
    Returns:
        DataFrame with time-based metrics
    """
    if date_column not in df.columns:
        print(f"Warning: Date column '{date_column}' not found")
        return pd.DataFrame()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Set date as index and resample
    df_ts = df.set_index(date_column)
    
    agg_dict = {}
    for col in ['impressions', 'clicks', 'spent', 'conversions']:
        if col in df_ts.columns:
            agg_dict[col] = 'sum'
    
    for col in ['CTR', 'CPC', 'CPM', 'conversion_rate']:
        if col in df_ts.columns:
            agg_dict[col] = 'mean'
    
    ts_metrics = df_ts.resample(freq).agg(agg_dict).reset_index()
    
    return ts_metrics


def identify_top_performers(df, metric='spent', top_n=5, segment_by='campaign_id'):
    """
    Identify top performing segments.
    
    Args:
        df: DataFrame
        metric: Metric to rank by
        top_n: Number of top performers to return
        segment_by: Column to segment by
    
    Returns:
        DataFrame with top performers
    """
    if segment_by not in df.columns or metric not in df.columns:
        return pd.DataFrame()
    
    top_df = df.groupby(segment_by)[metric].sum().nlargest(top_n).reset_index()
    top_df.columns = [segment_by, f'total_{metric}']
    
    return top_df


if __name__ == "__main__":
    from src.ingestion import load_from_directory
    from src.preprocessing import clean_data, engineer_features
    from src.config import INPUT_DIR
    
    # Test metrics calculation
    try:
        df = load_from_directory(INPUT_DIR)
        df = clean_data(df)
        df = engineer_features(df)
        
        print("\n" + "="*50)
        print("SUMMARY METRICS")
        print("="*50)
        summary = calculate_summary_metrics(df)
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        
        print("\n" + "="*50)
        print("TOP CAMPAIGNS BY SPEND")
        print("="*50)
        if 'campaign_id' in df.columns:
            top_campaigns = identify_top_performers(df, metric='spent', segment_by='campaign_id')
            print(top_campaigns)
        
    except Exception as e:
        print(f"Error: {e}")
