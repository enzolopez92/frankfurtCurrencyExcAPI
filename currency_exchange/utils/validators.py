import re
from datetime import datetime
from typing import List, Optional

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_currency_code(code: str) -> bool:
    """Validate currency code format."""
    if not re.match(r'^[A-Z]{3}$', code):
        raise ValidationError(f"Invalid currency code: {code}")
    return True

def validate_date(date_str: str) -> bool:
    """Validate date string format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        raise ValidationError(f"Invalid date format: {date_str}")
