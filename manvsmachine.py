from __future__ import print_function

import keras, ttt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

class TTT():

	def __init__(self, storage=200000):
		self.move_seq = np.zeros((storage, 9))
		self.episode = 0

	def initialize_game(self, first_player=1):
		self.board = np.zeros(9)
		self.moves = np.full(9, -1)
		self.turn = first_player
		self.move_num = 0

	def move(self, x):
		self.board[x] = self.turn
		self.moves[self.move_num] = x
		if self.check_game():
			self.winner = self.turn
		elif self.move_num == 8:
			self.winner = 0
		else:
			self.turn *= -1
			self.move_num += 1
			return False
		# next code only reached if game ends
		self.move_seq[self.episode] = self.moves
		self.episode += 1
		return True

	def check_game(self):
		over     =     0 != self.board[4] == self.board[0] == self.board[8] or 0 != self.board[4] == self.board[1] == self.board[7] or 0 != self.board[4] == self.board[2] == self.board[6] or 0 != self.board[4] == self.board[3] == self.board[5]
		return over or 0 != self.board[0] == self.board[1] == self.board[2] or 0 != self.board[0] == self.board[3] == self.board[6] or 0 != self.board[8] == self.board[2] == self.board[5] or 0 != self.board[8] == self.board[6] == self.board[7]

	def get_input_board(self):
		newboard = self.board*self.turn
		return np.concatenate((newboard==1, newboard==-1, newboard==0))

ttt = TTT()

model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.1))
model.load_weights('v2test.h5')

numpad_to_grid = [0,6,7,8,3,4,5,0,1,2]
num_games = input('how many games do you want to play?')

for episode in range(num_games):
	player = input('which player do you want to play? (1 or -1)')
	ttt.initialize_game()
	game_over = False
	turn = player
	while not game_over:
		if turn == 1:
			print(np.reshape(ttt.board, (3,3)))
			move = numpad_to_grid[input('make your move.')]
			game_over = ttt.move(move)
		elif turn == -1:
			preprocessed_board = ttt.get_input_board()
			raw_policy = model.predict_on_batch(np.array([preprocessed_board]))[0]
			raw_policy = (ttt.board == 0) * raw_policy #removes illegal moves
			print(np.reshape(raw_policy, (3,3)))
			move = np.argmax(raw_policy)
			game_over = ttt.move(move)
		turn *= -1
	if ttt.winner*player == 1:
		print("you win!")
	elif ttt.winner*player == -1:
		print("you lose!")
	else:
		print("tie!")
	print(ttt.moves)