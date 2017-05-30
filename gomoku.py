from board import Board
from board import Marker
import logging

class Gomoku:
	def __init__(self):
		self.board = Board(5)
		self.realUser = Marker(1)
		self.computerUser = Marker(-1)
	
	def getBoard(self):
		return self.board.returnBoard()
		
	def playRealUser(self, x, y):
		isEmpty = self.board.setField(self.realUser, int(x),int(y))
		self.board.checkWin(self.realUser)
		return isEmpty
		
	def playComputerUser(self):
		pass
