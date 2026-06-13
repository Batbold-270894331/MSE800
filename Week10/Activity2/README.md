# Tic-tac-toe Game

Player 1 uses **X**.
Player 2 uses **O**.

## Features

* Two-player CLI game
* Input validation
* Screen clears after each valid move
* Exit command support
* Winner checking
* Early draw checking when no player can win

## Project Structure

```text
tic-tac-toe/
│
├── main.py
├── game.py
├── board.py
├── player.py
└── README.md
```

## File Description

| File        | Description                                             |
| ----------- | ------------------------------------------------------- |
| `main.py`   | Application entry point                                 |
| `game.py`   | Controls the main game flow                             |
| `board.py`  | Handles board display, moves, winner, and draw checking |
| `player.py` | Defines the player model                                |
| `README.md` | Project documentation                                   |

## Game Rules

- Tic-tac-toe is played on a 3x3 board.
- Each player takes turns choosing a position from 1 to 9.
- The first player who places three symbols in a row wins.

Winning lines can be:

* horizontal
* vertical
* diagonal

If no player can win anymore, the game ends as a draw.

## Requirements

Python 3.8 or higher is recommended.

No external package is required to run the game.

## How to Run

Open the terminal in the project folder and run:

```bash
python main.py
```
### `Board` class

The `Board` class manages the game board.

* displaying the board
* validating moves
* updating cells
* checking the winner
* checking draw condition

### `TicTacToeGame` class

The `TicTacToeGame` class controls the main game flow.

* starting the game
* showing the header
* getting player input
* switching players
* clearing the screen
* showing the final result

### `main.py`

The `main.py` file starts the application.

## Main Classes and Methods

| Class           | Method               | Description                            |
| --------------- | -------------------- | -------------------------------------- |
| `Player`        | `__init__()`         | Creates a player with name and symbol  |
| `Board`         | `display()`          | Displays the board                     |
| `Board`         | `is_valid_move()`    | Checks if the move is valid            |
| `Board`         | `update()`           | Updates the board cell                 |
| `Board`         | `check_winner()`     | Checks if a player has won             |
| `Board`         | `has_possible_win()` | Checks if a player can still win       |
| `Board`         | `is_draw()`          | Checks if the game is a draw           |
| `TicTacToeGame` | `play()`             | Runs the main game loop                |
| `TicTacToeGame` | `get_player_move()`  | Gets input from the current player     |
| `TicTacToeGame` | `switch_player()`    | Switches between Player 1 and Player 2 |
| `TicTacToeGame` | `show_result()`      | Displays the winner or draw result     |
| `TicTacToeGame` | `clear_screen()`     | Clears the terminal screen             |
| `TicTacToeGame` | `exit_game()`        | Exits the game safely                  |

## Screenshots

### Game Screenshot

![Tic-tac-toe Game Screenshot](screenshot.png)

### Pylint Result

![Pylint Result Screenshot](pylint.png)