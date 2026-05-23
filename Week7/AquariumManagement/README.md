# Auckland Aquarium Management System

## Description

This project is a Python-based aquarium management system.

The system allows users to:
- Add fish into the aquarium
- Manage fish categories
- Display the number of fish available

Supported fish categories:
- Goldfish
- Shark
- Angelfish
- Tuna
- Salmon

---

# Design Patterns Used

## 1. Factory Pattern

Implemented in:
- `fish_factory.py`

Purpose:
- Centralizes fish object creation
- Simplifies object management
- Makes the system extensible

Example:
```python
fish = FishFactory.create_fish("Shark")

---

## 2. Singleton Pattern

Implemented in:
- `aquarium.py`

Purpose:
- Ensures only one aquarium inventory exists
- Prevents multiple inventory instances

Example:
```python
def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(Aquarium, cls).__new__(cls)

            # Initialize inventory once
            cls.__instance.fish_inventory = {}

        return cls.__instance

Example of usage:
```python
aquarium = Aquarium()

---

# How to Run

## 3. Run the program
```python
python main.py