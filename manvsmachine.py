import keras
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
model.load_weights('gay.h5')

num_weights = input('how many games do you want to play?')
turn = input('which player do you want to play? (1 or 2)')

for episode in range(num_weights):
	ttt.initialize_game()
	game_state = ttt.check_game()
	while not game_state[0]:
		board = ttt.get_board()
		move_probs = model.predict_on_batch(np.array([board]))[0]
		#move = np.random.choice(9, p=move_probs)
		move = np.argmax(move_probs)
		ttt.move(move)
		game_state = ttt.check_game()
	print "game %d done!" % episode