import socket 
import pacotes

def enviaComando(endereco, porta, comando, parametros):
	ipOrigem = '127.0.0.1' #loopback
	ipDestino = '127.0.0.1'
	
	addr = (endereco,porta)
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: #tentando conectar a maquina
		cliente.connect(addr) 
	except socket.error:
		return 'Conexao recusada!\nTalvez a maquina esteja desligada'
		
	#Codificando e enviando pacote
	packet = pacotes.codificaPacote(comando,parametros,ipOrigem,ipDestino,'000','00001111',0)
	cliente.send(packet) 
	
	#Recebendo e decodificando pacote
	packet = cliente.recv(8192) 
	comando,resposta,ipOrigem,ipDestino,ttl,id = pacotes.decodificaComandoPacote(packet);
	
	cliente.close()
	return resposta