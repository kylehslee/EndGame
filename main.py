# Main file to run game of Mastermind based on command-line arguments.
# See example.ipynb for other ways to use the Mastermind representation.

import argparse
from scsa import *
from player import *
from mastermind import *
from Endgame_B1 import *
from Endgame_B2 import *
from Endgame_d3_2 import *
import timeit

## TEST
from Endgame_beta import *
## END

start = timeit.default_timer()

parser = argparse.ArgumentParser(description="Play a game of Mastermind.")
parser.add_argument("--board_length", nargs="?", type=int, required=True)
parser.add_argument(
    "--num_colors", nargs="?", type=int, required=True, choices=range(1, 27)
)

parser.add_argument(
    "--player_name",
    nargs="?",
    type=str,
    required=True,
    choices=["RandomFolks", "Boring", "Baseline1", "Baseline2", "Endgame", "Beta"],
)

parser.add_argument(
    "--scsa_name",
    nargs="?",
    type=str,
    required=True,
    choices=[
        "InsertColors",
        "TwoColor",
        "ABColor",
        "TwoColorAlternating",
        "OnlyOnce",
        "FirstLast",
        "UsuallyFewer",
        "PreferFewer",
    ],
)

parser.add_argument("--num_rounds", nargs="?", type=int, required=True)
args = parser.parse_args()

def str_to_player(player_name: str) -> Player:
    if player_name == "RandomFolks":
        player = RandomFolks()
    elif player_name == "Boring":
        player = Boring()
    elif player_name == "Baseline1":
        player = Baseline1()
    elif player_name == "Baseline2":
        player = Baseline2()
    elif player_name == "Endgame":
        player = Endgame()     
    elif player_name == "Beta":
        player = Endgame_Beta()   
    else:
        raise ValueError("Unrecognized Player.")
    return player


def str_to_scsa(scsa_name: str) -> SCSA:
    if scsa_name == "InsertColors":
        scsa = InsertColors()
    elif scsa_name == "TwoColor":
        scsa = TwoColor()
    elif scsa_name == "ABColor":
        scsa = ABColor()
    elif scsa_name == "TwoColorAlternating":
        scsa = TwoColorAlternating()
    elif scsa_name == "OnlyOnce":
        scsa = OnlyOnce()
    elif scsa_name == "FirstLast":
        scsa = FirstLast()
    elif scsa_name == "UsuallyFewer":
        scsa = UsuallyFewer()
    elif scsa_name == "PreferFewer":
        scsa = PreferFewer()
    else:
        raise ValueError("Unrecognized SCSA.")
    return scsa

player = str_to_player(args.player_name)
scsa = str_to_scsa(args.scsa_name)
colors = [chr(i) for i in range(65, 91)][: args.num_colors]
mastermind = Mastermind(args.board_length, colors)

mastermind.play_tournament(player, scsa, args.num_rounds) # for regular scsas

# mastermind.practice_tournament(player, scsa, "mystery5_7_5.txt") # for 

stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time)+" seconds") # It returns time in seconds