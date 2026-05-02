# Money Exchange Database

## Overview

**money exchange application** using Python and SQLite. The system manages customers, accounts, currencies, transactions, exchange rates, and employees.

---

## Tables

Including **6 tables**:

1. **Customer** – Stores customer personal and contact details
2. **Account** – Manages customer accounts and balances
3. **Currency** – Stores supported currencies
4. **ExchangeRate** – Maintains currency conversion rates
5. **Employee** – Stores employee information
6. **Transactions** – Records all exchange transactions

---

## Relationships

* One Customer → Many Accounts (1:N)
* One Account → Many Transactions (1:N)
* One Currency → Many Accounts & Exchange Rates (1:N)
* One ExchangeRate → Many Transactions (1:N)
* One Employee → Many Transactions (1:N)

---

## Technologies Used

* Python (sqlite3)
* SQLite database

---

## How to Run

1. Run the Python script:

   ```bash
   python main.py
   ```
2. This will create the database file:

   ```
   money_exchange.db
   ```

