# Cabo main file!

import board
import sys


class Game(object):
    def __init__(self):
        # Read player names from command line arguments
        self.player_count = len(sys.argv) - 1
        assert(2 <= self.player_count <= 5)
        self.player_names = []
        for i in range(1, len(sys.argv)):
            self.player_names.append(sys.argv[i])

        self.players = [Player(self.player_names[i], i, self.player_count)
                        for i in range(self.player_count)]

        self.setup_subgame()

    def setup_subgame(self):
        self.board = board.Board(self.player_count)
        self.active_player = None

        for i, player in enumerate(self.players):
            player.new_game()
            player.pregame_peek(self.board.hands[i].callback(2))

    def run_subgame(self, active_player=0):
        self.active_player = active_player

        self.run_turn()
        self.run_turn()
        self.run_turn()

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
    Active Player: {self.active_player}"""


class Unknown(object):
    def __repr__(self):
        return "?"


unknown = Unknown()


class Player(object):
    def __init__(self, name, index, player_count):
        self.name = name
        self.index = index
        self.player_count = player_count

    def new_game(self):
        self.knowledge = [[unknown] * 4 for _ in range(self.player_count)]

    def pregame_peek(self, hand):
        self.knowledge[self.index][0] = hand.peek(0)
        self.knowledge[self.index][1] = hand.peek(1)

    def turn(self, board):
        # Wow, so much AI, so much clever.
        card = board.draw()
        board.replace_at(2)

    def update_knowledge(self, info):
        info.apply(self.knowledge)

    def __repr__(self):
        return f"Player({self.name}, {self.index}, {self.knowledge})"

    def __todo(self):
        pass
        # AI helper functions:
        #   - Check if there are pairs inside my own cards.
        #   - Check if a particular card would create a pair.
        #   - Track the discard pile over a reshuffle (maybe elsewhere).
        #   - Get (guarded) access to other players knowledge. (via BoardCallback)
        #   -


def main():
    game = Game()
    print(game)
    game.run_subgame()
    print(game)


if __name__ == "__main__":
    main()
