from abc import ABC, abstractmethod
import itertools
import random

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


class Endgame_Beta(Player):
    def __init__(self):
        """Constructor for Own Player"""
        self.player_name ="BETA"

        self.rule_out_dict = []      # knowledge dictionary.
        self.last_guess = None
        self.queue = []
        self.one_char = 0            # to keep track of which character we deal with now.
        self.gauntlet = []
        self.try_mode = False
        self.search_mode = False
        self.num_of_gems = 0         # number of correct colors with a correct place we discover so far.
        self.cur_char = '#'          # current character we deal with in try and search mode.


        # TEST
        self.cache = []
        self.possible_answers = []
        self.visited = set()
        self.current_best = ''
        self.correct_place_color = 0
        # END

    # Reinitialize member variables
    def late_constructor(self, pegs):
        self.rule_out_dict = []
        self.last_guess = None
        self.queue = []
        self.one_char = 0
        self.gauntlet = []                                  
        self.try_mode = False
        self.search_mode = False
        self.num_of_gems = 0    
        self.cur_char = '#'  

        # TEST
        self.cache = []
        self.possible_answers = []
        self.visited = set()
        self.current_best = ''
        self.correct_place_color = 0
        # END

        for i in range(pegs): # Initialize rule_out_dict array with empty sets.
            self.rule_out_dict.append(set()) 
            self.gauntlet.append('#')     

    # When iterating over the characters of guess,
    # if the n-th character is in the n-th set of 
    # rule_out_dict, it returns True, False otherwise.
    def rule_out(self, guess):
        for i in range(len(guess)):
            if guess[i] in self.rule_out_dict[i]:
                print("\n\n\n\n@@@@@@@@@@@@@OH: ", end='')
                print(guess)
                return True
        return False
 
    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        try:
            if last_response[2] == 0:             
                self.late_constructor(board_length)
                guess = 'A' * board_length
                self.cur_char = 'A' 
                self.one_char += 1  
                self.try_mode = True 
                self.search_mode = False
                self.last_guess = guess
                return guess

            else:
                print(last_response)       
                if self.try_mode:       
                    if last_response[0] > 0:
                        self.num_of_gems += last_response[0]
                        self.cache.extend(self.cur_char for i in range(last_response[0]))

                    else:
                        for i in range(len(self.last_guess)):
                            self.rule_out_dict[i].add(self.cur_char)  

                    if self.num_of_gems == board_length:
                        print(self.cache)
                        self.try_mode = False
                        self.search_mode = True

                        random.shuffle(self.cache)
                        next_guess = ''.join(map(str, self.cache))
                        self.visited.add(next_guess)
                        self.last_guess = next_guess
                        return next_guess

                    else:
                        next_possible = [chr(65 + (self.one_char % len(colors)))] * board_length
                        self.cur_char = chr(65 + (self.one_char % len(colors)))
                        self.one_char += 1
                        guess = ''.join(map(str, next_possible))
                        self.last_guess = guess
                        return guess

                elif self.search_mode: 
     

                    if last_response[0] <= self.num_of_gems:    
                        for i in range(len(self.last_guess)):
                            if self.gauntlet[i] == '#':       
                                self.rule_out_dict[i].add(self.last_guess[i])  
                    
                    if last_response[0] > self.correct_place_color:
                        self.correct_place_color = last_response[0]
                        self.current_best = self.last_guess

                    random.shuffle(self.cache)
                    next_guess = ''.join(map(str, self.cache))

                    while next_guess in self.visited and self.rule_out(next_guess):
                        self.visited.add(next_guess)
                        random.shuffle(self.cache)
                        next_guess = ''.join(map(str, self.cache))

                    print(next_guess)
                    self.visited.add(next_guess)
                    self.last_guess = next_guess
                    return next_guess

        except:
            self.late_constructor(board_length)
            guess = 'A' * board_length
            self.cur_char = 'A'
            self.one_char = 1
            self.try_mode = True
            self.search_mode = False
            self.last_guess = guess       
            return guess
