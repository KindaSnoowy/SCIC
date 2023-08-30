import socket, pickle

ip = '192.168.246.277' # ip
port = 55555 # porta

class Network:
	def __init__(self):
		self.conect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, HOST = ip, PORT = port): 
		self.HOST = HOST
		self.PORT = PORT

		try:
			self.conect.connect((self.HOST, self.PORT))
		except:
			print("Servidor não iniciado.")

	def send(self, data):
		try:
			self.conect.send(pickle.dumps(data))
		except:
			print("Erro ao enviar mensagem.")

	def recv(self, size):
		return self.conect.recv(size)


def Login(name):
	return {
		'type': 'LOGIN',
		'name': name
	}

def Client_Message(msg, bomba = False):
	return {
		'type':'MESSAGE',
		'msg': msg,
		'bomba': bomba
	}

def Arquivo_req():
	return {
		'type': 'ARQUIVO'
	}



