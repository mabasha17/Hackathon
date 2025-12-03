"""
PDF Report Generation Module
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from pathlib import Path
from src.config import PDF_DIR, COMPANY_NAME, REPORT_AUTHOR


def create_pdf_report(summary_metrics, insights_text, chart_paths, output_filename=None):
    """
    Generate a comprehensive PDF report.
    
    Args:
        summary_metrics: Dictionary of summary metrics
        insights_text: AI-generated insights text
        chart_paths: List of paths to chart images
        output_filename: Optional custom filename
    
    Returns:
        Path to generated PDF file
    """
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"campaign_report_{timestamp}.pdf"
    
    output_path = PDF_DIR / output_filename
    
    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2ca02c'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title Page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Campaign Performance Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Paragraph(f"Company: {COMPANY_NAME}", styles['Normal']))
    story.append(Paragraph(f"Report By: {REPORT_AUTHOR}", styles['Normal']))
    story.append(PageBreak())
    
    # Executive Summary Section
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Metrics Table
    metrics_data = [['Metric', 'Value']]
    for key, value in summary_metrics.items():
        key_formatted = key.replace('_', ' ').title()
        if isinstance(value, float):
            value_formatted = f"{value:,.2f}"
        else:
            value_formatted = f"{value:,}"
        metrics_data.append([key_formatted, value_formatted])
    
    metrics_table = Table(metrics_data, colWidths=[3.5*inch, 2*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Insights Section
    story.append(PageBreak())
    story.append(Paragraph("AI-Powered Insights & Recommendations", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Split insights into paragraphs
    for line in insights_text.split('\n'):
        if line.strip():
            if line.startswith('='):
                continue  # Skip separator lines
            elif line.isupper() or line.startswith('KEY') or line.startswith('EXECUTIVE'):
                story.append(Paragraph(f"<b>{line}</b>", styles['Heading3']))
            else:
                story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    # Visualizations Section
    if chart_paths:
        story.append(PageBreak())
        story.append(Paragraph("Performance Visualizations", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        for chart_path in chart_paths:
            if Path(chart_path).exists():
                try:
                    # Add chart with caption
                    img = Image(str(chart_path), width=6*inch, height=3.6*inch)
                    story.append(img)
                    
                    caption = Path(chart_path).stem.replace('_', ' ').title()
                    story.append(Paragraph(f"<i>{caption}</i>", styles['Normal']))
                    story.append(Spacer(1, 0.3*inch))
                except Exception as e:
                    print(f"Warning: Could not add chart {chart_path}: {e}")
    
    # Build PDF
    doc.build(story)
    
    print(f"✓ PDF report saved: {output_path}")
    return output_path


if __name__ == "__main__":
    # Test PDF generation
    sample_metrics = {
        'total_campaigns': 5,
        'total_ads': 12,
        'total_spent': 5000.00,
        'total_conversions': 150,
        'avg_CTR': 3.5,
        'avg_CPC': 0.75
    }
    
    sample_insights = """
EXECUTIVE SUMMARY
Campaign performance shows strong engagement with opportunity for optimization.

KEY FINDINGS
- CTR exceeds industry benchmarks
- Conversion rate needs improvement
- Budget allocation could be optimized
"""
    
    pdf_path = create_pdf_report(sample_metrics, sample_insights, [])
    print(f"Test PDF created: {pdf_path}")
