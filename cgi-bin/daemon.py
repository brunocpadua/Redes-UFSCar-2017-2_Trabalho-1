import socket 
import argparse
import pacotes
import subprocess

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
	
#Referencia https://pythonhelp.wordpress.com/2011/11/20/tratando-argumentos-com-argparse/
parser = argparse.ArgumentParser()
parser.add_argument('--port', action='store', type=int, dest='port', required=True, help='Porta em qual o daemon.py ira rodar')
args = parser.parse_args()
	
#criando o socket
host = 'localhost' 
port = int(args.port) 
addr = (host, port) 
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(addr) 
tcp.listen(1) 
while True:
	print 'Aguardando conexao na porta ' + str(port)
	conn, cliente = tcp.accept() 
	
	#Recebendo o pacote
	packet = conn.recv(1024) 
	print 'Requisicao recebida'
	comando,parametros,ipOrigem,ipDestino,ttl,id = pacotes.decodificaComandoPacote(packet);
	print 'Executando comando ' + comando + ' ' + parametros 
	resposta = executaComando(comando,parametros)
	
	#Enviando a resposta
	packet = pacotes.codificaPacote(comando, resposta, ipOrigem, ipDestino, '111', ttl, id)
	conn.send(packet)
	print 'Resposta enviada!'
tcp.close()