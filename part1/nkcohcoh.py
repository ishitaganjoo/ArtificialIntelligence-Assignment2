# -*- coding: utf-8 -*-
# Assignment 2: Task 1 (Ncoh-coh k)
#In this problem there are two possible moves at each time. Either 'w' or 'b'
#If the board is empty then the first move is given by w
#It is assumed that 'w' is always taking the first step..so no 'b' is allowed as first player
# So at initial state number of 'b' must be less than or equal to 'w'
#Initial state: initially the given state as input is the initial state
#successor: generates all possible combinations of marble placing from the given state and so on
#Terminal State: when any k number of consecutive 'w' or 'b' complete a row colum or diagonal
#cost function: There is no cost for going one state to another. So we can assume cost as uniform
#We implemented min max algorithm in order to find the best move from a given state. As long as 'w' is considered as first player 
#for each given step the algorithm gives the best outcome for the initial/first player
#To make the procedure faster Alpha beta pruning is implemented
#For time limit Iterative Deepening Search is applied
#First the depth limit(highest_level) is very low and we tried to find best solution from the depths below the depth limit
#if the time still allows then it increases the depth limit and try to find the best solution within that depth
#if after completing the search within the depth limit it seems that the time exceeds then it gives the best solution found till depth#
import time
import sys
#state="................"
#N=3
#k=2
ndepth = 1
#initial player
mainplayer='w'
first_player='w'
opponent='b'
infinity=9999999
#max_time=5
highest_level=1
start=0
final_str=""
#read inputs from command lines 
if len(sys.argv) < 5:
    print "Not enough arguments. Please check again"#
    sys.exit()
elif len(sys.argv) > 5:
    print "Too many arguments. Please check again"
    sys.exit()
else:
    N=int(sys.argv[1])
    k=int(sys.argv[2])
    state=sys.argv[3]
    max_time=int(sys.argv[4])

#initialize a N*N board for playing Ncohcoh-k
initial_board = [[0 for i in range(N)] for j in range(N)]

#Adding elements in the board
i=0
for r in range(N):
    for c in range(N):
        initial_board[r][c]=state[i]
        i=i+1
print "Initial Board:"
print initial_board
#total number of marbles in the board            
def current_number_marble(board):
    c=0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '.':
                c=c+1
    return c
#functions used from assignment 0 code
def add_piece(board, row, col, val):
    return board[0:row] + [board[row][0:col] + [val, ] + board[row][col + 1:]] + board[row + 1:]

#generate all possible states from any given state of the board
def successors(board):
    global first_player
    string=str(board)
    counterw=string.count('w')
    counterb=string.count('b')    
    if counterw > counterb:
        val='b'
    else:
        val='w'
    lst=[]
    for r in range(0, N):
        for c in range(0,N):
            if board[r][c]=='.': 
                #board[r][c]=val 
                #lst[r][c]=val             
                lst.append(add_piece(board, r, c, val))
    return lst

#check whether the board reached into a goal state
def is_goal(board):    
    global mainplayer
    global opponent
    countw=0 
    countb=0
    #check row wise
    for i in range(N):
        countw=0 
        countb=0
        for j in range(N):
            if board[i][j]==mainplayer:
                countw=countw+1
                countb=0
            elif board[i][j]==opponent:
                countb=countb+1
                countw=0
            else:
                countb=0
                countw=0
            if countb==k:
                return 1
            elif countw==k:
                return -1
    
    #check column wise for an end state
    for i in range(N):
        countw=0 
        countb=0
        for j in range(N):
            if board[j][i]==mainplayer:
                countw=countw+1
                countb=0
            elif board[j][i]==opponent:
                countb=countb+1
                countw=0
            else:
                countb=0
                countw=0
            if countb==k:
                return 1
            elif countw==k:
                return -1        
    #checking diagonal for an end state
    #checking main diagonal    
    for i in range(N):
        countw=0 
        countb=0
        for j in range(N-i):
            if  board[i+j][j]==mainplayer :
                countw=countw+1
                countb = 0
            elif board[i+j][j]==opponent:
                countb= countb+1
                countw = 0
            else:
                countw=0 
                countb=0
            if countb==k:
                return 1
            elif countw==k:
                return -1

    for i in range(N):
        countw=0 
        countb=0
        for j in range(N-i):
            if board[j][i+j]==mainplayer:
                countw=countw+1
                countb = 0
            elif board[j][i+j]==opponent:
                countb=countb+1
                countw = 0
            else:
                countw=0
                countb=0                
            if countb==k:
                return 1
            elif countw==k:
                return -1
    
    #Secondary Diagonal Checking
    for i in range(N):
        countw, countb = 0, 0
        for j in range(N-i):                   
            if board[ (N-1)-i-j][j]==mainplayer:
                countw=countw+1
                countb = 0
            elif board[ (N-1)- i - j][j]==opponent:
                countb=countb+1
                countw = 0
            else:
                countw=0 
                countb=0         
            if countb==k:
                return 1
            elif countw==k:
                return -1
    for i in range(N):
        countw, countb = 0, 0
        for j in range(N-i):                   
            if board[ (N-1)- j][i+j]==mainplayer:
                countw=countw+1
                countb = 0
            elif board[(N-1)-r][i+j]==opponent:
                countb=countb+1
                countw = 0
            else:
                countw=0
                countb=0                
            if countb==k:
                return 1
            elif countw==k:
                return -1
    #check for whether there is a draw
    if current_number_marble(board)==N*N:
        return 0
    #still not finished
    return "Not finished"
def minimize_func(board,alpha, beta,depth):
    global ndepth
    global highest_level
    global start
    #print "In terminal test: %s " %is_goal(board)
    if is_goal(board) != "Not finished": 
        if depth > ndepth:
            ndepth=depth
        return is_goal(board)    
    v=infinity    
    for succ in successors(board):
        if depth == highest_level:
            ndepth = depth
            return 0
        #print "Inside Min",
        #print_board(s)
        v = min(v,maximize_func(succ,alpha, beta,depth+1))
        if v <= alpha:
            return v
        beta=min(beta,v)
        if time.time()-start >max_time-0.1:
            return v
    #print "min value: %d" % v    
    return v

def maximize_func(board,alpha, beta,depth):
    global ndepth
    global highest_level
    global start
    #print "In terminal test: %s " %is_goal(board)
    if is_goal(board) != "Not finished":
        if depth > ndepth:
            ndepth=depth
        #print "In terminal test: %d " %is_goal(board) 
        return is_goal(board)    
    v = -infinity
    for succ in successors(board):
        if depth == highest_level:
            ndepth = depth
            return 0
        #print "Inside Max",
        #print_board(s)
        v = max(v,minimize_func(succ,alpha, beta,depth+1))
        if v >= beta:
            return v
        alpha=max(alpha,v)
        if time.time()-start>max_time -0.1:
            return v
    #print "max value: %d" % v    
    return v    
def ncohcoh_main(board):
    global ndepth
    global mainplayer
    global opponent
    global first_player
    global highest_level
    global start
    print "Thinking! Please wait::"
    fringe = [board]
    prev_boards=[]
    move = 0
    best_move = board
    #prev_board=board
    string=str(best_move)
    counterw=string.count('w')
    counterb=string.count('b')
    if counterw < counterb:
        print "B should not be the First Player"
        sys.exit()
    if counterw <= counterb:
        mainplayer='w'
        opponent='b'
    else:
        mainplayer='b'
        opponent='w'
    #first_player=mainplayer
    start = time.time()
    while (1):
    #while time.time()-start<max_time and not (ndepth < highest_level):
        #print "::::::::Starting from the beginning::::"
        #print_board(best_move)
        string=str(best_move)
        counterw=string.count('w')
        counterb=string.count('b')
        if counterw <= counterb:
            mainplayer='w'
            opponent='b'
        else:
            mainplayer='b'
            opponent='w'
        #print mainplayer    
        move=-infinity
        bdepth=-infinity        
        for s in successors(fringe.pop()):
            depth=0
            ndepth=0
            value = minimize_func(s,-infinity,infinity,depth)
            if value==move and ndepth>bdepth:  
                #print "222222222222222  Best Dept: *****************************%d" %ndepth                  
                bdepth,move,best_move =ndepth, value,s
            elif value > move:
                #print "Best Dept: *****************************%d" %ndepth
                bdepth,move,best_move =ndepth, value,s                
        time_elapsed=time.time()-start
        #print time_elapsed
        if time_elapsed < max_time-0.1 and ndepth<highest_level:            
            for i in range(N):
               for j in range(N):
                   if best_move[i][j]!=board[i][j]:
                       print("Hmm, I'd recommend putting your marble at Row", i, "Column:", j)                      
            return best_move           
        if time_elapsed < max_time-0.1 and ndepth==highest_level:            
            highest_level=3*highest_level
            prev_boards.append(best_move)
            best_move = board    
            #print "===============highest_level:::========= %d " %highest_level                  
        elif time_elapsed > max_time-0.1:
            for i in range(N):
               for j in range(N):
                   if best_move[i][j]!=board[i][j]:
                       print("Hmm, I'd recommend putting your marble at Row", i, "Column:", j)                      
            return best_move
        fringe.append(best_move)

final_board=ncohcoh_main(initial_board)
for i in range(N):
    for j in range(N):
        final_str+=final_board[i][j]
print "\n New Board:"        
print final_str
