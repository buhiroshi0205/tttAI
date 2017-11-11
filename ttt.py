import numpy as np


board = np.zeros(9)  # 0 = no piece; 1 = cross; -1 = circle
turn = 1
illegal_move = 0
move_seq = []
moves = []

def initialize_game():
	global board, turn, illegal_move, move_seq, moves
	board = np.zeros(9)
	turn = 1
	illegal_move = 0
	move_seq.append(moves)
	moves = []

def move(x):
	global board, turn, illegal_move, moves
	if board[x]:
		illegal_move = turn
	else:
		board[x] = turn
	turn *= -1
	moves.append(x)

def check_game():
	global board, illegal_move
	sum = np.zeros(8)
	for n in range(3):
		sum += [board[n],board[n+3],board[n+6],board[3*n],board[3*n+1],board[3*n+2],board[3*n+n],board[2*n+2]]
	if illegal_move:
		return (True, -illegal_move)
	elif 3 in sum:
		return (True, 1)
	elif -3 in sum:
		return (True, -1)
	elif not (0 in board):
		return (True, 0)
	else:
		return (False, 0)

def get_board():
	global board, turn
	newboard = board*turn
	return np.concatenate((newboard==1, newboard==-1, newboard==0))
