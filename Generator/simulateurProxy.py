import socket
import select
import sys
import time
import random
import generateurTrames

hote = 'localhost'
port = 12900

#Ouverture d'un port de connexion avec les clients
socketSimulateur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketSimulateur.bind((hote, port))
gen = generateurTrames.generateurTrames("identifiants.txt")

#En ecoute
socketSimulateur.listen(5)

#Recuperation du port de communication du client
socketClient, infoClient = socketSimulateur.accept()

#Envoi message de confirmation
socketClient.send(b"connected")

while True :

	wait = random.randint(1,10)

	try:
		#Envoi d'une trame parassite
		trame = gen.genericFrame()
		trame = trame.encode()
		socketClient.send(trame)

		#On appuie sur ON
		trame = gen.pressON()
		trame = trame.encode()
		socketClient.send(trame)

		time.sleep(wait);
		#On appuie sur OFF
		trame = gen.pressOFF()
		trame = trame.encode()
		socketClient.send(trame)

		#Envoi d'une trame parassite
		trame = gen.genericFrame()
		trame = trame.encode()
		socketClient.send(trame)

		time.sleep(wait);

	except KeyboardInterrupt:
		print '\nFermeture de la connection'
		socketSimulateur.close()
		break
