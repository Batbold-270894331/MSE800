"""
Insurance Strategy Pattern
==========================
Demonstrates the Strategy design pattern.

Different insurance plans (Basic, Standard, Premium) share the same
interface but calculate fees differently. The Booking class uses
whichever strategy the renter selects.
"""

from abc import ABC, abstractmethod


class InsuranceStrategy(ABC):
    """Abstract base class for all insurance strategies."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def daily_fee(self) -> float:
        pass

    @property
    @abstractmethod
    def coverage_limit(self) -> float:
        pass

    def calculate_fee(self, days: int) -> float:
        """Calculate the insurance fee for the given number of days."""
        return self.daily_fee * days

    def __str__(self):
        return (f"{self.name} (${self.daily_fee}/day, "
                f"coverage up to ${self.coverage_limit:,.0f})")


class NoInsurance(InsuranceStrategy):
    """No insurance option."""
    @property
    def name(self):
        return 'none'

    @property
    def daily_fee(self):
        return 0.0

    @property
    def coverage_limit(self):
        return 0.0


class BasicInsurance(InsuranceStrategy):
    """Basic insurance — minimal coverage."""
    @property
    def name(self):
        return 'basic'

    @property
    def daily_fee(self):
        return 5.0

    @property
    def coverage_limit(self):
        return 2000.0


class StandardInsurance(InsuranceStrategy):
    """Standard insurance — moderate coverage (recommended)."""
    @property
    def name(self):
        return 'standard'

    @property
    def daily_fee(self):
        return 10.0

    @property
    def coverage_limit(self):
        return 5000.0


class PremiumInsurance(InsuranceStrategy):
    """Premium insurance — full coverage."""
    @property
    def name(self):
        return 'premium'

    @property
    def daily_fee(self):
        return 15.0

    @property
    def coverage_limit(self):
        return 999999.0


# Factory helper for creating insurance strategies by name
def get_insurance(name: str) -> InsuranceStrategy:
    """Return an insurance strategy by name."""
    strategies = {
        'none':     NoInsurance(),
        'basic':    BasicInsurance(),
        'standard': StandardInsurance(),
        'premium':  PremiumInsurance(),
    }
    return strategies.get(name.lower(), NoInsurance())


def list_all_insurance():
    """Return all available insurance strategies (excluding none)."""
    return [BasicInsurance(), StandardInsurance(), PremiumInsurance()]
