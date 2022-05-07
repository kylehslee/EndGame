from abc import ABC, abstractmethod
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
        self.one_char = 0            # to keep track of which character we deal with now.
        self.gauntlet = []
        self.try_mode = False
        self.search_mode = False
        self.num_of_gems = 0         # number of correct colors with a correct place we discover so far.
        self.cur_char = '#'          # current character we deal with in try and search mode.

        self.cache = []
        self.possible_answers = []
        self.visited = set()
        self.current_best = ''
        self.correct_place_color = 0
        self.threshold = 0
        self.find_place_bit = False
        self.find_place_random_indexes_history = set()
        self.best_last_response = tuple()
        self.last_swapped_indexes = tuple()
        self.gauntlet_indexes = set()
        self.first_guess_after_try_mode = True
        self.indexes = []
        self.board_length = 0

    # Reinitialize member variables
    def initialize(self, pegs):
        self.rule_out_dict = []
        self.last_guess = None
        self.one_char = 0
        self.gauntlet = []                                  
        self.try_mode = False
        self.search_mode = False
        self.num_of_gems = 0    
        self.cur_char = '#'  

        self.cache = []
        self.possible_answers = []
        self.visited = set()
        self.current_best = ''
        self.correct_place_color = 0
        self.threshold = ((pegs // 2) // 2) * 2;
        self.find_place_bit = False
        self.find_place_random_indexes_history = set()
        self.best_last_response = tuple()
        self.last_swapped_indexes = tuple()
        self.gauntlet_indexes = set()
        self.first_guess_after_try_mode = True
        self.indexes = []
        self.board_length = pegs


        for i in range(pegs): # Initialize rule_out_dict array with empty sets.
            self.rule_out_dict.append(set()) 
            self.gauntlet.append('#')   
            self.indexes.append(i)  

    # When iterating over the characters of guess,
    # if the n-th character is in the n-th set of 
    # rule_out_dict, it returns True, False otherwise.
    def rule_out(self, guess):
        for i in range(len(guess)):
            if guess[i] in self.rule_out_dict[i]:
                return True
        return False

    def swap(self, s, i, j):
        lst = list(s)
        lst[i], lst[j] = lst[j], lst[i]
        return ''.join(lst)

    def swap_tuple(self, tu):
        list_x = list(tu)
        list_x[0], list_x[1] = list_x[1], list_x[0]
        return tuple(list_x)
    
    def clone(self, li):
        li_copy = li[:]
        return li_copy
 
    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        # print(last_response, " ,Last_guess: ", self.last_guess, " , Last_BEST_res: ", self.best_last_response, " , gauntlet: ", self.gauntlet, " , threshold: ", self.threshold, " , last_swapped_idx: ", self.last_swapped_indexes, ", num_gems: ", self.num_of_gems)
        if last_response[2] == 0:             
            self.initialize(board_length)
            guess = 'A' * board_length
            self.cur_char = 'A' 
            self.one_char += 1  
            self.try_mode = True 
            self.search_mode = False
            self.last_guess = guess
            return guess

        else:
            # In the try mode, do guess with all the same letters such as 'AAAA' and 'BBBB' 
            # and find out which colors and how many pegs of that color there are in the answer.
            # EX. Answer: 'AACD'
            # 1st try: 'AAAA', response => (2, 0, 1)
            # 2nd try: 'BBBB', response => (0, 0, 2)
            # 3rd try: 'CCCC', response => (1, 0, 3)
            # 4th try: 'DDDD', response => (1, 0, 4)
            if self.try_mode:       
                if last_response[0] > 0:
                    self.num_of_gems += last_response[0]
                    self.cache.extend(self.cur_char for i in range(last_response[0]))

                else:
                    for i in range(len(self.last_guess)):
                        self.rule_out_dict[i].add(self.cur_char)  

                if self.num_of_gems == board_length:
                    self.try_mode = False
                    self.search_mode = True
                    self.num_of_gems = 0

                    return self.get_next_guess_by_shuffle()

                else:
                    next_possible = [chr(65 + (self.one_char % len(colors)))] * board_length
                    self.cur_char = chr(65 + (self.one_char % len(colors)))
                    self.one_char += 1
                    guess = ''.join(map(str, next_possible))
                    self.last_guess = guess
                    return guess

            # In the search mode, it tries to find the answer by random shuffling or swapping colors
            elif self.search_mode: 
                
                # If the first element of last response is less than or equal to num_of_gems,
                # it means that the last guess it tried was meaningless, so update the knowledge base.
                if last_response[0] <= self.num_of_gems:    
                    for i in range(len(self.last_guess)):
                        if self.gauntlet[i] == '#':       
                            self.rule_out_dict[i].add(self.last_guess[i])  

                # While trying to guess with random shuffling, turn on the find_place_bit 
                # once it finds more correct colors with a correct place than the predefined
                # threshold. The threshold was set in self.initialize(). It's about half of
                # the number of pegs.
                if not self.find_place_bit and last_response[0] == self.threshold:
                    self.find_place_bit = True
                    self.best_last_response = last_response
                    self.current_best = self.last_guess
                
                # Once the find_place_bit was turned on, now it tries to find positions of pegs 
                # by swapping. If pegs were swapped and tried to guess with it and the response it
                # received back was bigger by 2, it means that those two swapped pegs were at the 
                # wrong positions before, but now those are positioned at the right places.
                # ---------------------------------------------------------
                # Ex. Answer: 'AACDBB'
                # 1. Previous guess: 'BBDCAA' and response: (0, 6). 
                # 2 .Swapped (2, 3) of 'BBDCAA' so it became 'BBCDAA'
                # 3. Guess again with 'BBCDAA'
                # 4. The response will be (2, 4)
                # Now we know 2th and 3th positions' colors.
                # It is the same as the opposite case. That's why there are
                # two branches (when diff == 2 or -2).
                # ----------------------------------------------------------
                if self.find_place_bit:  
                    diff = last_response[0] - self.best_last_response[0]
                    if diff == 2:
                        self.current_best = self.last_guess
                        self.update_gauntlet_and_cache()
                    elif diff == -2:
                        self.update_gauntlet_and_cache()

                    # Once it finds threshold amount of correct colors with a correct place,
                    # update the threshold by incrementing by 2.
                    if self.threshold <= self.num_of_gems:
                        self.visited.clear()
                        self.find_place_bit = False
                        self.threshold += 2
                        if self.threshold > board_length:
                            self.threshold = board_length

                    return self.get_next_guess_by_swap()

                return self.get_next_guess()

    def get_next_guess_by_shuffle(self):
        tmp = self.clone(self.cache)
        random.shuffle(tmp)
        for idx in range(len(self.gauntlet)):
            if not self.gauntlet[idx] == '#':
                tmp.insert(idx, self.gauntlet[idx])
        next_guess = ''.join(map(str, tmp))

        cnt = 0
        while next_guess in self.visited:
            self.visited.add(next_guess)
            tmp = self.clone(self.cache)
            random.shuffle(tmp)
            for idx in range(len(self.gauntlet)):
                if not self.gauntlet[idx] == '#':
                    tmp.insert(idx, self.gauntlet[idx])
            next_guess = ''.join(map(str, tmp))
            cnt += 1
            if cnt == 1000:
                break

        self.visited.add(next_guess)
        self.last_guess = next_guess
        return next_guess

    def get_next_guess_by_swap(self):

        cnt = 0
        limit = (self.board_length - self.num_of_gems) * (self.board_length - self.num_of_gems - 1) - 1

        swapped_indexes = tuple(random.sample(self.indexes, 2))
        while swapped_indexes[0] in self.gauntlet_indexes or \
              swapped_indexes[1] in self.gauntlet_indexes or \
              swapped_indexes in self.find_place_random_indexes_history:
            swapped_indexes = tuple(random.sample(self.indexes, 2))
            cnt += 1

            if cnt == limit:
                self.find_place_bit = False
                return self.get_next_guess_by_shuffle()


        self.last_swapped_indexes = swapped_indexes
        self.find_place_random_indexes_history.add(swapped_indexes)
        self.find_place_random_indexes_history.add(self.swap_tuple(swapped_indexes))

        next_guess = self.swap(self.current_best, swapped_indexes[0], swapped_indexes[1])
        self.visited.add(next_guess)
        self.last_guess = next_guess
        return next_guess    

    def get_next_guess(self):
        if self.find_place_bit:
            return self.get_next_guess_by_swap() 
        else:
            return self.get_next_guess_by_shuffle()
    
    def update_gauntlet_and_cache(self):
        self.find_place_random_indexes_history.clear()
        
        self.gauntlet[self.last_swapped_indexes[0]] = self.current_best[self.last_swapped_indexes[0]]
        self.gauntlet[self.last_swapped_indexes[1]] = self.current_best[self.last_swapped_indexes[1]]
        self.num_of_gems += 2

        tmp_cache = self.clone(self.cache)
        tmp_cache.remove(self.current_best[self.last_swapped_indexes[0]])
        tmp_cache.remove(self.current_best[self.last_swapped_indexes[1]])
        self.cache = tmp_cache

        self.indexes.remove(self.last_swapped_indexes[0])
        self.indexes.remove(self.last_swapped_indexes[1])
        
        self.gauntlet_indexes.add(self.last_swapped_indexes[0])
        self.gauntlet_indexes.add(self.last_swapped_indexes[1])            

