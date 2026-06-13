"""Password reset service module for forgot password and reset password features."""

import secrets
from datetime import datetime, timedelta
from models import UserModel, PasswordResetModel


def forgot_password():
    """Handle forgot password process."""
    print("\n--- Forgot Password ---")

    email = input("Enter your registered email: ").strip().lower()

    user = UserModel.get_user_by_email(email)

    if user is None:
        print("Email not found.")
        return

    user_id = user[0]
    reset_token = secrets.token_urlsafe(16)
    expires_at = datetime.now() + timedelta(minutes=30)

    PasswordResetModel.create_reset_token(user_id, reset_token, expires_at)

    print("Password reset token generated.")
    print("Use this token to reset your password:")
    print(reset_token)


def reset_password():
    """Handle reset password process."""
    print("\n--- Reset Password ---")

    token = input("Enter reset token: ").strip()
    new_password = input("Enter new password: ").strip()

    if not token or not new_password:
        print("Token and new password are required.")
        return

    reset_record = PasswordResetModel.get_reset_token(token)

    if reset_record is None:
        print("Invalid reset token.")
        return

    reset_id = reset_record[0]
    user_id = reset_record[1]
    expires_at = reset_record[2]
    used = reset_record[3]

    if used == 1:
        print("This token has already been used.")
        return

    if datetime.now() > datetime.fromisoformat(expires_at):
        print("This token has expired.")
        return

    UserModel.update_password(user_id, new_password)
    PasswordResetModel.mark_token_used(reset_id)

    print("Password reset successfully.")