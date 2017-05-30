class ReplaceInfo(object):
    def __init__(self, public, player_index, card_index, card):
        self.public = public
        self.player_index = player_index
        self.card_index = card_index
        self.card = card

    def apply(self, knowledge_matrix, further_knowledge):
        knowledge_matrix[self.player_index][self.card_index] = self.card

class CaboInfo(object):
    def __init__(self, called_cabo):
        self.public = True
        self.called_cabo = called_cabo

    def apply(self, knowledge_matrix, further_knowledge):
        further_knowledge.called_cabo = self.called_cabo
