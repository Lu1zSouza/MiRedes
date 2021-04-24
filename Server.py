#!/usr/bin/env python3
from __future__ import print_function
from datetime import datetime
import mercury, time, socket, sys, time, os, json


HOST=''
PORT=5027
portaSerial = ""
baud = 0
regiao = ""
antena = 0
protocolo = ""
readPower = 0
reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=230400)

def iniciaLeitor():
    global portaSerial, baudrate, regiao, antena, protocolo, readPower
    reader = mercury.Reader(portaSerial, baudrate=baudrate)
    reader.set_region(regiao)
    reader.set_read_plan([antena], protocolo, read_power=readPower)
    print(reader.read())
    print("Leitor Iniciado")
    return reader
    
def configRasp(connection, JSON):
	global portaSerial, baudrate, regiao, antena, protocolo, readPower
	portaSerial = JSON['portaSerial']
	baudrate = int(JSON['baudrate'])
	regiao = JSON['regiao']
	antena = int(JSON['antena'])
	protocolo = JSON['protocolo']
	readPower = int(JSON['power'])
	print("Leitor Configurado")
	mensagem = '{"URL":"configRasp", "return":"OK"}'
	mensagemRetorno = mensagem + "\n"
	connection.sendall(bytes(mensagemRetorno.encode('utf-8')))

def lerTagCadastroCarro(connection):
    reader = iniciaLeitor()
    tags = list(map(lambda t: t.epc, reader.read()))
    jsonRetornoCadCarro = '{'
    for x in range(len(tags)):
        inform = str(tags[x])
        jsonRetornoCadCarro = jsonRetornoCadCarro + '"EPC'+str(x)+ '":"' + inform + '", '
	
    size = len(jsonRetornoCadCarro)
    remove = jsonRetornoCadCarro[:size - 2]
    jsonRetornoCadCarro = remove
    jsonRetornoCadCarro = jsonRetornoCadCarro +'}'
    jsonRetornoCadCarro = jsonRetornoCadCarro +	"\n"
    print("Devolvendo TAGS")
    print(jsonRetornoCadCarro)
    print("Devolvendo TAGS")
    connection.sendall(bytes(jsonRetornoCadCarro.encode('utf-8')))
    
def inicio(connection):
    while True:
        print ("Escutando mensagem")
        #Connetion.recv -> Informa o que o cliente quer receber (1024 bytes)
        #Recebido -> Nome do arquivo que o cliente quer
        recebido = connection.recv(1024).decode('utf-8') 
        if not recebido: break
        print(recebido);
        print("Eu")
        objetoJson = json.loads(recebido)
        if(objetoJson['METODO'] == "POST"):
            if(objetoJson['URL'] == "configRasp"):
                configRasp(connection, objetoJson)
        elif (objetoJson['METODO'] == "GET"):
            if (objetoJson['URL'] == "lerTagCadastroCarro"):
                lerTagCadastroCarro(connection)
        else:
            print("Não é um POST e nem um GET")
            print ('requisição finalizada!')

 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET -> Conexões feitas via IPV4 SOCK_STREAM -> Via Protocolo TCP
try:
    print ("Iniciado,  porta -> ", PORT, socket.gethostname())
    s.bind((HOST,PORT)) #Liga o Socket ao endereço do Servidor
except socket.error :
    print ("Nao foi")
    sys.exit(-1)
    
s.listen(1) #O Socket vai ouvir nesse endereço. O Parêmetro (1) é a quantidade de conexões

#Quando o cliente se conectar, o servidor aceita a conexão.
#Objeto Connection -> Conexão com o cliente
#Objeto address -> Endereço do cliente
connection, address = s.accept()
print ('Conectou', address)

while 1:
	inicio(connection)	
	
print ('Finalizando conexao do cliente', address)
connection.close()
