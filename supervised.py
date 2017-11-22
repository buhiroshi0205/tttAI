import keras, minimax, random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K

def custom_loss(y_true, y_pred):
	return K.sum(y_true * -K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred))

model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss='mse', optimizer='rmsprop')

boards = np.empty((4519, 27))
raw_boards = np.zeros((4519, 9))
labels = np.empty((4519, 9))
index = 0

# prepare dataset
with open('states.txt', 'r') as file:
	for i in range(4519):
		state = file.readline().strip()
		if state.count('X') == state.count('O'):
			p1, p2 = 'O', 'X'
		else:
			p1, p2 = 'X', 'O'
		state = list(state)
		temp = np.array(state)
		available_moves = [j for j in range(9) if state[j] == '-']
		evaluation = np.full(9, -2)
		for move in available_moves:
			state[move] = p1
			evaluation[move] = minimax.evaluate(state, p2)
			state[move] = '-'
		label = np.zeros(9)
		max_eval = max(evaluation)
		if max_eval == 1:
			for j in range(9):
				if evaluation[j] == 1: label[j] = 1
		elif max_eval == 0:
			for j in range(9):
				if evaluation[j] == 0: label[j] = 1
		else:
			continue
		boards[index] = np.concatenate((temp==p1, temp==p2, temp=='-'))
		labels[index] = label
		for i in range(9):
			if temp[i] == 'X':
				raw_boards[index][i] = -1
			elif temp[i] == 'O':
				raw_boards[index][i] = 1
		index += 1
model.fit(boards[:index], labels[:index], epochs=50)
model.save_weights('supervised.h5')
