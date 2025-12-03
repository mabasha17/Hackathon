"""
Streamlit UI for Automated Insight Engine
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

# Add D drive Python libraries to path
D_DRIVE_LIBS = r"D:\python_libs"
if D_DRIVE_LIBS not in sys.path:
    sys.path.insert(0, D_DRIVE_LIBS)

# Import project modules
from src.config import INPUT_DIR, OUTPUT_DIR, PLOTS_DIR, PDF_DIR, PPTX_DIR
from src.ingestion import load_data, load_from_directory
from src.preprocessing import clean_data, engineer_features
from src.metrics import calculate_summary_metrics, calculate_segment_performance
from src.visualization import create_dashboard_charts
from src.insight_engine import generate_insights_with_gemini
from src.report_pdf import create_pdf_report
from src.report_pptx import create_pptx_report

# Page configuration
st.set_page_config(
    page_title="Automated Insight Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2ca02c;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Automated Insight Engine</h1>', unsafe_allow_html=True)
st.markdown("### AI-Powered Marketing Analytics & Reporting Platform")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=H-001+Insight+Engine", use_container_width=True)
    st.markdown("## 🎯 Navigation")
    
    page = st.radio(
        "Select Module:",
        ["🏠 Dashboard", "📤 Upload Data", "🔍 Analyze", "📊 Visualizations", "📄 Reports", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    
    # Check for existing data
    csv_files = list(INPUT_DIR.glob("*.csv"))
    if csv_files:
        st.success(f"✅ {len(csv_files)} dataset(s) loaded")
        try:
            df = load_from_directory(INPUT_DIR)
            st.info(f"📊 {len(df):,} total records")
        except:
            pass
    else:
        st.warning("⚠️ No data loaded")
    
    st.markdown("---")
    st.markdown("### 🛠️ Tools")
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Main content based on selected page
if page == "🏠 Dashboard":
    st.header("Dashboard Overview")
    
    csv_files = list(INPUT_DIR.glob("*.csv"))
    
    if not csv_files:
        st.warning("⚠️ No data available. Please upload a dataset first.")
        st.info("👉 Go to **Upload Data** section to get started.")
    else:
        with st.spinner("Loading data..."):
            df = load_from_directory(INPUT_DIR)
            df_clean = clean_data(df)
            df_processed = engineer_features(df_clean)
            metrics = calculate_summary_metrics(df_processed)
        
        # Display metrics
        st.subheader("📊 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Impressions",
                f"{metrics.get('total_impressions', 0):,.0f}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Total Clicks",
                f"{metrics.get('total_clicks', 0):,.0f}",
                delta=None
            )
        
        with col3:
            ctr = metrics.get('avg_CTR', 0)
            st.metric(
                "Average CTR",
                f"{ctr:.2f}%",
                delta="Good" if ctr > 2 else "Low"
            )
        
        with col4:
            conversions = metrics.get('total_conversions', 0)
            st.metric(
                "Conversions",
                f"{conversions:,.0f}",
                delta=None
            )
        
        st.markdown("---")
        
        # Data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df_processed.head(10), use_container_width=True)
        
        # Summary statistics
        with st.expander("📈 Detailed Statistics"):
            st.write(df_processed.describe())

elif page == "📤 Upload Data":
    st.header("Upload Your Data")
    
    tab1, tab2 = st.tabs(["📁 Upload File", "🌐 Kaggle Dataset"])
    
    with tab1:
        st.markdown("### Upload CSV, Excel, or JSON file")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls', 'json'],
            help="Upload your marketing campaign data"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file
                file_path = INPUT_DIR / uploaded_file.name
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"✅ File uploaded successfully: {uploaded_file.name}")
                
                # Preview data
                df = load_data(file_path)
                st.subheader("Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Rows:** {len(df):,}")
                with col2:
                    st.info(f"**Columns:** {len(df.columns)}")
                
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
    
    with tab2:
        st.markdown("### Download from Kaggle")
        
        dataset_name = st.text_input(
            "Enter Kaggle dataset identifier",
            placeholder="e.g., programmer3/social-media-ad-campaign-dataset",
            help="Format: username/dataset-name"
        )
        
        if st.button("🔽 Download Dataset"):
            if dataset_name:
                with st.spinner("Downloading from Kaggle..."):
                    try:
                        from src.kaggle_downloader import download_kaggle_dataset
                        csv_path = download_kaggle_dataset(dataset_name)
                        
                        if csv_path:
                            st.success(f"✅ Dataset downloaded: {csv_path.name}")
                            df = load_data(csv_path)
                            st.dataframe(df.head(), use_container_width=True)
                        else:
                            st.error("❌ Download failed. Please check the dataset name and your Kaggle credentials.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Please enter a dataset identifier")

elif page == "🔍 Analyze":
    st.header("Data Analysis")
    
    csv_files = list(INPUT_DIR.glob("*.csv"))
    
    if not csv_files:
        st.warning("⚠️ No data available. Please upload a dataset first.")
    else:
        with st.spinner("Analyzing data..."):
            df = load_from_directory(INPUT_DIR)
            df_clean = clean_data(df)
            df_processed = engineer_features(df_clean)
            metrics = calculate_summary_metrics(df_processed)
        
        # Generate insights
        st.subheader("🤖 AI-Powered Insights")
        
        if st.button("🚀 Generate Insights", key="generate_insights"):
            with st.spinner("Generating insights..."):
                data_summary = f"Dataset with {len(df_processed)} records"
                insights = generate_insights_with_gemini(metrics, data_summary)
                
                st.markdown("### 📝 Analysis Results")
                st.text_area("Insights", insights, height=400)
        
        st.markdown("---")
        
        # Segment analysis
        st.subheader("🎯 Segment Analysis")
        
        segment_options = [col for col in df_processed.columns if df_processed[col].dtype == 'object' or df_processed[col].nunique() < 20]
        
        if segment_options:
            segment_by = st.selectbox("Segment by:", segment_options)
            
            if segment_by:
                segment_df = calculate_segment_performance(df_processed, segment_by)
                st.dataframe(segment_df, use_container_width=True)
                
                # Visualization
                if not segment_df.empty and 'total_impressions' in segment_df.columns:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    segment_df.head(10).plot(
                        x=segment_by,
                        y='total_impressions',
                        kind='bar',
                        ax=ax,
                        color='#1f77b4'
                    )
                    ax.set_title(f"Impressions by {segment_by}")
                    ax.set_xlabel(segment_by)
                    ax.set_ylabel("Total Impressions")
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

elif page == "📊 Visualizations":
    st.header("Visual Analytics")
    
    csv_files = list(INPUT_DIR.glob("*.csv"))
    
    if not csv_files:
        st.warning("⚠️ No data available. Please upload a dataset first.")
    else:
        with st.spinner("Loading data..."):
            df = load_from_directory(INPUT_DIR)
            df_clean = clean_data(df)
            df_processed = engineer_features(df_clean)
        
        st.subheader("🎨 Generate Visualizations")
        
        if st.button("📈 Create All Charts", key="create_charts"):
            with st.spinner("Generating charts..."):
                chart_paths = create_dashboard_charts(df_processed)
                st.success(f"✅ Generated {len(chart_paths)} charts")
        
        # Display existing charts
        chart_files = list(PLOTS_DIR.glob("*.png"))
        
        if chart_files:
            st.subheader("📊 Generated Charts")
            
            cols = st.columns(2)
            for idx, chart_path in enumerate(chart_files):
                with cols[idx % 2]:
                    st.image(str(chart_path), use_container_width=True, caption=chart_path.stem.replace('_', ' ').title())
        else:
            st.info("No charts generated yet. Click 'Create All Charts' to generate visualizations.")

elif page == "📄 Reports":
    st.header("Report Generation")
    
    csv_files = list(INPUT_DIR.glob("*.csv"))
    
    if not csv_files:
        st.warning("⚠️ No data available. Please upload a dataset first.")
    else:
        st.subheader("📋 Generate Professional Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_format = st.selectbox(
                "Select Report Format:",
                ["PDF Only", "PowerPoint Only", "Both PDF & PowerPoint"]
            )
        
        with col2:
            include_charts = st.checkbox("Include Visualizations", value=True)
        
        if st.button("🎯 Generate Report", key="generate_report"):
            with st.spinner("Generating report..."):
                try:
                    # Load and process data
                    df = load_from_directory(INPUT_DIR)
                    df_clean = clean_data(df)
                    df_processed = engineer_features(df_clean)
                    metrics = calculate_summary_metrics(df_processed)
                    
                    # Generate insights
                    data_summary = f"Dataset with {len(df_processed)} records"
                    insights = generate_insights_with_gemini(metrics, data_summary)
                    
                    # Generate charts if needed
                    chart_paths = []
                    if include_charts:
                        chart_paths = create_dashboard_charts(df_processed)
                    
                    # Generate reports
                    generated_reports = []
                    
                    if report_format in ["PDF Only", "Both PDF & PowerPoint"]:
                        pdf_path = create_pdf_report(metrics, insights, chart_paths)
                        generated_reports.append(pdf_path)
                    
                    if report_format in ["PowerPoint Only", "Both PDF & PowerPoint"]:
                        pptx_path = create_pptx_report(metrics, insights, chart_paths)
                        generated_reports.append(pptx_path)
                    
                    st.success(f"✅ Report(s) generated successfully!")
                    
                    # Download buttons
                    for report_path in generated_reports:
                        with open(report_path, 'rb') as f:
                            st.download_button(
                                label=f"📥 Download {report_path.name}",
                                data=f,
                                file_name=report_path.name,
                                mime='application/octet-stream'
                            )
                
                except Exception as e:
                    st.error(f"❌ Error generating report: {e}")
        
        # Show existing reports
        st.markdown("---")
        st.subheader("📚 Generated Reports")
        
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        pptx_files = list(PPTX_DIR.glob("*.pptx"))
        
        if pdf_files or pptx_files:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**PDF Reports:**")
                for pdf_file in pdf_files:
                    with open(pdf_file, 'rb') as f:
                        st.download_button(
                            label=f"📄 {pdf_file.name}",
                            data=f,
                            file_name=pdf_file.name,
                            mime='application/pdf',
                            key=f"pdf_{pdf_file.name}"
                        )
            
            with col2:
                st.markdown("**PowerPoint Reports:**")
                for pptx_file in pptx_files:
                    with open(pptx_file, 'rb') as f:
                        st.download_button(
                            label=f"📊 {pptx_file.name}",
                            data=f,
                            file_name=pptx_file.name,
                            mime='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                            key=f"pptx_{pptx_file.name}"
                        )
        else:
            st.info("No reports generated yet.")

elif page == "⚙️ Settings":
    st.header("Settings & Configuration")
    
    st.subheader("🔧 System Configuration")
    
    with st.expander("📁 Directory Paths"):
        st.code(f"Input Directory: {INPUT_DIR}")
        st.code(f"Output Directory: {OUTPUT_DIR}")
        st.code(f"Reports Directory: {PLOTS_DIR.parent}")
    
    with st.expander("🔑 API Configuration"):
        st.markdown("**Gemini AI API Key**")
        api_key = st.text_input(
            "Enter your Gemini API key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        
        if st.button("Save API Key"):
            if api_key:
                # Update .env file
                env_path = Path(".env")
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith("GEMINI_API_KEY="):
                        lines[i] = f"GEMINI_API_KEY={api_key}\n"
                        updated = True
                        break
                
                if not updated:
                    lines.append(f"\nGEMINI_API_KEY={api_key}\n")
                
                with open(env_path, 'w') as f:
                    f.writelines(lines)
                
                st.success("✅ API key saved!")
            else:
                st.warning("Please enter an API key")
    
    with st.expander("🗑️ Data Management"):
        st.markdown("**Clear Data**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear Input Data"):
                for file in INPUT_DIR.glob("*"):
                    if file.is_file():
                        file.unlink()
                st.success("Input data cleared!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Reports"):
                for file in PDF_DIR.glob("*"):
                    if file.is_file():
                        file.unlink()
                for file in PPTX_DIR.glob("*"):
                    if file.is_file():
                        file.unlink()
                st.success("Reports cleared!")
                st.rerun()
        
        with col3:
            if st.button("🗑️ Clear Charts"):
                for file in PLOTS_DIR.glob("*"):
                    if file.is_file():
                        file.unlink()
                st.success("Charts cleared!")
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🚀 Automated Insight Engine v1.0 | Built with Streamlit</p>
        <p>© 2025 H-001 Project | Powered by AI</p>
    </div>
    """,
    unsafe_allow_html=True
)
