from game import Game, Player, Card
from setup import generate_cards, deal_cards


def test_generate_cards():
    game: Game = Game(
        deck=[],
        pile=[],
        top_card=0,
        active_player=None,
        color=None,
        player=Player(name="Player", hand=[]),
        computer=Player(name="Computer", hand=[]))
    generate_cards(game)
    assert len(game.deck) == 108
    for number in range(0, 10):
        occurrence = count_occurrences(game.deck, number)
        if number == 0:
            assert occurrence == 4
        else:
            assert occurrence == 8
    for action in ["Draw 2", "Skip", "Reverse"]:
        assert count_occurrences(game.deck, action) == 8

    for wild in ["Wild", "Wild Draw 4"]:
        assert count_occurrences(game.deck, wild) == 4


def test_deal_cards():
    cards: [Card] = []
    for card in range(0, 10):
        cards.append(Card(color="red", number=card, action=None))
        cards.append(Card(color="yellow", number=card, action=None))
    game: Game = Game(
        deck=cards,
        pile=[],
        top_card=0,
        active_player=None,
        color=None,
        player=Player(name="Player", hand=[]),
        computer=Player(name="Computer", hand=[]))
    deal_cards(game)
    assert game.top_card == 14
    assert len(game.player.hand) == 7
    assert len(game.computer.hand) == 7
    assert game.player.hand == cards[0:7]
    assert game.computer.hand == cards[7:14]


def count_occurrences(cards: [Card], element: str or int):
    count = 0
    for card in cards:
        if card.number == element or card.action == element:
            count += 1
    return count


if __name__ == "__main__":
    test_generate_cards()
    print("Everything passed!")
