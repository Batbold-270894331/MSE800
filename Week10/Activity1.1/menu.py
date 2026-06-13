"""Command line menu module for the system."""

from authService import signup, login
from profileService import view_profile, update_profile
from passwordResetService import forgot_password, reset_password


def user_menu(user_id):
    """Display user menu after successful login."""
    while True:
        print("\n--- User Menu ---")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Logout")

        choice = input("Choose option: ").strip()

        if choice == "1":
            view_profile(user_id)

        elif choice == "2":
            update_profile(user_id)

        elif choice == "3":
            print("Logged out successfully.")
            break

        else:
            print("Invalid option.")


def main_menu():
    """Display the main menu for the system."""
    while True:
        print("\n==============================")
        print("Main menu")
        print("==============================")
        print("1. Sign Up")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Reset Password")
        print("5. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            signup()

        elif choice == "2":
            user_id = login()

            if user_id:
                user_menu(user_id)

        elif choice == "3":
            forgot_password()

        elif choice == "4":
            reset_password()

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")