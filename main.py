from __future__ import print_function

import random, game
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.animation as anime
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense

EPSILON = 0.1
EPISODES = 20
BATCH = 20

def custom_loss(y_true, y_pred):
	return K.mean(K.square(y_true) * K.square(y_true - y_pred))

def custom_loss2(y_true, y_pred):
	return K.sum((y_true+1)*(y_true-2)/(-2) * K.square(y_true - y_pred))

'''
def custom_loss3(y_true, y_pred):
	return np.sum((y_true+1)*(y_true-2)/(-2) * (y_true - y_pred)**2, axis = 1)
'''
model = Sequential()
model.add(Dense(81, activation='relu', input_shape=(27,)))
model.add(Dense(81, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(27, activation='relu'))
model.add(Dense(9, activation='softmax'))
model.compile(loss=custom_loss2, optimizer='RMSprop')
model.load_weights('weights_1000000.h5')

ttt = game.TTT(EPISODES)

board_batch = []
label_batch = []

file = open('game_lengths.txt', 'w')

for episode in range(EPISODES):
	board_data = np.empty((9,27))
	move_data = [None]*9
	ttt.initialize_game()
	game_over = False

	# play a game
	while not game_over:

		# obtain policy from ANN
		preprocessed_board = ttt.get_input_board()
		raw_policy = model.predict_on_batch(np.array([preprocessed_board]))[0]
		raw_policy = preprocessed_board[18:] * raw_policy #removes illegal moves
		#policy = raw_policy / np.sum(raw_policy) #scales probabilities to add up to 1

		# choose a move from policy
		
		if random.random() < EPSILON:
			random_policy = preprocessed_board[18:].astype('float32')/(9-ttt.move_num)
			move = np.random.choice(9, p=random_policy)
		else:
			move = np.argmax(raw_policy)
		
		#move = np.random.choice(9, p=policy)

		# save data for RL backprop
		board_data[ttt.move_num] = preprocessed_board
		move_data[ttt.move_num] = move

		game_over = ttt.move(move)

	# if someone won, save data to training queue
	file.write('%d\n' % ttt.move_num)
	if ttt.winner != 0:
		reward = (ttt.winner+1)/2
		labels = np.full((ttt.move_num+1,9), -1)
		for i in range(ttt.move_num+1):
			labels[i] = board_data[i][18:] * labels[i]
			labels[i][move_data[i]] = reward
			reward = 1 - reward
		board_batch.extend(board_data[:ttt.move_num+1])
		label_batch.extend(labels)

	# train-on-batch
	if (episode+1) % BATCH == 0:
		'''
		predict = model.predict_on_batch(np.array(board_batch))
		for i in range(len(label_batch)):
			print(predict[i])
			print(label_batch[i])
			print(custom_loss3(np.array(label_batch), predict)[i])
			print('\n\n')
			'''
		if len(label_batch) != 0: model.train_on_batch(np.array(board_batch), np.array(label_batch))/len(label_batch)
		board_batch = []
		label_batch = []

	if (episode+1) % 1000 == 0: print("game %d done!" % (episode + 1))
	if (episode+1) % 50000 == 0: model.save_weights('weights_%d.h5' % (episode + 1+200000))
#model.save_weights(str(input("Please specify a file name to store the ANN's weights:")))
#model.save_weights('v2test.h5')
print(ttt.move_seq[EPISODES-100:EPISODES])
file.close()