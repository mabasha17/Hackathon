"""
Enhanced Visualization Module - 15+ Advanced Charts
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from src.config import PLOTS_DIR, CHART_DPI, CHART_FIGSIZE, COLOR_PALETTE

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette(COLOR_PALETTE)


def plot_advanced_time_series(df, date_column='date', metrics=['CTR'], title='Performance Trend'):
    """Create multi-metric time series with trend lines."""
    if date_column not in df.columns:
        return None
    
    available_metrics = [m for m in metrics if m in df.columns]
    if not available_metrics:
        return None
    
    fig, axes = plt.subplots(len(available_metrics), 1, figsize=(12, 4*len(available_metrics)), dpi=CHART_DPI)
    if len(available_metrics) == 1:
        axes = [axes]
    
    for idx, metric in enumerate(available_metrics):
        ax = axes[idx]
        
        # Plot actual data
        ax.plot(df[date_column], df[metric], marker='o', label='Actual', color=COLOR_PALETTE[0], linewidth=2)
        
        # Add trend line
        z = np.polyfit(range(len(df)), df[metric], 1)
        p = np.poly1d(z)
        ax.plot(df[date_column], p(range(len(df))), "--", label='Trend', color=COLOR_PALETTE[1], linewidth=2)
        
        # Add moving average
        if len(df) >= 7:
            df['MA7'] = df[metric].rolling(window=min(7, len(df))).mean()
            ax.plot(df[date_column], df['MA7'], label='7-Day MA', color=COLOR_PALETTE[2], alpha=0.7, linewidth=2)
        
        ax.set_title(f'{metric} Over Time', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel(metric, fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    output_path = PLOTS_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
    plt.close()
    
    print(f"✓ Saved: {output_path.name}")
    return output_path


def plot_correlation_heatmap(df, title='Correlation Matrix'):
    """Create correlation heatmap for numeric features."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return None
    
    corr = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10), dpi=CHART_DPI)
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": .8}, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    output_path = PLOTS_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
    plt.close()
    
    print(f"✓ Saved: {output_path.name}")
    return output_path


def plot_distribution_analysis(df, column, title=None):
    """Create distribution plot with statistics."""
    if column not in df.columns or df[column].dtype not in [np.number, 'float64', 'int64']:
        return None
    
    title = title or f'{column} Distribution'
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=CHART_DPI)
    
    # Histogram with KDE
    axes[0].hist(df[column], bins=30, edgecolor='black', alpha=0.7, color=COLOR_PALETTE[0])
    axes[0].axvline(df[column].mean(), color=COLOR_PALETTE[1], linestyle='--', linewidth=2, label=f'Mean: {df[column].mean():.2f}')
    axes[0].axvline(df[column].median(), color=COLOR_PALETTE[2], linestyle='--', linewidth=2, label=f'Median: {df[column].median():.2f}')
    axes[0].set_title('Histogram', fontsize=14, fontweight='bold')
    axes[0].set_xlabel(column, fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Box plot
    box = axes[1].boxplot(df[column], vert=True, patch_artist=True)
    box['boxes'][0].set_facecolor(COLOR_PALETTE[0])
    axes[1].set_title('Box Plot', fontsize=14, fontweight='bold')
    axes[1].set_ylabel(column, fontsize=12)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Add stats text
    stats_text = f'Mean: {df[column].mean():.2f}\nStd: {df[column].std():.2f}\nMin: {df[column].min():.2f}\nMax: {df[column].max():.2f}'
    axes[1].text(1.5, df[column].median(), stats_text, fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    output_path = PLOTS_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
    plt.close()
    
    print(f"✓ Saved: {output_path.name}")
    return output_path


def plot_top_performers(df, category_col, value_col, title='Top Performers', top_n=10):
    """Create horizontal bar chart for top performers."""
    if category_col not in df.columns or value_col not in df.columns:
        return None
    
    top_data = df.groupby(category_col)[value_col].sum().nlargest(top_n).sort_values()
    
    fig, ax = plt.subplots(figsize=(12, 8), dpi=CHART_DPI)
    
    bars = ax.barh(range(len(top_data)), top_data.values, color=COLOR_PALETTE[0], edgecolor='black')
    ax.set_yticks(range(len(top_data)))
    ax.set_yticklabels(top_data.index)
    ax.set_xlabel(value_col, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_data.values)):
        ax.text(value, i, f' {value:,.0f}', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = PLOTS_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
    plt.close()
    
    print(f"✓ Saved: {output_path.name}")
    return output_path


def plot_funnel_conversion(df, stages, values, title='Conversion Funnel'):
    """Create conversion funnel visualization."""
    fig, ax = plt.subplots(figsize=(10, 8), dpi=CHART_DPI)
    
    colors = sns.color_palette("YlOrRd", len(stages))
    
    y_pos = np.arange(len(stages))
    ax.barh(y_pos, values, color=colors, edgecolor='black', linewidth=2)
    
    # Add percentage labels
    for i, (stage, value) in enumerate(zip(stages, values)):
        percentage = (value / values[0] * 100) if i > 0 else 100
        ax.text(value/2, i, f'{stage}\n{value:,.0f} ({percentage:.1f}%)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        if i > 0:
            drop_off = ((values[i-1] - value) / values[i-1] * 100)
            ax.text(values[i-1] + 10, i-0.3, f'↓ {drop_off:.1f}%', 
                    fontsize=10, color='red', fontweight='bold')
    
    ax.set_yticks([])
    ax.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_path = PLOTS_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
    plt.close()
    
    print(f"✓ Saved: {output_path.name}")
    return output_path


def plot_segment_comparison(df, segment_col, metrics, title='Segment Comparison'):
    """Create grouped bar chart for segment comparison."""
    if segment_col not in df.columns:
        return None
    
    available_metrics = [m for m in metrics if m in df.columns]
    if not available_metrics:
        return None
    
    segment_data = df.groupby(segment_col)[available_metrics].mean()
    
    fig, ax = plt.subplots(figsize=(14, 7), dpi=CHART_DPI)
    
    x = np.arange(len(segment_data))
    width = 0.8 / len(available_metrics)
    
    for i, metric in enumerate(available_metrics):
        offset = width * i - (width * len(available_metrics) / 2) + width / 2
        bars = ax.bar(x + offset, segment_data[metric], width, label=metric, color=COLOR_PALETTE[i])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(segment_data.index, rotation=45, ha='right')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = PLOTS_DIR / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
    plt.close()
    
    print(f"✓ Saved: {output_path.name}")
    return output_path


def create_comprehensive_dashboard(df):
    """
    Create comprehensive set of 15+ visualization charts.
    """
    print("\n" + "="*60)
    print("CREATING COMPREHENSIVE VISUALIZATIONS")
    print("="*60)
    
    charts = []
    
    # 1. Correlation Heatmap
    chart = plot_correlation_heatmap(df, 'Feature Correlation Matrix')
    if chart:
        charts.append(chart)
    
    # 2-4. Distribution Analysis for key metrics
    for col in ['impressions', 'clicks', 'CTR']:
        if col in df.columns:
            chart = plot_distribution_analysis(df, col, f'{col.upper()} Distribution Analysis')
            if chart:
                charts.append(chart)
    
    # 5-7. Top Performers by different dimensions
    if 'ad_id' in df.columns and 'impressions' in df.columns:
        chart = plot_top_performers(df, 'ad_id', 'impressions', 'Top 10 Ads by Impressions', top_n=10)
        if chart:
            charts.append(chart)
    
    if 'ad_category' in df.columns and 'clicks' in df.columns:
        chart = plot_top_performers(df, 'ad_category', 'clicks', 'Top Categories by Clicks', top_n=8)
        if chart:
            charts.append(chart)
    
    if 'ad_platform' in df.columns and 'engagement_score' in df.columns:
        chart = plot_top_performers(df, 'ad_platform', 'engagement_score', 'Platform Performance', top_n=5)
        if chart:
            charts.append(chart)
    
    # 8. Conversion Funnel
    if all(col in df.columns for col in ['impressions', 'clicks']):
        total_impressions = df['impressions'].sum()
        total_clicks = df['clicks'].sum()
        total_conversions = df['conversion'].sum() if 'conversion' in df.columns else total_clicks * 0.05
        
        chart = plot_funnel_conversion(
            df,
            ['Impressions', 'Clicks', 'Conversions'],
            [total_impressions, total_clicks, total_conversions],
            'Marketing Conversion Funnel'
        )
        if chart:
            charts.append(chart)
    
    # 9-11. Segment Comparisons
    if 'gender' in df.columns:
        chart = plot_segment_comparison(df, 'gender', ['CTR', 'clicks', 'impressions'], 'Performance by Gender')
        if chart:
            charts.append(chart)
    
    if 'device_type' in df.columns:
        chart = plot_segment_comparison(df, 'device_type', ['CTR', 'engagement_score'], 'Performance by Device Type')
        if chart:
            charts.append(chart)
    
    if 'ad_platform' in df.columns:
        chart = plot_segment_comparison(df, 'ad_platform', ['CTR', 'clicks'], 'Performance by Platform')
        if chart:
            charts.append(chart)
    
    # 12-13. Advanced visualizations
    if 'age' in df.columns and 'CTR' in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6), dpi=CHART_DPI)
        age_ctr = df.groupby('age')['CTR'].mean().sort_values(ascending=False)
        ax.plot(range(len(age_ctr)), age_ctr.values, marker='o', markersize=10, color=COLOR_PALETTE[0], linewidth=2)
        ax.fill_between(range(len(age_ctr)), age_ctr.values, alpha=0.3, color=COLOR_PALETTE[0])
        ax.set_xticks(range(len(age_ctr)))
        ax.set_xticklabels(age_ctr.index, rotation=45, ha='right')
        ax.set_title('CTR Performance by Age Group', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Average CTR (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Age Group', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        output_path = PLOTS_DIR / "ctr_by_age_group.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
        plt.close()
        charts.append(output_path)
        print(f"✓ Saved: {output_path.name}")
    
    # 14. Engagement heatmap
    if 'day_of_week' in df.columns and 'ad_type' in df.columns and 'engagement_score' in df.columns:
        pivot = df.pivot_table(values='engagement_score', index='ad_type', columns='day_of_week', aggfunc='mean')
        fig, ax = plt.subplots(figsize=(12, 6), dpi=CHART_DPI)
        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlOrRd', linewidths=1, ax=ax)
        ax.set_title('Engagement Score Heatmap: Ad Type vs Day of Week', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
        ax.set_ylabel('Ad Type', fontsize=12, fontweight='bold')
        plt.tight_layout()
        output_path = PLOTS_DIR / "engagement_heatmap_ad_type_day.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
        plt.close()
        charts.append(output_path)
        print(f"✓ Saved: {output_path.name}")
    
    # 15. ROI/Performance scatter
    if 'clicks' in df.columns and 'impressions' in df.columns and 'engagement_score' in df.columns:
        fig, ax = plt.subplots(figsize=(12, 8), dpi=CHART_DPI)
        scatter = ax.scatter(df['clicks'], df['impressions'], 
                            c=df['engagement_score'], s=100, 
                            cmap='viridis', alpha=0.6, edgecolors='black')
        ax.set_xlabel('Clicks', fontsize=12, fontweight='bold')
        ax.set_ylabel('Impressions', fontsize=12, fontweight='bold')
        ax.set_title('Performance Matrix: Clicks vs Impressions (colored by Engagement)', 
                     fontsize=16, fontweight='bold', pad=20)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Engagement Score', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        output_path = PLOTS_DIR / "performance_matrix_scatter.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=CHART_DPI)
        plt.close()
        charts.append(output_path)
        print(f"✓ Saved: {output_path.name}")
    
    print(f"\n✓ Created {len(charts)} comprehensive charts")
    return charts
