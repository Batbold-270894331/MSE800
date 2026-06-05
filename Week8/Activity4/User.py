# =========================
# Base Class: User
# =========================

class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

    def login(self):
        print(f"{self.name} logged in.")

    def logout(self):
        print(f"{self.name} logged out.")

    def view_profile(self):
        print(f"User: {self.name}, Role: {self.role}")


# =========================
# Admin (inherits User)
# =========================

class Admin(User):

    def __init__(self, user_id, name, admin_level):
        super().__init__(user_id, name, role="Admin")
        self.admin_level = admin_level

    def create_flight(self):
        print("Flight created successfully.")

    def delete_flight(self):
        print("Flight deleted successfully.")

    def view_all_flights(self):
        print("Displaying all flights in system.")


# =========================
# Passenger (inherits User)
# =========================

class Passenger(User):

    def __init__(self, user_id, name, passport_number, nationality):
        super().__init__(user_id, name, role="Passenger")
        self.passport_number = passport_number
        self.nationality = nationality

    def book_flight(self):
        print("Flight booked successfully.")

    def cancel_booking(self):
        print("Booking cancelled.")

    def view_ticket(self):
        print("Ticket details displayed.")