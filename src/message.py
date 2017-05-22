class ReplaceInfo(object):
    def __init__(self, public, player_index, card_index, card):
        self.public = public
        self.player_index = player_index
        self.card_index = card_index
        self.card = card

    def apply(self, knowledge_matrix):
        knowledge_matrix[self.player_index][self.card_index] = self.card
