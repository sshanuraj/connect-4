from c4Agent import Agent, HumanAgent
from c4board import c4Board
import random as rd
import numpy as np 
import pickle, os

RED = 2
YELLOW = 1

class Connect4:
	def __init__(self):
		self.r = 0  #agent(color, epsilon, discount_factor, alpha)
		self.y = 0
		self.h = 0
		self.getAgentModel()
		self.b = c4Board()

	def checkParams(self):
		print("NN input array length for RED Agent:", len(self.r.nnInp))
		print("State value length for RED Agent:", len(self.r.state_value))

		print("NN input array length for YELLOW Agent:", len(self.y.nnInp))
		print("State value length for YELLOW Agent:", len(self.y.state_value))

	def getAgentModel(self):
		filenames = ["1_agent.model", "2_agent.model", "h_agent.model"]
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
				if file == "1_agent.model":
					self.y = Agent(YELLOW, 0.8, 0.9, 0.9)
				elif file == "2_agent.model":
					self.r = Agent(RED, 0.8, 0.9, 0.9)
				else:
					self.h = HumanAgent()
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
		# print(len(self.y.state_value))
		# print(len(self.r.state_value))
		self.r.setEpsilon(0)
		self.y.setEpsilon(0)
		for game in range(n):
			win = False
			if game%20000 == 0 and game != 0:
				self.r.decayEps(0.5)
				self.y.decayEps(0.5)

			# self.r.eps = 0
			# self.y.eps = 0

			redR = self.r.rating
			yellowR = self.y.rating

			for i in range(42):
				if i%2 == 0:
					col = -1
					h_ini = self.r.getHash(self.b.board)
					self.r.nnInp.add(h_ini)
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
						self.r.calculateRating(yellowR, 1)
						self.y.calculateRating(redR, 0)
						print("GAME %s : Red wins.\n"%str(game))
						win = True
						break
				else:
					col = -1
					h_ini = self.y.getHash(self.b.board)
					self.y.nnInp.add(h_ini)
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
						self.r.calculateRating(yellowR, 0)
						self.y.calculateRating(redR, 1)
						print("GAME %s : Yellow wins.\n"%str(game))
						win = True
						break
			if win != True:
				self.y.getReward(0.4)
				self.r.getReward(0.4)
				self.y.resetState()
				self.r.resetState()
				self.b.displayBoard()
				self.r.calculateRating(yellowR, 0.5)
				self.y.calculateRating(redR, 0.5)
				print("GAME %s : Draw.\n"%str(game))
			self.b.resetBoard()
		self.saveAgentModel()

	def playHumanvsYellow(self, n):
		for game in range(n):
			win = False
			self.r.eps = 0
			self.y.eps = 0

			yellowR = self.y.rating
			humanR = self.h.rating

			for i in range(42):
				if i%2 == 0:  #human move
					col = int(input("Enter input:"))
					self.b.makeMove(self.r.color, col)
					self.b.displayBoard()
					print("\n")

					if self.b.checkWin():
						self.y.getReward(0)
						self.y.resetState()
						self.h.calculateRating(yellowR, 1)
						self.y.calculateRating(humanR, 0)
						print("GAME %s : Human wins.\n"%str(game))
						win = True
						break
				else:   #yellow agent move
					col = -1
					if self.y.eps < rd.uniform(0, 1):
						col = self.y.getBestMoveNN(self.b)
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
						self.y.calculateRating(humanR, 1)
						self.h.calculateRating(yellowR, 0)
						print("GAME %s : Yellow wins.\n"%str(game))
						win = True
						break
			if win != True:
				print("GAME %s : Draw."%str(game))
				self.y.getReward(0.4)
				self.y.resetState()
				self.y.calculateRating(humanR, 0.5)
				self.h.calculateRating(yellowR, 0.5)

			print("Human Rating: %s"%(str(self.h.rating)))
			print("Yellow Rating: %s"%(str(self.y.rating)))
			self.b.resetBoard()
		self.saveAgentModel()

	def playHumanvsRed(self, n):
		for game in range(n):
			win = False
			self.r.eps = 0
			self.y.eps = 0

			redR = self.r.rating
			humanR = self.h.rating

			for i in range(42):
				if i%2 == 0:  #red agent move
					col = -1
					if self.r.eps < rd.uniform(0, 1):
						col = self.r.getBestMoveNN(self.b)
					else:
						col = self.r.getRandomMove(self.b)

					self.b.makeMove(self.r.color, col)
					self.b.displayBoard()
					h = self.r.getHash(self.b.board)
					self.r.game_states.append(h)
					print("\n")

					if self.b.checkWin():
						self.r.getReward(1)
						self.r.resetState()
						self.y.resetState()
						self.r.calculateRating(humanR, 1)
						self.h.calculateRating(redR, 0)
						print("GAME %s : Red wins.\n"%str(game))
						win = True
						break
					
				else:  #human move
					col = int(input("Enter input:"))
					self.b.makeMove(self.y.color, col)
					self.b.displayBoard()
					print("\n")

					if self.b.checkWin():
						self.r.getReward(0)
						self.r.resetState()
						self.y.resetState()
						self.r.calculateRating(humanR, 0)
						self.h.calculateRating(redR, 1)
						print("GAME %s : Human wins.\n"%str(game))
						win = True
						break
			if win != True:
				print("GAME %s : Draw."%str(game))
				self.r.getReward(0.4)
				self.r.resetState()
				self.r.calculateRating(humanR, 0.5)
				self.h.calculateRating(redR, 0.5)

			print("Human Rating: %s"%(str(self.h.rating)))
			print("Red Rating: %s"%(str(self.r.rating)))
			self.b.resetBoard()
		self.saveAgentModel()

c4 = Connect4()
c4.play(1)
c4.r.train()
c4.y.train()
c4.saveAgentModel()

# c4.playHumanvsYellow(1)
c4.checkParams()

