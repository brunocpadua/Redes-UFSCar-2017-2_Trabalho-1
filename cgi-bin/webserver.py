#!/usr/bin/env python
#Referencia https://docs.python.org/2/library/cgi.html
import cgitb
import cgi
import backend

cgitb.enable()    

#pegando os parametros da pagina HTML inicial
resultadoHTML = cgi.FieldStorage()

#separando e codificando os resultados da pagina HTML
resultadoHTMLKeys = resultadoHTML.keys() #pegando as keys - nomes dos campos no resultadoHTML
resultadoHTMLKeys.remove('submit') #removendo a key do botao de envio
resultadoHTMLKeys.sort() #ordena as keys para ordenar os comandos por maquina (1,2,3)

listaComandos = []
for key in resultadoHTMLKeys:
	#verifica se o key eh do tipo 'maqX_comando' (comando sem argumento)
	if '_' in key:
		#se existir alguma outra key do tipo 'maqX-comando' (comando com argumento)
		#entao, ele da preferencia a esse key e nao usa a atual
		if not key[:4] + '-' + key[5:] in resultadoHTMLKeys:
			listaComandos.insert(len(listaComandos),{'maq':key[3],'cmd':resultadoHTML[key].value,'arg':''})
	else: #senao, eh do tipo 'maqX-comando' (comando com argumento)
		
			listaComandos.insert(len(listaComandos),{'maq':key[3],'cmd':key[5:],'arg':resultadoHTML[key].value})

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print("Teste!")

print '<p>'
for comando in listaComandos:
	print backend.enviaComando(int(comando['maq'])-1,comando['cmd'],comando['arg'])
print '</p>'


	
