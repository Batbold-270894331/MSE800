# ==================================================
# Main Program
# ==================================================

from Flight import DomesticFlight
from Flight import DomesticFlight


def app():
    
    # Create a DomesticFlight object
    flight = DomesticFlight(
        flight_number="NZ501",
        origin="Auckland",
        destination="Wellington",
        departure_time="08:30 AM",
        seat_class="Economy",
        baggage_allowance=23,
        regional_flight=False
    )

    # Inherited method from Flight
    flight.display_flight_info()

    print()

    # Inherited method from Flight
    flight.board_passengers()

    print()

    # Method from DomesticFlight
    flight.display_regional_info()

    print()


if __name__ == "__main__":
    app()