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
    return data['Hard'],data['Soft'],data['Split'],data['Bets'],data['Settings']


def build_deck(number_of_decks):
    """build a stack of cards based on the number of decks specified"""
    values = [2,3,4,5,6,7,8,9,10,10,10,10,11]

    # TODO At some future date, I'll incorporate card suits; but for now, they are not needed.
    # suits = ['Spade','Heart','Club','Diamond']
    # a = list(product(values,suits)) * nod

    # Build the shoe; 4 different suits * the number of decks specified.
    shoe = values * 4 * number_of_decks

    # Shuffle everything together
    random.shuffle(shoe)
    return shoe

def play_player(player_hand: list, dealer_card: int, split_already: bool) -> int:
    """Plays the players hand; returns the value of the hand"""
    player_outcome = 0
    doubled = 1
    num_of_cards = 2

    getting_cards = True
    while getting_cards:
        getting_cards = False

        # If the player has more than 3 cards, combine them
        if len(player_hand) > 2:
            player = sorted(player_hand)
            x = player_hand.pop(0) + player_hand.pop(0)
            player_hand.insert(0,x)
            # print(player)

        action = None
        player_t = str(tuple(sorted(tuple(player_hand))))
        if player_t in splits and split_already == False and num_of_cards == 2:
            action = splits[player_t][dealer_card-2]
        elif player_t in softs:
            action = softs[player_t][dealer_card-2]
        elif str(sum(player_hand)) in hards:
            action = hards[str(sum(player_hand))][dealer_card-2]
        
        # print("action:",action)
        match action:
            case "S":   # Stand
                getting_cards = False
            case "H":   # Hit
                player_hand.append(deck.pop(0))
                if sum(player_hand) > 21 and 11 in player_hand:
                    player_hand[player_hand.index(11)] = 1
                num_of_cards += 1
                getting_cards = True
            case "Sr":  # Surrender, or hit
                if settings["Surrender"] == 'Y':
                    getting_cards = False
                else:
                    player_hand.append(deck.pop(0))
                    getting_cards = True
                    num_of_cards += 1
            case "D":   # Double
                if num_of_cards == 2 and ((split_already == True and settings["DAS"] == 'Y') or split_already == False):
                    player_hand.append(deck.pop(0))
                    getting_cards = False
                    num_of_cards += 1
                    doubled = 2
                else:   # Can't double; just hit
                    player_hand.append(deck.pop(0))
                    getting_cards = True
                    num_of_cards += 1

            case "Ds":  # Double, or stand
                if num_of_cards == 2:   # double allowed
                    player_hand.append(deck.pop(0))
                    getting_cards = False
                    num_of_cards += 1
                    doubled = 2
                else:
                    getting_cards = False

            case "Y":   # Split
                # This case is handled before the hand is played (in play_hand())
                pass

            case "Da":  # Split if double after split allowed
                # This case is handled before the hand is played (in play_hand())
                pass
            case _:
                pass

    return sum(player_hand), doubled


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


def play_hand(bet: int) -> int:
    """setup for playing the round; does either have BJ? Returns the value (bet) of the win/loss"""
    global deck

    # Deal the cards
    dealer = []
    player = []
    player.append(deck.pop(0))
    dealer.append(deck.pop(0))
    player.append(deck.pop(0))
    dealer.append(deck.pop(0))

    # Does the dealer AND the player have blackjack?
    if sum(dealer) == 21 and sum(player) == 21:
        return 0
    
    # Does the dealer have blackjack?
    if sum(dealer) == 21:
        return -bet
    
    # Does the player have blackjack?
    if sum(player) == 21:
        return bet * 1.5

    # Play the player's hand
    p_out1,p_out2 = 0,0
    p_dub1,p_dub2 = 1,1

    player_t = str(tuple(sorted(tuple(player))))
    if player_t in splits and (splits[player_t][dealer[0]-2] == 'Y' or (splits[player_t][dealer[0]-2] == 'Da' and settings["DAS"] == 'Y')):
        player1 = [player[0],deck.pop(0)]
        player2 = [player[1],deck.pop(0)]
        p_out1,p_dub1 = play_player(player1,dealer[0],True)
        p_out2,p_dub2 = play_player(player2,dealer[0],True)
    else:
        p_out1,p_dub1 = play_player(player,dealer[0],False)

    # Play the dealer's hand
    d_out = play_dealer(dealer)

    # Determine the outcome of the round
    total_outcome = 0
    if d_out > p_out1:
        total_outcome -= bet * p_dub1
    if d_out < p_out1:
        total_outcome += bet * p_dub1
    
    if p_out2 > 0:
        if d_out > p_out2:
            total_outcome -= bet * p_dub2
        if d_out < p_out2:
            total_outcome += bet * p_dub2

    return total_outcome


def simulate():
    """ """
    global deck

    bet_count = 0
    winnings = 0
    max_bet_count = 0
    nextbet = 0
    wins = 0
    losses = 0
    draws = 0

    for h in range(0,settings["Rounds"]):
    # for h in range(0,2):
        if (float(len(deck)) / (52 * settings["Decks"])) * 100 < settings["MaxPenetration"]:
            deck = build_deck(settings["Decks"])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # deck = [11,9,11,3,10,9,4,2,6]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        outcome = play_hand(bets[nextbet])
        winnings += outcome
        if outcome < 0:
            losses += 1
            bet_count +=1
            max_bet_count = max([bet_count,max_bet_count])
            if bet_count >= len(bets):
                nextbet = len(bets) - 1
                # nextbet = 0
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
    print("Hands:",settings["Rounds"])
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

