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

hards, softs, splits, bets, settings = None,None,None,None,None
deck = []

def parse_strategy(filename: str):
    with open(filename, 'r') as fn:
        data = json.load(fn)

    return data['Hard'],data['Soft'],data['Split'],data['Bets'],data['Settings'],


def build_deck(nod):
    """build a stack of cards based on the number of decks (nod) specified"""
    values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    # suits = ['Spade','Heart','Club','Diamond']
    # a = list(product(values,suits)) * nod
    a = values * 4 * nod
    random.shuffle(a)
    return a


def play_hand(bet: int, split: bool, dealer: list, player: list) -> int:    # return winnings (+bet = win; -bet = lose; 0 = draw)
    """arguments: 
            bet: the value of the bet
            split: if the hand has already been split (cannot split more than once)
            dealer: dealer's hand
            player: player's hand
        returns:
            the value of the bet
                bet x 2 means a win
                -bet means a loss
                0 means a draw                      """

    global deck

    print("Dealer:",dealer)
    print("Player:",player)

    getting_cards = True
    num_of_cards = 2
    while getting_cards:
        getting_cards = False
        # Dealer card
        d = dealer[0]

        print("Dealer", sum(dealer))
        print("Player",sum(player))

        # Dealer Blackjack?
        if sum(dealer) == 21:
            if sum(player) == 21 and num_of_cards == 2:
                return 0    # both got blackjack; return draw
            else:
                return -bet # only the dealer got blackjack; return lose
        
        # Player Blackjack?
        if sum(player) == 21 and num_of_cards == 2:
            return bet * 1.5

        action = None
        player_t = str(tuple(player))
        if player_t in splits:
            action = splits[player_t][dealer[0]-2]
        elif player_t in softs:
            action = softs[player_t][dealer[0]-2]
        elif str(sum(player)) in hards:
            action = hards[str(sum(player))][dealer[0]-2]
        
        print("action:",action)

        # Surrender?

        # Split?
        # outcome1 = play_hand(5,True)
        # outcome2 = play_hand(5,True)

        # Double?

        # Hit?
        # player.append(deck.pop(0))
        # getting_cards = True
    
    if sum(player) > 21:
        return -bet

    # Play the dealer's hand
    while sum(dealer) < 17:
        if sum(dealer) < 17:
            dealer.append(deck.pop(0))
        if sum(dealer) > 21 and 11 in dealer:
            dealer[dealer.index(11)] = 1


    # determine outcome
    if sum(dealer) == sum(player):
        return 0
    elif sum(player) > 21 or (sum(dealer) < 22 and sum(dealer) > sum(player)):
        return -bet
    else:
        return bet * 2




def simulate():
    # 

    global deck

    bet_index = 0
    winnings = 0
    max_bet_index = 0
    wins = 0
    losses = 0
    draws = 0


    for h in range(0,settings["Hands"]):
    # for h in range(0,2):
        if (float(len(deck)) / (52 * settings["Decks"])) * 100 < settings["ShufflePercent"]:
            deck = build_deck()

        print("\nHand: ",h)
        dealer = []
        player = []

        player.append(deck.pop(0))
        dealer.append(deck.pop(0))
        player.append(deck.pop(0))
        dealer.append(deck.pop(0))

        outcome = play_hand(bets[bet_index],False,dealer,player)
        winnings += outcome
        if outcome < 0:
            losses += 1
            bet_index +=1
            max_bet_index = max([bet_index,max_bet_index])
            if bet_index >= len(bets):
                nextbet = bet_index[-1]
        elif outcome == 0:
            draws += 1
        elif outcome > 0:
            wins += 1
            bet_index = 0


    # display the summary
    print("=========================================")
    print("Summary")
    print("=========================================")
    print("Hands:",settings["Hands"])
    print("Win:",wins)
    print("Loss:",losses)
    print("Draw:",draws)
    print("Winnings:",winnings)
    print("Losing Streak:",max_bet_index)
    print("=========================================")




# hards, softs, splits, bets, settings = parse_strategy("basic_strategy.pbs")
hards, softs, splits, bets, settings = parse_strategy("basic_strategy.pbs")

deck = build_deck(settings["Decks"])
print(deck)

simulate()

