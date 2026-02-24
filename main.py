import os
from data_loader import load_excel
from chart_planner import create_visualization_plan
from analyzer import generate_charts
from ai_insights import generate_chart_insight
from report_builder import build_report


def get_latest_file_from_data(folder="data"):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Data folder '{folder}' does not exist.")

    files = [
        f for f in os.listdir(folder)
        if f.endswith(".xlsx") or f.endswith(".xls")
    ]

    if not files:
        raise FileNotFoundError("No Excel files found in data folder.")

    # Pick most recently modified file
    files.sort(
        key=lambda x: os.path.getmtime(os.path.join(folder, x)),
        reverse=True
    )

    return os.path.join(folder, files[0])


def run():

    print("Searching for dataset in data folder...")
    file_path = get_latest_file_from_data()

    print(f"Loading dataset: {file_path}")
    df = load_excel(file_path)

    print("Creating visualization plan using LLM...")
    plan = create_visualization_plan(df)

    # Convert Pydantic model → dict
    if hasattr(plan, "dict"):
        plan = plan.dict()

    print("Generating charts...")
    charts = generate_charts(df)

    if not charts:
        print("No charts generated. Exiting.")
        return

    insights = {}

    for chart in charts:
        print(f"Generating insight for: {chart['title']}")
        insight = generate_chart_insight(chart, df)
        insights[chart["title"]] = insight

    print("Building final report...")
    report_path = build_report(charts, insights)

    print("Report generated at:", report_path)


if __name__ == "__main__":
    run()
