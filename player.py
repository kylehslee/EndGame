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
        self.iters = None

    def make_colors(self, color):
        colors = []
        for i in range(color):
            colors.append(chr(i + 65))
        return colors

    def make_guess(
        self,
        board_length: int,
        colors,
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        try:
            if last_response[2] == 0:
                self.iters = itertools.product(self.make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))

        except:
            self.iters = itertools.product(self.make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))

   

class EndGame_b2(Player):
    def __init__(self):
        """Constructor for BaseLine1 Player"""

        self.player_name ="Baseline2"
        self.iters = None
        self.rule_out_dict = []
        self.last_guess = None


    def late_constructor(self, pegs):
        self.rule_out_dict = []
        for i in range(pegs): # Initialize rule_out_dict array with empty sets.
            self.rule_out_dict.append(set())   #     

    def rule_out(self, guess):
        for i in range(len(guess)):
            if guess[i] in self.rule_out_dict[i]:
                return True
        return False
    
    def make_colors(self, color):
        colors = []
        for i in range(color):
            colors.append(chr(i + 65))
        return colors

    def make_guess(
        self,
        board_length: int,
        colors,
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        # print('----------------')
        # print(last_response)
        try:
            if last_response[2] == 0:
                self.late_constructor(board_length)
                self.iters = itertools.product(self.make_colors((len(colors))), repeat=int(board_length))

            if last_response[2] == 0:    
                guess = ''.join(next(self.iters))
                # print('initial guess:', guess)
                self.last_guess = guess       
                return guess

            else:
                if last_response[0] == 0 and last_response[1] == 0:                                                                                   
                    for i in range(len(self.last_guess)):       
                        self.rule_out_dict[i].add(self.last_guess[i])  
                    # print(self.rule_out_dict)

                guess = ''.join(next(self.iters))
                # print('initial guess:', guess)

                while self.rule_out(guess) == True:
                    guess = ''.join(next(self.iters))
                    # print('next guess:', guess)
                
                self.last_guess = guess
                return guess

        except:
            # print("FILL IT AGAIN")
            self.iters = itertools.product(self.make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))


