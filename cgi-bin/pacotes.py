#Referencia https://en.wikipedia.org/wiki/Fletcher%27s_checksum
def crc16(packet):
	sum1, sum2 = 0, 0
	for i in range(0,len(packet)):
		sum1 = (sum1 + int(packet[i],2)) % 255
		sum2 = (sum2 + sum1) % 255
	sum = (sum2 << 8) | sum1
	return format((~sum & 0xFFFF),'016b')

def confereCheckSum(pacote):
	checksum = pacote[80:96]
	#zerando para o pacote ficar igual a quando seu Checksum foi calculado
	pacote = pacote[:80] + '0000000000000000' + pacote[96:]
	return  checksum == crc16(pacote)
	
def decodificaComandoPacote(pacote):
	version = pacote[0:4]
	IHL = pacote[4:8]
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
	options = pacote[160:totalLength];
	
	if (protocol == '00000001'):
		comando = 'ps'
	elif (protocol == '00000010'):
		comando = 'df'
	elif (protocol == '00000011'):
		comando = 'finger'
	elif (protocol == '00000100'):
		comando = 'uptime'
	
	parametros = ''.join(chr(int(options[i*8:i*8+8],2)) for i in range(0,len(options)/8))
	ipOrigem = BinarioparaIP(sourceAddress)
	ipDestino = BinarioparaIP(destinationAddress)
	id = int(identification,2)
	
	#verificando erros do pacote
	if not confereCheckSum(pacote): #verifica checksum
		raise Exception(comando,'Checksum nao confere, envie novamente a requisicao!',ipOrigem,ipDestino,timeToLive)
	
	return (comando,parametros,ipOrigem,ipDestino,timeToLive,id)
	
#Referencia https://stackoverflow.com/questions/19744206/converting-dot-decimal-ip-address-to-binary-python
def IPparaBinario(IP):
	return '' .join(format(int(x), '08b') for x in IP.split('.'))
 
def BinarioparaIP(binario):
	return '.'.join(str(int(binario[8*i:8*i+8],2),) for i in range(0,4))
	
def codificaPacote(comando, parametros, ipOrigem, ipDestino, flags, ttl, id):
	version = '0010' #versao 2
	IHL = '1010' #10 bytes
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
	
	totalLength = format(len(version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options),'016b')
	headerChecksum = crc16(version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options)
	return version + IHL + typeOfService + totalLength + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceAddress + destinationAddress + options