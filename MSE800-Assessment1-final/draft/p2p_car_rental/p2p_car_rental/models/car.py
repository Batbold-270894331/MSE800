"""
Car model
=========
Represents a car listed on the platform.
"""


class Car:
    """A car available for rent."""

    def __init__(self, car_id, owner_id, make, model, year, mileage,
                 location, daily_rate, min_rent_period=1, max_rent_period=30,
                 is_approved=False, is_available=True):
        self._id = car_id
        self._owner_id = owner_id
        self._make = make
        self._model = model
        self._year = year
        self._mileage = mileage
        self._location = location
        self._daily_rate = daily_rate
        self._min_rent_period = min_rent_period
        self._max_rent_period = max_rent_period
        self._is_approved = bool(is_approved)
        self._is_available = bool(is_available)

    # ── Properties ──────────────────────────────────────────────────────────
    @property
    def id(self):
        return self._id

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def make(self):
        return self._make

    @property
    def model(self):
        return self._model

    @property
    def year(self):
        return self._year

    @property
    def location(self):
        return self._location

    @property
    def daily_rate(self):
        return self._daily_rate

    @property
    def min_rent_period(self):
        return self._min_rent_period

    @property
    def max_rent_period(self):
        return self._max_rent_period

    @property
    def is_approved(self):
        return self._is_approved

    @property
    def is_available(self):
        return self._is_available

    # ── Business methods ────────────────────────────────────────────────────
    def get_details(self):
        """Return car details as a dictionary."""
        return {
            'ID': self._id,
            'Make': self._make,
            'Model': self._model,
            'Year': self._year,
            'Mileage': f"{self._mileage:,} km",
            'Location': self._location,
            'Daily Rate': f"${self._daily_rate:.2f}",
            'Min Rent (days)': self._min_rent_period,
            'Max Rent (days)': self._max_rent_period,
            'Approved': 'Yes' if self._is_approved else 'No',
            'Available': 'Yes' if self._is_available else 'No',
        }

    def calculate_base_price(self, days: int) -> float:
        """Calculate base rental price for a given number of days."""
        return self._daily_rate * days

    def __str__(self):
        return f"{self._year} {self._make} {self._model} @ ${self._daily_rate:.2f}/day"
