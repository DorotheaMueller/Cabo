# Cabo main file!

import board
import sys
import random
from player import RandomPlayer, HeuristicPlayer
from commandLine import InteractivePlayer
import argparse
from helper import match

class Game(object):
    def __init__(self, debug=False):
        parser = argparse.ArgumentParser(description = 'Argument parser to start the game Cabo.')
        parser.add_argument('-d', '--debug', action='store_true', help = 'If you would like the whole game output for debugging.')

        parser.add_argument('-p', '--player', action = 'append', nargs = '+', metavar = ('player_type', 'name'))
        args = parser.parse_args()
        # args = parser.parse_args(['-d', '-p', 'h', 'Sara', '-p', 'h', 'Rolf', '-p', 'r'])

        player_types = set(['r', 'h', 'i', 'random', 'human', 'intelligent'])
        default_names = ['Primus', 'Secundus', 'Tertius', 'Quartus', 'Quintus']
        name_set = set()
        # Only 2 to 5 players.
        assert(2 <= len(args.player) <= 5)
        for i,l in enumerate(args.player):
            print(l[0].lower())
            assert(l[0].lower() in player_types)
            assert(len(l) <= 2)
            if len(l) == 1:
                l.append('Player ' + default_names[i])
            name_set.add(args.player[i][1].lower())
        # Only unique names.
        assert(len(name_set) == len(args.player))

        # Create game.
        self.debug = args.debug
        self.player_count = len(args.player)
        self.player_names = [l[1] for l in args.player]
        self.player_indices = {l[1]:i for i,l in enumerate(args.player)}
        self.players = []
        for l in args.player:
            self.create_player(*l)

        self.total_scores = [0] * self.player_count
        self.setup_subgame()

    def create_player(self, player_type, player_name):
        player_type = player_type.lower()
        if match(player_type, 'random'):
            self.players.append(RandomPlayer(player_name, self.player_indices[player_name], self.player_count))
        elif match(player_type, 'intelligent'):
            self.players.append(HeuristicPlayer(player_name, self.player_indices[player_name], self.player_count))
        elif match(player_type, 'human'):
            self.players.append(InteractivePlayer(player_name, self.player_indices[player_name], self.player_count, self.player_indices))

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
            if self.debug:
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
    game.run_subgame()
    print("Final state:")
    print(game)


if __name__ == "__main__":
    main()
