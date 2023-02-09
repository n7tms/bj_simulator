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
import csv
import time

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

def play_player(player_hand: list, dealer_card: int, split_already: bool) -> int:
    """Plays the players hand; returns the value of the hand (1=BJ)"""
    player_outcome = 0



    return player_outcome


def play_dealer(dealer_hand: list) -> int:
    """Plays the dealer's hand; return the value of the hand (1=BJ)"""
    global deck

    dealer_sum = sum(dealer_hand)
    while dealer_sum < 17:
        if dealer_sum < 17:
            dealer_hand.append(deck.pop(0))
        if dealer_sum > 21 and 11 in dealer_hand:
            dealer_hand[dealer_hand.index(11)] = 1
        dealer_sum = sum(dealer_hand)
        
    return dealer_sum


def play_hand(bet: int, dealer_hand: list, player_hand: list) -> int:
    """setup for playing the round; does either have BJ? Returns the value (bet) of the win/loss"""


def play_hand2(bet: int, split: bool, dealer: list, player: list) -> int:    # return winnings (+bet = win; -bet = lose; 0 = draw)
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


    # print("Dealer:",dealer)
    # print("Player:",player)

    getting_cards = True
    num_of_cards = 2
    out1,out2 = 0,0

    while getting_cards:
        getting_cards = False

        # print("Dealer", sum(dealer))
        # print("Player",sum(player))

        # Dealer Blackjack?
        if sum(dealer) == 21:
            if sum(player) == 21 and num_of_cards == 2:
                return 0    # both got blackjack; return draw
            else:
                return -bet # only the dealer got blackjack; return lose
        
        # Player Blackjack?
        if sum(player) == 21 and num_of_cards == 2 and split == False:
            return bet * 1.5

        # Bust?
        if sum(player) > 21 and num_of_cards > 2:
            return -bet
        
        # If the player has more than 3 cards, combine them
        if len(player) > 2:
            player = sorted(player)
            x = player.pop(0) + player.pop(0)
            player.insert(0,x)
            # print(player)

        action = None
        player_t = str(tuple(sorted(tuple(player))))
        if player_t in splits and split == False and num_of_cards == 2:
            action = splits[player_t][dealer[0]-2]
        elif player_t in softs:
            action = softs[player_t][dealer[0]-2]
        elif str(sum(player)) in hards:
            action = hards[str(sum(player))][dealer[0]-2]
        
        # print("action:",action)
        match action:
            case "S":   # Stand
                getting_cards = False
            case "H":   # Hit
                player.append(deck.pop(0))
                if sum(player) > 21 and 11 in player:
                    player[player.index(11)] = 1
                num_of_cards += 1
                getting_cards = True
            case "Sr":  # Surrender, or hit
                if settings["Surrender"] == 'Y':
                    getting_cards = False
                else:
                    player.append(deck.pop(0))
                    getting_cards = True
                    num_of_cards += 1
            case "D":   # Double
                if num_of_cards == 2 and ((split == True and settings["DAS"] == 'Y') or split == False):
                    player.append(deck.pop(0))
                    getting_cards = False
                    num_of_cards += 1
                    bet += bet
                else:   # Can't double; just hit
                    player.append(deck.pop(0))
                    getting_cards = True
                    num_of_cards += 1

            case "Ds":  # Double, or stand
                if num_of_cards == 2:   # double allowed
                    player.append(deck.pop(0))
                    getting_cards = False
                    num_of_cards += 1
                    bet += bet
                else:
                    getting_cards = False
            case "Y":   # Split
                p1 = [player[0]]
                p2 = [player[1]]
                p1.append(deck.pop(0))
                p2.append(deck.pop(0))
                out1 = play_hand(bet,True,dealer,p1)
                out2 = play_hand(bet,True,dealer,p2)
                bet = out1 + out2
                getting_cards = False
            case "Da":  # Split if double after split allowed
                # TODO currently treating this like a normal split
                p1 = [player[0]]
                p2 = [player[1]]
                p1.append(deck.pop(0))
                p2.append(deck.pop(0))
                out1 = play_hand(bet,True,dealer,p1)
                out2 = play_hand(bet,True,dealer,p2)
                return out1 + out2
            case _:
                pass

# TODO When player splits, both hands need to play out, then the dealer's hand plays, then an outcome is determined.
# TODO Currently, first hand plays, dealer plays, outcome, second hand, dealer plays, outcome
# TODO Wrong!

    if sum(player) > 21 or (action == 'Sr' and getting_cards == False):
        return -bet

    # Play the dealer's hand
    while sum(dealer) < 17 and split == False:
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
        return bet




def simulate():
    # 

    global deck

    
    bet_count = 0
    winnings = 0
    max_bet_count = 0
    nextbet = 0
    wins = 0
    losses = 0
    draws = 0


    for h in range(0,settings["Hands"]):
    # for h in range(0,2):
        if (float(len(deck)) / (52 * settings["Decks"])) * 100 < settings["ShufflePercent"]:
            deck = build_deck(settings["Decks"])

        # print("\nHand: ",h)
        dealer = []
        player = []

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        deck = [11,9,11,3,10,9,4,5,6]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        player.append(deck.pop(0))
        dealer.append(deck.pop(0))
        player.append(deck.pop(0))
        dealer.append(deck.pop(0))

        outcome = play_hand(bets[nextbet],False,dealer,player)
        winnings += outcome
        if outcome < 0:
            losses += 1
            bet_count +=1
            max_bet_count = max([bet_count,max_bet_count])
            if bet_count >= len(bets):
                # nextbet = len(bets) - 1
                nextbet = 0
            else:
                nextbet = bet_count
        elif outcome == 0:
            draws += 1
        elif outcome > 0:
            wins += 1
            bet_count = 0
            nextbet = 0


    # display the summary
    print("=========================================")
    print("Summary")
    print("=========================================")
    print("Hands:",settings["Hands"])
    print("Win:",wins)
    print("Loss:",losses)
    print("Draw:",draws)
    print("Winnings:",winnings)
    print("Losing Streak:",max_bet_count)
    print("=========================================")




# hards, softs, splits, bets, settings = parse_strategy("basic_strategy.pbs")
hards, softs, splits, bets, settings = parse_strategy("basic_strategy.pbs")

deck = build_deck(settings["Decks"])
# print(deck)

start_time = time.time()
simulate()
duration = time.time() - start_time
print(f"Execution time: {duration:.2f}")


# TODO write summary to a csv file so we can use Excel to graph it....or PyPlot?

# Potential bets
# [5,15,30,60]
# [5,15,30,60,60,60,180,240,480,1000]
# [5,11,23,47,95,191,383,767]