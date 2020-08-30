import random

from game import Game, Card


class Rules:
    @staticmethod
    def colors():
        return ['red', 'yellow', 'green', 'blue']

    @staticmethod
    def actions():
        return [
            'Skip',
            'Reverse',
            'Draw 2',
            'Wild',
            'Wild Draw 4',
        ]

    @staticmethod
    def numbers():
        return range(0, 10)

    @staticmethod
    def game_over(game):
        return len(game.player.hand) == 0 or len(game.computer.hand) == 0

    @staticmethod
    def is_uno(game):
        return len(game.player.hand) == 1 or len(game.computer.hand) == 1


def setup_game(game: Game):
    generate_cards(game)
    shuffle_cards(game)
    deal_cards(game)


def generate_cards(game: Game):
    for color in Rules.colors():
        for number in Rules.numbers():
            card: Card = Card(color=color, number=number, action=None)
            game.deck.append(card)
            if number != 0:
                game.deck.append(card)

        for action in Rules.actions():
            action_color = color
            if "Wild" in action:
                action_color = None

            card: Card = Card(color=action_color, number=None, action=action)
            game.deck.append(card)

            if "Wild" not in action:
                game.deck.append(card)


def shuffle_cards(game: Game):
    random.shuffle(game.deck)


def deal_cards(game: Game):
    for card in range(0, 7):
        game.player.hand.append(game.deck[card])
        game.computer.hand.append(game.deck[card + 1])
        game.top_card = card + 2
