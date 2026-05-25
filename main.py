'''
Command: python3 main.py --file <file.ext> --provider <llm>
'''

import argparse
from pathlib import Path

def detect_file_ext(file_path: str) -> str:
    path = Path(file_path)
    suffix = Path(file_path).suffix.lower()
    if not suffix:
        raise ValueError(f"File has no extension. Supported: .csv, .xlsx, .pdf")
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if path.stat().st_size == 0:
        raise ValueError(f"File is empty: {file_path}")
    if suffix == ".csv":
        return "csv"
    elif suffix in [".xlsx", ".xls"]:
        return "excel"
    elif suffix == ".pdf":
        return "pdf"
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: .csv, .xlsx, .pdf")

def extract(file_path: str, provider: str = "groq") -> list[dict]:
    file_type = detect_file_ext(file_path)

    if file_type == "csv":
        from extractors.csv_extractor import extract_from_csv
        print(f"Detected: CSV file")
        return extract_from_csv(file_path)

    elif file_type == "excel":
        from extractors.excel_extractor import extract_from_excel
        print(f"Detected: Excel file")
        return extract_from_excel(file_path)

    elif file_type == "pdf":
        from extractors.pdf_extractor import extract_text_from_pdf
        from extractors.ai_extractor import extract_with_ai
        print(f"Detected: PDF file")
        text = extract_text_from_pdf(file_path)
        return extract_with_ai(text, provider)

def main():
    parser = argparse.ArgumentParser(description="Document Extractor")
    parser.add_argument("--file", required=True, help="Path to the file")
    parser.add_argument("--provider", default="groq", choices=["groq", "openai", "anthropic"], help="LLM provider")
    args = parser.parse_args()

    try:
        customers = extract(args.file, args.provider)
        print(f"\nExtracted {len(customers)} customer(s)")
        import json
        print(json.dumps(customers, indent=2))
    except FileNotFoundError as e:
        print(f"{e}")
    except ValueError as e:
        print(f"{e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()