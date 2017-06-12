# Some unit tests

from board import Board
from mock import patch
import sys
import main

# To do: Check if knowledge of players is consistent with actual cards.

def test_board_card_count():
    """Create a board and check if the amount of cards is what we expect."""

    board = Board(4)
    count = len(board.pile.draw_pile) + len(board.pile.discard_pile)
    for hand in board.hands:
        count += sum(1 for _ in filter(lambda x: x is not None, hand))
    assert(count == 52)


def test_full_example_run():
    """Run a full example game with AIs
    Throwing no exceptions passes the test."""

    testargs = [sys.argv[0], "Doro", "Rolf", "Judita"]
    with patch.object(sys, 'argv', testargs):
        full_example_run()


def full_example_run():
    game = main.Game()
    game.run_subgame()
    print(game)

def test_knowledge_consistency():
    """Run a full example game with AIs
    Throwing no exceptions passes the test."""

    testargs = [sys.argv[0], "Doro", "Rolf", "Judita", "Sara"]
    with patch.object(sys, 'argv', testargs):
        knowledge_testing_run()

def knowledge_testing_run():
    game = main.Game()

    # A modified copy of game.run_subgame()
    game.active_player = 0
    while game.active_player != game.board.called_cabo:
        game.run_turn()
        verify_knowledge_consistency(game)

def verify_knowledge_consistency(game):
    for player in game.players:
        for player_index in range(len(player.knowledge)):
            for card_index in range(4):
                believe = player.knowledge[player_index][card_index]
                truth = game.board.hands[player_index][card_index]
                if believe != main.unknown:
                    assert(believe == truth)
