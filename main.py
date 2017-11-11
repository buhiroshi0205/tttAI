from __future__ import print_function

import ttt
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD


model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.1))



for episode in range(100000):
	p1, p2 = [[],[],[]], [[],[],[]]
	ttt.initialize_game()
	game_state = ttt.check_game()
	while not game_state[0]:
		board = ttt.get_board()
		move_probs = model.predict_on_batch(np.array([board]))[0]
		move = np.random.choice(9, p=move_probs)
		if ttt.turn == 1:
			p1[0].append(board)
			p1[1].append(move_probs)
			p1[2].append(move)
		else:
			p2[0].append(board)
			p2[1].append(move_probs)
			p2[2].append(move)
		ttt.move(move)
		game_state = ttt.check_game()
	if game_state[1] != 0:
		label = (1,0)
		if game_state[1] == -1:
			label = (0,1)
		for i in range(len(p1[0])):
			p1[1][i][p1[2][i]] = label[0]
		for i in range(len(p2[0])):
			p2[1][i][p2[2][i]] = label[1]
		#gradient update
		data = np.concatenate((np.array(p1[0]), np.array(p2[0])))
		label = np.concatenate((np.array(p1[1]), np.array(p2[1])))
		data = data.astype('float32')
		model.train_on_batch(data, label)
	print("game %d done!" % episode)
