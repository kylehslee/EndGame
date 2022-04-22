import random
from abc import ABC, abstractmethod
from scsa import list_to_str, InsertColors
import itertools
from sympy.utilities.iterables import multiset_permutations

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



class EndGame_Own(Player):
    def __init__(self):
        """Constructor for Own Player"""

        self.player_name ="Own"
        self.rule_out_dict = []
        self.last_guess = None

        self.queue = []
        self.one_char = 0
        self.visited = []
        self.reg_que = []
        self.never_list = []
        self.gauntlet = []
        self.try_mode = False
        self.search_mode = False
        self.num_of_gems = 0
        self.cur_char = '#'

        self.cnt = 0

    def late_constructor(self, pegs):

        self.queue = []
        self.one_char = 0
        self.visited = []
        self.reg_que = []
        self.never_list = []
        self.gauntlet = []
        self.try_mode = False
        self.search_mode = False
        self.num_of_gems = 0
        self.cur_char = '#'
        self.cnt = 0
        self.rule_out_dict = []
        for i in range(pegs): # Initialize rule_out_dict array with empty sets.
            self.rule_out_dict.append(set()) 
            self.gauntlet.append('#')     

    # When iterating over the characters of guess,
    # if the n-th character is in the n-th set of 
    # rule_out_dict, it returns True, False otherwise.
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
        colors: list[str],
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:
        try:
            if last_response[2] == 0:
                # print("WHYY")
                self.late_constructor(board_length)
                guess = 'A' * board_length
                self.cur_char = 'A'
                self.one_char += 1
                self.try_mode = True
                self.search_mode = False
                self.last_guess = guess       
                return guess
            else:
                # print("WHATTTT")
                if self.try_mode:
                    if (last_response[0] + last_response[1]) <= self.num_of_gems:    
                        # print("WHATTTT     2")
                        for i in range(len(self.last_guess)):
                            if self.gauntlet[i] == '#':       
                                self.rule_out_dict[i].add(self.cur_char)  

                        next_possible = [chr(65 + (self.one_char % len(colors)))] * board_length
                        for i in range(board_length):
                            if not self.gauntlet[i] == '#':
                                next_possible[i] = self.gauntlet[i]

                        self.queue.append(''.join(map(str, next_possible)))
                        self.cur_char = chr(65 + (self.one_char % len(colors)))
                        self.one_char += 1

                        guess = self.queue.pop(0)
                        self.last_guess = guess 
                        return guess

                    elif (last_response[0] + last_response[1]) > self.num_of_gems:
                        # print("WHATTTT      3")
                        next_set = [self.cur_char] * (last_response[0] + last_response[1] - self.num_of_gems) \
                        + [chr(65 + (self.one_char % len(colors)))] * (board_length - (last_response[0] + last_response[1]))
                        # print('SUB WHAT          1')
                        next_set = multiset_permutations(next_set)
                        # next_set = set(itertools.permutations(next_set))
                        # print('SUB WHAT          2')
                        for i in next_set:
                            tmp = list(i)
                            for idx in range(len(self.gauntlet)):
                                if not self.gauntlet[idx] == '#':
                                    tmp.insert(idx, self.gauntlet[idx])

                            self.queue.append(''.join(map(str, tmp)))

                        
                        self.search_mode = True
                        self.try_mode = False

                        guess = self.queue.pop(0)
                        self.last_guess = guess 
                        return guess

                elif self.search_mode:
                    # print("WHATTTT          4")
                    if (last_response[0] + last_response[1]) > self.num_of_gems:    ## NOT NEEDED. DELETE THIS LINE.
                        if last_response[0] == (last_response[0] + last_response[1]) and last_response[1] == 0:
                            for i in range(board_length):
                                if self.last_guess[i] == self.cur_char:
                                    self.gauntlet[i] = self.cur_char
                                    self.num_of_gems += 1
                            self.queue.clear()

                            next_possible = [chr(65 + (self.one_char % len(colors)))] * board_length
                            for i in range(board_length):
                                if not self.gauntlet[i] == '#':
                                    next_possible[i] = self.gauntlet[i]

                            self.queue.append(''.join(map(str, next_possible)))
                            self.cur_char = chr(65 + (self.one_char % len(colors)))
                            self.one_char += 1

                            self.search_mode = False
                            self.try_mode = True

                            guess = self.queue.pop(0)
                            self.last_guess = guess 
                            return guess

                    guess = self.queue.pop(0)
                    while self.rule_out(guess) == True:
                        guess = self.queue.pop(0)
                    
                    self.last_guess = guess 
                    return guess

        except:
            print("DAMN----------------------------@@@!!  " , self.cnt)
            self.cnt += 1
            self.late_constructor(board_length)
            guess = 'A' * board_length
            self.cur_char = 'A'
            self.one_char += 1
            self.try_mode = True
            self.search_mode = False
            self.last_guess = guess       
            return guess
