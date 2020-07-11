from c4Agent import Agent 
from c4board import c4Board
import random as rd
import numpy as np 

RED = 2
YELLOW = 1

class Connect4:
	def __init__(self):
		self.r = Agent(RED, 0.85, 0.9, 0.9)  #agent(color, epsilon, discount_factor, alpha)
		self.y = Agent(YELLOW, 0.85, 0.9, 0.9)
		self.b = c4Board()

	def play(self, n):
		for game in range(n):
			win = False
			if game%500 == 0 and game != 0:
				self.r.decayEps(0.8)
				self.y.decayEps(0.8)

			for i in range(42):
				if i%2 == 0:
					col = -1
					if self.r.eps < rd.uniform(0, 1):
						col = self.r.getBestMove(self.b)
					else:
						col = self.r.getRandomMove(self.b)

					self.b.makeMove(self.r.color, col)
					h = self.r.getHash(self.b.board)
					self.r.game_states.append(h)

					if self.b.checkWin():
						self.r.getReward(1)
						self.y.getReward(0)
						self.r.resetState()
						self.y.resetState()
						self.b.displayBoard()
						print("GAME %s : Red wins.\n"%str(game))
						win = True
						break
				else:
					col = -1
					if self.y.eps < rd.uniform(0, 1):
						col = self.y.getBestMove(self.b)
					else:
						col = self.y.getRandomMove(self.b)

					self.b.makeMove(self.y.color, col)
					h = self.y.getHash(self.b.board)
					self.y.game_states.append(h)

					if self.b.checkWin():
						self.y.getReward(1)
						self.r.getReward(0)
						self.y.resetState()
						self.r.resetState()
						self.b.displayBoard()
						print("GAME %s : Yellow wins.\n"%str(game))
						win = True
						break
			if win != True:
				print("GAME %s : Draw.\n"%str(i))
				self.y.getReward(0.4)
				self.r.getReward(0.4)
				self.y.resetState()
				self.r.resetState()
			self.b.resetBoard()
		self.r.saveModel()
		self.y.saveModel()

	def playHuman(self, n):
		self.y.getModel()
		for game in range(n):
			win = False
			self.r.eps = 0
			self.y.eps = 0
			for i in range(42):
				if i%2 == 0:
					col = int(input("Enter input:"))
					self.b.makeMove(self.r.color, col)
					self.b.displayBoard()
					print("\n")

					if self.b.checkWin():
						self.y.getReward(0)
						self.y.resetState()
						print("GAME %s : Red wins.\n"%str(game))
						win = True
						break
				else:
					col = -1
					if self.y.eps < rd.uniform(0, 1):
						col = self.y.getBestMove(self.b)
					else:
						col = self.y.getRandomMove(self.b)

					self.b.makeMove(self.y.color, col)
					self.b.displayBoard()
					h = self.y.getHash(self.b.board)
					self.y.game_states.append(h)
					print("\n")

					if self.b.checkWin():
						self.y.getReward(1)
						self.y.resetState()
						print("GAME %s : Yellow wins.\n"%str(game))
						win = True
						break
			if win != True:
				print("GAME %s : Draw."%str(game))
				self.y.getReward(0.4)
				self.y.resetState()
			self.b.resetBoard()
		self.y.saveModel()

c4 = Connect4()
c4.playHuman(1)
