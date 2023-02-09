# bj_simulator
Blackjack Simulator to evaluate different strategies

Define a strategy for both the dealer and the player.
Define a betting structure.
Set the game parameters:
- Number of decks
- number of hands to play

Tracked Statistics
- hands won
- hands lost
- profit/loss
- highest bet value
- total cumulative bet

It might also be beneficial to track the card count and factor that into the betting strategy


## Strategy Syntax
A JSON file that defines what to do for hard values, soft values, and splits, as well as some settings.
For example, here is a basic strategy:

```
{    
    "Hard": {
        "20":["S","S","S","S","S","S","S","S","S","S"],
        "19":["S","S","S","S","S","S","S","S","S","S"],
        "18":["S","S","S","S","S","S","S","S","S","S"],
        "17":["S","S","S","S","S","S","S","S","S","S"],
        "16":["S","S","S","S","S","H","H","Sr","Sr","Sr"],
        "15":["S","S","S","S","S","H","H","H","Sr","H"],
        "14":["S","S","S","S","S","H","H","H","H","H"],
        "13":["S","S","S","S","S","H","H","H","H","H"],
        "12":["H","H","S","S","S","H","H","H","H","H"],
        "11":["D","D","D","D","D","D","D","D","D","D"],
        "10":["D","D","D","D","D","D","D","D","H","H"],
        "9":["H","D","D","D","D","H","H","H","H","H"],
        "8":["H","H","H","H","H","H","H","H","H","H"],
        "7":["H","H","H","H","H","H","H","H","H","H"],
        "6":["H","H","H","H","H","H","H","H","H","H"],
        "5":["H","H","H","H","H","H","H","H","H","H"],
        "4":["H","H","H","H","H","H","H","H","H","H"]
    },

    "Soft" : {
        "(9, 11)":["S","S","S","S","S","S","S","S","S","S"],
        "(8, 11)":["S","S","S","S","Ds","S","S","S","S","S"],
        "(7, 11)":["Ds","Ds","Ds","Ds","Ds","S","S","H","H","H"],
        "(6, 11)":["H","D","D","D","D","H","H","H","H","H"],
        "(5, 11)":["H","H","D","D","D","H","H","H","H","H"],
        "(4, 11)":["H","H","D","D","D","H","H","H","H","H"],
        "(3, 11)":["H","H","H","D","D","H","H","H","H","H"],
        "(2, 11)":["H","H","H","D","D","H","H","H","H","H"]
    },

    "Split": {
        "(11, 11)":["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"],
        "(10, 10)":["S","S","S","S","S","S","S","S","S","S"],
        "(9, 9)":["Y","Y","Y","Y","Y","S","Y","Y","S","S"],
        "(8, 8)":["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"],
        "(7, 7)":["Y","Y","Y","Y","Y","Y","H","H","H","H"],
        "(6, 6)":["D","Y","Y","Y","Y","H","H","H","H","H"],
        "(5, 5)":["D","D","D","D","D","D","D","D","H","H"],
        "(4, 4)":["H","H","H","Da","Da","H","H","H","H","H"],
        "(3, 3)":["Da","Da","Y","Y","Y","Y","H","H","H","H"],
        "(2, 2)":["Da","Da","Y","Y","Y","Y","H","H","H","H"]
    },

    "Bets": [1,2,4,8,16,32],

    "Settings": {
        "Rounds": 10000,
        "Decks": 6,
        "DAS": "Y",
        "Surrender": "N",
        "MaxPenetration": 75
    }
}
```
S = stand  
H = hit   
Sr = surrender if possible; otherwise hit  
D = double  
Ds = double if possible; otherwise stand  
Da = split if double-after-split allowed; otherwise, don't split  
