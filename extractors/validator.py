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

