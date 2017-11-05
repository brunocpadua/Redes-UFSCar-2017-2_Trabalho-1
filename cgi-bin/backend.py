import socket 
import pacotes

def enviaComando(maquina, comando, parametros):
	ipOrigem = '127.0.0.1' #loopback
	ipDestino = '127.0.0.1'
	portas = [8000, 8001, 8002] #portas para comunicacao com cada maquina
	
	addr = ('localhost' ,portas[maquina])
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cliente.connect(addr) 
	
	#Codificando e enviando pacote
	packet = pacotes.codificaPacote(comando,parametros,ipOrigem,ipDestino,'000','00001111',0)
	cliente.send(packet) 
	
	#Recebendo e decodificando pacote
	packet = cliente.recv(8192) 
	comando,resposta,ipOrigem,ipDestino,ttl,id = pacotes.decodificaComandoPacote(packet);
	
	cliente.close()
	return resposta