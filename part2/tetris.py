# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
from copy import deepcopy

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()
##1.ABSTRACTION : 
## START STATE : An empty tetris board.
## GOAL STATE : A complete row.
## SUCCESSOR FUNCTION : For a given incoming piece, calculate all the possible placements on the board, and assign each position a heuritic value.
## STATE SPACE : The board.
## Edge Weights : Assuming all the edge weights to be the same.
## HEURISTIC FUNCTION :
## Heuristic formula: a*aggregate height + b*no of completed lines + c*no of holes + d*bumpiness
## where a,b,c,d are the coefficients such that a,c,d are smaller as compared to b, because we want to maximize the completed lines.
## And a,c,d aim to minimize the variation in the height and the no of holes in the current board state.
## Our goal is to maximize the score which can be achieved by maximizing the no of completed lines. The heuristic will aim to do that.
## We will place the piece in all possible permutations on the board and choose the best option.

##2.EXPLANATION : Take the current tetris object,create a deepcopy of it, rotate the copy  and move it to left till it reaches column 0.
## Save all the moves and the current state of the object in a dictionary when we move left.
## Now move the rotated tetris object to the right till it reaches the last column.
## Save this permutation too in the dictionary with key as the moves and value as the state of the board.
## Now the dictionary contains all possible permutations of the current tetris object.
## HEURISTIC : Design a heuristic that minimizes the no of holes in the state, minimizes the difference in heights of adjacent columns, minimizes
## the average height of the board, and maximizes the no of completed lines.
## Pass each value(state of the board) to the heuristic function and compute a heuristic value for it.
## Save heuristic values for all the states in a dictionary and pick the best possible value of the heuristic.
## Return the moves corresponding to the maximum heuristic value.

##3.Problems faced - While designing the heuristics,faced problem to estimate the value of  the coefficients.
## Used a reference to estimate the value of the coefficients for the heuristic function.
## REFERENCE - https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/ 
## Assumptions - We are assuming that all the pieces have equal probability.

## High level discussion to find all the possible permutations of the object done with Rohil Bansal
#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    
    def calculate_heuristic(self,current_state):
        # use four possible heuristics:
        #reference used :https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        a = -0.510066
        b =  0.760666
        c = -0.35633
        d = -0.184483
        dict={}
        dict_holes = {} #will contain values corresponding to each column
        for k in range(10):
            dict[k]=0 #intialize dictionary
        
        noOfCompleteLines,noOfHoles,count,bumpiness,x,y = 0,0,0,0,0,1
        #noOfCompleteLines = n #add lines that vanished after moving the block down
        for i in range(0,20): #from 0 to 20
            row = current_state[i]
            count = row.count('x')
            if count== 10:
                noOfCompleteLines+=1
            for j in range(0,10): #from 0 to 10 for all the column values in the row
                if dict[j] == 0 and row[j] == 'x': #to calculate the height of each column
                    dict[j] = 20-i
                    
                if j not in dict_holes: #append the value of each column
                    dict_holes[j] = [row[j]]
                else:
                    dict_holes[j].append(row[j])    
        
         
        while y<10:
            bumpiness+=abs(dict[x]-dict[y]) #difference between heights of adjacent columns
            x+=1
            y+=1
        
        #calculate the number of holes by iterating on each column
        for key in dict_holes:
            startCount = False
            valueOfColumn = dict_holes[key]
            
            for m in range(0, len(valueOfColumn)):
                if startCount and valueOfColumn[m] == ' ': #check if an x has been encountered, count the no of holes below that
                    noOfHoles+=1
                if not startCount and valueOfColumn[m]=='x':
                    startCount = True
            
        aggregateHeight = sum(dict.values()) # sum of all the values of columns
        
        heuristic_val = a*aggregateHeight + b*noOfCompleteLines + c*noOfHoles + d*bumpiness 
        return heuristic_val
    
    
    # calculate all the possible moves for the current piece!!
    def getPossibleMove(self, tetris):
        dictionary = {}
        for i in range(0, 4):
            moves = ""
            copy = deepcopy(tetris)
            for j in range(0, i+1):
                copy.rotate()
                moves += "n" #Append n for each rotation
                movesLeft = moves
                movesRight = moves
                copyLeft = deepcopy(copy)
                copyRight = deepcopy(copy)
                current_piece_col = copy.get_piece()[2]
                for k in range(0, current_piece_col):
                    for j in range(0, k+1):
                        copyLeft.left()
                        movesLeft += "b" #Append b everytime the piece moves left
                    copyLeft.down()
                    dictionary[movesLeft] = copyLeft.get_board()
                    copyLeft = deepcopy(copy)
                    movesLeft = moves
                for k in range(0, 10-current_piece_col):
                    for j in range(0, k):
                        copyRight.right()
                        movesRight += "m" #Append m everytime the piece moves right
                    copyRight.down()
                    dictionary[movesRight] = copyRight.get_board()
                    copyRight = deepcopy(copy)
                    movesRight = moves
                    
        return dictionary
                
    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        #create a dictionary of all possible moves and a dictionary of all possible heuristics
        dictionary =  self.getPossibleMove(tetris)
        dict_heuristics = {}
        for key in dictionary:
            heuristic_val = self.calculate_heuristic(dictionary[key])
            dict_heuristics[key] = heuristic_val
        #pick the moves corresponding to the maximum heuristic value
	return (max(dict_heuristics, key=dict_heuristics.get))
        
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)
            
            dictionary = self.getPossibleMove(tetris)
            dict_heuristics = {}
            for key in dictionary:
                heuristic_val = self.calculate_heuristic(dictionary[key])
                dict_heuristics[key] = heuristic_val
        
        #pick the moves corresponding to the maximum heuristic value
            strVal = (max(dict_heuristics, key=dict_heuristics.get))
            for i in range(0, len(strVal)):
	        if(strVal[i] == 'b'):
                    tetris.left()
		elif(strVal[i] == 'm'):
                    tetris.right()
            	else:
                    tetris.rotate()
            tetris.down()
            


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s

