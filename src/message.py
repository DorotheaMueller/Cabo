from main import unknown

class CardInfo(object):
    def __init__(self, public, player_index, card_index, card):
        self.public = public
        self.player_index = player_index
        self.card_index = card_index
        self.card = card

    def apply(self, knowledge_matrix, further_knowledge):
        knowledge_matrix[self.player_index][self.card_index] = self.card

class ClearInfo(object):
    def __init__(self, player, index):
        self.public = True
        self.player = player
        self.index = index

    def apply(self, knowledge_matrix, further_knowledge):
        knowledge_matrix[self.player][self.index] = unknown

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

class CaboInfo(object):
    def __init__(self, called_cabo):
        self.public = True
        self.called_cabo = called_cabo

    def apply(self, knowledge_matrix, further_knowledge):
        further_knowledge.called_cabo = self.called_cabo
