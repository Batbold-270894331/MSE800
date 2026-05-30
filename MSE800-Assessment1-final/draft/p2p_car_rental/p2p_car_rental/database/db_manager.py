"""
Database Manager - Singleton Pattern
=====================================
Ensures only ONE database connection exists throughout the application.

Optimizations applied:
  - Indexes on foreign keys + email (faster lookups)
  - Connection pooling via Singleton (no repeated connect/disconnect)
  - PRAGMA settings tuned for performance
  - Schema migrations centralized (single source of truth)
  - Context manager support (with-statement for clean shutdown)
"""

import sqlite3
import os
from typing import Optional, List
from config import DB_FILE, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD


class DatabaseManager:
    """
    Singleton class for managing SQLite database connection.

    Why Singleton?
        SQLite supports multiple connections, but for a small CLI app
        a single shared connection is faster (no repeated handshake)
        and prevents accidental race conditions.
    """

    # Class-level (not instance-level) variables — shared across all "instances"
    _instance: Optional['DatabaseManager'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        """
        Override __new__ to enforce the Singleton pattern.

        How it works:
            - First call: creates a new instance, stores it on the class.
            - Subsequent calls: returns the already-stored instance.
            - Result: every `DatabaseManager()` call returns the SAME object.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Set up DB connection, schema, indexes, and seed data."""
        # Ensure the database/ directory exists (skip for in-memory DBs)
        if DB_FILE != ':memory:':
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

        # check_same_thread=False — needed because Python's REPL/IDE
        # may call us from different threads. Safe here since we're
        # single-threaded application logic.
        self._connection = sqlite3.connect(DB_FILE, check_same_thread=False)

        # Make rows behave like dicts: row['email'] instead of row[2]
        # — far more readable and refactor-safe than positional indexing.
        self._connection.row_factory = sqlite3.Row

        # ── Performance & integrity PRAGMAs ──────────────────────────────────
        # Enforce foreign keys (OFF by default in SQLite, surprisingly!)
        self._connection.execute("PRAGMA foreign_keys = ON")

        # WAL = Write-Ahead Logging — much faster concurrent reads + safer writes.
        # Doesn't apply to in-memory DBs, so guard with a check.
        if DB_FILE != ':memory:':
            self._connection.execute("PRAGMA journal_mode = WAL")

        # NORMAL gives good speed without sacrificing crash safety
        self._connection.execute("PRAGMA synchronous = NORMAL")

        # Set up tables, indexes, default data
        self._create_tables()
        self._create_indexes()
        self._seed_default_admin()

    # ── Public API ──────────────────────────────────────────────────────────

    def get_connection(self) -> sqlite3.Connection:
        """Return the active SQLite connection (for advanced usage)."""
        return self._connection

    def execute(self, query: str, params: Optional[tuple] = None) -> sqlite3.Cursor:
        """
        Execute a parameterized SQL query.

        ALWAYS use parameterized queries (the ? placeholders) instead of
        f-string interpolation — this is the ONLY safe way to prevent
        SQL injection attacks.

        Args:
            query: SQL with ? placeholders
            params: Tuple of values to substitute for the ?s

        Returns:
            sqlite3.Cursor (use .lastrowid, .rowcount, etc.)
        """
        cursor = self._connection.cursor()
        # params=() means "no params"; passing None to execute() crashes
        cursor.execute(query, params or ())
        # commit() persists changes — required for INSERT/UPDATE/DELETE
        self._connection.commit()
        return cursor

    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[sqlite3.Row]:
        """Fetch a SINGLE row (or None if no match). Convenience wrapper."""
        return self.execute(query, params).fetchone()

    def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[sqlite3.Row]:
        """Fetch ALL matching rows. Returns [] if no matches."""
        return self.execute(query, params).fetchall()

    # ── Context manager support ─────────────────────────────────────────────
    # Lets us write:  `with DatabaseManager() as db: ...`
    # Auto-closes the connection at the end, even on exceptions.

    def __enter__(self) -> 'DatabaseManager':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Close the connection and reset the Singleton."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            # Reset class-level state so the NEXT __new__ creates fresh
            DatabaseManager._instance = None

    # ── Schema setup (called once on first init) ────────────────────────────

    def _create_tables(self) -> None:
        """Create all tables if they don't exist (idempotent)."""

        # USERS — every actor (Owner, Renter, Admin) lives here.
        # The `role` column is what discriminates them.
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                email           TEXT UNIQUE NOT NULL,        -- DB-level uniqueness
                password_hash   TEXT NOT NULL,
                phone           TEXT,
                role            TEXT NOT NULL
                                CHECK(role IN ('owner','renter','admin')),
                license_number  TEXT,
                is_verified     INTEGER DEFAULT 0,           -- 0=pending, 1=verified
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # CARS — each car belongs to ONE owner (FK to users.id)
        self.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id        INTEGER NOT NULL,
                make            TEXT NOT NULL,
                model           TEXT NOT NULL,
                year            INTEGER NOT NULL,
                mileage         INTEGER DEFAULT 0,
                location        TEXT NOT NULL,
                daily_rate      REAL NOT NULL,
                min_rent_period INTEGER DEFAULT 1,
                max_rent_period INTEGER DEFAULT 30,
                is_approved     INTEGER DEFAULT 0,
                is_available    INTEGER DEFAULT 1,
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # BOOKINGS — the heart of the system. 3 FKs: car, renter, owner.
        # owner_id is intentionally denormalized (also in cars table)
        # to speed up "show me all my bookings as an owner" queries.
        self.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id          INTEGER NOT NULL,
                renter_id       INTEGER NOT NULL,
                owner_id        INTEGER NOT NULL,
                start_date      TEXT NOT NULL,
                end_date        TEXT NOT NULL,
                insurance_type  TEXT DEFAULT 'none',
                insurance_fee   REAL DEFAULT 0,
                platform_fee    REAL DEFAULT 0,
                owner_amount    REAL DEFAULT 0,
                total_amount    REAL NOT NULL,
                status          TEXT DEFAULT 'pending'
                                CHECK(status IN
                                  ('pending','approved','rejected',
                                   'cancelled','completed')),
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (car_id)    REFERENCES cars(id),
                FOREIGN KEY (renter_id) REFERENCES users(id),
                FOREIGN KEY (owner_id)  REFERENCES users(id)
            )
        """)

        # REVIEWS — bidirectional: renter→owner AND owner→renter
        self.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id      INTEGER NOT NULL,
                reviewer_id     INTEGER NOT NULL,            -- who wrote it
                reviewee_id     INTEGER NOT NULL,            -- who's being reviewed
                rating          INTEGER CHECK(rating BETWEEN 1 AND 5),
                comment         TEXT,
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (booking_id)  REFERENCES bookings(id),
                FOREIGN KEY (reviewer_id) REFERENCES users(id),
                FOREIGN KEY (reviewee_id) REFERENCES users(id)
            )
        """)

        # INSURANCE_CLAIMS — filed by owner when damage happens
        self.execute("""
            CREATE TABLE IF NOT EXISTS insurance_claims (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id      INTEGER NOT NULL,
                description     TEXT NOT NULL,
                claim_amount    REAL NOT NULL,
                status          TEXT DEFAULT 'pending'
                                CHECK(status IN ('pending','approved','rejected')),
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (booking_id) REFERENCES bookings(id)
            )
        """)

    def _create_indexes(self) -> None:
        """
        Create indexes for frequently-queried columns.

        Without indexes, every SELECT does a full table scan (slow).
        With indexes, lookups are O(log n) instead of O(n).
        SQLite uses these automatically — we just declare them.
        """
        indexes = [
            # Login queries hit users.email constantly
            "CREATE INDEX IF NOT EXISTS idx_users_email   ON users(email)",
            # Owner viewing their own cars
            "CREATE INDEX IF NOT EXISTS idx_cars_owner    ON cars(owner_id)",
            # "Show me available approved cars" — used in search
            "CREATE INDEX IF NOT EXISTS idx_cars_avail    ON cars(is_approved, is_available)",
            # Booking lookups by status (pending/approved/etc.)
            "CREATE INDEX IF NOT EXISTS idx_book_status   ON bookings(status)",
            # Renter and owner dashboards filter by user
            "CREATE INDEX IF NOT EXISTS idx_book_renter   ON bookings(renter_id)",
            "CREATE INDEX IF NOT EXISTS idx_book_owner    ON bookings(owner_id)",
            # Availability check (the most expensive query in the app)
            "CREATE INDEX IF NOT EXISTS idx_book_car_dates ON bookings(car_id, start_date, end_date)",
        ]
        for sql in indexes:
            self.execute(sql)

    def _seed_default_admin(self) -> None:
        """Create default admin on first run (idempotent — safe to re-run)."""
        # Local import to avoid circular dependency
        from utils.security import hash_password

        # Skip seeding if ANY admin already exists
        existing = self.fetch_one(
            "SELECT id FROM users WHERE role = 'admin' LIMIT 1"
        )
        if existing:
            return

        # Use config values, not hard-coded literals
        self.execute("""
            INSERT INTO users (name, email, password_hash, phone, role, is_verified)
            VALUES (?, ?, ?, ?, 'admin', 1)
        """, ('System Admin', DEFAULT_ADMIN_EMAIL,
              hash_password(DEFAULT_ADMIN_PASSWORD), '0000000000'))
