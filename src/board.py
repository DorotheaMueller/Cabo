"""This module contains all "physical" components.
"""

import random
import message

"""A Hand class which represents the true cards each player holds.
If a ._cardX is None, then the place is empty (by multiple-replace).
To indicate it holds a card this stores an integer."""


class Hand(object):
    def __init__(self, pile):
        self._card0, _ = pile.draw()
        self._card1, _ = pile.draw()
        self._card2, _ = pile.draw()
        self._card3, _ = pile.draw()

    def callback(self, max_peeks):
        return HandCallback(self, max_peeks)

    def sum(self):
        with_default = lambda x: x if x is not None else 0
        return (with_default(self._card0) + with_default(self._card1) +
                with_default(self._card2) + with_default(self._card3))

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

        self.discard(self.draw()[0])

        # TODO: Add size information functions
        # TODO: Somewhere save information over a reshuffle.
        # TODO: Count swaps in discard (and all other specials)
        #       Maybe have one counter per card.


    def draw(self):
        # Returns tuple: First the drawn card, then whether the pile has been shuffled.
        try:
            return (self.draw_pile.pop(), False)
        except IndexError:
            random.shuffle(self.discard_pile)
            self.draw_pile = self.discard_pile
            self.discard_pile = []
            return (self.draw_pile.pop(), True)

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
        self.called_cabo = None

    def __str__(self):
        return f"""Board Object:
    Hands: {self.hands}
    {self.pile}
    Called Cabo: {self.called_cabo}"""


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
            self.hand_card, reshuffle = self._board.pile.draw()
            self.drawn_from_deck = True
        else:
            self.hand_card = self._board.pile.discard_draw()

        return self.hand_card

    def call_cabo(self):
        assert(self.hand_card is None)
        assert(not self.turn_over)
        assert(self._board.called_cabo is None)
        self._board.called_cabo = self.active_player
        cabo_info = message.CaboInfo(self.active_player)
        self.information.append(cabo_info)
        self.turn_over = True

    def cabo_allowed(self):
        if self._board.called_cabo is None:
            return True
        else:
            return False

    def discard(self):
        assert(self.hand_card is not None)
        assert(not self.turn_over)
        self._board.pile.discard(self.hand_card)
        self.hand_card = None
        self.turn_over = True

    def peek_at(self, index):
        assert(self.hand_card is not None)
        assert(self.hand_card == 8 or self.hand_card == 7)
        assert(self.drawn_from_deck)
        assert(not self.turn_over)
        peek_card = self._board.hands[self.active_player][index]
        assert(peek_card is not None)
        peek_info = message.CardInfo(False, self.active_player, index, peek_card)
        self.information.append(peek_info)
        self._board.pile.discard(self.hand_card)
        self.hand_card = None
        self.turn_over = True

    def spy_at(self, spied_player, index):
        assert(self.hand_card is not None)
        assert(self.hand_card == 9 or self.hand_card == 10)
        assert(self.drawn_from_deck)
        assert(not self.turn_over)
        spied_card = self._board.hands[spied_player][index]
        assert(spied_card is not None)
        assert(spied_player is not self.active_player)
        spy_info = message.CardInfo(False, spied_player, index, spied_card)
        self.information.append(spy_info)
        self._board.pile.discard(self.hand_card)
        self.hand_card = None
        self.turn_over = True

    def swap_with(self, swap_player, swap_index, own_index):
        assert(self.hand_card is not None)
        assert(self.hand_card == 11 or self.hand_card == 12)
        assert(self.drawn_from_deck)
        assert(not self.turn_over)
        assert(self.active_player is not swap_player)
        swap_card = self._board.hands[swap_player][swap_index]
        assert(swap_card is not None)
        own_card = self._board.hands[self.active_player][own_index]
        assert(own_card is not None)

        self._board.hands[self.active_player][own_index] = swap_card
        self._board.hands[swap_player][swap_index] = own_card

        swap_info = message.SwapInfo(swap_player, swap_index, self.active_player, own_index)
        self.information.append(swap_info)

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

        # Possible knowledge is cleared.
        self.information.append(message.ClearInfo(self.active_player, index))

        # If the card was drawn from the discard pile, then this is
        # public information.
        replace_info = message.CardInfo(
            not self.drawn_from_deck, self.active_player, index, self.hand_card)
        self.information.append(replace_info)

        self.hand_card = None
        self.turn_over = True

        return old_card

    def replace_many(self, indices, card_value):
        assert(self.hand_card is not None)
        assert(not self.turn_over)
        assert(len(indices) >= 2)
        assert(isinstance(card_value, int))

        index_counter = {}

        correct_value_named = True
        for i in indices:
            index_counter[i] = index_counter.setdefault(i, 0) + 1
            card = self._board.hands[self.active_player][i]
            assert(card is not None)
            correct_value_named = correct_value_named and card == card_value

        for k, v in index_counter.items():
            # check if each index was only used once.
            assert(v == 1)

        if correct_value_named:
            for i in indices:
                self._board.pile.discard(self._board.hands[self.active_player][i])
                # There are no cards.
                self._board.hands[self.active_player][i] = None
                self.information.append(message.CardInfo(True, self.active_player, i, None))
            self._board.hands[self.active_player][indices[0]] = self.hand_card
            # One replace card, but it depends on the publicity of the draw whether it is known.
            self.information.append(message.ClearInfo(self.active_player, indices[0]))
            self.information.append(message.CardInfo(not self.drawn_from_deck, self.active_player, indices[0], self.hand_card))

            self.hand_card = None
            self.turn_over = True
        else:
            # Broadcast all information and discard
            self._board.pile.discard(self.hand_card)
            for i in indices:
                self.information.append(message.CardInfo(True, self.active_player, i, self._board.hands[self.active_player][i]))
            self.hand_card = None
            self.turn_over = True
