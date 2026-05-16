# Zoo Admin Login System

An application demonstrating a secure admin login system using decorators. This application simulates a Zoo Management System where only authenticated administrators can view or alter the animal database.

## Project Structure

* **`auth.py`**: The core authentication module. It handles a session state, verify credentials, and houses the `@admin_required` decorator.
* **`main.py`**: The start point of the application. It contains the dashboard and database functions, protected by the authentication decorator.

## Functionality

1. **Session Management**: Tracks whether a user is currently logged in using a dictionary (`session`).
2. **Access Control**: Users attempting to run sensitive functions (like viewing the inventory or adding animals) without being authenticated are blocked.
3. **Authentication**: Provides `login()` and `logout()` functions to securely alter the session state.

## How the Decorator is Implemented

The `@admin_required` decorator found in `auth.py`. 

A decorator is a function that takes another function. In this app, the decorator works as follows:

1. **Interception**: When a protected function like `view_animal_inventory()` is called, the `@admin_required` decorator intercepts the call.
2. **Verification**: The `wrapper` function inside the decorator checks the current `session` dictionary. It verifies two things:
    * Is `logged_in` set to `True`?
    * Is the `user` set to `"admin"`?
3. **Execution or Rejection**: 
    * If both conditions are met, the decorator returns and executes the original function (`func(*args, **kwargs)`). 
    * If the conditions are not met, the decorator prints an `[Access Denied]` message and returns `None`.

## Usage

Run the main file from terminal:

```bash
python main.py