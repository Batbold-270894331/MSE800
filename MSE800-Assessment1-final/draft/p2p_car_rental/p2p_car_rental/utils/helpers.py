"""
Helper utilities
================
CLI display helpers, formatters, and prompts.
"""

import os
from datetime import datetime


def clear_screen():
    """Clear the terminal screen (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, width: int = 60):
    """Print a formatted header box."""
    print()
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def print_section(title: str, width: int = 60):
    """Print a section divider."""
    print()
    print("-" * width)
    print(f" {title}")
    print("-" * width)


def print_success(msg: str):
    """Print a success message."""
    print(f"\n[OK] {msg}\n")


def print_error(msg: str):
    """Print an error message."""
    print(f"\n[ERROR] {msg}\n")


def print_info(msg: str):
    """Print an info message."""
    print(f"\n[INFO] {msg}\n")


def prompt(message: str, allow_empty: bool = False) -> str:
    """Prompt user for input. Re-asks if empty (unless allowed)."""
    while True:
        value = input(f"{message}: ").strip()
        if value or allow_empty:
            return value
        print("[ERROR] This field cannot be empty.")


def prompt_choice(message: str, valid_choices: list) -> str:
    """Prompt user for input that must match one of valid_choices."""
    while True:
        value = input(f"{message}: ").strip()
        if value in valid_choices:
            return value
        print(f"[ERROR] Invalid choice. Please choose from: {', '.join(valid_choices)}")


def prompt_yes_no(message: str) -> bool:
    """Prompt for yes/no answer. Returns True if yes."""
    while True:
        value = input(f"{message} (y/n): ").strip().lower()
        if value in ('y', 'yes'):
            return True
        if value in ('n', 'no'):
            return False
        print("[ERROR] Please enter 'y' or 'n'.")


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def days_between(start_date: str, end_date: str) -> int:
    """Calculate number of days between two YYYY-MM-DD dates (inclusive)."""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return (end - start).days + 1


def pause():
    """Pause and wait for user to press Enter."""
    input("\nPress Enter to continue...")
