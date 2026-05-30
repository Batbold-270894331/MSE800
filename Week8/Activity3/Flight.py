# ==================================================
# Parent Class: Flight
# ==================================================

class Flight:

    def __init__(self,
                 flight_number,
                 origin,
                 destination,
                 departure_time,
                 seat_class,
                 baggage_allowance,
                 passport_required,
                 visa_required):

        # Attributes shared by all flights
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.seat_class = seat_class
        self.baggage_allowance = baggage_allowance
        self.passport_required = passport_required
        self.visa_required = visa_required

    # Shared method
    def display_flight_info(self):
        print("\n===== Air New Zealand Flight Information =====")
        print(f"Flight Number      : {self.flight_number}")
        print(f"Origin             : {self.origin}")
        print(f"Destination        : {self.destination}")
        print(f"Departure Time     : {self.departure_time}")
        print(f"Seat Class         : {self.seat_class}")
        print(f"Baggage Allowance  : {self.baggage_allowance} kg")
        print(f"Passport Required  : {self.passport_required}")
        print(f"Visa Required      : {self.visa_required}")

    # Shared method
    def board_passengers(self):
        print("Passengers are now boarding.")


# ==================================================
# Child Class: DomesticFlight
# Inherits from Flight
# ==================================================

class DomesticFlight(Flight):

    def __init__(self,
                 flight_number,
                 origin,
                 destination,
                 departure_time,
                 seat_class,
                 baggage_allowance,
                 regional_flight):

        # Call the parent class constructor
        super().__init__(
            flight_number,
            origin,
            destination,
            departure_time,
            seat_class,
            baggage_allowance,
            passport_required=False,  # NZ domestic flights
            visa_required=False       # do not require visas
        )

        # Attribute specific to domestic flights
        self.regional_flight = regional_flight

    # Method specific to DomesticFlight
    def display_regional_info(self):

        if self.regional_flight:
            print("Flight Type: Regional Domestic Flight")
        else:
            print("Flight Type: Main Domestic Flight")