"""
Main Menu — Entry point CLI
============================
Handles login / register / exit.
"""

from services.auth_service import AuthService
from ui.owner_menu import owner_menu
from ui.renter_menu import renter_menu
from ui.admin_menu import admin_menu
from utils.helpers import (
    clear_screen, print_header, print_success, print_error,
    prompt, prompt_choice, pause,
)


def show_main_menu():
    """Display main menu and handle user choice."""
    auth = AuthService()

    while True:
        clear_screen()
        print_header("P2P CAR RENTAL SYSTEM", 60)
        print()
        print("  1. Login")
        print("  2. Register")
        print("  3. Exit")
        print()

        choice = prompt_choice("Select option", ['1', '2', '3'])

        if choice == '1':
            _handle_login(auth)
        elif choice == '2':
            _handle_register(auth)
        elif choice == '3':
            print("\nThank you for using P2P Car Rental System. Goodbye!\n")
            break


def _handle_login(auth):
    """Login flow."""
    clear_screen()
    print_header("LOGIN", 60)
    email = prompt("Email")
    password = prompt("Password")

    ok, msg, user = auth.login(email, password)
    if not ok:
        print_error(msg)
        pause()
        return

    print_success(msg)

    # Check verification (admin auto-verified)
    if user.role != 'admin' and not user.is_verified:
        print_error("Your account is not yet verified by admin.")
        print("Please wait for an admin to verify your account.")
        pause()
        return

    pause()

    # Route based on role (Polymorphism!)
    if user.role == 'owner':
        owner_menu(user)
    elif user.role == 'renter':
        renter_menu(user)
    elif user.role == 'admin':
        admin_menu(user)


def _handle_register(auth):
    """Registration flow."""
    clear_screen()
    print_header("REGISTER NEW USER", 60)
    print("Hint: select 'owner' to list cars, 'renter' to rent cars.\n")

    name = prompt("Full name")
    email = prompt("Email")
    password = prompt("Password (min 6 chars)")
    phone = prompt("Phone")
    role = prompt_choice("Role (owner/renter)", ['owner', 'renter'])
    license_number = prompt("Driver's license number", allow_empty=True)

    ok, msg, user = auth.register(name, email, password, phone, role,
                                   license_number or None)
    if ok:
        print_success(msg)
    else:
        print_error(msg)
    pause()
