import logging

class Marker:
	def __init__(self,m):
		if(m == 1):
			self.marker = "X"
		elif(m == -1):
			self.marker = "O"
		else:
			print "Incorrect marker was chosen. Setting default \"X\""
			logging.info("Choose of incorrect sign of marker.")
			
class Field:
	def __init__(self):
		self.state = "-"
	
	def change(self, s):
		if(self.state == "-"):
			self.state = s.marker
			return True
		else:
			logging.info("User tried to change field which is already set")
			return False

class Board:
	def __init__(self, sizeBoard):
		self.sizeBoard = sizeBoard
		self.board = [[Field() for x in range(sizeBoard)] for y in range(sizeBoard)] 

	def returnBoard(self):
		boardAsString = " "
		for y in range(self.sizeBoard):
			boardAsString += str(y)
		boardAsString += "\n"
		for y in range(self.sizeBoard):
			boardAsString +=  str(y)
			for x in range(self.sizeBoard):
				boardAsString +=  self.board[y][x].state
			boardAsString +=  "\n"
		return boardAsString
	
	def setField(self, user, x, y):
		try:
			return self.board[y][x].change(user)
		except IndexError:
			return False
	
	def checkWin(self, user):
		#checking horizontal
		win = 0
		for y in range(self.sizeBoard):
			for x in range(self.sizeBoard):
				if( self.board[y][x].state == user.marker):
					win = win+1
				else:
					win = 0
				if( win >= 3):
					return True
		#checking vertical
		win = 0
		for x in range(self.sizeBoard):
			for y in range(self.sizeBoard):
				if( self.board[y][x].state == user.marker):
					win = win+1
				else:
					win = 0
				if( win >= 3):
					return True
		
		#checking diagonal
		win = 0
		for x in range(self.sizeBoard):
			for y in range(self.sizeBoard-x):
				if( self.board[y+x][y].state == user.marker):
					win = win+1
				else:
					win = 0
				if( win >= 3):
					return True
		win = 0
		for x in range(self.sizeBoard):
			for y in range(self.sizeBoard-x):
				if( self.board[y][y+x].state == user.marker):
					win = win+1
				else:
					win = 0
				if( win >= 3):
					return True
		#checking antidiagonal
		win = 0
		for x in range(self.sizeBoard):
			for y in range(self.sizeBoard-x):
				if( self.board[self.sizeBoard-1-(y+x)][y].state == user.marker):
					win = win+1
				else:
					win = 0
				if( win >= 3):
					return True
		win = 0
		for x in range(self.sizeBoard):
			for y in range(self.sizeBoard-x):
				if( self.board[self.sizeBoard-1-y][y+x].state == user.marker):
					win = win+1
				else:
					win = 0
				if( win >= 3):
					return True
		
		
		return False
		
		
		
