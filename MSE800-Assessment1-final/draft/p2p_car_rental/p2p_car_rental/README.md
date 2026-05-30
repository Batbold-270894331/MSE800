# P2P Car Rental System

A peer-to-peer (P2P) car rental platform built in Python (CLI). Car owners list their vehicles on the platform; renters search and book cars; admins moderate the marketplace.

**Course:** MSE800 — Professional Software Engineering
**Assignment:** Assignment 1 — Object-Oriented Programming
**Type:** Individual Assignment

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [How to Run](#how-to-run)
5. [Usage Guide](#usage-guide)
6. [Project Structure](#project-structure)
7. [Design Patterns](#design-patterns)
8. [OOP Principles](#oop-principles)
9. [Default Admin Credentials](#default-admin-credentials)
10. [Known Issues / Limitations](#known-issues--limitations)
11. [License](#license)
12. [Credits](#credits)

---

## Features

### For Car Owners
- Register and get verified by admin
- Add / Remove car listings
- Approve or reject incoming booking requests
- View earnings and booking history

### For Renters
- Search and filter cars by location and price
- View detailed car information
- Make bookings with date selection
- Optional: Select insurance (Basic / Standard / Premium)
- Optional: Apply discount codes
- Submit reviews after a completed rental
- Cancel bookings

### For Admin
- Verify pending user registrations (KYC)
- Approve or reject new car listings
- View all platform bookings
- Handle insurance claims
- View platform reports & statistics
- Suspend misbehaving users

---

## Architecture

The system uses a **layered architecture**:

```
┌─────────────────────────────────────┐
│  Presentation Layer (CLI Menus)     │
├─────────────────────────────────────┤
│  Service Layer (Business Logic)     │
├─────────────────────────────────────┤
│  Model Layer (OOP Classes)          │
├─────────────────────────────────────┤
│  Data Access Layer (SQLite)         │
└─────────────────────────────────────┘
```

---

## Installation

### Prerequisites
- **Python 3.8+** ([download here](https://www.python.org/downloads/))
- pip (comes with Python)

### Setup Steps

1. **Extract the zip file** to a folder of your choice.

2. **Open a terminal** in that folder.

3. **(Optional but recommended) Create a virtual environment:**
   ```bash
   python -m venv venv

   # Activate it:
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `tabulate` — for nice CLI tables
   - `colorama` — for cross-platform colored output (optional)

---

## How to Run

From the project root folder:

```bash
python main.py
```

That's it! No manual configuration needed.

On first run, the system automatically:
- Creates the SQLite database file (`database/car_rental.db`)
- Sets up all required tables
- Creates a default admin account

---

## Usage Guide

### First-time Setup

1. Launch the program with `python main.py`
2. Login as admin first to verify users (see [admin credentials](#default-admin-credentials))
3. Register new accounts (owner or renter)
4. Login as admin again to verify the new accounts

### Demo Discount Codes

When making a booking, you can try these codes:
- `SAVE10` — 10% off
- `WELCOME20` — 20% off
- `SUMMER15` — 15% off

### Sample Workflow

1. **Admin** logs in and verifies a new owner
2. **Owner** logs in and adds a car listing
3. **Admin** approves the car listing
4. **Renter** registers (Admin verifies them)
5. **Renter** searches cars, picks one, selects dates
6. Renter optionally selects insurance and applies a discount
7. **Owner** approves the booking
8. After the rental ends, **Renter** submits a review

---

## Project Structure

```
p2p_car_rental/
│
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── README.md                  # This file
│
├── database/                  # Data access layer
│   ├── db_manager.py          # Singleton DB manager
│   └── car_rental.db          # SQLite file (auto-created)
│
├── models/                    # OOP entities
│   ├── user.py                # Abstract User class
│   ├── owner.py               # Inherits User
│   ├── renter.py              # Inherits User
│   ├── admin.py               # Inherits User
│   ├── car.py                 # Car entity
│   ├── booking.py             # Booking entity
│   └── review.py              # Review entity
│
├── factories/                 # Factory pattern
│   └── user_factory.py        # Creates User subclasses
│
├── patterns/                  # Design patterns
│   └── insurance_strategy.py  # Strategy pattern (insurance plans)
│
├── services/                  # Business logic
│   ├── auth_service.py        # Login & registration
│   ├── car_service.py         # Car CRUD
│   ├── booking_service.py     # Booking workflow
│   ├── review_service.py      # Reviews
│   └── admin_service.py       # Admin operations
│
├── ui/                        # CLI menus
│   ├── main_menu.py           # Login / register
│   ├── owner_menu.py
│   ├── renter_menu.py
│   └── admin_menu.py
│
├── utils/                     # Helpers
│   ├── security.py            # Password hashing
│   ├── validators.py          # Input validators
│   └── helpers.py             # CLI display helpers
│
└── docs/                      # Documentation
    ├── UML/                   # UML diagrams (PNG)
    └── Maintenance_Plan.pdf
```

---

## Design Patterns

The project uses **three** design patterns:

### 1. Singleton — `DatabaseManager`
Ensures only one database connection exists throughout the application's lifecycle. Prevents resource leaks and connection conflicts.

**File:** `database/db_manager.py`

### 2. Factory Method — `UserFactory`
Centralizes user creation. Given a role string (`'owner'`, `'renter'`, `'admin'`), it returns the correct subclass instance.

**File:** `factories/user_factory.py`

### 3. Strategy — `InsuranceStrategy`
Different insurance plans (Basic, Standard, Premium) share a common interface but compute fees differently. A booking picks any strategy at runtime.

**File:** `patterns/insurance_strategy.py`

---

## OOP Principles

All four pillars of OOP are demonstrated:

### Encapsulation
Private attributes prefixed with `_` are accessed only through getter properties.
```python
self._password_hash = "..."   # private
@property
def password_hash(self): ...
```

### Inheritance
`Owner`, `Renter`, and `Admin` all extend `User`.
```python
class Owner(User):
    def __init__(self, ...):
        super().__init__(...)
```

### Abstraction
`User` is an abstract base class with abstract methods.
```python
from abc import ABC, abstractmethod
class User(ABC):
    @abstractmethod
    def view_dashboard(self): pass
```

### Polymorphism
The same method `view_dashboard()` behaves differently per role.
```python
user.view_dashboard()   # Owner / Renter / Admin all override this
```

---

## Default Admin Credentials

On first run, the system creates a default admin account:

| Field    | Value             |
|----------|-------------------|
| Email    | `admin@p2p.com`   |
| Password | `admin123`        |

> ⚠️ **Important:** Change the default admin password before deploying to production.

---

## Known Issues / Limitations

- **No email notifications.** "Send notification" is currently logged in DB only, not sent via SMTP.
- **No payment gateway.** Bookings track amounts but do not process real money.
- **Single-user CLI.** No concurrent multi-user support (one terminal at a time).
- **No data export.** Reports are shown on screen only; cannot export CSV/PDF yet.
- **Dates aren't validated against real calendars.** A renter can technically pick a past start date.

These are planned improvements for future versions (see `docs/Maintenance_Plan.pdf`).

---

## License

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2025 P2P Car Rental System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

## Credits

**Developer:** [Your Name]
**Course:** MSE800 — Professional Software Engineering
**Institution:** Yoobee College of Creative Innovation
**Year:** 2025

**Built with:**
- Python 3.8+
- SQLite (built-in)
- `tabulate` library for CLI tables
