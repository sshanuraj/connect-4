import numpy as np 


class c4Board:
	def __init__(self):
		self.board = np.zeros((6, 7))
		self.cols = [5, 5, 5, 5, 5, 5, 5]
		self.colorCnt = [0, 0]
		self.moveCnt = 0
		self.lastMove = [-1, -1]
		
	def displayBoard(self):
		dic = {0:"-", 1:"Y", 2:"R"}
		for i in range(6):
			for j in range(7):
				print(dic[self.board[i][j]], end = " ")
			print()

	def makeMove(self, player, colNo):
		self.board[self.cols[colNo]][colNo] = player
		self.lastMove = [self.cols[colNo], colNo]
		self.cols[colNo] -= 1
		self.moveCnt += 1
		self.colorCnt[player - 1] += 1

	def inBoundary(self, x, y):
		if x<0 or x>5:
			return False
		if y<0 or y>6:
			return False
		return True

	def checkDown(self, board, lastMove):
		x = lastMove[0]
		y = lastMove[1]
		color = board[x][y] 
		count = 0
		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				return False
			x += 1
			count += 1
			if count == 4:
				return True
		return False

	def checkHorizontal(self, board, lastMove):
		x = lastMove[0]
		y = lastMove[1]
		color = board[x][y]
		count = 0
		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				break
			y += 1
			count += 1
			if count == 4:
				return True

		x = lastMove[0]
		y = lastMove[1] - 1

		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				break
			y -= 1
			count += 1
			if count == 4:
				return True

		if count >= 4:
			return True
		return False

	def checkDiag(self, board, lastMove):
		x = lastMove[0]
		y = lastMove[1]
		color = board[x][y]
		count = 0
		# upright 
		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				break
			x -= 1
			y += 1
			count += 1
			if count == 4:
				return True

		#downleft
		x = lastMove[0] + 1
		y = lastMove[1] - 1
		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				break
			x -= 1
			y += 1
			count += 1
			if count == 4:
				return True

		#upleft
		x = lastMove[0]
		y = lastMove[1]
		count = 0
		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				break
			x -= 1
			y -= 1
			count += 1
			if count == 4:
				return True

		#down right
		x = lastMove[0] + 1
		y = lastMove[1] + 1
		while True:
			if not self.inBoundary(x, y) or color != board[x][y]:
				break
			x += 1
			y += 1
			count += 1
			if count == 4:
				return True
		return False


	def checkWin(self):
		if self.checkDown(self.board, self.lastMove):
			return True
		if self.checkDiag(self.board, self.lastMove):
			return True
		if self.checkHorizontal(self.board, self.lastMove):
			return True
		return False

	def checkWinVirtual(self, board, x, y):
		lm = [x, y]
		if self.checkDown(board, lm):
			return True
		if self.checkDiag(board, lm):
			return True
		if self.checkHorizontal(board, lm):
			return True
		return False

	def resetBoard(self):
		self.board = np.zeros((6, 7))
		self.cols = [5, 5, 5, 5, 5, 5, 5]
		self.colorCnt = [0, 0]
		self.moveCnt = 0
		self.lastMove = [-1, -1]
