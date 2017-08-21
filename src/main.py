# Cabo main file!

import board
import sys
import random
from player import RandomPlayer
from commandLine import InteractivePlayer

class Game(object):
    def __init__(self):
        # # Read player names from command line arguments
        # self.player_count = len(sys.argv) - 1
        # assert(2 <= self.player_count <= 5)
        # # TODO: assert that all player names are unique.
        # # TODO: Build a player dictionary and pass it to interactive players.
        # self.player_names = []
        # for i in range(1, len(sys.argv)):
        #     self.player_names.append(sys.argv[i])

        self.player_count = 3
        self.player_names = ["Sara", "Rolf", "Doro"]
        self.player_indices = {"Sara":0, "Rolf":1, "Doro":2}
        self.players = [RandomPlayer("Sara", 0, 3), RandomPlayer("Rolf", 1, 3),
            InteractivePlayer("Doro", 2, 3, self.player_indices)]

        # self.players = [RandomPlayer(self.player_names[i], i, self.player_count)
        #                 for i in range(self.player_count)]
        self.total_scores = [0] * self.player_count

        self.setup_subgame()

    def run_game(self):
        self.run_subgame()
        while max(self.total_scores) < 100:
            self.setup_subgame()
            self.run_subgame()

    def setup_subgame(self):
        self.board = board.Board(self.player_count)
        self.active_player = None

        for i, player in enumerate(self.players):
            player.new_game()
            player.pregame_peek(self.board.hands[i].callback(2))

    def run_subgame(self, active_player=0):
        self.active_player = active_player

        while self.active_player != self.board.called_cabo:
            self.run_turn()
            print(self)

        self.score_game()

    def score_game(self):
        scores = [hand.sum() for hand in self.board.hands]
        min_score = min(scores)
        if scores[self.board.called_cabo] == min_score:
            scores[self.board.called_cabo] = 0
            # todo: sum scores over many games
        else:
            # Punish cabo player for their wrong guess
            scores[self.board.called_cabo] += 5
            for i in range(self.player_count):
                score = scores[i]
                if score == min_score:
                    scores[i] = 0

        for i in range(self.player_count):
            self.total_scores[i] += scores[i]
            if self.total_scores[i] == 100:
                self.total_scores[i] = 50

    def run_turn(self):
        board_callback = board.BoardCallback(self.board, self.active_player)
        self.players[self.active_player].turn(board_callback)
        for info in board_callback.information:
            if info.public:
                for player in self.players:
                    player.update_knowledge(info)
            else:
                self.players[self.active_player].update_knowledge(info)

        self.active_player = (self.active_player + 1) % self.player_count

    def __str__(self):
        return f"""Game object:
    Board: {self.board}
    Players: {self.players}
    Scores: {self.total_scores}
    Active Player: {self.active_player}"""

def main():
    game = Game()
    print(game)
    game.run_subgame()
    print(game)


if __name__ == "__main__":
    main()
