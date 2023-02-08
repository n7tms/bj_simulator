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
import json

number_of_decks = 1
strategy = "{16:['S','S','S','S','S','H','H','Sr','Sr','Sr']}"

def parse_strategy(filename: str):
    whole_file = ""

    with open(filename, 'r') as fn:
        data = json.load(fn)

    return data['Hard'],data['Soft'],data['Split'],data['Bets'],data['Settings'],



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


# deck = shuffle(build_cards(number_of_decks))

# hards, softs, splits, bets, settings = parse_strategy("basic_strategy.pbs")
hards, softs, splits, bets, settings = parse_strategy("small_strategy.pbs")
print(bets)
print(settings["Decks"])
