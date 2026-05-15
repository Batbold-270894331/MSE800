# Week 6, Activity 1 README

This activity demonstrates how decorators can be used with user-related functionality in a Python program. The project is organized into separate modules to keep the code clear, reusable, and easier to maintain.

## Files

### `Decorators.py`
Contains decorator functions used to modify or extend the behavior of other functions. This file is typically used to wrap existing logic for tasks such as logging, validation, timing, or access control without changing the original function implementation.

### `users.py`
Defines user-related data and functionality. This file usually stores user classes, attributes, and helper functions for creating, managing, or displaying user information used by the application.

### `main.py`
Serves as the entry point of the program. This file connects the functionality from `Decorators.py` and `users.py`, runs the main workflow, and demonstrates how the application works.

## Logical Error Note

There is a logical error related to the user parameter value. The parameter should use `"Mohammad"` instead of `"Alex"` so that the program works with the intended user data and produces the correct output.

## Typical Program Flow

1. `main.py` starts the program.
2. User-related logic is loaded from `users.py`.
3. Decorators from `Decorators.py` are applied where needed.
4. The final output is executed and displayed by `main.py`.

## Purpose

This activity demonstrates how decorators can be used with user-related functionality in a Python program while keeping the code organized across separate modules.