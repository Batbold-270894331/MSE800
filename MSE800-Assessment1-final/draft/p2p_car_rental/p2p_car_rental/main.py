"""
P2P Car Rental System — Main Entry Point
=========================================
A peer-to-peer car rental platform that connects car owners with renters.

USAGE
-----
    # Default (development environment):
    python main.py

    # Test environment (in-memory DB, wiped on every run):
    APP_ENV=test python main.py          # Linux/macOS
    set APP_ENV=test && python main.py   # Windows

    # Production environment:
    APP_ENV=prod python main.py

ARCHITECTURE
------------
The system has 4 layers:
    1. Presentation (ui/)      — CLI menus
    2. Service     (services/) — Business logic
    3. Model       (models/)   — OOP entities
    4. Data Access (database/) — SQLite via Singleton

DESIGN PATTERNS USED
--------------------
    - Singleton  (DatabaseManager)
    - Factory    (UserFactory)
    - Strategy   (InsuranceStrategy)

Author: MSE800 Assignment 1
"""

import sys

# Import config FIRST so all downstream modules see consistent settings
from config import APP_ENV, DEBUG, print_active_config
from database.db_manager import DatabaseManager
from ui.main_menu import show_main_menu


def main() -> int:
    """
    Application entry point.

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    try:
        # ── Step 1: Show which environment we're running ─────────────────────
        # Helpful when troubleshooting "why is my DB different?" issues
        if DEBUG:
            print_active_config()

        # ── Step 2: Initialize the Singleton database manager ────────────────
        # This call:
        #   1) Opens the SQLite connection
        #   2) Creates all tables (idempotent)
        #   3) Creates indexes
        #   4) Seeds the default admin account if missing
        # All future `DatabaseManager()` calls return this SAME instance.
        DatabaseManager()

        # ── Step 3: Hand off to the CLI menu loop ────────────────────────────
        # show_main_menu() runs until the user picks "Exit"
        show_main_menu()

        return 0   # exited normally

    except KeyboardInterrupt:
        # User hit Ctrl+C — this is normal, not an error
        print("\n\n[INFO] Program interrupted by user. Goodbye!")
        return 0

    except Exception as e:
        # Catch-all — any uncaught exception lands here
        print(f"\n[FATAL ERROR] {e}")
        # Print full traceback in debug mode so devs can find the bug
        if DEBUG:
            import traceback
            traceback.print_exc()
        return 1

    finally:
        # ── Step 4: Always close the DB connection cleanly ───────────────────
        # finally runs even after Ctrl+C or exceptions — guarantees cleanup
        try:
            DatabaseManager().close()
        except Exception:
            # Don't crash on cleanup errors — they're not critical
            pass


# Python convention: this file can be imported OR run directly.
# This `if` block only runs when executed via `python main.py`,
# not when something else does `import main`.
if __name__ == '__main__':
    sys.exit(main())
