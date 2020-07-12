from c4board import c4Board
import numpy as np
import random as rd
import pickle 

class Agent:
	def __init__(self, color, eps, df, alpha):
		self.color = color
		self.eps = eps
		self.discount_factor = df
		self.alpha = alpha
		self.state_value = {}
		self.game_states = []
		self.rating = 1600

	def calculateExpectedScore(self, oppRating):
		return 1/(1+(10**((oppRating - self.rating)/400)))

	def calculateRating(self, oppRating, res):
		self.rating = self.rating + (16 * (res - self.calculateExpectedScore(oppRating)))

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
				bcopy[board.cols[i]][i] = self.color
				if board.checkWinVirtual(bcopy, board.cols[i], i):
					return i
				h = self.getHash(bcopy)
				if self.state_value.get(h):
					val = self.state_value[h]
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
					elif 0.5 == maxv:
						moves.append(i)
		if len(moves) == 1:
			return moves[0]
		else:
			return moves[rd.randint(0, len(moves)-1)]

	def getHash(self, board): #get hash of current board
		h = ""
		dic = {0: "_", 2: "R", 1:"Y"}
		for i in range(6):
			for j in range(7):
				h = h + dic[board[i][j]]
		return h
	"""	
	def saveModel(self):
		f = open(str(self.color) + "_state_values.model", "wb")
		pickle.dump(self.state_value, f)
		f.close()

	def getModel(self):
		f = open(str(self.color) + "_state_values.model", "rb")
		self.state_value = pickle.load(f)
		f.close()
	"""
class HumanAgent:
	def __init__(self):
		self.rating = 1600

	def calculateExpectedScore(self, oppRating):
		return 1/(1+(10**((oppRating - self.rating)/400)))

	def calculateRating(self, oppRating, res):
		self.rating = self.rating + (16 * (res - self.calculateExpectedScore(oppRating)))
