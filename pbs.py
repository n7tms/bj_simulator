import random
import multiprocessing
import math
import time

simulations = 100000
num_decks = 4
shuffle_perc = 75

def simulate(queue, batch_size):
    deck = []

    def new_deck():
        std_deck = [
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
        ]

        std_deck = std_deck * num_decks
        random.shuffle(std_deck)
        return std_deck
    
    def play_hand():
        dealer = []
        player = []

        player.append(deck.pop(0))
        dealer.append(deck.pop(0))
        player.append(deck.pop(0))
        dealer.append(deck.pop(0))
        
        while sum(player) < 12:
            player.append(deck.pop(0))
        
        while sum(dealer) < 18:
            exit = False
            if sum(dealer) == 17:
                exit = True
                for i,card in enumerate(dealer):
                    if card == 11:
                        exit = False
                        dealer[i] = 1
            if exit:
                break

            dealer.append(deck.pop(0))

        p_sum = sum(player)
        d_sum = sum(dealer)

        if d_sum > 21:
            return 1;
        if d_sum == p_sum:
            return 0;
        if d_sum > p_sum:
            return -1
        if d_sum < p_sum:
            return 1
        
    # starting deck
    deck = new_deck()

    # play hands
    win = 0
    draw = 0
    lose = 0
    for i in range(0,simulations):
        if (float(len(deck)) / (52 * num_decks)) * 100 < shuffle_perc:
            deck = new_deck()
        
        result = play_hand()

        if result == 1:
            win += 1
        if result == 0:
            draw += 1
        if result == -1:
            lose += 1
    
    print(f"Simulations: {simulations}")
    print(f"wins: {win}")
    print(f"draws: {draw}")
    print(f"lose: {lose}")


simulate(0,0)




