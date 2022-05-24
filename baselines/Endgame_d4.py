from abc import ABC, abstractmethod
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
        colors: 'list[str]',
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



class Endgame(Player):
    def __init__(self):
        """Constructor for Own Player"""

        self.player_name ="EndGame"

        self.rule_out_dict = []      # knowledge dictionary.
        self.last_guess = None
        self.queue = []
        self.one_char = 0            # to keep track of which character we deal with now.
        self.gauntlet = []           # holds our knowledge about the correct code
        self.try_mode = False        # mode in which we find the right colors
        self.search_mode = False     # mode in which we find the right place for a correct color
        self.num_of_gems = 0         # number of correct colors with a correct place we discover so far.
        self.cur_char = '#'          # current character we deal with in try and search mode.

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
    
    def make_guess(
        self,
        board_length: int,
        colors: 'list[str]',
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:
        try:
                # First guess
                if last_response[2] == 0:             
                    self.late_constructor(board_length)
                    guess = 'A' * board_length
                    self.cur_char = 'A' 
                    self.one_char += 1  
                    self.try_mode = True 
                    self.search_mode = False
                    self.last_guess = guess
                    return guess

                # From second guess.
                else:
                    # In try mode, try with all the same letters except for indexes at which we have knowledge.
                    # For example, start with 'AAAA' and if there is a 'A' in the answer, then switch to 
                    # search mode and find which index the 'A' is positioned at.
                    # Once we get the index of 'A', let's say 'A' is at the first index( 0-indexed ),
                    # then we will try to guess with all B's except the first index. 
                    # Our next try guess would look like 'BABB'
                    if self.try_mode:   
                        
                        # if the sum of correct colors with a correct place and correct colors with a wrong place is
                        # less than or equal to the number of correct colors with a correct place we discover so far,
                        # then it means the color we try right now is not in the answer, so try with the next 
                        # characters.
                        if (last_response[0] + last_response[1]) <= self.num_of_gems:    
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

                        # Once we get to know the current character we deal with is in the answer,
                        # it generates all possible next guesses using multiset permutations.
                        elif (last_response[0] + last_response[1]) > self.num_of_gems:
                            next_set = [self.cur_char] * (last_response[0] + last_response[1] - self.num_of_gems) \
                            + [chr(65 + (self.one_char % len(colors)))] * (board_length - (last_response[0] + last_response[1]))
                            #print(next_set)
                            next_set = set(itertools.permutations(next_set)) #Using Standard Library for permutations. Contains duplicates
                                                                            #need to filter them out or utilize random restart for D4 when scaling up

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

                    # In search mode, it tries to find an index of the current character, which we deal with now,
                    # is. 
                    elif self.search_mode:

                        # This is when it finds the index of the current character.
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

                        # Try with the next guess in the queue.
                        guess = self.queue.pop(0)
                        while self.rule_out(guess) == True:
                            guess = self.queue.pop(0)
                        
                        self.last_guess = guess 
                        return guess

        # If no possible guesses in the queue, start again.
        except:
            self.late_constructor(board_length)
            guess = 'A' * board_length
            self.cur_char = 'A'
            self.one_char = 1
            self.try_mode = True
            self.search_mode = False
            self.last_guess = guess       
            return guess


####WORK IN PROGRESS CODE FROM PATRICK#######
#This is a alternate version of the algorithm, intended to find the correctr colors for the code, and then use a knowledge base of each prg's correctness
#to swap elements until it guesses the correcrt code. The first part works, but still working on the swapping logic.
#considering if I should have the positional KB set up differently
#once done, this should perform better for algorithms with fewer colors(two color, etc), or for those that do well with random restart
"""
class Endgame(Player):
    def __init__(self):
        #Constructor for Own Player

        self.player_name ="EndGame"

        self.rule_out_dict = []      # knowledge dictionary.
        self.last_guess = None
        self.queue = []
        self.one_char = 0            # to keep track of which character we deal with now.
        self.gauntlet = []           # holds our knowledge about the correct code
        self.try_mode = False        # mode in which we find the right colors
        self.search_mode = False     # mode in which we find the right place for a correct color
        self.num_of_gems = 0         # number of correct colors with a correct place we discover so far.
        self.cur_char = '#'          # current character we deal with in try and search mode.
        self.gem_map = []            # charmap with the correct colors and how many for each
        self.correct_colors = 0        # number of correct colors 
        self.color_map = []
        self.position_confidence = []   #0 means unsure, -1 means wrong, 1 means correct
        self.response_before_last = tuple([int, int, int])
        self.guess_before_last = str
        self.last_swap = (int, int)
        self.color_options = ['A','B','C','D','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

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
    
    def make_guess(
        self,
        board_length: int,
        colors: 'list[str]',
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:
        try:
            if scsa_name == "InsertColor":
                #this one is entirely random. i think the basic strategy works best
                print("poo")
            elif scsa_name == "TwoColorAlternatin":
                #once we have two correct colors, we can go right to placements. placements here is unique too, only two guess, ABA or BAB
                print("poo")
            elif scsa_name == "UsusallyFewe":
                #should only be 2-3 colors in this one, but sometimes more
                print("poo)")
            elif scsa_name == "mystery":
                #this one repeats a 3 color pattern. find 3 colors, find the first 3 placements, then done
                print("poo")
            else:
                # First guess
                if last_response[2] == 0:             
                    self.late_constructor(board_length)
                    guess = 'A' * board_length
                    self.cur_char = 'A' 
                    self.one_char += 1  
                    self.try_mode = True 
                    self.search_mode = False
                    self.last_guess = guess
                    return guess
                # From second guess, continue guessing all one color to record how many of each color is in answer
                else:
                    if self.correct_colors < board_length:
                        if last_response[0] > 0:
                            self.correct_colors += last_response[0]
                            self.color_map.append((self.last_guess[0],last_response[0]))
                            self.cur_char = chr(65 + (self.one_char % len(colors)))
                            self.one_char += 1
                            #check if we found all colors after update
                            #if so get ready for next phase
                            if self.correct_colors == board_length:
                                guess = ""
                                print(self.color_map)
                                for i in range(len(self.color_map)):
                                    guess += self.color_map[i][0] * self.color_map[i][1]
                                self.guess_before_last = self.last_guess
                                self.last_guess = guess
                                self.position_confidence = [0] * board_length
                                return guess
                        else: #color not in code, just go next
                            self.cur_char = chr(65 + (self.one_char % len(colors)))
                            self.one_char += 1
                        #update and submit guess
                        guess = self.cur_char * board_length 
                        self.last_guess = guess   
                        return guess
                    else:
                        #have all our colors, repeatedly swap attempting to get closer to the answer.
                        possible_swaps = [] #indexes not values

                        #populate swap contenders from confidence values
                        #pick one, remove it from possible swaps
                        #remove any from possible swaps with the same color
                        #pick one from remaining
                        #make sure its not the same as the last swap, if so, pick a different second number
                        #perform swap
                        #update guesses & swap variables
                        #submit guess
                        for i in range(board_length):
                            if self.position_confidence[i] <= 0:
                                possible_swaps.append(i)

                        #analyze the results of the last swap
                        if self.response_before_last[0] > last_response[0]:
                            #old guess was better, go back
                            guess = self.guess_before_last
                            #if we lost 2 points, both spots were correct. update position confidence
                            if self.response_before_last[0] - last_response[0] == -2:
                                self.position_confidence[self.last_swap[0]] = 1
                                self.position_confidence[self.last_swap[1]] = 1
                            #if we lost one point, one position was right
                            elif self.response_before_last[0] - last_response[0] == -1:
                                self.position_confidence[self.last_swap[0]] = 0
                                self.position_confidence[self.last_swap[1]] = 0

                        elif self.response_before_last[0] == last_response[0]:
                            #neither position is or was correct
                                self.position_confidence[self.last_swap[0]] = -1
                                self.position_confidence[self.last_swap[1]] = -1
                        else:
                            #our swap improved the answer
                            if self.response_before_last[0] - last_response[0] == 2:
                                #both are right!
                                self.position_confidence[self.last_swap[0]] = 1
                                self.position_confidence[self.last_swap[1]] = 1
                            else: #one is right, unsure which
                                self.position_confidence[self.last_swap[0]] = 0
                                self.position_confidence[self.last_swap[1]] = 0
                        #prepare our next swap
                        #record last response 
                        #update KB from last response (after 1st)

                        #randomize order
                        #guess until correct place > incorrect place

                        #reverse swap if necessary
                        #select new swap, record it, submit guess
                        print("help")

        # If no possible guesses in the queue, start again.
        except:
            self.late_constructor(board_length)
            guess = 'A' * board_length
            self.cur_char = 'A'
            self.one_char = 1
            self.try_mode = True
            self.search_mode = False
            self.last_guess = guess       
            return guess

"""