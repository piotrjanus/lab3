import abc
import os
import logging
import socket

class FSM(object):
	__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def handle(self, reponse):
		pass
	@abc.abstractmethod
	def getNextState(self):
		pass

class GomokuClient(FSM):
	
	def handle(self, response):
		print response
		if("win" in response):
			logging.info(response)
			self.next_state = ChooseGameClient()
			response = "b"
			return response
		
		response = raw_input("Please give postion in form X,Y or argument: e - exit, b - back to menu \n")
		self.next_state = self
		if(response == "b"):
			logging.info("next state ChooseGameClient")
			self.next_state = ChooseGameClient()
		
		return response
	
	def getNextState(self):
		return self.next_state

class ChooseGameClient(FSM):
	
	def handle(self, response):
		
		msg = ""
		if( response == "1"):
			logging.info("next state GomokuClient")
			self.next_state = GomokuClient()
			msg = "runGame"
		else:
			msg = raw_input("1 - gomoku, 2 - more/less \n")
			logging.info("next state ChooseGameClient")
			self.next_state = self
			
		return msg
	
	def getNextState(self):
		return self.next_state

class EchoClient:
	def __init__(self,address, port, data_size):
		self.data_size = data_size
		self._createTcpIpSocket()
		self._connectToServer(address, port)
		logging.info("Client initialized")
		
	def sendAndReceiveMsg(self, msg):
		logging.info("Client sent msg: "+msg)
		self.sock.send(msg)
		response  = self.sock.recv(self.data_size)
		logging.info("Client received msg: "+response)
		return response
		
	def _createTcpIpSocket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def _connectToServer(self, address, port):
		server_address = (address, port)
		print("bind to %s port %s" % server_address)
		self.sock.connect(server_address)
		
		
if __name__   == "__main__":
	try:
		os.remove("client.log")
	except OSError:
		pass
	logging.basicConfig( format="%(asctime)s %(message)s", filename="client.log", level=logging.INFO)
	host = "localhost"
	port = 50001
	data_size = 1024
	logging.info("host: "+host+" port:"+str(port)+" data_size:"+str(data_size))
	client = EchoClient(host, port, data_size)
	
	response = ""
	fsm = ChooseGameClient()
	
	#w petli
	while(1):
		response = fsm.handle(response)
		fsm = fsm.getNextState()
		response = client.sendAndReceiveMsg(response)
		if (response=="e"):
			break
	
	
	
	
	
	
	
	
	
	