from __future__ import print_function

import keras, ttt
import numpy as np
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
model.load_weights('model1.h5')

num_games = input('how many games do you want to play?')

for episode in range(num_games):
	player = input('which player do you want to play? (1 or -1)')
	ttt.initialize_game()
	game_state = ttt.check_game()
	turn = player
	while not game_state[0]:
		if turn == 1:
			print(np.reshape(ttt.board, (3,3)))
			move = input('make your move.') - 1
			ttt.move(move)
		elif turn == -1:
			board = ttt.get_board()
			move_probs = model.predict_on_batch(np.array([board]))[0]
			move = np.argmax(move_probs)
			ttt.move(move)
		game_state = ttt.check_game()
		turn *= -1
	if game_state[1]*player == 1:
		print("you win!")
	else:
		print("you lose!")
	print(ttt.moves)

