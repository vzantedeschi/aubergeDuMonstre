#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import sys
import time
import random
import threading
import generateurTrames

def envoiTramesAbsence():
	trame = gen.nothingDetected()
	trame = trame.encode()
	socketClient.send(trame)

hote = 'localhost'
port = 12800

#Ouverture d'un port de connexion avec les clients
socketSimulateur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketSimulateur.bind((hote, port))

#En ecoute
socketSimulateur.listen(5)

#Recuperation du port de communication du client
socketClient, infoClient = socketSimulateur.accept()

<<<<<<< HEAD
gen = generateurTrames.generateurTrames("identifiants.txt")
=======
#Envoi message de confirmation
#provoque une erreur lors du test des identifiants dans le main
#socketClient.send(b"connected")
>>>>>>> 17e3727c04134ea753d3c531620d058eca6f2c2d

#Creation d'un timer pour l'envoi de trames nulles du capteur de presence toute les 2 minutes
t = threading.Timer(120, envoiTramesAbsence)
t.start()

<<<<<<< HEAD
print "BIENVENUE DANS L'AUBERGE DU MONSTRE !"
print "\nA travers ce menu, vous pourriez simuler des scenarios"

#Envoi de trames
while True :

	try:
=======
        # temps aléatoire d'attente entre deux messages
	wait = random.randint(1,10)

	try:
		#Envoi d'une trame parasite
		trame = gen.genericFrame()
		trame = trame.encode()
		socketClient.send(trame)
>>>>>>> 17e3727c04134ea753d3c531620d058eca6f2c2d

		print "\n***Choisissez un evenement : (tapez ^C pour sortir)"
		print "1. Quelqu'un entre dans une piece"
		print "2. On allume la lumiere dans un piece"
		print "3. On etend la lumiere dans une piece"
		print "4. "

		event = int(input())

		print "\nDans quelle piece?"
		print "1. Couloir"
		print "2. Cuisine"
		print "3. Salon"

		piece = int(input())

		if event not in [2,3] :
			
			print "\nQuel personnage?"
			print "1. Meduse"
			print "2. Vampire"
			print "3. Un inconnu"

			perso = int(input())
		
		trame = ""

		if event == 1 :
			trame = gen.presenceDetected()

		elif event == 2 :
			trame = gen.pressON()

		elif event == 3 :
			trame = gen.pressOFF()

<<<<<<< HEAD
=======
		#Envoi d'une trame parasite
		trame = gen.genericFrame()
>>>>>>> 17e3727c04134ea753d3c531620d058eca6f2c2d
		trame = trame.encode()
		print 'Scenario cree, trame envoyee'
		socketClient.send(trame)		


	except KeyboardInterrupt:
		print '\nFermeture de la connexion'
		socketSimulateur.close()

		#Arret du timer
		t.cancel()
		break
