from __future__ import print_function

import random, game
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense

EPSILON = 0.1
EPISODES = 5000

def custom_loss(y_true, y_pred):
	return K.square(y_true) * K.square(y_true - y_pred)

def custom_loss2(y_true, y_pred):
	return (y_true+1)*(y_true-2)/(-2) * K.square(y_true - y_pred)

model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss=custom_loss2, optimizer='RMSprop')
#model.load_weights('v2test.h5')

ttt = game.TTT(EPISODES + 10)

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
	if (episode % 100) == 99: print("game %d done!" % (episode + 1))
	if (episode % 50000) == 49999: model.save_weights('weights_%d.h5' % (episode + 1))
#model.save_weights(str(input("Please specify a file name to store the ANN's weights:")))
#model.save_weights('v2test.h5')
print(ttt.move_seq[EPISODES-100:EPISODES])

#1. add illegal moves -> zero training
#2. mini-batch training
#3. rectify loss function