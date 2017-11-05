# Redes-UFSCar-2017-2_Trabalho-1
Primeiro trabalho da disciplina de Redes de Computadores, oferecida no segundo semestre de 2017.

## Servidor de Consultas Linux

### Descrição do projeto (retirado de [projeto1_v2.pdf](https://github.com/brunoinfo/Redes-UFSCar-2017-2_Trabalho-1/blob/master/doc/projeto1_v2.pdf))
<p align="justify">A aplicação que será desenvolvida pelo grupo, irá permitir a um usuário realizar uma busca de resultados de comandos de linha, a partir de um conjunto de “máquinas” Linux, através de uma interface web. Especificamente, a aplicação começa apresentando ao usuário uma página web. Nessa página, o usuário poderá selecionar K máquinas de uma lista, e para cada máquina, selecionar um ou mais dos seguintes comandos: ps, df, finger e uptime. Uma vez que essa interface web (em python) receber estas instruções do browser do usuário, um aplicativo backend, também em python, irá se conectar (sequencialmente, ou em paralelo) a um conjunto de “daemons” rodando em cada uma das “máquinas” da lista. O programa backend então passará os comandos que precisam ser executados as respectivas máquinas remotas. Os “daemons” receberão o comando do programa backend e executarão localmente o comando correspondente. Eles então redirecionarão a saída desses comandos, e o backend juntará todas as respostas para criar uma página web de resultados.</p>

Descrição completa do projeto: [projeto1_v2.pdf](https://github.com/brunoinfo/Redes-UFSCar-2017-2_Trabalho-1/blob/master/doc/projeto1_v2.pdf)

Tutorial para instalação da VM utilizada: [VM-desenvolvimento.pdf](https://github.com/brunoinfo/Redes-UFSCar-2017-2_Trabalho-1/blob/master/doc/VM-desenvolvimento.pdf)
