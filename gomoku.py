from board import Board
from board import Marker
from random import randint
import logging

class Gomoku:
	def __init__(self):
		self.board = Board(5)
		self.realUser = Marker(1)
		self.computerUser = Marker(-1)
		self.win = 0
	
	def getBoard(self):
		return self.board.returnBoard()
		
	def playRealUser(self, x, y):
		isEmpty = self.board.setField(self.realUser, int(x),int(y))
		if(self.board.checkWin(self.realUser)):
			self.win = 1
		return isEmpty
		
	def playComputerUser(self):
		emptyFields = self.board.nOfEmptyFields()
		self.board.setOnNthEmpty(self.computerUser, randint(0,emptyFields))
		if(self.board.checkWin(self.computerUser)):
			self.win = -1
