#!/usr/bin/env python
#Referencia https://docs.python.org/2/library/cgi.html
import cgitb
import cgi
import backend

cgitb.enable()    

#configuracao do endereco e porta de cada maquina
deamons = {'1':{'endereco':'localhost','porta':8000},'2':{'endereco':'localhost','porta':8001},'3':{'endereco':'localhost','porta':8002}}

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
		#entao, usa a key com o argumento 
		keyComArg = key[:4] + '-' + key[5:]
		if keyComArg in resultadoHTMLKeys:
			listaComandos.insert(len(listaComandos),{'maq':key[3],'cmd':key[5:],'arg':resultadoHTML[keyComArg].value})
		else: #senao, ele usa a key sem argumento mesmo
			listaComandos.insert(len(listaComandos),{'maq':key[3],'cmd':resultadoHTML[key].value,'arg':''})
			
#executando e imprimindo os resultados em HTML
print 'Content-Type: text/html;charset=utf-8\r\n\r\n'
print '<html><head><title>Resposta</title><meta charset="utf-8"/></head><body>'
print '<a href="javascript:window.history.go(-1)">Voltar</a>'
for comando in listaComandos:
	print '<h3>Maquina #' + comando['maq'] + ' ($ ' + comando['cmd'] + ' ' + comando['arg'] + ')</h3>'
	print '<div class="text"><pre>'
	print backend.enviaComando(deamons[comando['maq']]['endereco'],deamons[comando['maq']]['porta'],comando['cmd'],comando['arg'])
	print '</pre></div>'
print '<a href="javascript:window.history.go(-1)">Voltar</a>'
print '</body></html>'	