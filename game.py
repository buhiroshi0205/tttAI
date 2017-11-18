import numpy as np

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
