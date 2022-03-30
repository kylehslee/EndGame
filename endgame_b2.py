import sys
import itertools

#-------------------------------------------------------------------
# B2: Exhaustively enumerate all possibilities. 
# Guess each possibility in lexicographic order 
# unless it was ruled out by some previous response. 
# For example, for p = 4, if guess AAAB got 0 0 1 in 
# response, you would never again on that round make 
# any guess that began with AAA or ended in B. 




# It returns a string formed with letters alpabetically
# with the length of the parameter 'color'. 
# [EX] if color is 3, it returns 'ABC'
# [EX] if color is 4, it returns 'ABCD'
def make_colors(color):
    colors = []
    for i in range(color):
        colors.append(chr(i + 65))
    return colors


# EX] rule_out_dict = [ 0:{'A','C'}, 1:{'A','B'}, 2:{'A'}, 3:{'B'} ]
rule_out_dict = []

# When iterating over the characters of guess,
# if the n-th character is in the n-th set of 
# rule_out_dict, it returns True, False otherwise.
def rule_out(guess):
    for i in range(len(guess)):
        if guess[i] in rule_out_dict[i]:
            return True
    return False


#----------------START---------------------------------START--------------------------------------------
#  Belwo two functions should already be defined in SCSA.py.
#  Since SCSA.py professor uploaded on the BB does have errors, 
#  below functions were defined for testing.



# [DESCRIPTION]
# Every time your player makes a
# guess, our tournament engine returns three numbers: how many exact pegs (correct color in the correct position),
# how many “almost” pegs (correct color in the wrong position), and what number guess you just made. For
# example, if the reply to your guess BBACDC is [2, 1, 39], it means that on your 39th guess two of those pegs have
# the correct color in the correct position and one other peg is the correct color in the wrong position.
def checker(guess, answer, nth):  
    correct_color_correct_place = 0
    guess_dict = {}
    answer_dict = {}
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            correct_color_correct_place += 1
        else:
            guess_dict[guess[i]] = guess_dict[guess[i]] + 1 if guess[i] in guess_dict else 1
            answer_dict[answer[i]] = answer_dict[answer[i]] + 1 if answer[i] in answer_dict else 1
    
    correct_color_wrong_place = sum([min(guess_dict[k], answer_dict[k]) for k in guess_dict if k in answer_dict])
    return tuple([correct_color_correct_place, correct_color_wrong_place, nth])   

# ABColor generator. Had to define it manually because SCSA.py professor provided has errors.
# It returns something like 'ABABA' with 5 pegs, 'ABA' with 3 pegs.
def ABColor(pegs):
    answer = ''
    for i in range(pegs):
        if i % 2 == 0:
            answer += 'A'
        else:
            answer += 'B'
    return answer
#---------------------END----------------------------------------END-----------------------------------



if __name__=="__main__":
    ## IMPORTANT ##
    ## When you run this file,
    ## two commands must be provided as of now.
    ## EX: python3 main.py 4 2
    ## 4 is the number of colors
    ## 2 is the number of pegs

    
    # print(sys.argv[1])  # colors ex) 3
    # print(sys.argv[2])  # pegs   ex) 5

    example_answer = ABColor(int(sys.argv[2]))  # ONLY FOR TEST. This program should get an answer from SCSA.py
    print('EXAMPLE_ANSWER:', example_answer)    # ONLY FOR TEST

    for i in range(int(sys.argv[2])): # Initialize rule_out_dict array with empty sets.
        rule_out_dict.append(set())   # 

    cnt = 0 # nth guess

    # [Wikipedia explains Cartesian product well]
    #
    # Used Cartesian product below. It basiaclly gives you 
    # the first iterator of the set of all ordered pairs.
    # So, used for-loop to print all pairs.
    for prod in itertools.product(make_colors(int(sys.argv[1])), repeat=int(sys.argv[2])):
        cnt += 1
        
        guess = ''.join(prod) # Example: ''.join(['ab', 'pq', 'rs']) -> 'abpqrs'

        result = checker(guess, example_answer, cnt) # Suppose this checker is from SCSA. It returns a tuple with
                                # 3 elements(correct colors with correct places, correct colors with wrong places, nth step)

        if rule_out(guess): # If the guess was ruled out, skip it.
            
            # print('RULED OUT: ', guess, ' (DO NOT PRINT THIS GUESS. ONLY FOR TESTING)') # ONLY FOR TESTING, DO NOT PRINT IT ON SUBMISSION
            continue
        else:        
            if result[0] == 0 and result[1] == 0:  # If the first two elements of variable 'result' are zero,
                                                   # it means there were not correct colors with correct places
                                                   # and correct colors with wrong places.
                for i in range(len(guess)):        # Then, we will update the dictionary, rule_out_dict.
                    rule_out_dict[i].add(guess[i]) # For example, suppose our guess was 'CD' and the answer              
            print(guess, end=', ')                 # was 'AB'. Then chekcer function would give us [0, 0, nth guess]. 
                                                   # The reason is that 'CD' has 'no right colors with right places' 
                                                   # and 'no colors with wrong places'.
                                                   # Now it's time to update our rule-out-dict. It's obvious that
                                                   # we don't have to check our next guess if the first letter of it
                                                   # is 'C'. Also, we don't need to check if the second letter of 
                                                   # our next guess is 'D'.
                                                    
    # print('total counts:', cnt)
