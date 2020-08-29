import random
import colorful as cf


class Card:
    def __init__(self, color: str, number: int or None, action: str or None):
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
        else:
            text = cf.blue(text)
        return text


class Player:
    def __init__(self, name: str, hand: [Card]):
        self.name = name
        self.hand = hand


class Rules:
    @staticmethod
    def colors():
        return ['red', 'yellow', 'green', 'blue']

    @staticmethod
    def actions():
        return [
            'do_nothing',
            'Draw 2',
            'Skip',
            'Reverse',
            'Draw 4',
            'Wild'
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


class Game:
    def __init__(self, deck: [Card], draw_card: int, player: Player, computer: Player):
        self.deck = deck
        self.draw_card = draw_card
        self.player = player
        self.computer = computer

    def is_won(self):
        return len(self.player.hand) == 0


def get_cards(game: Game):
    for color in Rules.colors():
        for number in Rules.numbers():
            card = Card(color=color, number=number, action=None)
            game.deck.append(card)


def deal_cards(game: Game):
    for card in range(0, 7):
        game.player.hand.append(game.deck[card])
        game.computer.hand.append(game.deck[card + 1])
        game.draw_card = card + 2


def shuffle_cards(game: Game):
    random.shuffle(game.deck)


def new_game():
    return Game(
        deck=[],
        draw_card=0,
        player=Player(name="Player", hand=[]),
        computer=Player(name="Computer",
                        hand=[]))


def setup_game(game: Game):
    get_cards(game)
    shuffle_cards(game)
    deal_cards(game)


def determine_first_player(game: Game):
    players: [Player] = [game.player, game.computer]
    random.shuffle(players)
    print(players[0].name, players[1].name)
    return players[0]


def player_turn(game: Game):
    return None


def computer_turn(game: Game):
    return None


def start_game(game: Game):
    current_player: Player = determine_first_player(game)
    print("{player} goes first".format(player=current_player.name))
    if current_player.name == "Player":
        player_turn(game)
    else:
        computer_turn(game)


def play_again():
    answer: str = input("Would you like to play again?\n[Enter 'yes' or 'y' to play again.]\n").lower()
    return answer == "yes" or answer == "y"


def get_wins(games: [Game]):
    wins = 0
    for game in games:
        if game.is_won():
            wins += 1
    return wins


def run_uno():
    games: [Game] = [new_game()]
    for game in games:
        setup_game(game)
        start_game(game)
        if play_again():
            games.append(new_game())
        else:
            print("You won {wins} out of {total} games".format(wins=get_wins(games), total=len(games)))


if __name__ == '__main__':
    run_uno()
