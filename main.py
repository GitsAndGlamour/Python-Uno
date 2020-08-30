import random

from game import Game, new_game, start_game
from setup import setup_game


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
