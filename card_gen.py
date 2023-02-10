# Deck of cards using a generator


import random

def deck(nod=1):
    def shuffle_deck():
        values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        shoe = values * 4 * nod
        random.shuffle(shoe)
        return shoe
    
    shoe = shuffle_deck()
    deck_size = len(shoe)
    while True:
        if len(shoe) > deck_size * .25:
            yield shoe.pop(0)
        else:
            shuffle_deck()
            yield shoe.pop(0)


# card = deck(1)

# for _ in range(52):
#     print(next(card))


def gen():
    def init():
        return 0
    i = init()
    while True:
        val = (yield i)
        if val=='restart':
            i = init()
        else:
            i += 1


g = gen()
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(g.send('restart'))
print(next(g))
print(next(g))
print(next(g))
