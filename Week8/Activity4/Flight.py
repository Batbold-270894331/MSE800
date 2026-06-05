
# =========================
# Base Class: Flight
# =========================

class Flight:

    def __init__(self, flight_number, origin, destination, seat_class):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.seat_class = seat_class

    def display_info(self):
        print(f"\nFlight: {self.flight_number}")
        print(f"{self.origin} -> {self.destination}")
        print(f"Class: {self.seat_class}")

    def board_passengers(self):
        print("Passengers are boarding...")

    def calculate_price(self):
        print("Base ticket price calculated.")


# =========================
# Domestic Flight
# =========================

class DomesticFlight(Flight):

    def __init__(self, flight_number, origin, destination, seat_class, baggage_allowance):
        super().__init__(flight_number, origin, destination, seat_class)
        self.baggage_allowance = baggage_allowance

    def check_weather(self):
        print("Checking NZ weather conditions...")

    def apply_nz_rules(self):
        print("Applying New Zealand domestic flight rules.")

    def baggage_policy(self):
        print(f"Baggage limit: {self.baggage_allowance} kg")


# =========================
# International Flight
# =========================

class InternationalFlight(Flight):

    def __init__(self, flight_number, origin, destination, seat_class,
                 passport_required, visa_required):
        super().__init__(flight_number, origin, destination, seat_class)
        self.passport_required = passport_required
        self.visa_required = visa_required

    def customs_check(self):
        print("Customs clearance required.")

    def immigration_info(self):
        print(f"Passport Required: {self.passport_required}")

    def currency_info(self):
        print("Foreign currency exchange may apply.")