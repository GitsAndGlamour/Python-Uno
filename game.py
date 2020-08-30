import random
import colorful as cf


class Card:
    def __init__(self, color: str or None, number: int or None, action: str or None):
        self.color = color
        self.number = number
        self.action = action

    def __repr__(self):
        text = str(self.number)
        if self.number is None:
            text = self.action

        if self.color == "red":
            text = cf.red(text)
        elif self.color == "green":
            text = cf.green(text)
        elif self.color == "yellow":
            text = cf.yellow(text)
        elif self.color == "blue":
            text = cf.blue(text)
        return text


class Player:
    def __init__(self, name: str, hand: [Card]):
        self.name = name
        self.hand = hand


class Game:
    def __init__(self,
                 deck: [Card],
                 pile: [Card],
                 top_card: int,
                 player: Player,
                 computer: Player,
                 active_player: Player or None,
                 color: str or None,
                 ):
        self.deck = deck
        self.pile = pile
        self.top_card = top_card
        self.active_player = active_player
        self.player = player
        self.computer = computer
        self.color = color

    def is_won(self):
        return len(self.player.hand) == 0

    def is_over(self):
        if len(self.player.hand) == 0:
            return self.player
        elif len(self.computer.hand) == 0:
            return self.computer
        else:
            return None


def new_game():
    return Game(
        deck=[],
        pile=[],
        top_card=0,
        active_player=None,
        color=None,
        player=Player(name="Player", hand=[]),
        computer=Player(name="Computer", hand=[]))


def determine_first_player(game: Game):
    players: [Player] = [game.player, game.computer]
    random.shuffle(players)
    return players[0]


def start_game(game: Game):
    game.active_player = determine_first_player(game)
    print("{player} goes first!\n".format(player=game.active_player.name))
    winner = None
    while winner is None:
        winner = game.is_over()
        if winner is not None:
            print(f"{winner} has won!")
            return
        else:
            if game.active_player.name == game.player.name:
                player_turn(game)
            else:
                computer_turn(game)


def draw_card(game: Game, player: Player):
    top_card = game.deck[game.top_card]
    player.hand.append(top_card)
    game.top_card += 1


def can_play(game: Game, hand: [Card]):
    if len(game.pile) == 0:
        return True
    last_card: Card = game.pile[-1]
    print("Last Card: [" + last_card.__repr__() + "] \n")
    if "Wild" in [card.action for card in hand]:  # Player has wild card
        return True
    if last_card.action is not None:
        if "Wild" in last_card.action and game.color in [card.color for card in hand]:  # Last card is Wild
            return True
        elif last_card.action in [card.action for card in hand] and last_card.action is not None:  # Matching action card
            return True
    elif last_card.color in [card.color for card in hand]:  # Matching color card
        return True
    elif last_card.number in [card.number for card in hand]:  # Matching number card
        return True
    else:
        return False


def perform_card_action(game: Game, player: Player, opponent: Player, card: Card):
    if "Draw 4" in card.action:
        for draw in range(0, 4):
            draw_card(game, opponent)
        game.active_player = player
    elif "Draw 2" == card.action:
        for draw in range(0, 2):
            draw_card(game, opponent)
        game.active_player = player
    elif "Skip" == card.action or "Reverse" == card.action:
        game.active_player = player
    if "Wild" in card.action:
        color = None
        while color is None:
            selected_color = int(input(
                f"What is the color?\n 1. {cf.red('red')} "
                f"2. {cf.yellow('yellow')}  "
                f"3. {cf.green('green')}  "
                f"4. {cf.blue('blue')} "))
            if selected_color == 1:
                color = 'red'
            elif selected_color == 2:
                color = 'yellow'
            elif selected_color == 3:
                color = 'green'
            elif selected_color == 4:
                color = 'blue'
            else:
                print(f"{selected_color} is not a valid response.\n")


def play_card(game: Game, player: Player, opponent: Player, card: Card):
    player.hand.remove(card)
    game.pile.append(card)
    game.active_player = opponent
    if card.action is not None:
        perform_card_action(game, player, opponent, card)


def valid_play(game: Game, card: Card):
    if len(game.pile) == 0:
        return True

    last_card: Card = game.pile[-1]
    if card.action is not None:
        if "Wild" in card.action:  # If Wild, choose a color set
            return True
        elif card.action == last_card.action:
            return True
    if last_card.action is not None:
        if "Wild" in last_card.action and card.color == game.color:
            return True
        elif card.action == last_card.action:
            return True
    elif card.color == last_card.color:
        return True
    elif card.number == last_card.number:
        return True
    else:
        return False


def computer_turn(game: Game):
    done = False
    while not done:
        print_hand_count(game.computer.hand)
        play = can_play(game, game.computer.hand)
        if play:
            card: Card = valid_card(game, game.computer.hand)
            play_card(game, game.computer, game.player, card)
            done = True
        else:
            print("Computer is drawing a card...")
            draw_card(game, game.computer)


def valid_card(game: Game, hand: [Card]):
    for card in hand:
        if valid_play(game, card):
            return card


def print_hand_count(hand: [Card]):
    print(f"Computer has {len(hand)} cards.")


def player_turn(game: Game):
    done = False
    while not done:
        print_hand(game.player.hand)
        play = can_play(game, game.player.hand)
        if play:
            selected_card: int = int(
                input(f"Which card would you like to play? [Select 1 - {len(game.player.hand)}]\n"))
            if selected_card in range(1, len(game.player.hand) + 1):
                card: Card = game.player.hand[selected_card - 1]
                print(f"You selected [{card.__repr__()}].\n")
                if valid_play(game, card):
                    play_card(game, game.player, game.computer, card)
                    done = True
                else:
                    print(f"[{card.__repr__()}] is not a valid play. Please try again.\n")
            else:
                print(f"Uh oh! {selected_card} is not a valid selection.\n")
        else:
            input("Looks like you don't have any cards you can play. Please press Enter to continue.\n")
            draw_card(game, game.player)


def print_hand(hand: [Card]):
    hand_display: [str] = ""
    for index, card in enumerate(hand):
        hand_display += (f"{index + 1}: [" + card.__repr__() + "] ")
    print(hand_display + "\n")
