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


# B1: Exhaustively enumerate all possibilities. Guess each possibility 
# in lexicographic order one at a time, and pay no attention to the 
# system’s responses. For example, if pegs p = 4 and colors c = 3, 
# guess AAAA, AAAB, AAAC, AABA, AABB, AABC and so on. This method 
# will take at most 𝑐1 guesses.
class EndGame_B1(Player):
    def __init__(self):
        """Constructor for BaseLine1 Player"""

        self.player_name ="Baseline1"
        self.iters = None

    # It returns a string formed with letters alpabetically
    # with the length of the parameter 'color'. 
    # [EX] if color is 3, it returns 'ABC'
    # [EX] if color is 4, it returns 'ABCD'
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

        # [Wikipedia explains Cartesian product well]
        #
        # Used Cartesian product below. It basiaclly gives you 
        # the first iterator of the set of all ordered pairs.
        # So, used for-loop to print all pairs.
        try:
            if last_response[2] == 0:
                self.iters = itertools.product(self.make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))

        except:
            self.iters = itertools.product(self.make_colors((len(colors))), repeat=int(board_length))
            return ''.join(next(self.iters))


     
