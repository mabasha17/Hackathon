"""
Enhanced AI Insight Engine using Google Gemini API
"""
import os
import sys
sys.path.insert(0, r'D:\python_libs')

import pandas as pd
from src.config import USE_GEMINI, GEMINI_API_KEY

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("⚠ google-generativeai not installed. Using rule-based insights.")
    GEMINI_AVAILABLE = False


def initialize_gemini():
    """Initialize Gemini API."""
    if not GEMINI_AVAILABLE or not USE_GEMINI:
        return None
    
    if not GEMINI_API_KEY:
        print("⚠ GEMINI_API_KEY not found. Using rule-based insights.")
        return None
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        print("✓ Google Gemini API initialized")
        return model
    except Exception as e:
        print(f"⚠ Gemini init failed: {e}")
        return None


def generate_detailed_analysis(df, metrics):
    """Generate comprehensive AI analysis for reports."""
    model = initialize_gemini()
    
    if model:
        try:
            # Prepare data summary
            demo_breakdown = ""
            if 'gender' in df.columns and 'age' in df.columns:
                demo_breakdown = df.groupby(['gender', 'age']).size().head(10).to_string()
            
            platform_perf = ""
            if 'ad_platform' in df.columns:
                platform_perf = df.groupby('ad_platform')[['impressions', 'clicks', 'CTR']].mean().to_string()
            
            category_perf = ""
            if 'ad_category' in df.columns:
                category_perf = df.groupby('ad_category')[['impressions', 'clicks', 'CTR']].mean().head(8).to_string()
            
            top_ads = ""
            if 'CTR' in df.columns and 'ad_id' in df.columns:
                top_ads = df.nlargest(5, 'CTR')[['ad_id', 'impressions', 'clicks', 'CTR']].to_string()
            
            device_analysis = ""
            if 'device_type' in df.columns:
                device_analysis = df.groupby('device_type')[['impressions', 'clicks', 'engagement_score']].mean().to_string()
            
            day_trends = ""
            if 'day_of_week' in df.columns:
                day_trends = df.groupby('day_of_week')[['impressions', 'clicks', 'CTR']].mean().to_string()
            
            prompt = f"""You are a senior marketing analytics strategist preparing a comprehensive C-level executive report. Analyze this campaign data with extreme precision and strategic depth:

DATASET OVERVIEW:
- Total Records: {len(df):,}
- Data Columns: {', '.join(df.columns.tolist())}

KEY PERFORMANCE METRICS:
- Total Impressions: {metrics.get('total_impressions', 0):,}
- Total Clicks: {metrics.get('total_clicks', 0):,}
- Total Conversions: {metrics.get('total_conversions', 0):,}
- Average CTR: {metrics.get('avg_ctr', 0):.2f}%
- Average CPC: ${metrics.get('avg_cpc', 0):.4f}
- Average CPM: ${metrics.get('avg_cpm', 0):.2f}
- Conversion Rate: {metrics.get('conversion_rate', 0):.2f}%
- Total Campaign Spend: ${metrics.get('total_spent', 0):,.2f}

DEMOGRAPHIC BREAKDOWN:
{demo_breakdown}

PLATFORM PERFORMANCE:
{platform_perf}

CATEGORY PERFORMANCE:
{category_perf}

TOP PERFORMING ADS:
{top_ads}

DEVICE ANALYSIS:
{device_analysis}

DAY OF WEEK TRENDS:
{day_trends}

Provide a COMPREHENSIVE, CEO-READY analysis with the following sections:

**1. EXECUTIVE SUMMARY (3-4 paragraphs)**
Deliver a high-level strategic overview summarizing overall performance, major achievements, and critical findings. Highlight key strengths, weaknesses, and the most impactful insights. Maintain a strategic, CEO-ready tone focusing on essential business takeaways. Include specific percentages and dollar amounts.

**2. PERFORMANCE ANALYSIS (5-6 paragraphs)**
Deep dive into impressions, clicks, conversions, CTR, CPC, CPM, and ROAS. Evaluate trends, correlations, performance patterns, outliers, and anomalies. Explain underlying causes behind strong or weak performance. Discuss spend allocation efficiency. Interpret how metrics evolved and how variables relate. Compare against industry benchmarks (2-3% CTR standard).

**3. DEMOGRAPHIC INSIGHTS (3-4 paragraphs)**
Analyze performance across age groups, gender, regions, and interests. Identify high/low-performing audience clusters, cost-efficient segments, behavioral engagement patterns, and conversion effectiveness. Explain strategic implications for future targeting. Quantify differences between segments with specific numbers.

**4. PLATFORM & CHANNEL ANALYSIS (3-4 paragraphs)**
Compare performance across platforms, channels, and device types. Identify which platforms delivered best engagement, conversions, or ROAS and explain why. Evaluate each channel's contribution to overall performance. Highlight platform-specific nuances impacting cost and efficiency.

**5. TEMPORAL PATTERNS (2-3 paragraphs)**
Discuss day-of-week performance, weekday vs weekend variations, peak engagement periods, and notable timeline shifts. Explain how these insights inform scheduling, bidding optimization, and budget pacing strategies.

**6. TOP PERFORMERS (2-3 paragraphs)**
Identify top-performing ads, campaigns, audience segments, or creative categories. Explain characteristics contributing to strong performance: messaging, targeting, timing, platform alignment. Provide insight into what made these stand out.

**7. AREAS OF CONCERN (2-3 paragraphs)**
Highlight underperforming campaigns, demographics, platforms, or time periods. Identify red flags: high CPC/CPM segments, low-engagement audiences, poor ROAS regions, inefficient budget utilization. Discuss root causes and business risks.

**8. STRATEGIC RECOMMENDATIONS (5-6 detailed bullets)**
Provide specific, actionable, high-impact recommendations. Each must include:
  • WHAT to change
  • WHY it matters
  • EXPECTED business impact (quantified where possible)

**9. FUTURE OPPORTUNITIES (4-5 detailed bullets)**
Highlight advanced opportunities: new audience clusters, predictive modeling potential, cross-platform expansion, AI-driven optimization, creative strategy refinement, advanced segmentation.

**10. RISK ASSESSMENT (2-3 paragraphs)**
Discuss operational, financial, or performance risks: spend inefficiency, platform dependency, demographic imbalance, seasonal volatility, data instability. Provide specific mitigation strategies to reduce exposure and maintain consistent performance.

Use professional business language. Include specific numbers, percentages, and dollar amounts throughout. Make it actionable and strategic."""
            
            response = model.generate_content(prompt)
            print("✓ Generated detailed AI analysis")
            return response.text
            
        except Exception as e:
            print(f"⚠ Gemini error: {e}. Using rule-based analysis.")
            return generate_rule_based_analysis(df, metrics)
    else:
        return generate_rule_based_analysis(df, metrics)


def generate_rule_based_analysis(df, metrics):
    """Comprehensive rule-based analysis following CEO-ready report structure."""
    analysis = []
    
    # 1. EXECUTIVE SUMMARY
    analysis.append("="*70)
    analysis.append("1. EXECUTIVE SUMMARY")
    analysis.append("="*70)
    
    total_imp = metrics.get('total_impressions', 0)
    total_clicks = metrics.get('total_clicks', 0)
    total_conv = metrics.get('total_conversions', 0)
    ctr = metrics.get('avg_ctr', 0)
    cpc = metrics.get('avg_cpc', 0)
    cpm = metrics.get('avg_cpm', 0)
    conv_rate = metrics.get('conversion_rate', 0)
    total_spent = metrics.get('total_spent', 0)
    
    analysis.append(f"\nThis comprehensive campaign analysis examines {len(df):,} marketing records, "
                   f"representing {total_imp:,} total impressions and {total_clicks:,} clicks across "
                   f"multiple platforms, demographics, and creative categories. The campaign achieved an "
                   f"overall CTR of {ctr:.2f}%, generating {total_conv:,} conversions with a total "
                   f"expenditure of ${total_spent:,.2f}.\n")
    
    # Performance assessment
    if ctr > 5:
        performance_verdict = "exceptionally strong performance, significantly exceeding industry benchmarks"
        strength_level = "EXCELLENT"
    elif ctr > 3:
        performance_verdict = "solid performance, surpassing standard industry CTR benchmarks of 2-3%"
        strength_level = "STRONG"
    elif ctr > 2:
        performance_verdict = "moderate performance, aligning with industry standards"
        strength_level = "MODERATE"
    else:
        performance_verdict = "below-benchmark performance requiring immediate strategic intervention"
        strength_level = "NEEDS IMPROVEMENT"
    
    analysis.append(f"Performance Assessment: The campaign demonstrates {performance_verdict}. "
                   f"With an average CPC of ${cpc:.4f} and CPM of ${cpm:.2f}, cost efficiency is "
                   f"{'highly competitive' if cpc < 0.50 else 'within acceptable ranges' if cpc < 1.00 else 'requiring optimization'}. "
                   f"The conversion rate of {conv_rate:.2f}% indicates "
                   f"{'exceptional' if conv_rate > 5 else 'strong' if conv_rate > 3 else 'moderate' if conv_rate > 1 else 'weak'} "
                   f"post-click engagement and funnel effectiveness.\n")
    
    # Key strengths
    strengths = []
    if ctr > 3:
        strengths.append(f"superior click-through performance ({ctr:.2f}% CTR)")
    if conv_rate > 3:
        strengths.append(f"high conversion efficiency ({conv_rate:.2f}% rate)")
    if cpc < 0.50:
        strengths.append(f"cost-effective acquisition (${cpc:.4f} CPC)")
    
    analysis.append(f"Key Strengths: {', '.join(strengths) if strengths else 'Baseline performance established across all metrics'}. "
                   f"Critical findings reveal significant performance variation across demographic segments, "
                   f"platforms, and temporal patterns, presenting clear optimization opportunities worth an estimated "
                   f"15-30% performance improvement through strategic reallocation and targeting refinement.\n")
    
    # 2. PERFORMANCE ANALYSIS
    analysis.append("\n" + "="*70)
    analysis.append("2. PERFORMANCE ANALYSIS")
    analysis.append("="*70)
    
    analysis.append(f"\nImpression Volume & Reach: The campaign generated {total_imp:,} total impressions, "
                   f"averaging {total_imp/len(df):.0f} impressions per record. This reach establishes "
                   f"{'strong' if total_imp > 1000000 else 'moderate' if total_imp > 100000 else 'initial'} "
                   f"brand visibility across target audiences. Impression distribution patterns reveal "
                   f"{'concentrated' if df['impressions'].std()/df['impressions'].mean() < 0.5 else 'highly variable'} "
                   f"performance across creative units, indicating "
                   f"{'consistent delivery' if df['impressions'].std()/df['impressions'].mean() < 0.5 else 'audience fragmentation or targeting inconsistencies'}.\n")
    
    analysis.append(f"Click Performance & Engagement: With {total_clicks:,} total clicks at {ctr:.2f}% CTR, "
                   f"the campaign {'significantly outperforms' if ctr > 4 else 'meets' if ctr > 2 else 'underperforms'} "
                   f"the industry standard 2-3% benchmark. Click distribution analysis shows "
                   f"{'concentrated engagement' if df['clicks'].std()/df['clicks'].mean() < 1 else 'dispersed engagement patterns'}, "
                   f"suggesting {'effective creative resonance' if ctr > 3 else 'opportunities for creative optimization'}. "
                   f"The clicks-to-impressions ratio demonstrates {'strong audience-message alignment' if ctr > 4 else 'baseline engagement requiring enhancement'}.\n")
    
    analysis.append(f"Conversion Efficiency: The campaign achieved {total_conv:,} conversions, representing a "
                   f"{conv_rate:.2f}% conversion rate from total clicks. This conversion efficiency is "
                   f"{'exceptional' if conv_rate > 5 else 'competitive' if conv_rate > 2 else 'below expectations'}, "
                   f"indicating {'highly effective' if conv_rate > 5 else 'adequate' if conv_rate > 2 else 'suboptimal'} "
                   f"landing page experience and offer-audience fit. The conversion funnel demonstrates "
                   f"{'minimal' if conv_rate > 5 else 'moderate' if conv_rate > 2 else 'significant'} drop-off, "
                   f"with {'strong potential' if conv_rate < 3 else 'opportunities'} for post-click optimization.\n")
    
    analysis.append(f"Cost Metrics & Efficiency: At ${cpc:.4f} average CPC and ${cpm:.2f} CPM, the campaign's "
                   f"cost structure is {'highly efficient' if cpc < 0.50 else 'competitive' if cpc < 1.00 else 'elevated'}. "
                   f"Total spend of ${total_spent:,.2f} yielded {total_conv:,} conversions, resulting in a "
                   f"cost-per-acquisition of ${total_spent/max(total_conv, 1):.2f}. This CPA is "
                   f"{'excellent' if (total_spent/max(total_conv, 1)) < 10 else 'acceptable' if (total_spent/max(total_conv, 1)) < 25 else 'requiring optimization'} "
                   f"for sustainable profitability.\n")
    
    analysis.append(f"Performance Patterns & Correlations: Analysis reveals {'strong positive correlation' if ctr > 3 else 'moderate correlation'} "
                   f"between impression quality and click performance. Outlier analysis identifies "
                   f"{len(df[df['CTR'] > df['CTR'].quantile(0.75)])} high-performing records (top quartile) and "
                   f"{len(df[df['CTR'] < df['CTR'].quantile(0.25)])} underperforming records (bottom quartile), "
                   f"representing a performance spread of {(df['CTR'].quantile(0.75) - df['CTR'].quantile(0.25)):.2f} percentage points. "
                   f"This variance indicates {'significant untapped potential' if (df['CTR'].quantile(0.75) - df['CTR'].quantile(0.25)) > 2 else 'optimization opportunities'} "
                   f"through targeted refinement.\n")
    
    # 3. DEMOGRAPHIC INSIGHTS
    analysis.append("\n" + "="*70)
    analysis.append("3. DEMOGRAPHIC INSIGHTS")
    analysis.append("="*70)
    
    if 'gender' in df.columns:
        gender_perf = df.groupby('gender').agg({'CTR': 'mean', 'clicks': 'sum', 'conversion': 'sum'})
        top_gender = gender_perf['CTR'].idxmax()
        gender_gap = ((gender_perf['CTR'].max() / gender_perf['CTR'].min() - 1) * 100)
        
        analysis.append(f"\nGender Performance Segmentation: {top_gender} audiences demonstrate superior engagement "
                       f"with {gender_perf.loc[top_gender, 'CTR']:.2f}% CTR, representing a {gender_gap:.1f}% "
                       f"performance advantage over other segments. This gender achieved {gender_perf.loc[top_gender, 'clicks']:.0f} clicks "
                       f"and {gender_perf.loc[top_gender, 'conversion']:.0f} conversions, indicating both engagement strength "
                       f"and conversion quality. Cost efficiency analysis reveals "
                       f"{'significant opportunity' if gender_gap > 20 else 'moderate potential'} for budget reallocation "
                       f"toward this high-performing demographic.\n")
    
    if 'age' in df.columns:
        age_perf = df.groupby('age').agg({'CTR': 'mean', 'clicks': 'sum', 'engagement_score': 'mean'})
        top_age = age_perf['CTR'].idxmax()
        low_age = age_perf['CTR'].idxmin()
        
        analysis.append(f"Age Group Performance Analysis: The {top_age} demographic emerges as the highest-performing "
                       f"segment at {age_perf.loc[top_age, 'CTR']:.2f}% CTR with "
                       f"{age_perf.loc[top_age, 'clicks']:.0f} total clicks. Conversely, the {low_age} segment "
                       f"shows {age_perf.loc[low_age, 'CTR']:.2f}% CTR, indicating either creative misalignment, "
                       f"incorrect targeting assumptions, or product-market fit challenges. Strategic implications "
                       f"suggest {'aggressive expansion' if age_perf.loc[top_age, 'CTR'] > 5 else 'cautious scaling'} "
                       f"within the {top_age} group and creative re-testing for {low_age} audiences.\n")
    
    if 'location' in df.columns:
        location_perf = df.groupby('location').agg({'CTR': 'mean', 'clicks': 'sum'}).nlargest(3, 'CTR')
        analysis.append(f"Geographic Performance: Top-performing locations include "
                       f"{', '.join([f'{loc} ({perf:.2f}% CTR)' for loc, perf in location_perf['CTR'].items()])}. "
                       f"Geographic concentration analysis reveals {'strong regional affinity' if location_perf['CTR'].std() < 1 else 'diverse regional performance'}, "
                       f"suggesting {'focused regional strategies' if location_perf['CTR'].std() < 1 else 'location-specific creative adaptation'} "
                       f"for maximum efficiency.\n")
    
    # 4. PLATFORM & CHANNEL ANALYSIS
    analysis.append("\n" + "="*70)
    analysis.append("4. PLATFORM & CHANNEL ANALYSIS")
    analysis.append("="*70)
    
    if 'ad_platform' in df.columns:
        platform_perf = df.groupby('ad_platform').agg({
            'CTR': 'mean', 'clicks': 'sum', 'impressions': 'sum', 'conversion': 'sum'
        })
        top_platform = platform_perf['CTR'].idxmax()
        platform_clicks_share = (platform_perf.loc[top_platform, 'clicks'] / platform_perf['clicks'].sum() * 100)
        
        analysis.append(f"\nPlatform Performance Comparison: {top_platform} leads all platforms with {platform_perf.loc[top_platform, 'CTR']:.2f}% CTR, "
                       f"capturing {platform_clicks_share:.1f}% of total clicks from {platform_perf.loc[top_platform, 'impressions']:.0f} impressions. "
                       f"This platform's superior performance stems from {'audience-platform alignment' if platform_perf.loc[top_platform, 'CTR'] > 5 else 'competitive positioning'}, "
                       f"{'advanced targeting capabilities' if platform_perf.loc[top_platform, 'CTR'] > 4 else 'standard delivery mechanisms'}, "
                       f"and {'exceptional creative-format fit' if platform_perf.loc[top_platform, 'CTR'] > 6 else 'adequate creative execution'}. "
                       f"Conversion analysis shows {platform_perf.loc[top_platform, 'conversion']:.0f} conversions from this platform, "
                       f"demonstrating {'strong end-to-end funnel performance' if platform_perf.loc[top_platform, 'conversion'] > 100 else 'baseline conversion efficiency'}.\n")
    
    if 'device_type' in df.columns:
        device_perf = df.groupby('device_type').agg({'CTR': 'mean', 'clicks': 'sum', 'engagement_score': 'mean'})
        top_device = device_perf['CTR'].idxmax()
        
        analysis.append(f"Device Type Analysis: {top_device} users exhibit highest engagement at {device_perf.loc[top_device, 'CTR']:.2f}% CTR "
                       f"with engagement scores averaging {device_perf.loc[top_device, 'engagement_score']:.2f}. "
                       f"This device-specific performance indicates {'critical importance of mobile optimization' if 'Mobile' in top_device else 'desktop-first strategy validation' if 'Desktop' in top_device else 'device-agnostic creative effectiveness'}. "
                       f"Cross-device analysis reveals {'significant performance variance' if device_perf['CTR'].std() > 1 else 'consistent cross-device experience'}, "
                       f"necessitating {'device-specific creative' if device_perf['CTR'].std() > 1 else 'unified creative strategies'}.\n")
    
    if 'ad_category' in df.columns:
        category_perf = df.groupby('ad_category').agg({'CTR': 'mean', 'clicks': 'sum'}).nlargest(3, 'CTR')
        analysis.append(f"Category Performance: Leading ad categories include "
                       f"{', '.join([f'{cat} ({perf:.2f}% CTR, {clicks:.0f} clicks)' for cat, (perf, clicks) in category_perf.iterrows()])}. "
                       f"Category-level performance spread demonstrates {'strong creative-category alignment' if category_perf['CTR'].std() < 1 else 'varying message-market fit'}, "
                       f"with top performers warranting {'aggressive scaling' if category_perf['CTR'].max() > 5 else 'measured expansion'}.\n")
    
    # 5. TEMPORAL PATTERNS
    analysis.append("\n" + "="*70)
    analysis.append("5. TEMPORAL PATTERNS")
    analysis.append("="*70)
    
    if 'day_of_week' in df.columns:
        day_perf = df.groupby('day_of_week').agg({'CTR': 'mean', 'clicks': 'sum', 'impressions': 'sum'})
        top_day = day_perf['CTR'].idxmax()
        low_day = day_perf['CTR'].idxmin()
        day_variance = ((day_perf['CTR'].max() / day_perf['CTR'].min() - 1) * 100)
        
        analysis.append(f"\nDay-of-Week Performance: {top_day} emerges as the peak performance day with {day_perf.loc[top_day, 'CTR']:.2f}% CTR "
                       f"and {day_perf.loc[top_day, 'clicks']:.0f} clicks, while {low_day} shows lowest engagement at {day_perf.loc[low_day, 'CTR']:.2f}% CTR. "
                       f"The {day_variance:.1f}% performance variance between peak and low days indicates {'strong weekly cyclicality' if day_variance > 30 else 'moderate temporal patterns'}, "
                       f"suggesting {'aggressive dayparting strategies' if day_variance > 30 else 'refined scheduling optimization'} "
                       f"can improve overall efficiency by an estimated {min(day_variance * 0.3, 25):.1f}%.\n")
        
        weekend_days = ['Saturday', 'Sunday']
        weekend_ctr = day_perf.loc[day_perf.index.isin(weekend_days), 'CTR'].mean() if any(d in day_perf.index for d in weekend_days) else 0
        weekday_ctr = day_perf.loc[~day_perf.index.isin(weekend_days), 'CTR'].mean()
        
        analysis.append(f"Weekday vs Weekend Analysis: {'Weekend' if weekend_ctr > weekday_ctr else 'Weekday'} performance "
                       f"leads with {max(weekend_ctr, weekday_ctr):.2f}% average CTR versus {min(weekend_ctr, weekday_ctr):.2f}%, "
                       f"revealing {'B2C consumer behavior patterns' if weekend_ctr > weekday_ctr else 'B2B or weekday-oriented engagement'}. "
                       f"This insight informs {'increased weekend bidding and budgets' if weekend_ctr > weekday_ctr else 'business-hours optimization strategies'} "
                       f"for maximum ROI capture. Peak engagement periods should receive {'30-50% budget weighting' if abs(weekend_ctr - weekday_ctr) > 1 else '15-25% budget adjustment'} "
                       f"for optimal performance.\n")
    
    # 6. TOP PERFORMERS
    analysis.append("\n" + "="*70)
    analysis.append("6. TOP PERFORMERS")
    analysis.append("="*70)
    
    if 'ad_id' in df.columns and 'CTR' in df.columns:
        top_ads = df.nlargest(5, 'CTR')[['ad_id', 'impressions', 'clicks', 'CTR', 'engagement_score']]
        top_ad_id = top_ads.iloc[0]['ad_id']
        top_ad_ctr = top_ads.iloc[0]['CTR']
        top_ad_clicks = top_ads.iloc[0]['clicks']
        
        analysis.append(f"\nTop-Performing Creative Units: Ad {top_ad_id} leads all creative with {top_ad_ctr:.2f}% CTR, "
                       f"generating {top_ad_clicks:.0f} clicks and demonstrating {top_ads.iloc[0].get('engagement_score', 'N/A')} engagement score. "
                       f"Success factors include {'superior creative quality' if top_ad_ctr > 10 else 'strong message-market fit'}, "
                       f"{'precise audience targeting' if top_ad_ctr > 8 else 'effective positioning'}, and "
                       f"{'exceptional timing alignment' if top_ad_ctr > 12 else 'competitive offer presentation'}. "
                       f"The top 5 ads collectively represent {top_ads['clicks'].sum():.0f} clicks at an average {top_ads['CTR'].mean():.2f}% CTR, "
                       f"significantly outperforming the campaign average by {((top_ads['CTR'].mean() / max(ctr, 0.01) - 1) * 100):.1f}%.\n")
    
    if 'ad_category' in df.columns:
        category_leaders = df.groupby('ad_category').agg({'CTR': 'mean', 'clicks': 'sum', 'conversion': 'sum'}).nlargest(3, 'CTR')
        analysis.append(f"Category Leaders: {category_leaders.index[0]} category demonstrates exceptional performance "
                       f"with {category_leaders.iloc[0]['CTR']:.2f}% CTR and {category_leaders.iloc[0]['clicks']:.0f} clicks, "
                       f"yielding {category_leaders.iloc[0]['conversion']:.0f} conversions. Success characteristics include "
                       f"{'strong product-market fit' if category_leaders.iloc[0]['CTR'] > 5 else 'competitive positioning'}, "
                       f"{'resonant messaging' if category_leaders.iloc[0]['conversion'] > 50 else 'adequate value proposition'}, and "
                       f"{'optimal audience targeting' if category_leaders.iloc[0]['CTR'] > 4 else 'baseline reach strategies'}. "
                       f"These top performers warrant {'immediate scaling' if category_leaders.iloc[0]['CTR'] > 6 else 'measured expansion'} and "
                       f"creative replication across similar categories.\n")
    
    # 7. AREAS OF CONCERN
    analysis.append("\n" + "="*70)
    analysis.append("7. AREAS OF CONCERN")
    analysis.append("="*70)
    
    low_performers = df[df['CTR'] < df['CTR'].quantile(0.25)]
    analysis.append(f"\nUnderperforming Segments: {len(low_performers)} records ({len(low_performers)/len(df)*100:.1f}% of total) "
                   f"fall into the bottom performance quartile with CTR below {df['CTR'].quantile(0.25):.2f}%. "
                   f"These underperformers consumed {low_performers['impressions'].sum():.0f} impressions "
                   f"({low_performers['impressions'].sum()/total_imp*100:.1f}% of budget) while generating only "
                   f"{low_performers['clicks'].sum():.0f} clicks ({low_performers['clicks'].sum()/total_clicks*100:.1f}% of total). "
                   f"This inefficiency represents approximately ${low_performers['impressions'].sum() * cpm / 1000:.2f} in "
                   f"suboptimal spend, presenting immediate optimization opportunities.\n")
    
    if 'ad_platform' in df.columns:
        platform_perf = df.groupby('ad_platform')['CTR'].mean()
        low_platform = platform_perf.idxmin()
        analysis.append(f"Platform Concerns: {low_platform} shows weakest performance at {platform_perf.min():.2f}% CTR, "
                       f"indicating {'fundamental platform-audience misalignment' if platform_perf.min() < 1 else 'creative-format incompatibility' if platform_perf.min() < 2 else 'optimization needs'}. "
                       f"Root causes likely include {'incorrect audience targeting parameters' if platform_perf.min() < 1.5 else 'creative format mismatches'}, "
                       f"{'bidding inefficiencies' if platform_perf.min() < 2 else 'message positioning errors'}, or "
                       f"{'platform-specific technical issues' if platform_perf.min() < 1 else 'competitive saturation'}. "
                       f"Business risk: Continued investment in this platform without corrective action risks "
                       f"${(df[df['ad_platform'] == low_platform]['impressions'].sum() * cpm / 1000):.2f} in wasted spend.\n")
    
    high_cpc_segments = df[df['CPC'] > df['CPC'].quantile(0.75)] if 'CPC' in df.columns else pd.DataFrame()
    if not high_cpc_segments.empty:
        analysis.append(f"Cost Efficiency Red Flags: {len(high_cpc_segments)} records exhibit elevated CPC above "
                       f"${df['CPC'].quantile(0.75):.4f} (75th percentile), with peak CPC reaching ${df['CPC'].max():.4f}. "
                       f"These high-cost segments demonstrate {'poor quality scores' if df['CPC'].max() > 2 else 'competitive pressure'}, "
                       f"{'targeting over-specificity' if df['CPC'].max() > 1.5 else 'bidding mismanagement'}, or "
                       f"{'low-quality creative performance' if df['CPC'].max() > 1 else 'market saturation'}. "
                       f"Immediate risk mitigation required to prevent budget depletion and maintain sustainable acquisition costs.\n")
    
    # 8. STRATEGIC RECOMMENDATIONS
    analysis.append("\n" + "="*70)
    analysis.append("8. STRATEGIC RECOMMENDATIONS")
    analysis.append("="*70)
    
    recommendations = []
    
    # Recommendation 1: Budget Reallocation
    if 'gender' in df.columns:
        gender_perf = df.groupby('gender')['CTR'].mean()
        top_gender = gender_perf.idxmax()
        
        if ctr > 0:
            improvement_pct = ((gender_perf.max()/ctr - 1)*100)
            additional_clicks = int((gender_perf.max()/max(ctr, 0.01) - 1)*total_clicks*0.25) if total_clicks > 0 else 0
        else:
            improvement_pct = 0
            additional_clicks = 0
        
        recommendations.append(
            f"• BUDGET REALLOCATION TO HIGH-PERFORMING DEMOGRAPHICS\n"
            f"  WHAT: Shift 25-35% of budget from bottom-quartile segments to {top_gender} demographic\n"
            f"  WHY: {top_gender} shows {gender_perf.max():.2f}% CTR, {improvement_pct:.1f}% above campaign average\n"
            f"  IMPACT: Projected {improvement_pct*0.25:.1f}% increase in overall click volume, "
            f"estimated {additional_clicks:,} additional clicks at current spend"
        )    # Recommendation 2: Platform Optimization
    if 'ad_platform' in df.columns:
        platform_perf = df.groupby('ad_platform')['CTR'].mean()
        top_platform = platform_perf.idxmax()
        low_platform = platform_perf.idxmin()
        recommendations.append(
            f"• PLATFORM PORTFOLIO OPTIMIZATION\n"
            f"  WHAT: Increase {top_platform} budget by 40%, reduce {low_platform} by 50% or pause entirely\n"
            f"  WHY: {top_platform} delivers {platform_perf.max():.2f}% CTR vs {low_platform}'s {platform_perf.min():.2f}%, "
            f"representing {((platform_perf.max()/platform_perf.min() - 1)*100):.0f}% performance gap\n"
            f"  IMPACT: Estimated ${(df[df['ad_platform']==low_platform]['impressions'].sum()*cpm/1000*0.5):.2f} cost savings, "
            f"reinvested for {int((platform_perf.max()/platform_perf.min())*df[df['ad_platform']==low_platform]['clicks'].sum()*0.5):,} additional high-quality clicks"
        )
    
    # Recommendation 3: Temporal Optimization
    if 'day_of_week' in df.columns:
        day_perf = df.groupby('day_of_week')['CTR'].mean()
        top_day = day_perf.idxmax()
        
        if ctr > 0:
            ctr_improvement = ((day_perf.max()/ctr - 1)*35)
            incremental_clicks = int((day_perf.max()/max(ctr, 0.01) - 1)*total_clicks*0.35) if total_clicks > 0 else 0
        else:
            ctr_improvement = 0
            incremental_clicks = 0
        
        recommendations.append(
            f"• DAYPARTING & SCHEDULE OPTIMIZATION\n"
            f"  WHAT: Implement aggressive dayparting with 45% budget allocation to {top_day} and similar peak days\n"
            f"  WHY: {top_day} shows {day_perf.max():.2f}% CTR vs {day_perf.min():.2f}% on low days, "
            f"{((day_perf.max()/day_perf.min() - 1)*100):.0f}% efficiency gap\n"
            f"  IMPACT: Improved overall CTR by estimated {ctr_improvement:.1f}%, "
            f"potential {incremental_clicks:,} incremental clicks at current budget"
        )
    
    # Recommendation 4: Creative Optimization
    if 'ad_id' in df.columns:
        top_ad_ctr = df.nlargest(1, 'CTR')['CTR'].values[0]
        ctr_diff = ((top_ad_ctr/max(ctr, 0.01) - 1)*100) if ctr > 0 else 0
        
        recommendations.append(
            f"• CREATIVE REPLICATION & A/B TESTING PROGRAM\n"
            f"  WHAT: Replicate top-performing ad elements (creative #{df.nlargest(1, 'CTR')['ad_id'].values[0]}) across 60% of active campaigns\n"
            f"  WHY: Top performer achieves {top_ad_ctr:.2f}% CTR, {ctr_diff:.0f}% above average, "
            f"proven success formula identified\n"
            f"  IMPACT: Conservative 15-25% CTR improvement campaign-wide, translating to "
            f"{int(total_clicks * 0.20):,} to {int(total_clicks * 0.35):,} additional clicks within existing budget envelope"
        )
    
    # Recommendation 5: Cost Control
    recommendations.append(
        f"• AUTOMATED PERFORMANCE-BASED BUDGET CONTROLS\n"
        f"  WHAT: Implement auto-pause rules for ads with CTR <{ctr*0.5:.2f}% after 1,000 impressions, "
        f"max CPC caps at ${cpc*1.5:.4f}\n"
        f"  WHY: Bottom-quartile performers consume {(len(low_performers)/len(df)*100):.1f}% of impressions "
        f"while delivering only {(low_performers['clicks'].sum()/total_clicks*100):.1f}% of clicks\n"
        f"  IMPACT: Prevent ${(low_performers['impressions'].sum()*cpm/1000):.2f} wasteful spend monthly, "
        f"improve portfolio-wide efficiency by {min((1 - low_performers['clicks'].sum()/total_clicks)*100, 35):.0f}%, "
        f"ensure sustainable CPA below ${(total_spent/max(total_conv,1))*1.5:.2f}"
    )
    
    # Recommendation 6: Conversion Funnel
    if conv_rate < 3:
        recommendations.append(
            f"• POST-CLICK LANDING PAGE OPTIMIZATION\n"
            f"  WHAT: A/B test landing page variants focusing on load speed, mobile UX, and value proposition clarity\n"
            f"  WHY: Current {conv_rate:.2f}% conversion rate leaves significant post-click value on table, "
            f"industry leaders achieve 4-7% in similar campaigns\n"
            f"  IMPACT: Increasing conversion rate from {conv_rate:.2f}% to conservative 3.5% would yield "
            f"{int((0.035/max(conv_rate/100, 0.001) - 1)*total_conv):,} additional conversions from existing traffic, "
            f"reducing CPA by {((1 - conv_rate/100/0.035)*100):.0f}%"
        )
    
    analysis.append("\n" + "\n\n".join(recommendations) + "\n")
    
    # 9. FUTURE OPPORTUNITIES
    analysis.append("\n" + "="*70)
    analysis.append("9. FUTURE OPTIMIZATION OPPORTUNITIES")
    analysis.append("="*70)
    
    opportunities = []
    
    opportunities.append(
        f"• PREDICTIVE ANALYTICS & MACHINE LEARNING IMPLEMENTATION\n"
        f"  Deploy ML models to predict campaign performance, optimal bid prices, and audience propensity scores. "
        f"Current data volume ({len(df):,} records) provides sufficient training data for statistically significant models. "
        f"Expected outcome: 20-30% improvement in targeting precision, 15-20% reduction in wasted spend, "
        f"automated real-time optimization replacing manual intervention."
    )
    
    ctr_threshold = ((df['CTR'].quantile(0.90)/max(ctr, 0.01) - 1)*75 + ctr) if ctr > 0 else df['CTR'].quantile(0.90)
    
    opportunities.append(
        f"• LOOKALIKE AUDIENCE EXPANSION\n"
        f"  Create precision lookalike audiences based on top 10% performing segments (CTR >{df['CTR'].quantile(0.90):.2f}%). "
        f"Leverage {top_gender if 'gender' in df.columns else 'high-performing'} demographic patterns and "
        f"{top_platform if 'ad_platform' in df.columns else 'leading platform'} behavioral data. "
        f"Projected reach expansion: 3-5x current audience size while maintaining {ctr_threshold:.1f}% CTR quality threshold."
    )
    
    opportunities.append(
        f"• CROSS-PLATFORM SEQUENTIAL MESSAGING STRATEGY\n"
        f"  Implement multi-touch attribution and sequential creative delivery across {df['ad_platform'].nunique() if 'ad_platform' in df.columns else '3+'} platforms. "
        f"Develop awareness → consideration → conversion funnel with platform-specific creative. "
        f"Expected impact: 40-60% improvement in assisted conversions, 25-35% increase in overall conversion rate, "
        f"better brand recall and engagement depth."
    )
    
    opportunities.append(
        f"• DYNAMIC CREATIVE OPTIMIZATION (DCO) DEPLOYMENT\n"
        f"  Implement automated creative assembly testing 50+ headline/image/CTA combinations in real-time. "
        f"Current top-performing creative elements provide strong baseline for automated variation. "
        f"Anticipated results: 30-50% faster optimization cycles, 15-25% CTR improvement through personalization, "
        f"reduced creative production costs by 40% through modular asset libraries."
    )
    
    opportunities.append(
        f"• ADVANCED RETARGETING & AUDIENCE SEGMENTATION\n"
        f"  Deploy granular retargeting for {total_clicks:,} engaged users who didn't convert, segment by engagement depth. "
        f"Create tiered messaging: high-engagement gets premium offers, medium-engagement receives education content, "
        f"low-engagement gets brand awareness refreshers. Expected conversion lift: 200-300% on retargeted traffic, "
        f"incremental {int(total_clicks * 0.7 * 0.05):,} to {int(total_clicks * 0.7 * 0.10):,} conversions from existing traffic."
    )
    
    analysis.append("\n" + "\n\n".join(opportunities) + "\n")
    
    # 10. RISK ASSESSMENT
    analysis.append("\n" + "="*70)
    analysis.append("10. RISK ASSESSMENT & MITIGATION STRATEGIES")
    analysis.append("="*70)
    
    # Check if CPC column exists
    cpc_analysis = ""
    if 'CPC' in df.columns:
        cpc_analysis = (f"Cost volatility analysis reveals CPC ranging from ${df['CPC'].min():.4f} to ${df['CPC'].max():.4f}, "
                       f"a {((df['CPC'].max()/max(df['CPC'].min(), 0.01) - 1)*100):.0f}% variance indicating "
                       f"{'severe bid management issues' if (df['CPC'].max()/max(df['CPC'].min(), 0.01)) > 3 else 'moderate cost instability'}. ")
    
    analysis.append(f"\nOperational & Financial Risks: Current campaign structure exhibits several risk factors requiring immediate attention. "
                   f"Budget allocation shows {(len(low_performers)/len(df)*100):.1f}% of activity in underperforming segments (CTR <{df['CTR'].quantile(0.25):.2f}%), "
                   f"representing ${(low_performers['impressions'].sum()*cpm/1000):.2f} monthly at-risk spend. "
                   f"{cpc_analysis}"
                   f"Without intervention, projected monthly waste: ${(low_performers['impressions'].sum()*cpm/1000*3):.2f} quarterly, "
                   f"${(low_performers['impressions'].sum()*cpm/1000*12):.2f} annually.\n")
    
    platform_concentration_risk = "N/A"
    if 'ad_platform' in df.columns:
        platform_perf = df.groupby('ad_platform')['impressions'].sum()
        top_platform_share = (platform_perf.max() / platform_perf.sum() * 100)
        platform_concentration_risk = f"{top_platform_share:.1f}%"
        
        analysis.append(f"Platform Dependency Risk: {platform_perf.idxmax()} accounts for {top_platform_share:.1f}% of impression volume, "
                       f"creating {'critical platform dependency vulnerability' if top_platform_share > 60 else 'moderate concentration risk' if top_platform_share > 40 else 'acceptable platform diversification'}. "
                       f"Risks include algorithm changes, policy updates, competitive saturation, and CPM inflation. "
                       f"A 20% performance drop on {platform_perf.idxmax()} would reduce overall clicks by {(top_platform_share/100 * 0.20 * 100):.0f}%, "
                       f"equating to {int(total_clicks * top_platform_share/100 * 0.20):,} lost clicks monthly. "
                       f"Mitigation strategy: Gradually diversify to maintain no single platform above 45% impression share, "
                       f"establish backup platforms with proven 3%+ CTR, allocate 15% of budget to platform testing and expansion.\n")
    
    demographic_risk = "N/A"
    if 'gender' in df.columns and 'age' in df.columns:
        gender_concentration = (df.groupby('gender').size().max() / len(df) * 100)
        demographic_risk = f"{gender_concentration:.1f}%"
        
        analysis.append(f"Demographic Imbalance & Market Risk: Campaign shows {demographic_risk} concentration in single demographic segment, "
                       f"limiting market penetration and creating audience fatigue risk. "
                       f"Narrow targeting increases vulnerability to: seasonal demand shifts, competitive targeting of same audiences, "
                       f"creative burnout (frequency saturation), and limited scale potential. "
                       f"Current approach caps maximum addressable audience at {int(len(df) / (gender_concentration/100)):.0f}x current size. "
                       f"Mitigation: Implement controlled audience expansion testing 10-15% budget monthly, "
                       f"develop segment-specific creative for 3-5 new demographic clusters, "
                       f"establish performance thresholds (minimum {ctr*0.75:.2f}% CTR) for new segment validation, "
                       f"create diversified portfolio targeting no segment >35% of total budget to ensure resilience and sustainable growth trajectory.\n")
    
    analysis.append("="*70)
    analysis.append(f"REPORT GENERATED: {len(df):,} records analyzed | Performance Grade: {strength_level}")
    analysis.append("="*70)
    
    return "\n".join(analysis)


def generate_ai_insights(df, metrics):
    """Generate quick AI insights summary."""
    model = initialize_gemini()
    
    if model:
        try:
            prompt = f"""Marketing campaign quick analysis:

Metrics: {metrics.get('total_impressions', 0):,} impressions, {metrics.get('total_clicks', 0):,} clicks, 
{metrics.get('avg_ctr', 0):.2f}% CTR, {metrics.get('total_conversions', 0):,} conversions

Top Categories: {df.groupby('ad_category')['CTR'].mean().nlargest(3).to_dict() if 'ad_category' in df.columns else 'N/A'}

Provide 3-5 key insights and 3 recommendations in concise bullets."""
            
            response = model.generate_content(prompt)
            return response.text
        except:
            return generate_quick_rule_insights(df, metrics)
    else:
        return generate_quick_rule_insights(df, metrics)


def generate_quick_rule_insights(df, metrics):
    """Quick rule-based insights."""
    insights = []
    
    ctr = metrics.get('avg_ctr', 0)
    insights.append(f"• CTR at {ctr:.2f}% {'exceeds' if ctr > 3 else 'meets' if ctr > 2 else 'below'} benchmarks")
    insights.append(f"• {metrics.get('total_conversions', 0):,} conversions at ${metrics.get('avg_cpc', 0):.4f} CPC")
    
    if 'ad_category' in df.columns:
        top_cat = df.groupby('ad_category')['CTR'].mean().idxmax()
        insights.append(f"• {top_cat} category leads performance")
    
    insights.append("\nRecommendations:")
    insights.append("• Optimize targeting for underperforming segments")
    insights.append("• Test new creative variations")
    insights.append("• Reallocate budget to top performers")
    
    return "\n".join(insights)
