import sys
import time
state="..............."
N=3
K=2
#board = []
depth = 0
initial_board = [[0 for c in range(N)] for r in range(N)]
mainplayer='w'
opponent='b'
#board=[]
def init_board(initial_board):
    i=0
    for r in range(N):
        for c in range(N):
            #board.append(add_piece(initial_board, r, c, state[i]))
            initial_board[r][c]=state[i]
            #print state[i]
            i=i+1
    print initial_board
    return initial_board 

def print_board(move):
    #i=0
    print "::::move::::"
    for r in move:
        print r
    
        
def number_of_piece(board):
    count = 0
    for r in range(N):
        for c in range(N):
            if board[r][c] != '.':
                count += 1
    return count

def terminal_test(board):
    cw,cb=0,0

    #check draw
    if number_of_piece(board) == N * N:
        return 0
    #check row wise
    for i in range(0,N):
        cw,cb=0,0
        for j in range(0,N):
            if board[i][j]==mainplayer:
                cw+=1
                cb=0
            elif board[i][j]==opponent:
                cb+=1
                cw=0
            else:
                cb=0
                cw=0
            if cw==K:
                return -1
            elif cb==K:
                return 1
    
    #check column wise for an end state
    for i in range(0,N):
        cw,cb=0,0
        for j in range(0,N):
            if board[j][i]==mainplayer:
                cw+=1
                cb=0
            elif board[j][i]==opponent:
                cb+=1
                cw=0
            else:
                cb=0
                cw=0
            if cw==K:
                return -1
            elif cb==K:
                return 1        
    #checking diagonal for an end state
    col = 0
    for row in range(0,N):
        count_self_pd1, count_opp_pd1 = 0, 0
        count_self_pd2, count_opp_pd2 = 0, 0
        count_self_sd1, count_opp_sd1 = 0, 0
        count_self_sd2, count_opp_sd2 = 0, 0
        for r in range(0, N - row):
            if  board[row + r][col + r] == mainplayer :
                count_self_pd1 += 1
                count_opp_pd1 = 0
            elif board[row + r][col + r] == opponent:
                count_opp_pd1 += 1
                count_self_pd1 = 0
            else:
                count_self_pd1, count_opp_pd1 = 0, 0
                 
            if board[col + r][row + r] == mainplayer:
                count_self_pd2 += 1
                count_opp_pd2 = 0
            elif board[col + r][row + r] == opponent:
                count_opp_pd2 += 1
                count_self_pd2 = 0
            else:
                count_self_pd2, count_opp_pd2 = 0, 0
                
            if board[ (N - 1) - row - r ][r] == mainplayer:
                count_self_sd1 += 1
                count_opp_sd1 = 0
            elif board[ (N - 1) - row - r ][r] == opponent:
                count_opp_sd1 += 1
                count_self_sd1 = 0
            else:
                count_self_sd1, count_opp_sd1 = 0, 0
                
            if board[ (N - 1) - r ][row + r] == mainplayer:
                count_self_sd2 += 1
                count_opp_sd2 = 0
            elif board[ (N - 1) - r ][row + r] == opponent:
                count_opp_sd2 += 1
                count_self_sd2 = 0
            else:
                count_self_sd2, count_opp_sd2 = 0, 0
                
            if count_self_pd1 == K or count_self_pd2 == K or count_self_sd1 == K or count_self_sd2 == K:
                return -1
            elif count_opp_pd1 == K or count_opp_pd2 == K or count_opp_sd1 == K or count_opp_sd2 == K:
                return +1

    return 404

def add_piece(board, row, col, player):
    return board[0:row] + [board[row][0:col] + [player, ] + board[row][col + 1:]] + board[row + 1:]

def successors(board):
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
    #lst=board
    return lst
    
def minmax_decision(board):
    global depth
    fringe = [board]
    best_value = 0
    best_board = board
    string=str(board)
    counterw=string.count('w')
    counterb=string.count('b')
    if counterw > counterb:
        mainplayer='w'
        opponent='b'
    else:
        mainplayer='b'
        opponent='w'
    while terminal_test(best_board) == 404:
        best_value = -99999
        best_depth = -1
        for s in successors(fringe.pop()):
            depth = 0
            temp = min_value(s)
            if temp >= best_value and depth > best_depth :
                best_depth = depth
                best_value = temp
                best_board = s
        print_board(best_board)
        fringe.append(best_board)
    return best_board

def min_value(board):
    global depth
    if terminal_test(board) != 404: 
        return terminal_test(board)
    
    depth += 1
    v=99999
    for s in successors(board):
        v = min(v,max_value(s))
        #if v <= alpha:
         #   return v
        #beta=min(beta,v)
    #print "min value: %d" % v    
    return v

def max_value(board):
    global depth
    if terminal_test(board) != 404: 
        return terminal_test(board)    
    v = -99999
    depth += 1
    for s in successors(board):
        v = max(v,min_value(s))
        #if v >= beta:
         #   return v
        #alpha=max(alpha,v)
    return v

initial_board=init_board(initial_board)
minmax_decision(initial_board)
#print(time.time() - start_time)
