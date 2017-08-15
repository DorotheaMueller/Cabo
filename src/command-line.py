import player
from enum import Enum


class InteractivePlayer(Player):
    def __init__(self, name, index, player_count, player_indices):
        Player.__init__(self, name, index, player_count)
        self.player_indices = player_indices

    def turn(self, board):
        print(f"It is your turn now {self.name}.")
        print("Draw from the 'De(ck)', 'Di(scard)' or call 'C(abo)'.")

        action = get_player_initial_action(board.cabo_allowed())
        card = None

        if action is InitialMoves.CABO:
            board.call_cabo()
            print("You have called Cabo. Everyone but you is allowed one final move.")
            return

        elif action is InitialMoves.DECK:
            card = board.draw()
        elif action is InitialMoves.DISCARD:
            card = board.draw(False)

        print("You drew a {card}. What do you want to do with it?")
        print("Discard it or replace one of your cards.")

        if board.drawn_from_deck:
            if card == 7 or card == 8:
                print(
                    "Since this is a {card}, you may also 'peek' at one of your cards.")
                get_player_card_use(board, self.knowledge,
                                    self.index, peek_allowed=True)
            elif (card == 9 or card == 10) and self.index != 0:
                print(
                    "Since this is a {card}, you may also 'spy' at another player's card.")
                get_player_card_use(board, self.knowledge,
                                    self.index, spy_allowed=True)
            elif (card == 11 or card == 12) and self.index != 2:
                print(
                    "Since this is a {card}, you may also 'swap' one of your cards with another player's card.")
                get_player_card_use(board, self.knowledge,
                                    self.index, swap_allowed=True)
            else:
                print("This card has no special powers.")
                get_player_card_use(board, self.knowledge, self.index)
        else:
            print("This card has no special powers.")
            get_player_card_use(board, self.knowledge, self.index)


class InitialMoves(Enum):
    CABO = 1
    DECK = 2
    DISCARD = 3


def get_player_initial_action(cabo_allowed):
    string = input(" -> ")

    if match(string, "cabo"):
        if cabo_allowed:
            return InitialMoves.CABO
        else:
            print("You are not allowed to call Cabo after another player has done so.")
            return get_player_initial_action(cabo_allowed)

    else if match(string, "deck", 2):
        return InitialMoves.DECK

    else if match(string, "discard", 2):
        return InitialMoves.DISCARD

    else:
        print("Please type 'c', 'de' or 'di' for one of the allowed actions.")
        return get_player_initial_action(cabo_allowed)


def match(user_string, string_constant, min_length=1):
    if len(user_string.strip()) < min_length:
        return False
    return string_constant.lowercase().startswith(user_string.strip.lowercase())


def get_player_card_use(board, knowledge, player_index, peek_allowed=False, spy_allowed=False, swap_allowed=False):
    string = input(" -> ")

    # TODO: Use the whole string instead of only the first segment.
    segments = string.lowercase().split()

    if match(segments[0], "discard"):
        board.discard()
    elif match(segments[0], "replace"):
        print("Which card(s) do you want to replace?")
        positions = get_position(knowledge, player_index, multiple=True)
        if len(positions) == 1:
            board.replace_at(positions[0])
            return
        else:
            print("Which value do the cards at {positions} have?")
            value = get_value()
            board.replace_many(positions, value)
            return
    elif match(segments[0], "peek"):
        if not peek_allowed:
            print("You are not allowed to peek.")
            get_player_card_use(board, knowledge, player_index,
                                peek_allowed, spy_allowed, swap_allowed)

        print("Which card do you want to look at?")
        card_index = get_position(knowledge, player_index)
        board.peek_at(card_index)
    elif match(segments[0], "spy", 2):
        if not spy_allowed:
            print("You are not allowed to spy.")
            get_player_card_use(board, knowledge, player_index,
                                peek_allowed, spy_allowed, swap_allowed)

        print("Which player do you want to spy at?")
        spied_player = get_player(self.player_indices, player_index)
        print("Which card do you want to spy?")
        spied_card_index = get_position(knowledge, spied_player)
        board.spy_at(spied_player, spied_card_index)
    elif match(segments[0], "swap", 2):
        if not swap_allowed:
            print("You are not allowed to swap.")
            get_player_card_use(board, knowledge, player_index,
                                peek_allowed, spy_allowed, swap_allowed)

        print("Which own card do you want to swap out?")
        own_card_index = get_position(knowledge, player_index)
        print("Which player do you want to swap with?")
        swapped_player = get_player(self.player_indices, player_index)
        print("Which card do you want to swap with?")
        swapped_card_index = get_position(knowledge, swapped_player)
        board.swap_with(swapped_player, swapped_card_index, own_card_index)
    else:
        print("Command not recognized.")
        get_player_card_use(board, knowledge, player_index,
                            peek_allowed, spy_allowed, swap_allowed)


def get_position(knowledge, player_index, multiple=False):
    legal_position = get_legal_positions(knowledge, player_index)
    print(f"You still have cards at {legal_positions}.")
    card_position_input = input(" -> ")

    card_string_positions = card_position_input.split()
    card_positions = []
    for string_position in card_string_positions:
        try:
            position = int(string_position)
            if position not in legal_positions:
                raise ValueError(f"Position {position} does not hold a card.")
            card_positions.append(int(string_position))
        except ValueError as e:
            print(f"Wrong input: {e}")
            return get_position(knowledge, player_index, multiple)

    # Remove duplicates
    card_positions = list(set(card_positions))

    if not multiples and len(card_positions) != 1:
        print("You must provide precisely one position.")
        return get_position(knowledge, player_index, multiple)
    elif multiples and len(card_positions) = 0:
        print("You must provide at least one position.")
        return get_position(knowledge, player_index, multiple)

    if multiples:
        return card_positions
    else:
        return card_positions[0]


def get_player(player_indices, *forbidden_indices):
    string = input(" -> ")
    try:
        index = int(string)
    except ValueError:
        pass
    else:
        # If the user supplied a number, we execute this branch.
        if not 0 <= value < len(player_indices):
            print(
                f"The player index must be between 0 and {len(player_indices)-1} (inclusive).")
            print("You can also type the player's name.")
            print(f"Playing: {player_indices.keys()}")
            return get_player(player_indices, *forbidden_indices)
        elif index in forbidden_indices:
            print(f"The indices {forbidden_indices} are not allowed.")
            return get_player(player_indices, *forbidden_indices)
        else:
            return index

    # The user did not supply a number, we try to find a matching name.
    matching_names = []
    for key in player_indices.keys():
        if key.startswith(string):
            matching_indices.append(key)

    if len(matching_names) == 0:
        print(f"'{string}' does not match any name of {player_indices.keys()}.")
        return get_player(player_indices, *forbidden_indices)
    elif len(matching_names) == 1:
        index = player_indices[matching_names[0]]
        if index in forbidden_indices:
            print(f"The indices {forbidden_indices} are not allowed.")
            print(f"Player {matching_names[0]} has index {index}.")
            return get_player(player_indices, *forbidden_indices)
        else:
            return index
    else:
        print(f"Your query '{string}' matches {matching_names}.")
        print("Make sure to narrow it down to a single match.")
        return get_player(player_indices, *forbidden_indices)


def get_value():
    string = input(" -> ")
    try:
        value = int(string)
        if not 0 <= value <= 13:
            raise ValueError(
                f"The value must be between 0 and 13 (inclusive).")
        return value
    except ValueError as e:
        print(f"Wrong input: {e}")
        return get_value()


def get_legal_positions(knowledge, player_index):
    positions = []
    for card_index in range(4):
        if knowledge[player_index][card_index] is not None:
            positions.append(card_index)
