from game import Game, Card, can_play, play_card, draw_card, valid_play


def computer_turn(game: Game):
    done = False
    play = False
    while not done:
        print_hand_count(game.computer.hand)
        play = can_play(game, game.computer.hand)
        if play:
            card: Card = valid_card(game, game.computer.hand)
            play_card(game, game.computer, game.player, card)
            play = True
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
