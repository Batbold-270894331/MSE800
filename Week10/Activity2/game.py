"""Main game logic for CLI Tic-tac-toe."""

import os
import sys

from board import Board
from player import Player


class TicTacToeGame:
    """Control the Tic-tac-toe game flow."""

    def __init__(self) -> None:
        """Initialize board and players."""
        self.board = Board()
        self.players = [
            Player("Player 1", "X"),
            Player("Player 2", "O"),
        ]
        self.current_player_index = 0

    @staticmethod
    def clear_screen() -> None:
        """Clear the command-line screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def exit_game() -> None:
        """Exit the game safely."""
        print("Goodbye!")
        sys.exit()

    @property
    def current_player(self) -> Player:
        """Return the current player."""
        return self.players[self.current_player_index]

    def display_header(self) -> None:
        """Display the game header."""
        print("=" * 35)
        print("        CLI TIC-TAC-TOE")
        print("=" * 35)
        print("Two-player game: Player 1 and Player 2")
        print("Player 1 uses X, Player 2 uses O.")
        print("Choose a position from 1 to 9.")
        print("Type 'exit' to quit the game.")
        print("Player 1 starts first.")

    def get_player_move(self) -> int:
        """Ask the current player to enter a valid move."""
        while True:
            move = input(
                f"{self.current_player.name} ({self.current_player.symbol}), "
                "choose position (1-9) or type exit: "
            ).strip().lower()

            if move == "exit":
                self.exit_game()

            if self.board.is_valid_move(move):
                return int(move) - 1

            print("Invalid move. Please choose an empty position from 1 to 9.")

    def switch_player(self) -> None:
        """Switch to the next player."""
        self.current_player_index = 1 - self.current_player_index

    def get_player_name_by_symbol(self, symbol: str) -> str:
        """Return player name by symbol."""
        for player in self.players:
            if player.symbol == symbol:
                return player.name

        return "Unknown Player"

    def show_result(self, winner_symbol: str | None) -> None:
        """Display the final game result."""
        self.board.display()

        if winner_symbol:
            winner_name = self.get_player_name_by_symbol(winner_symbol)
            print(f"{winner_name} ({winner_symbol}) wins!")
        else:
            print("The game is a draw!")

    def play(self) -> None:
        """Run the main game loop."""
        self.clear_screen()
        self.display_header()

        while True:
            self.board.display()

            position = self.get_player_move()
            self.board.update(position, self.current_player.symbol)

            self.clear_screen()

            winner_symbol = self.board.check_winner()

            if winner_symbol:
                self.show_result(winner_symbol)
                break

            if self.board.is_draw():
                self.show_result(None)
                break

            self.switch_player()