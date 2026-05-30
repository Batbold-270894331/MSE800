# P2P Car Rental System

A command-line peer-to-peer car rental platform built with Python.  
Car owners can list their vehicles, and renters can search and book them.  
An admin manages user verification and car approvals.

---

## Developer

**Name:** [Your Name]  
**Course:** MSE800 Professional Software Engineering  
**Institution:** Yoobee College of Creative Innovation  
**Assignment:** Assessment 1 - Object-Oriented Programming Assignment

---

## Project Structure

```
source_code/
│
├── main.py                        # Entry point. Run this file to start the program.
│
├── config.py                      # All settings in one place (database path, fees, discount codes).
│
├── requirements.txt               # Required Python packages.
│
├── database/
│   └── db_manager.py              # Manages the SQLite database connection (Singleton pattern).
│
├── models/
│   ├── user.py                    # Abstract base class for all user types.
│   ├── owner.py                   # Owner user (lists cars, approves bookings).
│   ├── renter.py                  # Renter user (searches and books cars).
│   ├── admin.py                   # Admin user (verifies users, approves cars).
│   ├── car.py                     # Car listing with details and pricing.
│   ├── booking.py                 # Booking record with status management.
│   └── review.py                  # Review submitted after a completed booking.
│
├── factories/
│   └── user_factory.py            # Creates the correct User object based on role (Factory pattern).
│
├── patterns/
│   └── insurance_strategy.py      # Insurance options using Strategy pattern (None/Basic/Standard/Premium).
│
├── services/
│   ├── auth_service.py            # User registration and login logic.
│   ├── car_service.py             # Add, remove, search, and approve cars.
│   ├── booking_service.py         # Create, approve, reject, and cancel bookings. Also calculates fees.
│   ├── admin_service.py           # Admin operations: verify users, handle claims, view stats.
│   └── review_service.py          # Submit and retrieve user reviews.
│
├── ui/
│   ├── main_menu.py               # Login and registration screen.
│   ├── owner_menu.py              # Menu for car owners.
│   ├── renter_menu.py             # Menu for renters.
│   └── admin_menu.py              # Menu for admins.
│
├── utils/
│   ├── helpers.py                 # CLI display functions, date utilities, and input prompts.
│   ├── security.py                # Password hashing and verification using SHA-256.
│   └── validators.py              # Input validation for email, password, phone, and dates.
│
└── docs/
    ├── 01_ERD.png                 # Entity Relationship Diagram.
    ├── 02_UseCase.png             # Use Case Diagram.
    ├── 03_Class.png               # Class Diagram.
    ├── 04_Sequence.png            # Sequence Diagram.
    ├── 05_Activity_MakeBooking.png
    ├── 06_Activity_AddCar.png
    ├── 07_Activity_ApproveBooking.png
    └── 08_Activity_HandleClaim.png
```

---

## Requirements

- Python 3.10 or higher
- pip (Python package manager)

The following packages are used:

| Package    | Purpose                              |
|------------|--------------------------------------|
| `tabulate` | Displays data in formatted tables.   |
| `colorama` | Adds color output in the terminal.   |

---

## Installation and Setup

Follow these steps to install and run the project.

**Step 1: Clone or download the project**

Download the project folder to your computer.

**Step 2: Open a terminal**

Navigate to the `source_code` folder:

```bash
cd path/to/source_code
```

**Step 3: Create a virtual environment**

```bash
python -m venv venv
```

**Step 4: Activate the virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS or Linux:
```bash
source venv/bin/activate
```

**Step 5: Install required packages**

```bash
pip install -r requirements.txt
```

**Step 6: Run the program**

```bash
python main.py
```

No other configuration is needed. The database file is created automatically on first run.

---

## Default Admin Account

When the program runs for the first time, it creates a default admin account automatically.

| Field    | Value             |
|----------|-------------------|
| Email    | admin@p2p.com     |
| Password | admin123          |

Please note: this account is for development and testing only.

---

## How to Use

### As a Renter
1. Select **Register** from the main menu.
2. Choose role **Renter**.
3. Wait for admin verification.
4. Log in and use the renter menu to search for cars and make bookings.

### As an Owner
1. Select **Register** from the main menu.
2. Choose role **Owner**.
3. Wait for admin verification.
4. Log in, add your car, and wait for admin approval.
5. Approve or reject booking requests from renters.

### As an Admin
1. Log in with the default admin account.
2. Verify new users under **View pending users**.
3. Approve car listings under **View pending car listings**.
4. Monitor all bookings and platform statistics.

---

## Environment Configuration

The system supports three environments. Set the `APP_ENV` variable before running:

```bash
# Development (default)
python main.py

# Test mode (uses in-memory database)
APP_ENV=test python main.py

# Production
APP_ENV=prod python main.py
```

---

## Design Patterns Used

| Pattern   | Location                    | Purpose                                      |
|-----------|-----------------------------|----------------------------------------------|
| Singleton | `database/db_manager.py`    | Only one database connection exists at a time. |
| Factory   | `factories/user_factory.py` | Creates Owner, Renter, or Admin objects by role. |
| Strategy  | `patterns/insurance_strategy.py` | Selects the correct insurance calculation at runtime. |

---

## OOP Concepts Applied

| Concept       | Example                                                       |
|---------------|---------------------------------------------------------------|
| Encapsulation | All model attributes are protected (`_name`) with `@property` access. |
| Abstraction   | `User` and `InsuranceStrategy` are abstract base classes.     |
| Inheritance   | `Owner`, `Renter`, `Admin` all inherit from `User`.           |
| Polymorphism  | Each user role has its own `view_dashboard()` implementation. |

---

## Known Bugs and Limitations

- Password hashing uses SHA-256 with a static salt. This is acceptable for a coursework project but is not suitable for a real production system.
- The system runs in the terminal only. There is no graphical user interface.
- There is no email notification system. Users must check the application manually for status updates.
- The admin cannot yet handle insurance claims through the menu. The backend logic exists but the UI option is not yet connected.
- Date validation checks the format only. It does not check if the start date is before the end date.

---

## Testing

To run the system in test mode with an in-memory database (no files created):

```bash
APP_ENV=test python main.py
```

This mode is useful for testing without affecting the real database.

---

*README written for MSE800 Assessment 1 submission.*
