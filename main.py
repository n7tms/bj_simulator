# bj_simulator
# Blackjack Simulator
#
# Define a strategy and tell bjs how many iterations.
# bjs will play that number of hands and report:
#   - hands won
#   - hands lost
#   - profit/loss
#   - highest bet value
#   - total cumulative bet

from itertools import combinations, product
import random

number_of_decks = 1


def build_cards(nod):
    """build a stack of cards based on the number of decks (nod) specified"""
    values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    suits = ['Spade','Heart','Club','Diamond']
    return list(product(values,suits)) * nod


def shuffle(d):
    """Shuffle Deck"""
    deck = []
    while d:
        # rnd_card = random.choice(whole_deck)
        deck.append(d.pop(d.index(random.choice(d))))
    return deck


deck = shuffle(build_cards(number_of_decks))
print(deck)
