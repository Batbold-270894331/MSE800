# A dictionary to simulate an active user session
session = {
    "logged_in": False,
    "user": None
}

def admin_required(func):
    """
    Decorator to ensure only logged-in admins can execute the wrapped function.
    """
    def wrapper(*args, **kwargs):
        if session.get("logged_in") and session.get("user") == "admin":
            # If logged in as admin, execute the function normally
            return func(*args, **kwargs)
        else:
            # Otherwise, block access
            print("\n[Access Denied] You must be logged in as an administrator to access this.")
            return None
    return wrapper

def login(username, password):
    """Simulates a secure login process."""
    # Hardcoded admin credentials
    ADMIN_USER = "admin"
    ADMIN_PASS = "zoopass123"

    if username == ADMIN_USER and password == ADMIN_PASS:
        session["logged_in"] = True
        session["user"] = username
        print(f"\n[Success] Welcome back, {username}!")
        return True
    else:
        print("\n[Error] Invalid username or password.")
        return False

def logout():
    """Logs the user out by clearing the session."""
    session["logged_in"] = False
    session["user"] = None
    print("\n[Success] You have been successfully logged out.")