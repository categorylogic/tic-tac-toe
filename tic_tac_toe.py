"""
Terminal Tic-Tac-Toe game supporting human vs. human or human vs. computer play.
Run `python tic_tac_toe.py` to start.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import random


@dataclass
class Player:
    name: str
    marker: str
    is_computer: bool = False


class Board:
    def __init__(self) -> None:
        self.cells: List[Optional[str]] = [None] * 9

    def display(self) -> None:
        def mark(value: Optional[str], index: int) -> str:
            return value if value is not None else str(index + 1)

        rows = [
            " | ".join(mark(self.cells[i + j], i + j) for j in range(3))
            for i in range(0, 9, 3)
        ]
        separator = "\n---------\n"
        print("\n" + separator.join(rows) + "\n")

    def available_moves(self) -> List[int]:
        return [i for i, value in enumerate(self.cells) if value is None]

    def place_marker(self, position: int, marker: str) -> bool:
        if position not in range(9) or self.cells[position] is not None:
            return False
        self.cells[position] = marker
        return True

    def winner(self) -> Optional[str]:
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),  # diagonals
        ]
        for a, b, c in win_conditions:
            if self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def is_full(self) -> bool:
        return all(cell is not None for cell in self.cells)


class TicTacToe:
    def __init__(self, player_one: Player, player_two: Player) -> None:
        self.board = Board()
        self.players = [player_one, player_two]
        self.current_turn = 0

    def play(self) -> None:
        while True:
            current_player = self.players[self.current_turn]
            self.board.display()
            move = self._get_move(current_player)
            if move is None:
                print("No moves available. Ending game.")
                return
            self.board.place_marker(move, current_player.marker)

            winner = self.board.winner()
            if winner:
                self.board.display()
                print(f"{current_player.name} wins! Congratulations!\n")
                break
            if self.board.is_full():
                self.board.display()
                print("It's a draw!\n")
                break
            self.current_turn = 1 - self.current_turn

    def _get_move(self, player: Player) -> Optional[int]:
        if player.is_computer:
            move = self._computer_move(player.marker)
            print(f"{player.name} chooses position {move + 1}.")
            return move
        return self._human_move(player)

    def _human_move(self, player: Player) -> Optional[int]:
        while True:
            try:
                choice = input(f"{player.name} ({player.marker}), enter position (1-9): ")
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted.")
                return None
            if not choice.strip().isdigit():
                print("Please enter a number between 1 and 9.")
                continue
            position = int(choice) - 1
            if position not in range(9):
                print("Choose a position between 1 and 9.")
                continue
            if not self.board.place_marker(position, player.marker):
                print("That spot is taken. Try again.")
                continue
            return position

    def _computer_move(self, marker: str) -> int:
        opponent_marker = self.players[1 - self.current_turn].marker
        # Win if possible
        for move in self.board.available_moves():
            if self._would_win(move, marker):
                return move
        # Block opponent win
        for move in self.board.available_moves():
            if self._would_win(move, opponent_marker):
                return move
        # Take center if free
        if 4 in self.board.available_moves():
            return 4
        # Pick random remaining corner or side
        return random.choice(self.board.available_moves())

    def _would_win(self, move: int, marker: str) -> bool:
        snapshot = list(self.board.cells)
        snapshot[move] = marker
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for a, b, c in win_conditions:
            if snapshot[a] and snapshot[a] == snapshot[b] == snapshot[c]:
                return True
        return False


def choose_game_mode() -> tuple[Player, Player]:
    while True:
        mode = input("Play vs computer? (y/n): ").strip().lower()
        if mode in {"y", "yes"}:
            name = input("Enter your name: ") or "Player"
            return Player(name=name, marker="X"), Player(name="Computer", marker="O", is_computer=True)
        if mode in {"n", "no"}:
            name1 = input("Player 1 name: ") or "Player 1"
            name2 = input("Player 2 name: ") or "Player 2"
            return Player(name=name1, marker="X"), Player(name=name2, marker="O")
        print("Please answer with 'y' or 'n'.")


def main() -> None:
    print("=== Tic-Tac-Toe ===")
    player_one, player_two = choose_game_mode()
    game = TicTacToe(player_one, player_two)
    game.play()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
