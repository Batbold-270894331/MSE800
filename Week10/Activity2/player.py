"""Player model for Tic-tac-toe game."""


class Player:
    """Represent a Tic-tac-toe player."""

    def __init__(self, name: str, symbol: str) -> None:
        """Initialize player name and symbol."""
        self.name = name
        self.symbol = symbol