"""Profile service module for viewing and updating user profile information."""

from models import UserModel


def view_profile(user_id):
    """Handle viewing a user's profile."""
    print("\n--- View Profile ---")

    user = UserModel.get_user_by_id(user_id)

    if user is None:
        print("User not found.")
        return

    print(f"Full Name     : {user[1]}")
    print(f"Date of Birth : {user[2]}")
    print(f"Email         : {user[3]}")
    print(f"Created At    : {user[4]}")


def update_profile(user_id):
    """Handle updating a user's profile information."""
    print("\n--- Update Profile ---")

    full_name = input("Enter new full name: ").strip()
    date_of_birth = input("Enter new date of birth (YYYY-MM-DD): ").strip()

    if not full_name or not date_of_birth:
        print("Full name and date of birth are required.")
        return

    UserModel.update_profile(user_id, full_name, date_of_birth)

    print("Profile updated successfully.")