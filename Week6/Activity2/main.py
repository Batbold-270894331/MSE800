from auth import login, logout, admin_required

# --- Protected Admin Functions ---

@admin_required
def view_animal_inventory():
    print("\n--- Admin Dashboard: Animal Inventory ---")
    print("1. Lions: 4")
    print("2. Penguins: 12")
    print("3. Elephants: 3")
    print("-----------------------------------------")

@admin_required
def add_new_animal(animal_name, count):
    print(f"\n--- Admin Action: Update Database ---")
    print(f"Successfully added {count} {animal_name}(s) to the zoo database.")

# --- Main Execution ---

def app():
    print("=== Welcome to the Zoo Management System ===")

    # 1. Attempt to access admin area BEFORE logging in (Fail)
    print("\nAttempting to view inventory as a guest...")
    view_animal_inventory()

    # 2. Attempt login with wrong credentials (Fail)
    login("admin", "wrongpassword")

    # 3. Successful Login
    login("admin", "zoopass123")

    # 4. Access admin area AFTER logging in (Succeed)
    view_animal_inventory()
    add_new_animal("Giraffe", 2)

    # 5. Logout
    logout()

    # 6. Attempt access again (Fail)
    view_animal_inventory()

if __name__ == "__main__":
    app()