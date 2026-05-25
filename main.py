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

def main():
    parser = argparse.ArgumentParser(description="Document Extractor")
    parser.add_argument("--file", required=True, help="Path to the file")
    args = parser.parse_args()

    try:
        file_type = detect_file_ext(args.file)
        print(f"Supported file type detected: {file_type}")
    except ValueError as e:
        print(f"{e}")
    except FileNotFoundError as e:
        print(f"{e}")

if __name__ == "__main__":
    main()