# Simple tetris program! v0.2
# D. Crandall, Sept 2016
from copy import deepcopy
from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
import random


def evaluate(b):#this function evaluates best position to place tetris block
	
	#print "******************************in evlaute"
	for i in b:#this loop gets count of x in each column
		c=[]
		for j in range(0,20):
			val=i[j].count('x')
			c.append(val)
		i.append(c)
	
	#print b
	#print "b\n"
	fringe=[[' ',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1]]] #simply called it fringe not a fringe in essence but close
	loop_cond=19
	#print i[-1][loop_cond]
	#print fringe[0][-1][loop_cond]
	while loop_cond >=0 :#find the highest populated column
		flag=True
		for i in b:
			if i[-1][loop_cond]>fringe[0][-1][loop_cond]:
				del fringe[:]
				flag=True
				fringe.append(i)
				#print '\n'
				#print i[-1][loop_cond]
				#print fringe[0][-1][loop_cond]
			if i[-1][loop_cond] == fringe[0][-1][loop_cond]:#check if the newly added element is same as the first
				fringe.append(i)
				#print '\n before the if'
				#print i[-1]
				#print fringe[0][-1]
				if i[-1]!=fringe[0][-1]:
					flag=False
		
		#print '\nfringe'
		#print fringe
		#print flag
		if flag == True:#if all elements in fringe have same arrangement value pick from random probably could do some thinking here
			h=random.randrange(0,len(fringe))
			#print fringe[h]
			#print 'chosen is'
			loop_cond=-1
			return fringe[h]  #return this
			
		if flag == False:#if they arent same start searching from the next coulmn
			loop_cond=loop_cond-1
			del b[:]
			b=fringe[:]
			del fringe[:]
			fringe=[[' ',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1]]]
		
				
			
		
	#print "****************************************"








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
	test=deepcopy(tetris)
	a=test.get_board()
	piece,row,col=tetris.get_piece()
	b=[]
	right=deepcopy(test)
	trace=1
	moves_list=[['x', 'x', 'x', 'x'],['xxxx'],['xx', 'xx'],['xxx', ' x '],[' x', 'xx', ' x'],[' x ', 'xxx'],['x ', 'xx', 'x '],['x  ', 'xxx'],['xx', 'x ', 'x '],['xxx', '  x'],[' x', ' x', 'xx'],['xx ', ' xx'],[' x', 'xx', 'x '],['xx ', ' xx'],[' x', 'xx', 'x ']]#this list contains all the moves of tetris, we now have more moves than mick jagger !!!
	ind=moves_list.index(piece)
	rot=0
	if ind <=1: #find which kind it belongs to
		rot=1#line
	elif ind==2:
		rot=0#box
	elif ind>2 and ind<7:
		rot=3#T
	elif ind>6 and ind<11:
		rot=3#L
	elif ind>10 and ind <15:
		rot=2#z
	count_rot=0
	while rot>=0:#while we have more rotations
		skip=1
		score=tetris.get_score()
		q=col
		w=col
		q=q-1
		while q >= 0 : #move left
			left=deepcopy(test)
			for i in range(0,trace):
				left.left()
			left.down()
			a=left.get_board()
			a.append('left')
			a.append(trace)
			a.append(count_rot)
			b.append(a)
			#new_score
			if left.get_score() > score:#we cleared a column
				del b[:]
				del a[:]
				b.append('left')
				b.append(trace)
				b.append(count_rot)
				#b.append(a)				
				b.append([-1,-1,-1,-1])
				w=11
				rot=-3
				skip=0
				break
				#print a
				#print 'yahtzee'
				#exit()
			q=q-1
			trace=1+trace
		w=w+1
		trace=1
		while w < 10 :
			right=deepcopy(test)#move right
			for i in range(0,trace):
				right.right()
			right.down()
			a=right.get_board()
			a.append('right')
			a.append(trace)
			a.append(count_rot)
			b.append(a)
			if right.get_score() > score:#we cleared a column
				#print 'yahtzee'
				del b[:]
				del a[:]
				b.append('right')
				b.append(trace)
				b.append(count_rot)
				#b.append(a)
				b.append([-1,-1,-1,-1])
				rot=-3
				skip=0
				break
				#print a
				#exit()
			w=w+1
			trace=1+trace
		rot=rot-1
		count_rot=count_rot+1
		test.rotate()			
	#print b
	if skip:
		k=evaluate(b) #got the place to move
	else:
		k=b[:]
		print k	
	#print k
	#print "^k"
	#print k[-4] # right or left
	#print k[-3] #position
	if k[-4]=='right':
		m='m'
	else:
		m='b'

	#print "####################################################"
	for i in range(0,k[-2]):
		tetris.rotate()
	return m * k[-3]
        #return random.choice("mnb") * random.randint(1, 10)
       
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



