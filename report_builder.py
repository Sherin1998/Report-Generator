"""Report builder module for constructing and formatting reports."""
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def build_report(charts, insights):
    """Build a PDF report from charts and insights."""
    doc = SimpleDocTemplate("output/AI_Analysis_Report.pdf")
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("AI Intelligent Data Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    for chart in charts:
        elements.append(Paragraph(chart["title"], styles["Heading2"]))
        elements.append(Spacer(1, 10))

        elements.append(Image(chart["path"], width=5*inch, height=3*inch))
        elements.append(Spacer(1, 10))

        insight = insights.get(chart["title"], {})

        trend = insight.get("trend_insight", "N/A") if isinstance(insight, dict) else "N/A"
        risk = insight.get("risk_analysis", "N/A") if isinstance(insight, dict) else "N/A"
        recommendation = insight.get("business_recommendation", "N/A") if isinstance(insight, dict) else "N/A"

        elements.append(Paragraph(f"Trend: {trend}", styles["Normal"]))
        elements.append(Spacer(1, 5))

        elements.append(Paragraph(f"Risk: {risk}", styles["Normal"]))
        elements.append(Spacer(1, 5))

        elements.append(Paragraph(f"Recommendation: {recommendation}", styles["Normal"]))
        elements.append(Spacer(1, 20))

    doc.build(elements)

    return "output/AI_Analysis_Report.pdf"