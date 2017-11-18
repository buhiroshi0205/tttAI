from __future__ import print_function

import keras, game
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

ttt = game.TTT()

model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss='mean_squared_error', optimizer='RMSprop')
model.load_weights('weights_800000.h5')

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