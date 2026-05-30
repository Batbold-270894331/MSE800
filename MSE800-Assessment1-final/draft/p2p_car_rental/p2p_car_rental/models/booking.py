"""
Booking model
=============
Represents a rental booking transaction.
"""


class Booking:
    """A rental booking made by a Renter for a Car."""

    STATUS_PENDING   = 'pending'
    STATUS_APPROVED  = 'approved'
    STATUS_REJECTED  = 'rejected'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'

    def __init__(self, booking_id, car_id, renter_id, owner_id,
                 start_date, end_date, insurance_type='none',
                 insurance_fee=0, platform_fee=0, owner_amount=0,
                 total_amount=0, status='pending'):
        self._id = booking_id
        self._car_id = car_id
        self._renter_id = renter_id
        self._owner_id = owner_id
        self._start_date = start_date
        self._end_date = end_date
        self._insurance_type = insurance_type
        self._insurance_fee = insurance_fee
        self._platform_fee = platform_fee
        self._owner_amount = owner_amount
        self._total_amount = total_amount
        self._status = status

    # ── Properties ──────────────────────────────────────────────────────────
    @property
    def id(self):
        return self._id

    @property
    def car_id(self):
        return self._car_id

    @property
    def renter_id(self):
        return self._renter_id

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def insurance_type(self):
        return self._insurance_type

    @property
    def insurance_fee(self):
        return self._insurance_fee

    @property
    def platform_fee(self):
        return self._platform_fee

    @property
    def owner_amount(self):
        return self._owner_amount

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def status(self):
        return self._status

    # ── State changers ─────────────────────────────────────────────────────
    def approve(self):
        self._status = self.STATUS_APPROVED

    def reject(self):
        self._status = self.STATUS_REJECTED

    def cancel(self):
        self._status = self.STATUS_CANCELLED

    def complete(self):
        self._status = self.STATUS_COMPLETED

    def get_summary(self):
        """Return booking summary as dict."""
        return {
            'Booking ID': self._id,
            'Period': f"{self._start_date} → {self._end_date}",
            'Insurance': self._insurance_type.capitalize(),
            'Total': f"${self._total_amount:.2f}",
            'Status': self._status.upper(),
        }
