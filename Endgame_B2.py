#import random
from abc import ABC, abstractmethod
from scsa import list_to_str, InsertColors
#import sys
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


#-------------------------------------------------------------------
# B2: Exhaustively enumerate all possibilities. 
# Guess each possibility in lexicographic order 
# unless it was ruled out by some previous response. 
# For example, for p = 4, if guess AAAB got 0 0 1 in 
# response, you would never again on that round make 
# any guess that began with AAA or ended in B. 
class Baseline2(Player):
    def __init__(self):
        """Constructor for BaseLine2 Player"""

        self.player_name ="Baseline2"
        self.iters = None
        self.rule_out_dict = []
        self.last_guess = None


    def late_constructor(self, pegs):
        self.rule_out_dict = []
        for i in range(pegs): # Initialize rule_out_dict array with empty sets.
            self.rule_out_dict.append(set())

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



#------------------------------------IGNORE BELOW-----------------------------------------------

# if __name__=="__main__":
#     ## IMPORTANT ##
#     ## When you run this file,
#     ## two commands must be provided as of now.
#     ## EX: python3 main.py 4 2
#     ## 4 is the number of colors
#     ## 2 is the number of pegs

    
#     # print(sys.argv[1])  # colors ex) 3
#     # print(sys.argv[2])  # pegs   ex) 5

#     example_answer = ABColor(int(sys.argv[2]))  # ONLY FOR TEST. This program should get an answer from SCSA.py
#     print('EXAMPLE_ANSWER:', example_answer)    # ONLY FOR TEST

#     for i in range(int(sys.argv[2])): # Initialize rule_out_dict array with empty sets.
#         rule_out_dict.append(set())   # 

#     cnt = 0 # nth guess

#     # [Wikipedia explains Cartesian product well]
#     #
#     # Used Cartesian product below. It basiaclly gives you 
#     # the first iterator of the set of all ordered pairs.
#     # So, used for-loop to print all pairs.
#     for prod in itertools.product(make_colors(int(sys.argv[1])), repeat=int(sys.argv[2])):
#         cnt += 1
        
#         guess = ''.join(prod) # Example: ''.join(['ab', 'pq', 'rs']) -> 'abpqrs'

#         result = checker(guess, example_answer, cnt) # Suppose this checker is from SCSA. It returns a tuple with
#                                 # 3 elements(correct colors with correct places, correct colors with wrong places, nth step)

#         if rule_out(guess): # If the guess was ruled out, skip it.
            
#             # print('RULED OUT: ', guess, ' (DO NOT PRINT THIS GUESS. ONLY FOR TESTING)') # ONLY FOR TESTING, DO NOT PRINT IT ON SUBMISSION
#             continue
#         else:        
#             if result[0] == 0 and result[1] == 0:  # If the first two elements of variable 'result' are zero,
#                                                    # it means there were not correct colors with correct places
#                                                    # and correct colors with wrong places.
#                 for i in range(len(guess)):        # Then, we will update the dictionary, rule_out_dict.
#                     rule_out_dict[i].add(guess[i]) # For example, suppose our guess was 'CD' and the answer              
#             print(guess, end=', ')                 # was 'AB'. Then chekcer function would give us [0, 0, nth guess]. 
#                                                    # The reason is that 'CD' has 'no right colors with right places' 
#                                                    # and 'no colors with wrong places'.
#                                                    # Now it's time to update our rule-out-dict. It's obvious that
#                                                    # we don't have to check our next guess if the first letter of it
#                                                    # is 'C'. Also, we don't need to check if the second letter of 
#                                                    # our next guess is 'D'.
                                                    
#     # print('total counts:', cnt)
