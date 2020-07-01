from c4Board import c4Board
import numpy as np
import random as rd

class Agent:
	def __init__(self, color, eps, df, alpha):
		self.color = color
		self.eps = eps
		self.discount_factor = df
		self.alpha = alpha
		self.state_value = {}
		self.game_states = []

	def getReward(self, reward):
		tot_reward = reward
		for i in range(len(self.game_states)-1, -1, -1):
			if self.state_value.get(self.game_states[i]) is None:
				self.state_value[self.game_states[i]] = 0.5

			if i == len(self.game_states) - 1:
				self.state_value[self.game_states[i]] = tot_reward
				continue
			
			self.state_value[self.game_states[i]] += ((self.alpha*(tot_reward - self.state_value[self.game_states[i]]))*self.discount_factor)
			tot_reward = self.state_value[self.game_states[i]]

	def resetState(self):
		self.game_states = []

	def decayEps(self, dec):
		self.eps = self.eps * dec

	def getRandomMove(self, board):
		while True:
			colR = rd.randint(0,6)
			if board.cols[colR] == -1:
				continue
			return colR

	def getBestMove(self, board):
		maxv = -1
		moves = []
		for i in range(7):
			if board.cols[i] != -1:
				bcopy = board.board.copy()
				bcopy[board.cols[i]][i] = color
				if board.checkWin(bcopy, [board.cols[i], i]):
					return i
				if self.state_value.get(self.getHash(bcopy)):
					if val > maxv:
						maxv = val
						moves = []
						moves.append(i)
					elif val == maxv:
						moves.append(i)
				else:
					if 0.5 > maxv:
						maxv = 0.5
						moves = []
						moves.append(i)


	def getHash(self, board): #get hash of current board
		return ""
		
	def saveStateValues(self):
		f = open(self.color + "_state_values", "wb")
		pickle.dump(self.state_value, f)
		f.close()

	def getStateValues(self):
		f = open(self.color + "_state_values", "rb")
		self.state_value = pickle.load(f)
		f.close()