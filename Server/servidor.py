import socket
from _thread import start_new_thread
import pickle, os
import random

HOST = 'localhost' # ip
PORT = 5555 # porta 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	server.bind((HOST, PORT))
	print(f"Servidor iniciado.\nHOST: {'127.0.0.1' if HOST == 'localhost' else HOST}\nPORT: {PORT}")
except:
	print("Servidor já aberto.")
	
server.listen()
falas_oppenheimer = ["SIM SOU O OPPENHEIMER", 
"uwu", 
"Einsten", 
"Bomba russas", 
"Frio e Calculadora", 
"Oppenheimer", 
"Agora eu me tornei a morte. Destruidor de mundos", 
"O poder fica nas sombras.", 
"Eles não vão temê-lo até que o entendam. E eles não vão entender até que tenham usado.", 
"Hiroshima, não é sobre você.",
"Por que você não luta?",
"Será que alguém, algum dia, vai dizer a verdade sobre o que está acontecendo aqui?",
"Zero seria bom",
"Não exclua todas as pessoas que entende o que você faz. Um dia você vai precisar delas.",
"Não estamos condenando. Apenas negando",
"Você não comete pecado e depois pede a todos nós que sintamos pena de você quando houver consequências",
"Acredito que sim"]

clients_connected = []
names = []
PATH = os.path.abspath("log.txt") # Caminho absoluto (tentativa de não bugar tudo.)

def _client_thread(client):
	try:
		name = ''
		while True:
			data = pickle.loads(client.recv(2048))

			if data['type'] == "LOGIN":
				if not (data['name'] in names):
					name = data['name']
					texto = f"O usuário [{name}] se conectou."

					log = open(f"{PATH}", 'a')
					log.write(f"{texto}\n")
					log.close()
					for i_conn in range(len(clients_connected)):
						conn = clients_connected[i_conn]
						if conn != client:
							conn.send(f"{texto}".encode())

					names.append(name)
					client.send("CONFIRMADO".encode('utf-8'))
				else:
					client.send('ERROR'.encode())

			elif data['type'] == "MESSAGE":
				try:
					log = open(f"{PATH}", 'a')

					if 'oppenheimer' in data['msg'].lower():
						texto = f"[{name}]:{data['msg']}\n[Oppenheimer]:{random.choice(falas_oppenheimer)}"
					elif not data['bomba']:
						texto = f"[{name}]:{data['msg']}"
					elif data['bomba']:
						x, y = data['msg'].split()
						texto = f"(BOMBA) O usuário [{name}] está lançando uma BOMBA nas coordenadas: x={x}, y={y}."
					
					log.write(f"{texto}\n")
					log.close()
					for i_conn in range(len(clients_connected)):
						conn = clients_connected[i_conn]
						conn.send(f"{texto}".encode())
				except:
					pass

			elif data['type'] == "ARQUIVO":
				log = open(f"{PATH}", 'r')
				text = log.read()[:-1]
				client.send(text.encode() if text != "" else " ".encode())
				log.close()

	except Exception as E:
		texto = f"O usuário [{name}] se desconectou."

		log = open(f"{PATH}", 'a')

		log.write(f"{texto}\n")
		log.close()
		for i_conn in range(len(clients_connected)):
			conn = clients_connected[i_conn]
			if conn != client:
				conn.send(f"{texto}".encode())
		clients_connected.remove(client)
		names.remove(name)

while True:
	conn, adress = server.accept()
	print(f"Cliente conectado: {adress}")
	clients_connected.append(conn)
	start_new_thread(_client_thread, (conn,))
