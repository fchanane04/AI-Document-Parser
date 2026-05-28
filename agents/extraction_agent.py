from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from extractors.llm_provider import get_llm
from extractors.validator import validate_customers
from dotenv import load_dotenv

import json

load_dotenv()

#Tools

@tool
def extract_csv(file_path: str) -> str:
    """Use this tool to extract customer data from CSV files (.csv extension).
    Input should be the full file path."""
    from extractors.csv_extractor import extract_from_csv
    customers = extract_from_csv(file_path)
    validated = validate_customers(customers)
    return json.dumps(validated)

@tool
def extract_excel(file_path: str) -> str:
    """Use this tool to extract customer data from Excel files (.xlsx or .xls extension).
    Input should be the full file path."""
    from extractors.excel_extractor import extract_from_excel
    customers = extract_from_excel(file_path)
    validated = validate_customers(customers)
    return json.dumps(validated)

@tool
def extract_pdf(file_path: str) -> str:
    """Use this tool to extract customer data from PDF files (.pdf extension).
    Input should be the full file path."""
    from extractors.pdf_extractor import extract_text_from_pdf
    from extractors.ai_extractor import extract_with_ai
    text = extract_text_from_pdf(file_path)
    customers = extract_with_ai(text)
    validated = validate_customers(customers)
    return json.dumps(validated)

@tool
def extract_image(file_path: str) -> str:
    """Use this tool to extract customer data from image files (.png, .jpg, .jpeg extension).
    Input should be the full file path."""
    from extractors.image_extractor import extract_text_from_image
    from extractors.ai_extractor import extract_with_ai
    text = extract_text_from_image(file_path)
    customers = extract_with_ai(text)
    validated = validate_customers(customers)
    return json.dumps(validated)

#Create agent

def create_extraction_agent(provider: str = "groq"):
    llm = get_llm(provider)
    tools = [extract_csv, extract_excel, extract_pdf, extract_image]

    agent = create_react_agent(llm, tools)

    return agent

def run_agent(task: str, provider: str = "groq") -> str:
    agent = create_extraction_agent(provider)
    result = agent.invoke({"messages": [HumanMessage(content=task)]})
    return result["messages"][-1].content


