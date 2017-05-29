# Some unit tests

from board import Board
from mock import patch
import sys
import main

# Create a board and check if the amount of cards is what we expect.


def test_board_card_count():
    board = Board(4)
    count = len(board.pile.draw_pile) + len(board.pile.discard_pile)
    for hand in board.hands:
        count += sum(1 for _ in filter(lambda x: x is not None, hand))
    assert(count == 52)

# Run a full example game with AIs
# Throwing no exceptions passes the test.


def test_full_example_run():
    testargs = [sys.argv[0], "Doro", "Rolf", "Judita"]
    with patch.object(sys, 'argv', testargs):
        full_example_run()


def full_example_run():
    game = main.Game()
    game.run_subgame()
    print(game)
