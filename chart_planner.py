"""
Chart planner module - LLM decides which charts to generate.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from config import OPENAI_API_KEY


# -----------------------------
# Strict Chart Schema
# -----------------------------
class ChartDefinition(BaseModel):
    title: str = Field(description="Business-friendly chart title")
    chart_type: str = Field(
        description='Must be one of: "histogram", "bar", "scatter", "box", "heatmap", "line"'
    )
    columns: List[str] = Field(
        description="List of dataset columns used in the chart"
    )


class VisualizationPlan(BaseModel):
    charts: List[ChartDefinition]


# -----------------------------
# Main Planner Function
# -----------------------------
def create_visualization_plan(df):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    metadata = {
        "row_count": len(df),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
    }

    output_parser = JsonOutputParser(pydantic_object=VisualizationPlan)

    prompt = PromptTemplate(
        template="""
You are a senior data visualization architect.

Dataset Information:
- Row count: {row_count}
- Numeric columns: {numeric_columns}
- Categorical columns: {categorical_columns}

Your task:
Create a diverse and business-relevant visualization plan.

STRICT RULES:
1. Only use the provided columns.
2. chart_type MUST be exactly one of:
   ["histogram", "bar", "scatter", "box", "heatmap", "line"]
3. Use lowercase only for chart_type.
4. Avoid duplicate column combinations.
5. Ensure charts are logically valid:
   - histogram → 1 numeric column
   - bar → 1 categorical OR categorical vs numeric
   - scatter → 2 numeric columns
   - box → categorical vs numeric
   - heatmap → numeric correlation
   - line → time-like or ordered numeric trends
6. Titles must be clear and business-friendly.
7. Generate between 8–12 high-value charts (not excessive).

Return JSON strictly in this format:
{format_instructions}
""",
        input_variables=["row_count", "numeric_columns", "categorical_columns"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0.2  # Lower = more structured, less hallucination
    )

    chain = prompt | llm | output_parser

    try:
        result = chain.invoke({
            "row_count": metadata["row_count"],
            "numeric_columns": metadata["numeric_columns"],
            "categorical_columns": metadata["categorical_columns"]
        })

        return result

    except Exception as e:
        print("Visualization planning failed:", e)
        return VisualizationPlan(charts=[])
