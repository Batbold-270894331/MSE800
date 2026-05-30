"""
Review model
============
Represents a rating + comment given after a completed booking.
"""


class Review:
    """A review left by one user (renter or owner) about the other."""

    def __init__(self, review_id, booking_id, reviewer_id, reviewee_id,
                 rating, comment=''):
        self._id = review_id
        self._booking_id = booking_id
        self._reviewer_id = reviewer_id
        self._reviewee_id = reviewee_id
        self._rating = rating
        self._comment = comment

    @property
    def id(self):
        return self._id

    @property
    def rating(self):
        return self._rating

    @property
    def comment(self):
        return self._comment

    def validate(self) -> bool:
        """Check if review is valid."""
        return isinstance(self._rating, int) and 1 <= self._rating <= 5
