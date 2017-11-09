#Referencia: livro do Kurose (5.2.2 da 5 ed), RFC 1071 e http://slideplayer.com/slide/6672096/
def checksum(packet):
	sum = 0
	for i in range(0,len(packet),16):
		sum += int(packet[i:i+16],2)
		sum = (sum >> 16) + (sum & 0xFFFF)
	return format(~sum & 0xFFFF,'016b')
	
def confereCheckSum(pacote):
	headerChecksum = pacote[80:96]
	IHL = int(pacote[4:8],2)
	cabecalho = pacote[0:160+32*(IHL-5)]
	#zerando para o pacote ficar igual a quando seu Checksum foi calculado
	cabecalho = cabecalho[:80] + '0000000000000000' + cabecalho[96:]
	return headerChecksum == checksum(cabecalho)


def decodificaComandoPacote(pacote):
	version = pacote[0:4]
	IHL = int(pacote[4:8],2)
	typeOfService = pacote[8:16]
	totalLength = int(pacote[16:32],2)
	identification = pacote[32:48]
	flags = pacote[48:51]
	fragmentOffset = pacote[51:64]
	timeToLive = pacote[64:72]
	protocol = pacote[72:80]
	headerChecksum = pacote[80:96]
	sourceAddress = pacote[96:128]
	destinationAddress = pacote[128:160]
	options = pacote[160:160+32*(IHL-5)]
	data = pacote[160+32*(IHL-5):totalLength];
	
	if (protocol == '00000001'):
		comando = 'ps'
	elif (protocol == '00000010'):
		comando = 'df'
	elif (protocol == '00000011'):
		comando = 'finger'
	elif (protocol == '00000100'):
		comando = 'uptime'
	
	parametros = ''.join(chr(int(options[i*8:i*8+8],2)) for i in range(0,len(options)/8))
	dados = ''.join(chr(int(data[i*8:i*8+8],2)) for i in range(0,len(data)/8))
	
	ipOrigem = BinarioparaIP(sourceAddress)
	ipDestino = BinarioparaIP(destinationAddress)
	id = int(identification,2)
	
	#verificando erros do pacote
	if not confereCheckSum(pacote): #verifica checksum
		raise Exception(comando,'Checksum nao confere, envie novamente a requisicao!',ipOrigem,ipDestino,timeToLive)
	
	return (comando,parametros,dados,ipOrigem,ipDestino,timeToLive,id)
	
#Referencia https://stackoverflow.com/questions/19744206/converting-dot-decimal-ip-address-to-binary-python
def IPparaBinario(IP):
	return '' .join(format(int(x), '08b') for x in IP.split('.'))
 
def BinarioparaIP(binario):
	return '.'.join(str(int(binario[8*i:8*i+8],2),) for i in range(0,4))
	
def codificaPacote(comando, parametros, dados, ipOrigem, ipDestino, flags, ttl, id):
	version = '0010' #versao 2
	IHL = '0000' #calculado abaixo
	typeOfService = '00000000'
	totalLength = '0000000000000000' #calculado abaixo
	identification = format(id,'016b')
	flags = flags #000 se requisicao e 111 se resposta
	fragmentOffset = '0000000000000'
	
	#campo timeToLeave
	if (flags == '000'):
		timeToLive = ttl
	else:
		timeToLive = format((int(ttl,2)-1),'08b') #decrementando 1 caso resposta
	
	#campo protocal
	if (comando == 'ps'): 
		protocol = '00000001'
	elif (comando == 'df'):
		protocol = '00000010'
	elif (comando == 'finger'):
		protocol = '00000011'
	elif (comando == 'uptime'):
		protocol = '00000100'
		
	headerChecksum = '0000000000000000' #calculado abaixo
	sourceAddress = IPparaBinario(ipOrigem)
	destinationAddress = IPparaBinario(ipDestino)
	options = ''.join(format(ord(x), '08b') for x in parametros)
	#faz o padding
	while (len(options)%32) != 0:
		options += '0'
	data = ''.join(format(ord(x), '08b') for x in dados)
	
	#calculando as informacoes que faltavam
	IHL = format((len(version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options)/32),'04b')
	totalLength = format(len(version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options + data),'016b')
	headerChecksum = checksum(version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options)
	return version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options + data