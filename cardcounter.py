# Card Counting Practice

import cards
import time

print("Card Counting Practice")
print("2-6: +1")
print("7-9: 0")
print("T-A: -1")

# get from user delay between cards
# ask user if print running count periodically
# ask user how many cards to display at a time
#
# while true:
#   display x cards
#   wait y seconds
#   display count?

delay = 0
while delay<1 or delay>9:
    delay = input("Delay between cards (1-9 seconds): ")
    if delay.isnumeric():
        delay = int(delay)
        if delay > 0 and delay < 10:
            break
    delay = 0
    print("Delay must be an integer between 1 and 9, inclusive.\n")

run_cnt = 'n'
while run_cnt == 'n':
    run_cnt = input("Periodically display running count (y/n):")
    if run_cnt == 'y' or run_cnt == 'n':
        break
    print("respond with y or n only, please.\n")

crd_dsp = 0
while crd_dsp < 1 or crd_dsp > 6:
    crd_dsp = input("How many cards to display (1-6): ")
    if crd_dsp.isnumeric():
        crd_dsp = int(crd_dsp)
        if crd_dsp > 0 and crd_dsp < 10:
            break
    print("You can display 1 to 6 cards.\n")

rounds = 0
running_count = 0
deck = cards.Cards(1,99)
while True:
    rounds += 1
    cards_to_show = []
    for i in range(crd_dsp):
        next_card = next(deck)
        if next_card < 7:
            running_count += 1
        elif next_card > 9:
            running_count -= 1
        cards_to_show.append(next_card)
    
    print("cards: ",cards_to_show)
    time.sleep(delay)
    if rounds % 5 == 0:
        print("Running count: ",running_count)

    if rounds > 10:
        print("Ending Running Count:",running_count)
        break

