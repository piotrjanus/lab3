import socket
import sys
import logging
import os
import abc
from gomoku import Gomoku

class FSM(object):
	__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def handle(self, reponse):
		pass
	@abc.abstractmethod
	def getNextState(self):
		pass
	
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
			
		else:
			if(argType == 0):
				msg = "Option or position written incorrectly"
				logging.info("Client wrote position or paramter incorrectly")
				self.next_state = self
			elif(argType == 1):
				logging.info("Client sent x="+str(self.x)+" and y="+str(self.y))
				if( not self.game.playRealUser(self.x, self.y)):
					logging.info("Inocorrect field (out of range or with marker)")
					msg = "Inocorrect field (out of range or with marker)"
				else:
					msg = self.game.getBoard()
				self.next_state = self
			elif(argType == 2):
				if(response == "e"):
					self.next_state = self
				elif(response == "b"):
					msg = "b"
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
			if(arg == "e" or arg == "b"):
				return 2
			else:
				return 0
		
	def getNextState(self):
		return self.next_state

class ChooseGameServer(FSM): 
	
	def handle(self, response):
		msg = ""
		if(response == "1"):	
			logging.info("Client chose Gomoku")
			logging.info("next state GomokuServer")
			self.next_state = GomokuServer()
			msg = "1"
		else:
			logging.info("Client chose invalid game")
			logging.info("next state ChooseGameServer")
			self.next_state = self
			
		return msg
		
	def getNextState(self):
		return self.next_state

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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	