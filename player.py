# File contains implementations for the players for Mastermind.
# See main.py or examples.ipynb for example usages.

import random
from abc import ABC, abstractmethod
from scsa import list_to_str, InsertColors
import sys
import itertools

class Player(ABC):
    """Player for Mastermind"""

    def __init__(self):
        """Constructor for Player"""

        self.player_name = ""

    @abstractmethod
    def make_guess(
        self,
        board_length: int,
        colors,
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list[str]]): All possible colors that can be used to generate a code.
            scsa_name (str): Name of SCSA used to generate secret code.
            last_response (tuple[int, int, int]): (First element in tuple is the number of pegs that match exactly with the secret
                                           code for the previous guess, the second element is the number of pegs that are
                                           the right color, but in the wrong location for the previous guess, and the third
                                           element is the number of guesses so far.)

        Raises:
            NotImplementedError: Function must be implemented by subclasses.
        """

        raise NotImplementedError




'''
EndGame player that inherits from the 'Player Class'

As per the project.pdf on BB
    Constructor should take no arguments
    Inherit the make_guess function and have it do the magic of whatever baseline we are working on

'''


class EndGame_b1(Player):
    def __init__(self):
        """Constructor for BaseLine1 Player"""

        self.player_name ="Baseline1"
        self.is_guess_generated = False
        self.iters = None

    def make_guess(
        self,
        board_length: int,
        colors,
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        #Inner Function#

        def make_colors(color):
            colors = []
            for i in range(color):
                colors.append(chr(i + 65))
            return colors


        """
        replaced the commandline arguments for the make_colors() and repeat=int() with the parameters of the make_guess function
        This may or may not be correct as whenever I try testing the player with the example given in BB - the command line doesn't pick up the arguments
        """
        try:
            if self.is_guess_generated == False:
                self.iters = itertools.product(make_colors((len(colors))), repeat=int(board_length))
                self.is_guess_generated = True
            return ''.join(next(self.iters))

        except:
            self.iters = itertools.product(make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))

    

class EndGame_b2(Player):
    def __init__(self):
        """Constructor for BaseLine1 Player"""

        self.player_name ="Baseline1"
        self.is_guess_generated = False
        self.iters = None

    def make_guess(
        self,
        board_length: int,
        colors,
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        #Inner Function#

        def make_colors(color):
            colors = []
            for i in range(color):
                colors.append(chr(i + 65))
            return colors


        """
        replaced the commandline arguments for the make_colors() and repeat=int() with the parameters of the make_guess function
        This may or may not be correct as whenever I try testing the player with the example given in BB - the command line doesn't pick up the arguments
        """
        try:
            if self.is_guess_generated == False:
                self.iters = itertools.product(make_colors((len(colors))), repeat=int(board_length))
                self.is_guess_generated = True
            return ''.join(next(self.iters))

        except:
            self.iters = itertools.product(make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))

    

