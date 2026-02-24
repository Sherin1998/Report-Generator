from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from config import OPENAI_API_KEY


class InsightResponse(BaseModel):
    trend_insight: str = Field(
        description="Clear explanation of trends or patterns observed."
    )
    risk_analysis: str = Field(
        description="Potential risks, anomalies, or business concerns."
    )
    business_recommendation: str = Field(
        description="Actionable strategic recommendation."
    )


def generate_chart_insight(chart_info, df=None):
    """
    Generate AI-driven business insights for a given chart.
    """

    parser = JsonOutputParser(pydantic_object=InsightResponse)

    chart_type = chart_info.get("chart_type", "")
    columns = chart_info.get("columns", [])
    title = chart_info.get("title", "")

    # Create readable column description
    if len(columns) == 2:
        columns_desc = f"{columns[0]} vs {columns[1]}"
    elif len(columns) == 1:
        columns_desc = columns[0]
    else:
        columns_desc = "Multiple columns"

    # Add basic statistics (if numeric column exists)
    stats_summary = ""
    if df is not None and len(columns) > 0:
        try:
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            for col in columns:
                if col in numeric_cols:
                    stats_summary += f"""
Basic statistics for {col}:
- Mean: {df[col].mean():.2f}
- Median: {df[col].median():.2f}
- Min: {df[col].min():.2f}
- Max: {df[col].max():.2f}
- Std Dev: {df[col].std():.2f}
"""
        except Exception:
            pass

    prompt = PromptTemplate(
        template="""
You are a senior business intelligence analyst.

A visualization has been generated with the following details:

Title: {title}
Chart Type: {chart_type}
Columns: {columns}

{stats_summary}

Your Tasks:
1. Clearly explain the key trend or insight.
2. Identify any potential risks, anomalies, or business concerns.
3. Provide a strategic and actionable business recommendation.

Guidelines:
- Be analytical and data-driven.
- Avoid generic statements.
- Be concise but insightful.
- Focus on business impact.

{format_instructions}
""",
        input_variables=["title", "chart_type", "columns", "stats_summary"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0.3
    )

    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "title": title,
            "chart_type": chart_type,
            "columns": columns_desc,
            "stats_summary": stats_summary
        })
        return result

    except Exception as e:
        print(f"Insight generation failed for {title}: {e}")

        # Safe fallback response
        return {
            "trend_insight": "Insight generation failed.",
            "risk_analysis": "Risk analysis unavailable due to processing error.",
            "business_recommendation": "Manual review recommended."
        }
