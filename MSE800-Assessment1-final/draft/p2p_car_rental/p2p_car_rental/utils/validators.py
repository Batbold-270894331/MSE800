"""
Input validators
================
Reusable functions for validating user input.
"""

import re
from datetime import datetime


def is_valid_email(email: str) -> bool:
    """Check if email format is valid."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone: str) -> bool:
    """Check if phone number is valid (digits only, 7-15 chars)."""
    if not phone:
        return False
    return phone.isdigit() and 7 <= len(phone) <= 15


def is_valid_password(password: str) -> tuple:
    """Check password strength. Returns (is_valid, message)."""
    if not password:
        return False, "Password cannot be empty"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "OK"


def is_valid_date(date_str: str) -> bool:
    """Check if date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def is_valid_year(year_str: str) -> bool:
    """Check if year is between 1990 and current year + 1."""
    try:
        year = int(year_str)
        current_year = datetime.now().year
        return 1990 <= year <= current_year + 1
    except (ValueError, TypeError):
        return False


def is_positive_number(value) -> bool:
    """Check if value is a positive number."""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def is_non_empty(value: str) -> bool:
    """Check if string is non-empty after stripping."""
    return value is not None and len(str(value).strip()) > 0
