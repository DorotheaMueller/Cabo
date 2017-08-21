from helper import unknown


class CardInfo(object):
    def __init__(self, public, player_index, card_index, card):
        self.public = public
        self.player_index = player_index
        self.card_index = card_index
        self.card = card

    def apply(self, knowledge_matrix, further_knowledge):
        knowledge_matrix[self.player_index][self.card_index] = self.card

    def display(self):
        return f"Player {self.player_index} now has a {self.card} at position {self.card_index}."


class ClearInfo(object):
    def __init__(self, player, index):
        self.public = True
        self.player = player
        self.index = index

    def apply(self, knowledge_matrix, further_knowledge):
        knowledge_matrix[self.player][self.index] = unknown

    def display(self):
        return f"Player {self.player} has replaced their card at {self.index} with an unknown card."


class SwapInfo(object):
    def __init__(self, swap_player, swap_index, own_player, own_index):
        self.public = True
        self.swap_player = swap_player
        self.swap_index = swap_index
        self.own_player = own_player
        self.own_index = own_index

    def apply(self, knowledge_matrix, further_knowledge):
        tmp = knowledge_matrix[self.swap_player][self.swap_index]
        knowledge_matrix[self.swap_player][self.swap_index] = knowledge_matrix[self.own_player][self.own_index]
        knowledge_matrix[self.own_player][self.own_index] = tmp

    def display(self):
        return f"Player {self.own_player} swapped their own card at {self.own_index} with player {self.swap_player}'s card at {self.swap_index}."


class CaboInfo(object):
    def __init__(self, called_cabo):
        self.public = True
        self.called_cabo = called_cabo

    def apply(self, knowledge_matrix, further_knowledge):
        further_knowledge.called_cabo = self.called_cabo

    def display(self):
        return f"The player {self.called_cabo} called cabo."
