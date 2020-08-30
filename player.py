import colorful as cf

from game import Game, can_play, play_card, draw_card, Card, valid_play


def player_turn(game: Game):
    done = False
    play = False
    while not done:
        print_hand(game.player.hand)
        play = can_play(game, game.player.hand)
        if play:
            selected_card: int = int(
                input(f"Which card would you like to play? [Select 1 - {len(game.player.hand)}]\n"))
            if selected_card in range(1, len(game.player.hand + 1)):
                card: Card = game.player.hand[selected_card - 1]
                if valid_play(game, card):
                    play_card(game, game.player, game.computer, card)
                    play = True
                    done = True
                else:
                    print(f"{card.__repr__()} is not a valid play. Please try again.\n")
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
