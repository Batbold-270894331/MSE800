"""Authentication service module for user sign up and login."""

import sqlite3
from models import UserModel


def signup():
    """Handle user sign-up process."""
    print("\n--- User Sign Up ---")

    full_name = input("Enter full name: ").strip()
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ").strip()
    email = input("Enter email: ").strip().lower()
    password = input("Enter password: ").strip()

    if not full_name or not date_of_birth or not email or not password:
        print("All fields are required.")
        return

    try:
        UserModel.create_user(full_name, date_of_birth, email, password)
        print("User registered successfully.")

    except sqlite3.IntegrityError:
        print("This email is already registered.")


def login():
    """Handle user login process."""
    print("\n--- User Login ---")

    email = input("Enter email: ").strip().lower()
    password = input("Enter password: ").strip()

    user = UserModel.get_user_by_email(email)

    if user is None:
        print("Invalid email or password.")
        return None

    user_id = user[0]
    full_name = user[1]
    stored_hash = user[4]
    stored_salt = user[5]

    if UserModel.verify_password(password, stored_hash, stored_salt):
        print(f"Login successful. Welcome, {full_name}!")
        return user_id

    print("Invalid email or password.")
    return None