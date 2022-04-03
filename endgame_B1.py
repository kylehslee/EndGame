import sys
import itertools

# B1: Exhaustively enumerate all possibilities. Guess each possibility 
# in lexicographic order one at a time, and pay no attention to the 
# system’s responses. For example, if pegs p = 4 and colors c = 3, 
# guess AAAA, AAAB, AAAC, AABA, AABB, AABC and so on. This method 
# will take at most 𝑐1 guesses.

# It returns a string formed with letters alpabetically
# with the length of the parameter 'color'. 
# [EX] if color is 3, it returns 'ABC'
# [EX] if color is 4, it returns 'ABCD'
def make_colors(color):
    colors = []
    for i in range(color):
        colors.append(chr(i + 65))
    return colors
    

if __name__=="__main__":
    ## IMPORTANT ##
    ## When you run this file,
    ## two commands must be provided as of now.
    ## EX: python3 main.py 4 2
    ## 4 is the number of colors
    ## 2 is the number of pegs

    # print(sys.argv[1])  # colors ex) 3
    # print(sys.argv[2])  # pegs   ex) 5


    cnt = 0 # nth guess

    # [Wikipedia explains Cartesian product well]
    #
    # Used Cartesian product below. It basiaclly gives you 
    # the first iterator of the set of all ordered pairs.
    # So, used for-loop to print all pairs.
    for i in itertools.product(make_colors(int(sys.argv[1])), repeat=int(sys.argv[2])):
        print(''.join(i), end=', ') # print a pair.
        cnt += 1 # increment the count by 1 every loop.

     
