from c4board import c4Board
from keras import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
import numpy as np
import random as rd
import pickle 
import os

class Agent:
	def __init__(self, color, eps, df, alpha):
		self.color = color
		self.eps = eps
		self.discount_factor = df
		self.alpha = alpha
		self.state_value = {}
		self.game_states = []
		self.nnInp = set()
		self.rating = 1600
		self.nnModel = 0
		self.initNNModel()

	def initNNModel(self):
		if not os.path.isfile("nn_%s_weights.h5"%(str(self.color))):
			print("Creating h5 Weight File.")
			self.nnModel = Sequential()
			self.nnModel.add(Dense(32, activation = "tanh", input_dim = 42))
			self.nnModel.add(Dense(32, activation = "tanh"))
			self.nnModel.add(Dense(7, activation = "sigmoid"))
			self.nnModel.save_weights("nn_%s_weights.h5"%(str(self.color)))

	def train(self):
		print("Start Training for Model %s."%(str(self.color)))
		X, Y = self.getNNInput()
		print("Shape for input and labels:", X.shape, Y.shape)
		self.nnModel.load_weights("nn_%s_weights.h5"%(str(self.color)))

		sgd = optimizers.SGD(lr = 0.5, clipnorm = 1.)
		self.nnModel.compile(loss = "mse", optimizer = sgd, metrics = ["accuracy"])
		self.nnModel.fit(X, Y, epochs = 100)
		self.nnModel.save_weights("nn_%s_weights.h5"%(str(self.color)))

		print("Training complete....Model For %s Saved" % (str(self.color)))

	def getBestMoveNN(self, board):
		inp = [] 
		inp.append(self.serialize(self.getHash(board.board)))
		wm = board.checkForWinningMove(self.color)
		if wm > -1:
			return wm
		self.nnModel.load_weights("nn_%s_weights.h5"%(str(self.color)))
		m = self.nnModel.predict(np.array(inp))
		# print(m)

		for i in range(7):
			if board.cols[i] == -1:
				m[0][i] = 0

		res = np.where(m[0] == max(m[0]))
		return res[0][rd.randint(0, len(res) - 1)]

	def getBoardFromHash(self, h):
		board = np.zeros((6, 7))
		k = 0  
		hToNum = {"_" : 0, "R" : 2, "Y" : 1}
		for i in range(6):
			for j in range(7):
				board[i][j] = hToNum[h[k]]
				k += 1
		return board

	def setEpsilon(self, eps):
		self.eps = eps

	def serialize(self, state):
		arr = []
		hToNum = {"_" : 0, "R" : 2, "Y" : 1 }
		for i in state:
			arr.append(hToNum[i])
		return arr

	def getNNInput(self):
		labels = []
		inp = []
		for i in self.nnInp:
			arr = self.serialize(i)
			inp.append(arr)
			board = self.getBoardFromHash(i)
			labels.append(self.getNextStateVals(board))
		return np.array(inp), np.array(labels)

	def calculateExpectedScore(self, oppRating):
		return 1/(1+(10**((oppRating - self.rating)/400)))

	def calculateRating(self, oppRating, res):
		self.rating = self.rating + (16 * (res - self.calculateExpectedScore(oppRating)))

	def getMaxFromRes(self, boardHash):
		return max(self.nnModel.predict(np.array([self.serialize(boardHash)]))[0])

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
					val = 0.5
					if val > maxv:
						maxv = val
						moves = []
						moves.append(i)
					elif val == maxv:
						moves.append(i)
		if len(moves) == 1:
			return moves[0]
		else:
			return moves[rd.randint(0, len(moves)-1)]

	def getNextStateVals(self, board):
		vals = [0, 0, 0, 0, 0, 0, 0]
		max_ = -10000
		max_ind = []
		for i in range(7):
			if board[0][i] == 0:
				bcopy = board.copy()
				k = 5
				while True:
					if bcopy[k][i] == 0:
						break
					k = k - 1

				bcopy[k][i] = self.color

				b = c4Board()

				if b.checkWinVirtual(bcopy, k, i):
					vals[i] = 1
					return vals

				h = self.getHash(bcopy)

				if self.state_value.get(h):
					val = self.state_value[h]
					if max_ < val:
						max_ = val
						max_ind = [i]
					elif max_ == val:
						max_ind.append(i)
				else:
					val = 0.5
					if max_ < val:
						max_ = val
						max_ind = [i]
					elif max_ == val:
						max_ind.append(i)

		if len(max_ind) == 1:
			vals[max_ind[0]] = 1
		else:
			vals[max_ind[rd.randint(0, len(max_ind) - 1)]] = 1

		return vals

	def getHash(self, board): #get hash of current board
		h = ""
		nToHash = {0: "_", 2: "R", 1:"Y"}
		for i in range(6):
			for j in range(7):
				h = h + nToHash[board[i][j]]
		return h
	
class HumanAgent:
	def __init__(self):
		self.rating = 1600

	def calculateExpectedScore(self, oppRating):
		return 1/(1+(10**((oppRating - self.rating)/400)))

	def calculateRating(self, oppRating, res):
		self.rating = self.rating + (16 * (res - self.calculateExpectedScore(oppRating)))


# a = Agent(1, 0.9, 0.8, 0.8)
# board = np.zeros((6,7))
# Hash = a.getHash(board)
# print(a.getBoardFromHash(Hash))

