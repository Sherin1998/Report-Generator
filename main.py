from data_loader import load_excel
from chart_planner import create_visualization_plan
from analyzer import generate_charts
from ai_insights import generate_chart_insight
from report_builder import build_report
import ssl
import os
ssl._create_default_https_context = ssl._create_unverified_context


def run():

    file_path = "data/fragrance_dataset_100.xlsx"

    print("Loading dataset...")
    df = load_excel(file_path)

    print("Creating visualization plan using LLM...")
    plan = create_visualization_plan(df)

    print("Generating charts...")
    charts = generate_charts(df, plan)

    insights = {}

    for chart in charts:
        print(f"Generating insight for: {chart['title']}")
        insight = generate_chart_insight(chart)
        insights[chart["title"]] = insight

    print("Building final report...")
    report_path = build_report(charts, insights)

    print("Report generated at:", report_path)


if __name__ == "__main__":
    run()