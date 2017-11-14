import numpy as np

class TTT():

	def __init__(self, storage=200000):
		self.move_seq = np.empty((storage, 9))
		self.episode = 0

	def initialize_game(self, first_player):
		self.move_seq[self.episode] = self.moves
		self.episode += 1
		self.board = np.zeros(9)
		self.moves = np.empty(9)
		self.turn = first_player
		self.move_num = 0

	def move(self, x):
		self.board[x] = self.turn
		moves[move_num] = x
		if self.check_game():
			self.winner = self.turn
			return True
		elif move_num == 8:
			self.winner = 0
			return True
		else:
			self.turn *= -1
			move_num += 1
			return False

	def check_game(self):
		over     =     self.board[4] == self.board[0] == self.board[8] or self.board[4] == self.board[1] == self.board[7] or self.board[4] == self.board[2] == self.board[6] or self.board[4] == self.board[3] == self.board[5]
		return over or self.board[0] == self.board[1] == self.board[2] or self.board[0] == self.board[3] == self.board[6] or self.board[8] == self.board[2] == self.board[5] or self.board[8] == self.board[6] == self.board[7]

	def get_input_board():
		newboard = self.board*self.turn
		return np.concatenate((newboard==1, newboard==-1, newboard==0))


		'''
		if x == 0:
			return turn == self.board[1] == self.board[2] or turn == self.board[3] == self.board[6] or turn == self.board[4] == self.board[8]
		elif x == 1:
			return turn == self.board[0] == self.board[2] or turn == self.board[4] == self.board[7]
		elif x == 2:
			return turn == self.board[1] == self.board[0] or turn == self.board[4] == self.board[6] or turn == self.board[5] == self.board[8]
		elif x == 3:
			return turn == self.board[0] == self.board[6] or turn == self.board[4] == self.board[5]
		elif x == 4:
			return turn == self.board[0] == self.board[8] or turn == self.board[1] == self.board[7] or turn == self.board[2] == self.board[6] or turn == self.board[3] == self.board[5]
		elif x == 5:
			return turn == self.board[3] == self.board[4] or turn == self.board[2] == self.board[8]
		elif x == 6:
			return turn == self.board[2] == self.board[4] or turn == self.board[0] == self.board[3] or turn == self.board[7] == self.board[8]
		elif x == 7:
			return turn == self.board[1] == self.board[4] or turn == self.board[6] == self.board[8]
		elif x == 8:
			return turn == self.board[0] == self.board[4] or turn == self.board[2] == self.board[5] or turn == self.board[6] == self.board[7]
		;;;