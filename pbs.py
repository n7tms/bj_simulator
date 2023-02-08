# Python Blackjack Simulator
# https://www.youtube.com/watch?v=IPMcV_IXtX4

import random
import multiprocessing
import math
import time

simulations = 1000000
num_decks = 1
shuffle_perc = 75

def simulate(queue, batch_size):
    deck = []

    def new_deck():
        std_deck = [
            2,3,4,5,6,7,8,9,10,10,10,10,11,
        ] * 4

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
    print(deck)

    # play hands
    win = 0
    draw = 0
    lose = 0
    for i in range(0,batch_size):
        if (float(len(deck)) / (52 * num_decks)) * 100 < shuffle_perc:
            deck = new_deck()
        
        result = play_hand()

        if result == 1:
            win += 1
        if result == 0:
            draw += 1
        if result == -1:
            lose += 1
    
    queue.put([win,draw,lose])


start_time = time.time()

cpus = multiprocessing.cpu_count()
print(cpus)
batch_size = int(math.ceil(simulations / float(cpus)))

queue = multiprocessing.Queue()
processes = []

for i in range(0,cpus):
    process = multiprocessing.Process(target=simulate, args=(queue, batch_size))
    processes.append(process)
    process.start()

for proc in processes:
    proc.join()

finish_time = time.time() - start_time

win,draw,lose = 0,0,0

for i in range(0,cpus):
    results = queue.get()
    win += results[0]
    draw += results[1]
    lose += results[2]


print(f"Simulations: {simulations}")
print(f"wins: {win}")
print(f"draws: {draw}")
print(f"lose: {lose}")
print(f"execution time: {finish_time:.2f}")





