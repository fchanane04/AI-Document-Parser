import pandas as pd
from pathlib import Path

STANDARD_FIELDS = ["company_name", "email", "country", "industry", "status", "joined_at"]

#columns mapping for different column possible names
COLUMN_MAPPING = {
    "company_name": ["company_name", "company", "business", "name", "organization", "client"],
    "email":        ["email", "email_address", "billing_email", "contact_email", "mail"],
    "country":      ["country", "country_code", "location", "region", "nation"],
    "industry":     ["industry", "sector", "business_type", "category", "vertical"],
    "status":       ["status", "account_status", "state", "subscription_status"],
    "joined_at":    ["joined_at", "created_at", "start_date", "signup_date", "date_joined"]
}

def find_column(df_columns: list, possible_names: list) -> str | None:
    """Find matching column name regardless of case"""
    df_columns_lower = [col.lower().strip() for col in df_columns]
    for name in possible_names:
        if name.lower() in df_columns_lower:
            idx = df_columns_lower.index(name.lower())
            return df_columns[idx]
    return None

def extract_from_csv(file_path: str) -> list[dict]:
    """
    Extract customer data from a CSV file.
    Returns a list of customer dictionaries.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path.suffix}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("CSV file is empty")

    print(f"Found {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")

    #map columns to standard fields
    column_map = {}
    for standard_field, possible_names in COLUMN_MAPPING.items():
        found_col = find_column(list(df.columns), possible_names)
        if found_col:
            column_map[standard_field] = found_col
            print(f"Mapped '{found_col}' → '{standard_field}'")
        else:
            print(f"No column found for '{standard_field}' — will use null")

    #build the customers dict
    customers = []
    for _, row in df.iterrows():
        customer = {}
        for standard_field in STANDARD_FIELDS:
            if standard_field in column_map:
                value = row[column_map[standard_field]]
                # Handle NaN values
                customer[standard_field] = None if pd.isna(value) else str(value).strip()
            else:
                customer[standard_field] = None
        customers.append(customer)

    print(f"\nExtracted {len(customers)} customers")
    return customers