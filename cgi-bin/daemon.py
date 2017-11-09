import socket 
import argparse
import pacotes
import subprocess
import threading

#funcao para executar comando
def executaComando(comando,argumentos):
	#Validando para verificar se nao existem parametros maliciosos nos argumentos adicionais
	if('|' in argumentos or ';' in argumentos or '>' in argumentos):
		return 'Existem parametros maliciosos nesta requisicao'
	
	#Executando o comando
	try:
		output = subprocess.check_output(comando + ' ' + argumentos, shell=True)
	except subprocess.CalledProcessError:                                                                                                   
		return "Comando invalido"

	return output
	
#Referencia https://stackoverflow.com/questions/23828264
class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port 
		addr = (host, port) 
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(addr)
		
	def listen(self):
		self.socket.listen(5)
		while True:
			cliente, endereco = self.socket.accept()
			cliente.settimeout(5)
			threading.Thread(target = self.listenToClient,args = (cliente,endereco)).start()

	def listenToClient(self, cliente, endereco):
		while True:
			try:
				#Recebendo o pacote
				packet = cliente.recv(1024)
				if packet:
					#Decodificando pacote
					print 'Requisicao recebida na porta ' + str(self.port)	
					try:
						comando,parametros,dados,ipOrigem,ipDestino,ttl,id = pacotes.decodificaComandoPacote(packet);
					except Exception as e:
						packet = pacotes.codificaPacote(e.args[0], '', e.args[1], e.args[2], e.args[3], '111', e.args[4], 0) #editar depois
						cliente.send(packet)
						print 'Erro: Checksum nao confere'
						print ''
					
					#Executando comando
					print 'Executando comando ' + comando + ' ' + parametros 
					resposta = executaComando(comando,parametros)
					#Enviando a resposta
					packet = pacotes.codificaPacote(comando, '', resposta, ipOrigem, ipDestino, '111', ttl, 0)
					cliente.send(packet)
					print 'Resposta enviada!'
					print ''
				else:
					raise error('Cliente desconectado')
			except:
				cliente.close()
				return False

if __name__ == "__main__":
	#Referencia https://pythonhelp.wordpress.com/2011/11/20/tratando-argumentos-com-argparse/
	parser = argparse.ArgumentParser()
	parser.add_argument('--port', action='store', type=int, dest='port', required=True, help='Porta em qual o daemon.py ira rodar')
	args = parser.parse_args()
	
	ThreadedServer('localhost',int(args.port)).listen()