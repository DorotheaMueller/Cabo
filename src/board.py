"""This module contains all "physical" components.
"""

import random
import message

"""A Hand class which represents the true cards each player holds.
If a ._cardX is None, then the place is empty (by multiple-replace).
To indicate it holds a card this stores an integer."""


class Hand(object):
    def __init__(self, pile):
        self._card0 = pile.draw()
        self._card1 = pile.draw()
        self._card2 = pile.draw()
        self._card3 = pile.draw()

    def callback(self, max_peeks):
        return HandCallback(self, max_peeks)

    def __str__(self):
        return f"Hand({self._card0}, {self._card1}, {self._card2}, {self._card3})"

    def __repr__(self):
        return f"Hand({self._card0}, {self._card1}, {self._card2}, {self._card3})"

    def __getitem__(self, index):
        if index == 0:
            return self._card0
        elif index == 1:
            return self._card1
        elif index == 2:
            return self._card2
        elif index == 3:
            return self._card3
        else:
            raise IndexError("There are only four hand cards.")

    def __setitem__(self, index, value):
        if index == 0:
            self._card0 = value
        elif index == 1:
            self._card1 = value
        elif index == 2:
            self._card2 = value
        elif index == 3:
            self._card3 = value
        else:
            raise IndexError("There are only four hand cards.")


class HandCallback(object):
    def __init__(self, hand, max_peeks):
        self.hand = hand
        self.peeks_left = max_peeks

    def peek(self, index):
        if self.peeks_left <= 0:
            raise RuntimeError("You don't have any peeks left.")
        if 0 <= index < 4:
            self.peeks_left -= 1
            return self.hand[index]
        else:
            raise IndexError("The index must be in 0, 1, 2, 3.")


class Pile(object):
    def __init__(self):
        self.draw_pile = [0, 13] * 2 + list(range(1, 13)) * 4
        random.shuffle(self.draw_pile)

        self.discard_pile = []

        self.discard(self.draw())

        # TODO: Add size information functions
        # TODO: Somewhere save information over a reshuffle.
        # TODO: Count swaps in discard (and all other specials)
        #       Maybe have one counter per card.

    def draw(self):
        # FIXME: Handle empty pile.
        return self.draw_pile.pop()

    def discard(self, card):
        self.discard_pile.append(card)

    def discard_draw(self):
        return self.discard_pile.pop()

    def top_discard(self):
        return self.discard_pile[-1]

    def __str__(self):
        return f"""Pile Object:
        Draw Pile: {self.draw_pile}
        Discard Pile: {self.discard_pile}"""


class Board(object):
    def __init__(self, player_count):
        self.player_count = player_count
        self.pile = Pile()
        self.hands = []
        for _ in range(player_count):
            self.hands.append(Hand(self.pile))

    def __str__(self):
        return f"""Board Object:
    Hands: {self.hands}
    {self.pile}"""


class BoardCallback(object):
    def __init__(self, board, active_player):
        self._board = board
        self.active_player = active_player
        self.hand_card = None
        self.drawn_from_deck = False
        self.turn_over = False
        self.information = []

    def discard_pile_top(self):
        return self._board.pile.top_discard()

    def draw(self, from_draw_pile=True):
        assert(self.hand_card is None)
        assert(not self.turn_over)
        if from_draw_pile:
            self.hand_card = self._board.pile.draw()
            self.drawn_from_deck = True
        else:
            self.hand_card = self._board.pile.discard_draw()

        return self.hand_card

    def discard(self):
        assert(self.hand_card is not None)
        assert(not self.turn_over)
        self._board.pile.discard(self.hand_card)
        self.hand_card = None
        self.turn_over = True

    def replace_at(self, index):
        assert(self.hand_card is not None)
        assert(not self.turn_over)
        old_card = self._board.hands[self.active_player][index]
        assert(old_card is not None)  # You can't replace cards you don't have.
        self._board.pile.discard(old_card)
        self._board.hands[self.active_player][index] = self.hand_card

        # If the card was drawn from the discard pile, then this is
        # public information.
        replace_info = message.ReplaceInfo(
            not self.drawn_from_deck, self.active_player, index, self.hand_card)
        self.information.append(replace_info)

        self.hand_card = None
        self.turn_over = True

        return old_card
