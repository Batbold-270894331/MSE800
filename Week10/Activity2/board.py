"""Board logic for Tic-tac-toe game."""

from typing import Optional


class Board:
    """Represent the Tic-tac-toe board."""

    BOARD_SIZE = 9

    WINNING_COMBINATIONS = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self) -> None:
        """Initialize the board with positions 1 to 9."""
        self.cells = [str(number) for number in range(1, self.BOARD_SIZE + 1)]

    def display(self) -> None:
        """Display the current board."""
        print()
        print("┌───┬───┬───┐")
        print(f"│ {self.cells[0]} │ {self.cells[1]} │ {self.cells[2]} │")
        print("├───┼───┼───┤")
        print(f"│ {self.cells[3]} │ {self.cells[4]} │ {self.cells[5]} │")
        print("├───┼───┼───┤")
        print(f"│ {self.cells[6]} │ {self.cells[7]} │ {self.cells[8]} │")
        print("└───┴───┴───┘")
        print()

    def is_valid_move(self, move: str) -> bool:
        """Check whether the move is valid."""
        if not move.isdigit():
            return False

        position = int(move)

        if position < 1 or position > self.BOARD_SIZE:
            return False

        return self.cells[position - 1] not in ("X", "O")

    def update(self, position: int, symbol: str) -> None:
        """Update the board with the player's symbol."""
        self.cells[position] = symbol

    def check_winner(self) -> Optional[str]:
        """Return the winner symbol if there is a winner."""
        for first, second, third in self.WINNING_COMBINATIONS:
            if self.cells[first] == self.cells[second] == self.cells[third]:
                return self.cells[first]

        return None

    def has_possible_win(self, symbol: str) -> bool:
        """Check whether a player still has a possible winning line."""
        opponent = "O" if symbol == "X" else "X"

        for first, second, third in self.WINNING_COMBINATIONS:
            line = [self.cells[first], self.cells[second], self.cells[third]]

            if opponent not in line:
                return True

        return False

    def is_draw(self) -> bool:
        """Check whether the game is a draw."""
        return not self.has_possible_win("X") and not self.has_possible_win("O")