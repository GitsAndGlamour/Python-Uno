import random
import colorful as cf

from computer import computer_turn
from player import player_turn


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
        elif len(self.computer.hand) ==0:
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
    print("{player} goes first".format(player=game.active_player.name))
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
        print("First play")
        return True
    last_card: Card = game.pile[-1]
    print("Last Card: [" + last_card.__repr__() + "] \n")
    if "Wild" in [card.action for card in hand]:  # Player has wild card
        return True
    elif "Wild" in last_card.action:
        if game.color in [card.color for card in hand]:  # Last card is Wild and Matching color picked
            return True
    elif last_card.color in [card.color for card in hand]:  # Matching color card
        return True
    elif last_card.number in [card.number for card in hand]:  # Matching number card
        return True
    if last_card.action in [card.action for card in hand] and last_card.action is not None:  # Matching action card
        return True
    else:
        return False


def perform_card_action(game: Game, player: Player, opponent: Player, card: Card):
    if "Draw 4" in card.action:
        for draw in range(0, 4):
            draw_card(game, opponent)
    elif "Draw 2" == card.action:
        for draw in range(0, 2):
            draw_card(game, opponent)
    elif "Skip" == card.action or "Reverse" == card.action:
        game.active_player = player


def play_card(game: Game, player: Player, opponent: Player, card: Card):
    player.hand.remove(card)
    game.pile.append(card)
    game.active_player = opponent
    if card.action is not None:
        perform_card_action(game, player, opponent, card)
