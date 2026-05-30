"""
Review Service
==============
Manages reviews submitted after bookings.
"""

from database.db_manager import DatabaseManager


class ReviewService:
    """Service for managing reviews."""

    def __init__(self):
        self.db = DatabaseManager()

    def submit_review(self, booking_id, reviewer_id, reviewee_id,
                       rating, comment='') -> tuple:
        """Submit a review for a completed booking."""
        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return False, "Rating must be an integer between 1 and 5"

        # Check booking exists and is approved/completed
        booking = self.db.fetch_one(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        )
        if not booking:
            return False, "Booking not found"
        if booking['status'] not in ('approved', 'completed'):
            return False, "Can only review approved/completed bookings"

        # Check duplicate review
        existing = self.db.fetch_one("""
            SELECT id FROM reviews
            WHERE booking_id = ? AND reviewer_id = ?
        """, (booking_id, reviewer_id))
        if existing:
            return False, "You already reviewed this booking"

        # Insert
        try:
            self.db.execute("""
                INSERT INTO reviews
                  (booking_id, reviewer_id, reviewee_id, rating, comment)
                VALUES (?, ?, ?, ?, ?)
            """, (booking_id, reviewer_id, reviewee_id, rating, comment))
            return True, "Review submitted. Thanks for your feedback!"
        except Exception as e:
            return False, f"Failed to submit review: {e}"

    def get_user_avg_rating(self, user_id) -> float:
        """Calculate average rating received by a user."""
        row = self.db.fetch_one("""
            SELECT AVG(rating) AS avg_rating, COUNT(*) AS count
            FROM reviews WHERE reviewee_id = ?
        """, (user_id,))
        if row and row['count'] > 0:
            return round(row['avg_rating'], 2)
        return 0

    def get_reviews_for_user(self, user_id):
        return self.db.fetch_all("""
            SELECT r.*, u.name AS reviewer_name
            FROM reviews r
            JOIN users u ON r.reviewer_id = u.id
            WHERE r.reviewee_id = ?
            ORDER BY r.id DESC
        """, (user_id,))
