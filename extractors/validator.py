import re
from datetime import datetime

VALID_STATUSES = ["active", "churned"]

#mapping status
STATUS_MAPPING = {
    "cancelled": "churned",
    "canceled": "churned",
    "inactive": "churned",
    "terminated": "churned",
    "expired": "churned",
    "paying": "active",
    "subscribed": "active",
    "current": "active",
}

def validate_email(email) -> str | None:
    if not email:
        return None
    email = str(email).strip().lower()

    #anything@anything.anything
    pattern = r'\S+@\S+\.\S+'
    if re.match(pattern, email):
        return email
    return None

def validate_status(status) -> str:
    #default
    if not status:
        return "active"
    status = str(status).strip().lower()
    
    #valid status
    if status in VALID_STATUSES:
        return status
    
    #mapping status
    if status in STATUS_MAPPING:
        return STATUS_MAPPING[status]
    
    #optional, either default as active or None
    return "active"

def validate_date(date_str) -> str | None:
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    #common date formats
    formats = [
        "%Y-%m-%d",    # 2024-01-15
        "%d/%m/%Y",    # 15/01/2024
        "%m/%d/%Y",    # 01/15/2024
        "%B %d %Y",    # January 15 2024
        "%b %d %Y",    # Jan 15 2024
        "%d-%m-%Y",    # 15-01-2024
    ]
    
    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt)
            #return in standard format
            return date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return None

def validate_company_name(name) -> str | None:
    if not name:
        return None
    
    name = str(name).strip()
    
    if len(name) < 2:
        return None
    
    return name

def validate_customer(customer: dict) -> dict | None:

    cleaned = {
        "company_name": validate_company_name(customer.get("company_name")),
        "email":        validate_email(customer.get("email")),
        "country":      str(customer.get("country", "")).strip() or None,
        "industry":     str(customer.get("industry", "")).strip() or None,
        "status":       validate_status(customer.get("status")),
        "joined_at":    validate_date(customer.get("joined_at")),
    }

    #skip record if both company_name and email are missing
    if not cleaned["company_name"] and not cleaned["email"]:
        print(f"Skipping record — no company name or email: {customer}")
        return None

    return cleaned

def validate_customers(customers: list[dict]) -> list[dict]:
    print(f"Validating {len(customers)} customer(s) in process ...")
    valid = []
    skipped = 0
    for customer in customers:
        cleaned = validate_customer(customer)
        if cleaned:
            valid.append(cleaned)
        else:
            skipped += 1
    print(f"Valid: {len(valid)}")
    if skipped:
        print(f"Skipped: {skipped}")
    return valid

