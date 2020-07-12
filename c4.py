from c4Agent import Agent, HumanAgent
from c4board import c4Board
import random as rd
import numpy as np 
import pickle, os

RED = 2
YELLOW = 1

class Connect4:
	def __init__(self):
		self.r = Agent(RED, 0.85, 0.9, 0.9)  #agent(color, epsilon, discount_factor, alpha)
		self.y = Agent(YELLOW, 0.85, 0.9, 0.9)
		self.h = HumanAgent()
		self.b = c4Board()

	def getAgentModel(self):
		filenames = ["1_agent.model", "2_agent.model", "h_agent.model"]
		agents = [self.y, self.r, self.h]
		i = 0
		for file in filenames:
			if os.path.isfile(file):
				f = open(file, "rb")
				print("%s opened."%file)
				if file[0] == '1':
					self.y = pickle.load(f)
				elif file[0] == '2':
					self.r = pickle.load(f)
				else:
					self.h = pickle.load(f)
				f.close()
			else:
				print("%s not found."%(file))
			i += 1

	def saveAgentModel(self):
		f = open("1_agent.model", "wb")
		g = open("2_agent.model", "wb")
		h = open("h_agent.model", "wb")
		pickle.dump(self.y, f)
		pickle.dump(self.r, g)
		pickle.dump(self.h, h)
		f.close()
		g.close()
		h.close()
		print("Agents saved.")

	def play(self, n):
		self.getAgentModel()
		# print(len(self.y.state_value))
		# print(len(self.r.state_value))

		for game in range(n):
			win = False
			if game%10000 == 0 and game != 0:
				self.r.decayEps(0.4)
				self.y.decayEps(0.4)
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
						self.r.calculateRating(self.y.rating, 1)
						self.y.calculateRating(self.r.rating, 0)
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
						self.r.calculateRating(self.y.rating, 0)
						self.y.calculateRating(self.r.rating, 1)
						print("GAME %s : Yellow wins.\n"%str(game))
						win = True
						break
			if win != True:
				self.y.getReward(0.4)
				self.r.getReward(0.4)
				self.y.resetState()
				self.r.resetState()
				self.b.displayBoard()
				self.r.calculateRating(self.y.rating, 0.5)
				self.y.calculateRating(self.r.rating, 0.5)
				print("GAME %s : Draw.\n"%str(game))
			self.b.resetBoard()
		self.saveAgentModel()

	def playHuman(self, n):
		self.getAgentModel()
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
						self.h.calculateRating(self.y.rating, 1)
						self.y.calculateRating(self.h.rating, 0)
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
						self.y.calculateRating(self.h.rating, 1)
						self.h.calculateRating(self.y.rating, 0)
						print("GAME %s : Yellow wins.\n"%str(game))
						win = True
						break
			if win != True:
				print("GAME %s : Draw."%str(game))
				self.y.getReward(0.4)
				self.y.resetState()
				self.y.calculateRating(self.h.rating, 0.5)
				self.h.calculateRating(self.y.rating, 0.5)

			print("Human Rating: %s"%(str(c4.h.rating)))
			print("Yellow Rating: %s"%(str(c4.y.rating)))
			self.b.resetBoard()
		self.saveAgentModel()

c4 = Connect4()
c4.play(50000)
print(c4.r.rating)
print(c4.y.rating)