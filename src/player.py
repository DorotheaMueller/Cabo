from helper import unknown
from abc import ABC, abstractmethod
import random

class FurtherKnowledge(object):
    def __init__(self):
        self.called_cabo = None

class Player(ABC):
    def __init__(self, name, index, player_count):
        self.name = name
        self.index = index
        self.player_count = player_count

    def new_game(self):
        self.knowledge = [[unknown] * 4 for _ in range(self.player_count)]
        self.further_knowledge = FurtherKnowledge()

    def pregame_peek(self, hand):
        self.knowledge[self.index][0] = hand.peek(0)
        self.knowledge[self.index][1] = hand.peek(1)

    @abstractmethod
    def turn(self, board):
        pass

    def update_knowledge(self, info):
        info.apply(self.knowledge, self.further_knowledge)

    def __repr__(self):
        return f"Player({self.name}, {self.index}, {self.knowledge}; multiples: {identify_multiple_cards(self.knowledge[self.index])})"

    def __todo(self):
        pass
        # AI helper functions:
        #   - Check if there are pairs inside my own cards.
        #   - Check if a particular card would create a pair.
        #   - Track the discard pile over a reshuffle (maybe elsewhere).
        #   - Get (guarded) access to other players knowledge. (via BoardCallback)
        #   -


def random_other_player_index(knowledge, player_index):
    other_player_index = random.randrange(len(knowledge)-1)
    if other_player_index >= player_index:
        return player_index + 1
    else:
        return other_player_index


def random_card_index(knowledge, player_index):
    while True:
        card_index = random.randrange(4)
        card = knowledge[player_index][card_index]
        if card is not None:
            return card_index

def identify_multiple_cards(cards):
    """Takes a list of knowledge [3, 5, ?, 5] and returns a list
    of multiples: {5 : [1,3]}. Here '5 : [1,3]' means that a five known
    both at position 1 and 3."""
    index_by_value = {}
    for i in range(4):
        if isinstance(cards[i], int):
            index_by_value.setdefault(cards[i], []).append(i)

    return {k: v for k, v in index_by_value.items() if len(v) >= 2}

class RandomPlayer(Player):
    def turn(self, board):
        # Wow, so much AI, so much clever.

        multiples = identify_multiple_cards(self.knowledge[self.index])
        for card_value, indices in multiples.items():
            # This loop is run at most once, as we return from turn().
            card = board.draw()
            board.replace_many(indices, card_value)
            return

        if random.random() < 0.15 and board.cabo_allowed():
            board.call_cabo()

        else:
            card = board.draw()
            if card == 7 or card == 8:
                card_index = random_card_index(self.knowledge, self.index)
                board.peek_at(card_index)
            elif (card == 9 or card == 10) and self.index != 0:
                other_index = random_other_player_index(self.knowledge, self.index)
                card_index = random_card_index(self.knowledge, other_index)
                board.spy_at(other_index, card_index)
            elif (card == 11 or card == 12) and self.index != 2:
                card_index = random_card_index(self.knowledge, self.index)
                other_index = random_other_player_index(self.knowledge, self.index)
                other_card_index = random_card_index(self.knowledge, other_index)
                board.swap_with(other_index, other_card_index, card_index)
            else:
                card_index = random_card_index(self.knowledge, self.index)
                board.replace_at(card_index)


class HeuristicPlayer(Player):
    def turn(self, board):
        if self.should_cabo():
            board.call_cabo()
            return

        draw_discarded_card = false
        # TODO: Add conditions, when we take the discarded card

        if draw_discarded_card:
            # Passing False draws from the discard pile
            card = board.draw(False)
            raise("Unimplemented")

        card = board.draw()

        if self.has_card(card):
            raise("Unimplemented")

        if card == 7 or card == 8:
            self.peek(board, card)
        elif (card == 9 or card == 10) and self.index != 0:
            self.spy(board, card)
        elif (card == 11 or card == 12) and self.index != 2:
            self.swap(board, card)
        else:
            self.plain_card(board, card)

    def peek(self, board, card):
        # Look at the first unknown card or discard the peek card.
        own_knowlede = self.knowledge[self.index]
        for i in range(4):
            if own_knowlede[i] is unknown:
                board.peek_at(i)
                return
        self.plain_card(board, card)

    def spy(self, board, card):
        # TODO
        other_index = random_other_player_index(self.knowledge, self.index)
        card_index = random_card_index(self.knowledge, other_index)
        board.spy_at(other_index, card_index)

    def swap(self, board, card):
        # TODO
        card_index = random_card_index(self.knowledge, self.index)
        other_index = random_other_player_index(self.knowledge, self.index)
        other_card_index = random_card_index(self.knowledge, other_index)
        board.swap_with(other_index, other_card_index, card_index)

    def plain_card(self, board, card):
        # TODO
        card_index = random_card_index(self.knowledge, self.index)
        board.replace_at(card_index)

    def has_card(self, card):
        # Do we know that we already have the card?
        for i in range(4):
            believe = self.knowledge[self.index][i]
            if believe == card:
                return True
        return False

    def should_cabo(self):
        """The Heuristic Player calls cabo if it knows all cards and has
        at most 10 points."""
        accumulator = 0
        for card in self.knowledge[self.index]:
            if isinstance(card, int):
                accumulator += card
            elif card is unknown:
                return False

        return accumulator <= 10
