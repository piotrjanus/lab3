import socket
import sys
import logging
import os
import abc
from random import randint
from gomoku import Gomoku

class FSM(object):
	__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def handle(self, reponse):
		pass
	
	def getNextState(self):
		return self.next_state
	
class MoreLessServer(FSM):
	def __init__(self):
		self.number = randint(0,100)
	
	def handle(self, response):
		argType = self.checkArg(response)
		msg = ""
		
		if(argType == 0):
			msg = "Incorrect argument"
			logging.info("Client sent incorrect parameter")
			self.next_state = self
			return msg
		if(argType == 1):
			msg = "Server generated number"
			self.next_state = self
			return msg
		if(argType == 2):
			msg = "b"
			logging.info("next state ChooseGameServer")
			self.next_state = ChooseGameServer()
			return msg
		if(argType == 3):
			logging.info("Client sent x="+str(self.clientNumber))
			if(self.clientNumber > self.number):
				msg = "Less"
			elif(self.clientNumber < self.number):
				msg = "More"
			else:
				msg = "win"
			self.next_state = self
			return msg
	
	def checkArg(self, arg):
		if(arg=="runGame"):
			return 1
		elif(arg=="b"):
			return 2
		else:
			try: 
				self.clientNumber = int(arg)
				return 3
			except ValueError:
				return 0
	
class GomokuServer(FSM):
	def __init__(self):
		self.game = Gomoku()
		
	def getInitialView(self):
		return self.game.getBoard()
		
	def handle(self, response):
		argType = self.checkArg(response)
		msg = ""
		if(response == "runGame"):
			msg = self.getInitialView()
			self.next_state = self
			return msg
			
		if(argType == 0):
			msg = "Option or position written incorrectly"
			logging.info("Client wrote position or paramter incorrectly")
			self.next_state = self
			return msg
		
		if(argType == 1):
			logging.info("Client sent x="+str(self.x)+" and y="+str(self.y))
			if( not self.game.playRealUser(self.x, self.y)):
				logging.info("Inocorrect field (out of range or with marker)")
				msg = "Inocorrect field (out of range or with marker)"
			else:
				self.game.playComputerUser()
				msg = self.game.getBoard()
			self.next_state = self
			
			if(self.game.win == 1):
				msg = "User win"
			elif(self.game.win == -1):
				msg = "Computer win"
			return msg
		
		if(argType == 2):
			msg = "b"
			logging.info("next state ChooseGameServer")
			self.next_state = ChooseGameServer()
			return msg
			
		
	
	def checkArg(self, arg):
		if(arg.find(",") != -1):
			coords = arg.split(",")
			if( len(coords) > 2):
				return 0
			try:
				self.x = int(coords[0])
				self.y = int(coords[1])
				return 1
			except ValueError:
				return 0
		
		else:
			if(arg == "b"):
				return 2
			else:
				return 0
		

class ChooseGameServer(FSM): 
	
	def handle(self, response):
		msg = ""
		if(response == "1"):	
			logging.info("Client chose Gomoku")
			logging.info("next state GomokuServer")
			self.next_state = GomokuServer()
			msg = response
		elif(response == "2"):	
			logging.info("Client chose MoreLess")
			logging.info("next state MoreLessServer")
			self.next_state = MoreLessServer()
			msg = response
		elif(response == "EMPTY"):
			logging.info("Client sent empty message")
			self.next_state = self
			msg = "EMPTY"
		else:
			logging.info("Client chose invalid game")
			logging.info("next state ChooseGameServer")
			self.next_state = self
			msg = "WRONG"
			
		return msg
		

class EchoServer:
	def __init__(self,address, port, data_size):
		self.data_size = data_size
		self._createTcpIpSocket()
		self._bindSocketToThePort(address, port)
		self.sock.listen(1)
		self.connection, client_address = self.sock.accept()
		logging.info("server initialized")
	
	def receive_msg(self):
		msg = self.connection.recv(self.data_size)
		logging.info("received msg: "+msg)
		return msg

	def send_msg(self, msg):
		logging.info("sent msg: "+msg)
		self.connection.send(msg)
		
	def _createTcpIpSocket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def _bindSocketToThePort(self, address, port):
		server_address = (address, port)
		logging.info("bind to %s port %s" % server_address)
		self.sock.bind(server_address)
		
		
if __name__ == "__main__":
	try:
		os.remove("server.log")
	except OSError:
		pass
	logging.basicConfig( format="%(asctime)s %(message)s", filename="server.log", level=logging.INFO)
	host = "localhost"
	port = 50001
	data_size = 1024
	logging.info("host: "+host+" port:"+str(port)+" data_size:"+str(data_size))
	server = EchoServer(host, port, data_size)
	
	
	fsm = ChooseGameServer()
	
	# w petli
	while(1):
		response = server.receive_msg()
		if (response=="e"):
			server.send_msg("e")
			break
		msg = fsm.handle(response)
		fsm = fsm.getNextState()
		server.send_msg(msg)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	