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


class Game:
    def __init__(self, deck: [Card], pile: [Card], top_card: int, player: Player, computer: Player):
        self.deck = deck
        self.pile = pile
        self.top_card = top_card
        self.player = player
        self.computer = computer

    def is_won(self):
        return len(self.player.hand) == 0


def get_cards(game: Game):
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


def deal_cards(game: Game):
    for card in range(0, 7):
        game.player.hand.append(game.deck[card])
        game.computer.hand.append(game.deck[card + 1])
        game.top_card = card + 2


def shuffle_cards(game: Game):
    random.shuffle(game.deck)


def new_game():
    return Game(
        deck=[],
        pile=[],
        top_card=0,
        player=Player(name="Player", hand=[]),
        computer=Player(name="Computer", hand=[]))


def setup_game(game: Game):
    get_cards(game)
    shuffle_cards(game)
    deal_cards(game)


def determine_first_player(game: Game):
    players: [Player] = [game.player, game.computer]
    random.shuffle(players)
    return players[0]


def valid_play(game: Game, card: Card):
    if len(game.pile[-1]) == 0:
        return True

    last_card: Card = game.pile[-1]
    if "Wild" in last_card.action:
        print("It's starting to get complicated here...")



def play_card(game: Game, card: Card):
    return None


def print_hand(hand: [Card]):
    hand_display: [str] = ""
    for index, card in enumerate(hand):
        hand_display += (f"{index + 1}: [" + card.__repr__() + "] ")
    print(hand_display + "\n")


def can_play(game: Game, hand: [Card]):
    if len(game.pile) == 0:
        print("First play")
        return True
    last_card: Card = game.pile[-1]
    print("Last Card: [" + last_card.__repr__() + "] \n")
    if "Wild" in [card.action for card in hand]:
        return True
    elif last_card.color in [card.color for card in hand]:
        return True
    elif last_card.number in [card.number for card in hand]:
        return True
    if last_card.action in [card.action for card in hand] and last_card.action is not None:
        return True
    else:
        return False


def draw_card(game: Game, player: Player):
    top_card = game.deck[game.top_card]
    player.hand.append(top_card)
    game.top_card += 1


def player_turn(game: Game):
    done = False
    play = False
    while not done:
        print_hand(game.player.hand)
        play = can_play(game, game.player.hand)
        if play:
            selected_card: int = int(
                input(f"Which card would you like to play? [Select 1 - {len(game.player.hand)}]\n"))
            if selected_card in range(1, 8):
                card: Card = game.player.hand[selected_card - 1]
                if valid_play(game, card):
                    play_card(game, card)
                    play = True
                    done = True
                else:
                    print(f"{card.__repr__()} is not a valid play. Please try again.\n")
            else:
                print(f"Uh oh! {selected_card} is not a valid selection.\n")
        else:
            enter = input("Looks like you don't have any cards you can play. Please press Enter to continue.\n")
            draw_card(game, game.player)


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
