"""
Configuration Module
====================
Centralized configuration for the P2P Car Rental System.

Supports multiple environments (dev, test, prod) via the
APP_ENV environment variable. Defaults to 'dev' if not set.

Usage:
    # On Linux/macOS:
    export APP_ENV=test
    python main.py

    # On Windows (CMD):
    set APP_ENV=test
    python main.py

    # Or just run with default (dev):
    python main.py

Why this matters:
    - Tests should use a SEPARATE database, not pollute the dev one
    - Production might need higher fees, different paths, etc.
    - All constants live in ONE place — easy to change later
"""

import os
from pathlib import Path


# ── Determine which environment we're running in ─────────────────────────────
# Pulls from OS environment variable APP_ENV; defaults to 'dev'
APP_ENV = os.environ.get('APP_ENV', 'dev').lower()


# ── Base paths (computed once at import time) ────────────────────────────────
# Path(__file__) is THIS file; .parent.parent goes up to project root
BASE_DIR = Path(__file__).parent.resolve()
DATABASE_DIR = BASE_DIR / 'database'


# ── Environment-specific configuration ───────────────────────────────────────
# Each environment is a dictionary so we can pick the right one at runtime
_ENVIRONMENTS = {
    'dev': {
        # Development DB — persists between runs for manual testing
        'DB_FILE': str(DATABASE_DIR / 'car_rental.db'),
        'DEBUG': True,
        'PLATFORM_FEE_PERCENT': 0.15,    # 15% platform commission
        'DEFAULT_ADMIN_EMAIL': 'admin@p2p.com',
        'DEFAULT_ADMIN_PASSWORD': 'admin123',
    },
    'test': {
        # Test DB — in-memory SQLite, wiped on every run (safe for unit tests)
        'DB_FILE': ':memory:',
        'DEBUG': True,
        'PLATFORM_FEE_PERCENT': 0.15,
        'DEFAULT_ADMIN_EMAIL': 'test_admin@p2p.com',
        'DEFAULT_ADMIN_PASSWORD': 'test_admin_pwd',
    },
    'prod': {
        # Production DB — separate file, no debug output
        'DB_FILE': str(DATABASE_DIR / 'car_rental_prod.db'),
        'DEBUG': False,
        'PLATFORM_FEE_PERCENT': 0.18,    # Higher fee in prod
        # In real production, these MUST come from env vars (never hard-coded)
        'DEFAULT_ADMIN_EMAIL': os.environ.get('ADMIN_EMAIL', 'admin@p2p.com'),
        'DEFAULT_ADMIN_PASSWORD': os.environ.get('ADMIN_PASSWORD', 'change_me'),
    },
}


# ── Validate the env name — fail fast if user typed something wrong ──────────
if APP_ENV not in _ENVIRONMENTS:
    valid = ', '.join(_ENVIRONMENTS.keys())
    raise ValueError(
        f"Invalid APP_ENV='{APP_ENV}'. Must be one of: {valid}"
    )


# ── Export the active config as module-level constants ───────────────────────
# Other modules import these directly: `from config import DB_FILE`
_cfg = _ENVIRONMENTS[APP_ENV]

DB_FILE                  = _cfg['DB_FILE']
DEBUG                    = _cfg['DEBUG']
PLATFORM_FEE_PERCENT     = _cfg['PLATFORM_FEE_PERCENT']
DEFAULT_ADMIN_EMAIL      = _cfg['DEFAULT_ADMIN_EMAIL']
DEFAULT_ADMIN_PASSWORD   = _cfg['DEFAULT_ADMIN_PASSWORD']


# ── Universal constants (same across all environments) ───────────────────────
# Business rules that don't change between dev/test/prod live here

# Long-term rental discounts (days → discount fraction)
LONG_TERM_DISCOUNTS = [
    (30, 0.20),    # 30+ days → 20% off
    (7,  0.10),    # 7-29 days → 10% off
]

# Demo discount codes (in a real app, these would be in a DB table)
DISCOUNT_CODES = {
    'SAVE10':    10,
    'WELCOME20': 20,
    'SUMMER15':  15,
}

# Password hashing salt
# WARNING: In production, this MUST come from a secure secret manager,
# never committed to source control.
PASSWORD_SALT = os.environ.get('APP_SALT', 'p2p_car_rental_2025')

# Valid user roles (used for input validation)
VALID_ROLES = ('owner', 'renter', 'admin')


def print_active_config():
    """Print the active config — useful for debugging."""
    print(f"[CONFIG] Active environment: {APP_ENV}")
    print(f"[CONFIG] Database: {DB_FILE}")
    print(f"[CONFIG] Debug mode: {DEBUG}")
    print(f"[CONFIG] Platform fee: {PLATFORM_FEE_PERCENT * 100:.0f}%")
