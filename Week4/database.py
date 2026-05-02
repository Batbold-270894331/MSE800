import sqlite3

def create_connection():
    conn = sqlite3.connect("money_exchange.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Customer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            DateOfBirth TEXT,
            Email TEXT UNIQUE,
            PhoneNumber TEXT,
            Address TEXT,
            CreatedDate DATE DEFAULT (DATE('now'))
        )
    ''')

    # Currency table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Currency (
            CurrencyId INTEGER PRIMARY KEY AUTOINCREMENT,
            CurrencyName TEXT NOT NULL,
            Symbol TEXT,
            Country TEXT
        );
    ''')

    # Account table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            AccountId INTEGER PRIMARY KEY AUTOINCREMENT,
            AccountNumber TEXT UNIQUE NOT NULL,
            Balance REAL DEFAULT 0,
            CustomerId INTEGER,
            CurrencyId INTEGER,
            Status TEXT,
            CreatedDate DATE DEFAULT (DATE('now')),
            FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
            FOREIGN KEY (CurrencyId) REFERENCES Currency(CurrencyId)
        );
    ''')

    # Employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT,
            Email TEXT UNIQUE,
            Phone TEXT,
            Role TEXT,
            HireDate date DEFAULT (DATE('now'))
        );
    ''')

    # ExchangeRate table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ExchangeRate (
            ExchangeRateId INTEGER PRIMARY KEY AUTOINCREMENT,
            EffectiveDate date DEFAULT (DATE('now')),
            FromCurrencyId INTEGER,
            ToCurrencyId INTEGER,
            Rate REAL,
            FOREIGN KEY (FromCurrencyId) REFERENCES Currency(CurrencyId),
            FOREIGN KEY (ToCurrencyId) REFERENCES Currency(CurrencyId)
        );
    ''')

    # Transaction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionId INTEGER PRIMARY KEY AUTOINCREMENT,
            TransactionDate date DEFAULT (DATE('now')),
            AccountId INTEGER,
            ExchangeRateId INTEGER,
            ApprovedEmployeeId INTEGER,
            BuyOrSell TEXT,
            FromAmount REAL,
            ToAmount REAL,
            Fee REAL,
            FOREIGN KEY (AccountId) REFERENCES Account(AccountId),
            FOREIGN KEY (ExchangeRateId) REFERENCES ExchangeRate(ExchangeRateId),
            FOREIGN KEY (ApprovedEmployeeId) REFERENCES Employee(EmployeeId)
        );
    ''')

    conn.commit()
    conn.close()
