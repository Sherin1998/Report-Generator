from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from config import OPENAI_API_KEY


class InsightResponse(BaseModel):
    trend_insight: str = Field(description="Clear explanation of trends or patterns observed.")
    risk_analysis: str = Field(description="Potential risks, anomalies, or business concerns.")
    business_recommendation: str = Field(description="Actionable strategic recommendation.")


def generate_chart_insight(chart_info):

    parser = JsonOutputParser(pydantic_object=InsightResponse)

    prompt = PromptTemplate(
        template="""
        You are a senior business intelligence analyst.

        A data visualization has been generated with the following details:

        Title: {title}
        Columns Used: {columns}

        Your task:
        1. Explain the main trend or insight clearly.
        2. Identify any potential risks or anomalies.
        3. Provide a strategic business recommendation.

        Be concise, analytical, and professional.

        {format_instructions}
        """,
        input_variables=["title", "columns"],
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

    result = chain.invoke({
        "title": chart_info["title"],
        "columns": ", ".join(chart_info["columns"])
    })

    return result
