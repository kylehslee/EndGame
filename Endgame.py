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
        self.scsa_color_first_mode = False# mode in which we populate a color map with the correct colors and how many of each
        self.scsa_test_color_by_peg_mode = False # after we know colors, loop through them peg by peg to find code
        self.num_of_gems = 0         # number of correct colors with a correct place we discover so far.
        self.cur_char = '#'          # current character we deal with in try and search mode.
        self.scsa_correct_colors = 0      # number of correct colors 
        self.scsa_color_map = []          #generated in color first mode, holds correct colos and how many of each
        self.scsa_color_map_index= 1


        ############ BETA VARIABLES ##############
        self.beta_bit = False
        self.beta_try_mode = False
        self.beta_search_mode = False
        self.correct_colors = []
        self.visited = set()
        self.current_best = ''
        self.threshold = 0
        self.search_index_bit = False
        self.swapped_indexes_history = set()
        self.best_last_response = tuple()
        self.last_swapped_indexes = tuple()
        self.gauntlet_indexes = set()
        self.unknown_indexes = []
        self.board_length = 0
        ##########################################

    # Reinitialize member variables
    def initialize(self, pegs):
        self.rule_out_dict = []
        self.last_guess = None
        self.queue = []
        self.one_char = 0
        self.gauntlet = []                                  
        self.try_mode = True
        self.search_mode = False
        self.scsa_color_first_mode = False
        self.scsa_test_color_by_peg_mode = False
        self.num_of_gems = 0   
        self.scsa_correct_colors = 0 
        self.cur_char = '#'  


        ############ BETA VARIABLES ##############
        self.beta_bit = False
        self.beta_try_mode = False
        self.beta_search_mode = False
        self.correct_colors = []
        self.visited = set()
        self.current_best = ''
        self.threshold = ((pegs // 2) // 2) * 2
        self.search_index_bit = False
        self.swapped_indexes_history = set()
        self.best_last_response = tuple()
        self.last_swapped_indexes = tuple()
        self.gauntlet_indexes = set()
        self.unknown_indexes = []
        self.board_length = pegs
        ##########################################

        for i in range(pegs): # Initialize rule_out_dict array with empty sets.
            self.rule_out_dict.append(set()) 
            self.gauntlet.append('#')   
            self.unknown_indexes.append(i)  

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
        colors: 'list[str]',
        scsa_name: str,
        last_response: tuple([int, int, int]),
    ) -> str:

        try:
            # First guess
            if last_response[2] == 0:             
                self.initialize(board_length)
                guess = 'A' * board_length
                self.cur_char = 'A' 
                self.one_char += 1
                if scsa_name == "ABColor" \
                    or scsa_name == "TwoColor" \
                    or scsa_name == "mystery1" \
                    or scsa_name == "TwoColorAlternating" \
                    or scsa_name == "mystery2":
                    self.try_mode = False 
                    self.scsa_color_first_mode = True
                    self.search_mode = False
                #Interestingly, prefer and ususally fewer have better accuracy without the randomized swapping, but
                #on average score better with random swapping, despite the drop in accuracy when it gets "unlucky"
                #In general, the swapping does well with fewer color options, even as the game scales the board.
                #The regular version is more certain of getting a win, but takes longer to do it.
                elif scsa_name == "PreferFewer" \
                    or scsa_name == "UsuallyFewer" \
                    or (scsa_name == "InsertColors" and board_length > 15) \
                    or (scsa_name == "OnlyOnce" and board_length > 22) \
                    or (scsa_name == "FirstLast" and board_length > 20) \
                    or scsa_name == "mystery3" \
                    or scsa_name == "mystery4" \
                    or scsa_name == "mystery5" \
                    or scsa_name == "mystery7":
                    self.beta_bit = True
                    self.beta_try_mode = True 
                    self.beta_search_mode = False

                    self.try_mode = False 
                    self.search_mode = False
                    self.scsa_color_first_mode = False

                else: #mystery6 or long board lengths
                    self.try_mode = True 
                    self.scsa_color_first_mode = False
                    self.search_mode = False

                self.last_guess = guess
                self.scsa_color_map= []
                return guess

            # From the second guess to the last guess
            else:
                #guess mono-color to find correct colors and how many of each, saved in color_map
                if self.scsa_color_first_mode == True:
                    if last_response[0] > 0:
                        self.scsa_correct_colors += last_response[0]
                        self.scsa_color_map.append((self.last_guess[0],last_response[0]))
                        self.cur_char = chr(65 + (self.one_char % len(colors)))
                        self.one_char += 1
                        #check if we found all colors after update
                        #if so get ready for next phase
                        if self.scsa_correct_colors == board_length:
                            #reset current char and guess to AAAA, for compatibility with other modes after obtaining color map
                            self.initialize(board_length)
                            guess = 'A' * board_length
                            self.cur_char = 'A'
                            self.one_char = 1
                            if scsa_name == "ABColor" or scsa_name == "TwoColor" or scsa_name == "mystery2" or scsa_name == "TwoColorAlternating":
                                self.try_mode = False 
                                self.scsa_color_first_mode = False
                                self.scsa_test_color_by_peg_mode = True
                                #guess should be homogenous of first color in color map
                                guess = self.scsa_color_map[0][0]* board_length
                            else:
                                self.try_mode = True 
                                self.scsa_color_first_mode = False
                            self.scsa_color_first_mode = False #update mode to exit
                            #self.try_mode = True #move to next mode-can change for scsa specific code
                            self.search_mode = False
                            self.last_guess = guess       
                            return guess
                    else: #color not in code, just go next
                        self.cur_char = chr(65 + (self.one_char % len(colors)))
                        self.one_char += 1
                    #update and submit guess
                    guess = self.cur_char * board_length 
                    self.last_guess = guess   
                    return guess

                # at each peg, loop through the colors in the color map until you find the correct one
                # then move to next peg, and repeat
                # mystery2 is a repetading 3 color code, hence the unique code block
                elif self.scsa_test_color_by_peg_mode:
                    guess = list(self.last_guess) #change guess into list so we can change elements
                    if scsa_name == "ABColor" or scsa_name == "TwoColor" or (scsa_name == "mystery2" and self.one_char < 3): 
                        if self.last_guess == self.scsa_color_map[0][0] * board_length: #this is our first guess in test_color_by_peg_mode
                            guess[0] = self.scsa_color_map[1][0]
                            guess = "".join(guess)
                            self.one_char = 0 #index of checking 
                            self.num_of_gems = last_response[0]
                            self.last_guess = guess
                            return guess
                        else:
                            if self.num_of_gems < last_response[0]: #change to B was good
                                self.num_of_gems += 1 #increment our correct pegs
                                self.one_char += 1 #go to next peg
                                self.scsa_color_map_index= 1 #reset colormap index for next peg
                                guess[self.one_char] = self.scsa_color_map[self.scsa_color_map_index][0]
                                guess = "".join(guess)
                            elif self.num_of_gems > last_response[0]:#change was bad, previous was correct
                                guess[self.one_char] = self.scsa_color_map[self.scsa_color_map_index-1][0] #change it back
                                self.one_char += 1 #next peg
                                self.scsa_color_map_index= 1
                                guess[self.one_char] = self.scsa_color_map[self.scsa_color_map_index][0]
                                guess = "".join(guess)
                            else: #no change in gems, neither previous nor change were right
                                self.scsa_color_map_index+= 1
                                guess[self.one_char] = self.scsa_color_map[self.scsa_color_map_index][0] #try next color in colormap at this peg
                                guess = "".join(guess)
                    elif scsa_name == "mystery2": #we are on 3rd or greater index of code, for this one it repeats pattern
                            guess = list(self.last_guess)
                            for i in range(3, board_length):
                                guess[i] = guess[i-3]
                    elif scsa_name == "TwoColorAlternating":
                        guess = ""
                        if self.last_guess == self.scsa_color_map[0][0] * board_length:
                            color1 = self.scsa_color_map[0][0]
                            color2 = self.scsa_color_map[1][0]
                        else: 
                            color1 = self.scsa_color_map[1][0]
                            color2 = self.scsa_color_map[0][0]
                        for i in range(board_length):
                            if i % 2 == 0:
                                guess += color1
                            else:
                                guess += color2
                        self.last_guess = guess
                        return guess
                    guess = "".join(guess)
                    self.last_guess = guess
                    return guess      

                # In try mode, try with all the same letters except for indexes at which we have knowledge.
                # For example, start with 'AAAA' and if there is a 'A' in the answer, then switch to 
                # search mode and find which index the 'A' is positioned at.
                # Once we get the index of 'A', let's say 'A' is at the first index( 0-indexed ),
                # then we will try to guess with all B's except the first index. 
                # Our next try guess would look like 'BABB'
                elif self.try_mode:   
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

                        # next_set = set(itertools.permutations(next_set)) # Standard permutations
                        next_set = list(unique_permutations(next_set))   # Endgame permutations

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
                
                elif self.beta_bit:
                    # There is some code duplication here with the color first mode, but as they feed into 
                    # different algorithms, we are leaving them both. Also they were made by different people
                    # In the beta try mode, do guess with all the same letters such as 'AAAA' and 'BBBB' 
                    # and find out which colors and how many pegs of that color there are in the answer.
                    # EX. Answer: 'AACD'
                    # 1st try: 'AAAA', response => (2, 0, 1)
                    # 2nd try: 'BBBB', response => (0, 0, 2)
                    # 3rd try: 'CCCC', response => (1, 0, 3)
                    # 4th try: 'DDDD', response => (1, 0, 4)
                    if self.beta_try_mode:       
                        if last_response[0] > 0:
                            self.num_of_gems += last_response[0]
                            self.correct_colors.extend(self.cur_char for i in range(last_response[0]))

                        else:
                            for i in range(len(self.last_guess)):
                                self.rule_out_dict[i].add(self.cur_char)  

                        if self.num_of_gems == board_length:
                            self.beta_try_mode = False
                            self.beta_search_mode = True
                            self.num_of_gems = 0
                            self.cache_backup = self.clone(self.correct_colors)

                            return self.get_next_guess_by_shuffle()

                        else:
                            next_possible = [chr(65 + (self.one_char % len(colors)))] * board_length
                            self.cur_char = chr(65 + (self.one_char % len(colors)))
                            self.one_char += 1
                            guess = ''.join(map(str, next_possible))
                            self.last_guess = guess
                            return guess

                    # In the beta search mode, it tries to find the answer by random shuffling or swapping colors
                    elif self.beta_search_mode: 
                        

                        # [[ OBSOLETE ]] - IGNORE LINE181 - 184 BELOW. RULE_OUT() NOT USED IN THIS CLASS
                        # If the first element of last response is less than or equal to num_of_gems,
                        # it means that the last guess it tried was meaningless, so update the knowledge base.
                        if last_response[0] <= self.num_of_gems:    
                            for i in range(len(self.last_guess)):
                                if self.gauntlet[i] == '#':       
                                    self.rule_out_dict[i].add(self.last_guess[i])  

                        # While trying to guess with random shuffling, turn on the search_index_bit 
                        # once it finds more correct colors with a correct place than the predefined
                        # threshold. The threshold was set in self.initialize(). It's about half of
                        # the number of pegs.
                        if not self.search_index_bit and last_response[0] >= self.threshold:
                            self.search_index_bit = True
                            self.best_last_response = last_response
                            self.current_best = self.last_guess
                        
                        # Once the search_index_bit was turned on, now it tries to find positions of pegs 
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
                        if self.search_index_bit:  
                            diff = last_response[0] - self.best_last_response[0]
                            if diff == 2:
                                # If diff is 2, it means that the swapped guess it tried the most recently
                                # is better than the current best guess, so self.current_best is updated,
                                # and self.best_last_response is also updated.
                                self.current_best = self.last_guess
                                self.best_last_response = last_response
                                self.update_gauntlet_and_cache()
                            
                            elif diff == -2:
                                self.update_gauntlet_and_cache()

                            # Once it finds threshold amount of correct colors with a correct place,
                            # update the threshold by incrementing by 2.
                            if (self.threshold // 2) * 2 <= self.num_of_gems:
                                self.visited.clear()
                                self.search_index_bit = False
                                self.threshold += 2
                                if self.threshold > board_length:
                                    self.threshold = board_length

                            return self.get_next_guess_by_swap()

                        return self.get_next_guess()


        # If no possible guesses in the queue, start again.
        except:
            self.initialize(board_length)
            guess = 'A' * board_length
            self.cur_char = 'A'
            self.one_char = 1
            self.try_mode = True
            self.search_mode = False
            self.last_guess = guess       
            return guess
    
    def get_next_guess_by_shuffle(self):
        # insignificant number, just needed a number for limit
        limit = (self.board_length - self.num_of_gems) * (self.board_length - self.num_of_gems - 1) 
        cnt = 0

        while True:
            tmp = self.clone(self.correct_colors) # Need a deep-copied list.
            random.shuffle(tmp)
            for idx in range(len(self.gauntlet)):  # Update randomly-shuffled next guess with the knowledge base
                if not self.gauntlet[idx] == '#':
                    tmp.insert(idx, self.gauntlet[idx])
            next_guess = ''.join(map(str, tmp))

            if not(next_guess in self.visited):
                break

            cnt += 1
            if cnt == limit:             # If the number of shuffling reaches the limit count,
                self.visited = set()     # clear the self.visited. The reason is that it could
            self.visited.add(next_guess) # be stuck in the while loop if most next possible  
                                         # guesses were already in the self.visited.
        ## END WHILE

        self.visited.add(next_guess)
        self.last_guess = next_guess
        return next_guess

    def get_next_guess_by_swap(self):
        # insignificant number, just needed a number for limit
        limit = (self.board_length - self.num_of_gems) * (self.board_length - self.num_of_gems - 1) 
        cnt = 0
        
        swapped_indexes = tuple(random.sample(self.unknown_indexes, 2))
        while swapped_indexes in self.swapped_indexes_history:
            swapped_indexes = tuple(random.sample(self.unknown_indexes, 2))
            cnt += 1

            if cnt == limit:
                cnt = 0
                self.swapped_indexes_history = set()

        self.last_swapped_indexes = swapped_indexes
        self.swapped_indexes_history.add(swapped_indexes)
        self.swapped_indexes_history.add(self.swap_tuple(swapped_indexes))

        next_guess = self.swap(self.current_best, swapped_indexes[0], swapped_indexes[1])
        self.visited.add(next_guess)
        self.last_guess = next_guess
        return next_guess    

    def get_next_guess(self):
        if self.search_index_bit:
            return self.get_next_guess_by_swap() 
        else:
            return self.get_next_guess_by_shuffle()

    # This function is called every time the program finds exact indexes of two swapped colors.
    def update_gauntlet_and_cache(self):
        self.swapped_indexes_history.clear()
        
        # Update the gauntlet(knowledge base)
        self.gauntlet[self.last_swapped_indexes[0]] = self.current_best[self.last_swapped_indexes[0]]
        self.gauntlet[self.last_swapped_indexes[1]] = self.current_best[self.last_swapped_indexes[1]]
        self.num_of_gems += 2

        tmp_cache = self.clone(self.correct_colors)
        tmp_cache.remove(self.current_best[self.last_swapped_indexes[0]])
        tmp_cache.remove(self.current_best[self.last_swapped_indexes[1]])
        self.correct_colors = tmp_cache

        # Remove the most recently swapped indexes
        self.unknown_indexes.remove(self.last_swapped_indexes[0])
        self.unknown_indexes.remove(self.last_swapped_indexes[1])
        
        # Exactly opposite to unknown_indexes
        # Add the most recently swapped indexes
        self.gauntlet_indexes.add(self.last_swapped_indexes[0])
        self.gauntlet_indexes.add(self.last_swapped_indexes[1])            



#Code to obtain unique multiset permutations. standard version includes duplicate permutaions, 
# this specifies the occurances of each value and returns the unique permutaions via recrusion
class unique_peg:
    def __init__(self, value, occurrences):
        self.value = value
        self.occurrences = occurrences

def unique_permutations(pegs):
    eset = set(pegs)
    unique_list = [unique_peg(i,pegs.count(i)) for i in eset]
    l = len(pegs)
    return unique_permutations_recursive_helper(unique_list, [0] * l, l - 1)

def unique_permutations_recursive_helper(unique_list, result, idx):
    if idx < 0:
        yield tuple(result)
    else:
        for i in unique_list:
            if i.occurrences > 0:
                result[idx]=i.value
                i.occurrences-=1
                for g in  unique_permutations_recursive_helper(unique_list,result,idx-1):
                    yield g
                i.occurrences+=1
