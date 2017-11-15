from __future__ import print_function

import random
import numpy as np
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense

#EPSILON = 0.1
EPISODES = 1000

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



def custom_loss(y_true, y_pred):
	return K.square(y_true) * K.square(y_true - y_pred)

model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss=custom_loss, optimizer='sgd')

ttt = TTT(EPISODES * 2)

for episode in range(EPISODES):
	board_data = np.empty((9,27))
	move_data = np.zeros((9, 9))
	ttt.initialize_game()
	game_over = False
	while not game_over:

		# obtain policy from ANN
		preprocessed_board = ttt.get_input_board()
		raw_policy = model.predict_on_batch(np.array([preprocessed_board]))[0]
		raw_policy = (ttt.board == 0) * raw_policy #removes illegal moves
		policy = raw_policy / np.sum(raw_policy) #scales probabilities to add up to 1

		# choose a move from policy
		'''
		if random.random() < EPSILON:
			move = random.randint(0,8)
		else:
			move = np.argmax(policy)
		'''
		move = np.random.choice(9, p=policy)

		# save data for RL backprop
		board_data[ttt.move_num] = preprocessed_board
		move_data[ttt.move_num][move] = ttt.turn

		game_over = ttt.move(move)

	# if someone won, gradient update
	if ttt.winner != 0:
		move_data *= ttt.winner
		model.train_on_batch(board_data[:ttt.move_num+1], move_data[:ttt.move_num+1])

	if (episode % 10) == 0: print("game %d done!" % episode)
#model.save_weights(str(input("Please specify a file name to store the ANN's weights:")))
model.save_weights('v2test.h5')
print(ttt.move_seq[EPISODES-100:EPISODES])