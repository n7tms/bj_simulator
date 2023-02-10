# Deck of cards using a generator
import random

class Cards:
    def __init__(self, num_of_decks=1, max_penetration=75) -> None:
        self.decks = num_of_decks
        self.shoe = self.shuffle()
        self.new_size = len(self.shoe)
        self.card_count = self.new_size
        assert max_penetration > 1 and max_penetration < 100, "max_penetrations must be between 1 and 100."
        self.penetration_limit = self.new_size * ((100 - max_penetration) / 100)


    def shuffle(self):
        values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        # suits = ['Spade','Heart','Club','Diamond']
        # a = list(product(values,suits)) * nod

        s = values * 4 * self.decks
        random.shuffle(s)
        return s

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.card_count < self.penetration_limit:
            self.shoe = self.shuffle()
            self.card_count = self.new_size
        self.card_count = len(self.shoe) - 1    # -1 because we give another card away after this statement.
        return self.shoe.pop(0)
        

