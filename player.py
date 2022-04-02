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
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
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


class RandomFolks(Player):
    """Mastermind Player that makes random guesses"""

    def __init__(self):
        """Constructor for RandomFolks"""

        self.player_name = "RandomFolks"

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
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

        Returns:
            str: Returns guess
        """

        scsa = InsertColors()

        guess = scsa.generate_codes(board_length, colors)[0]

        return guess


class Boring(Player):
    """Mastermind Player that guesses all the same color and chooses that color at random"""

    def __init__(self):
        """Constructor for Boring"""

        self.player_name = "Boring"

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
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

        Returns:
            str: Returns guess
        """

        color = random.sample(colors, k=1)

        guess = list_to_str(color * board_length)

        return guess

################################################################################

'''
EndGame player that inherits from the 'Player Class'

As per the project.pdf on BB
    Constructor should take no arguments
    Inherit the make_guess function and have it do the magic of whatever baseline we are working on

'''


class EndGame(Player):
    def __init__(self):
        """Constructor for BaseLine1 Player"""

        self.player_name ="Baseline1"
   
    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:

        #Inner Function#

        def make_colors(color):
            colors = []
            for i in range(color):
                colors.append(chr(i + 65))
            return colors

        cnt = 0 # nth guess


        """
        replaced the commandline arguments for the make_colors() and repeat=int() with the parameters of the make_guess function
        This may or may not be correct as whenever I try testing the player with the example given in BB - the command line doesn't pick up the arguments
        """
        for i in itertools.product(make_colors((len(colors))), repeat=int(board_length)):
            guess = i   # print a pair.
            cnt += 1    # increment the count by 1 every loop.
             
        return guess

    


