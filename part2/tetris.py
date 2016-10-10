# Simple tetris program! v0.2
# D. Crandall, Sept 2016
from copy import deepcopy
from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys



def evaluate(b):
	
	print "******************************in evlaute"
	for i in b:
		c=[]
		for j in range(0,20):
			val=i[j].count('x')
			c.append(val)
		i.append(c)
	
	#print b
	#print "\n b^"
	fringe=[[' ',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1]]]
	for i in b:
		#print i[-1][-1]
		#print '\n ^-i1'
		#print fringe[0][-1][-1]
		#print '\n ^fringe'
		if i[-1][-1]>fringe[0][-1][-1]:
			del fringe[:]
			fringe.append(i)
		elif i[-1][-1]==fringe[0][-1][-1]:
			fringe.append(i)
	
	print 'fringe'	
	print fringe
	print "****************************************"








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
    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
	print "\n##################################################"
	test=deepcopy(tetris)
	a=test.get_board()
	#print "first print"
	#print a
	piece,row,col=tetris.get_piece()
	b=[]
	q=col
	w=col
	q=q-1
	right=deepcopy(test)
	trace=1
	while q >= 0 :
		left=deepcopy(test)
		for i in range(0,trace):
			left.left()
		left.down()
		a=left.get_board()
		a.append('left')
		a.append(trace)
		b.append(a)
		q=q-1
		trace=1+trace
	w=w+1
	trace=1
	while w < 10 :
		right=deepcopy(test)
		for i in range(0,trace):
			right.right()
		right.down()
		a=right.get_board()
		a.append('right')
		a.append(trace)
		b.append(a)
		w=w+1
		trace=1+trace			
	
	evaluate(b)
	for i in b:
		print "\n"
		print i
	#print "piece row col"
	#print piece,row,col
	#test.left()
	#test.down()
	#a=test.get_board()
	#print "second print"
	#print a
	#print "length of rows" - its 20 rows , 10 columns
	#print len(a)
	#for i in a:
		#print len(i)
		#print i.count('x')
	print "####################################################"
        return random.choice("mnb") * random.randint(1, 10)
       
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

            board = tetris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < tetris.col):
                tetris.left()
            elif(index > tetris.col):
                tetris.right()
            else:
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



