"""Chart planner module - LLM decides which charts to generate."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from config import OPENAI_API_KEY


class VisualizationPlan(BaseModel):
    """Schema for visualization plan."""
    charts: list = Field(description="A list of charts to generate")


def create_visualization_plan(df):
    """Generate visualization plan using LLM."""
    # Extract metadata
    metadata = {
        "row_count": len(df),
        "columns": []
    }

    for col in df.columns:
        metadata["columns"].append({
            "name": col,
            "dtype": str(df[col].dtype),
            "unique_values": int(df[col].nunique())
        })

    # Define structured output schema
    output_parser = JsonOutputParser(pydantic_object=VisualizationPlan)

    prompt = PromptTemplate(
        template="You are a senior data visualization expert. Analyze the dataset metadata below and design the most meaningful visualizations for business intelligence. Guidelines: Use line charts for trends, Use scatter for relationships, Use heatmap for correlations between numeric columns, Avoid redundant charts, Focus on business value. Dataset Metadata: {metadata} {format_instructions}",
        input_variables=["metadata"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        }
    )

    try:
        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o-mini",
            temperature=0.2
        )

        chain = prompt | llm | output_parser
        result = chain.invoke({"metadata": str(metadata)})

        return result.get("charts") if isinstance(result, dict) else result
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        print("Make sure your OPENAI_API_KEY is set correctly in .env")
        print("And check your SSL certificates with: python -m certifi")
        raise
