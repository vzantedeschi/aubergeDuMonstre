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
port = 13700

#Ouverture d'un port de connexion avec les clients
socketSimulateur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketSimulateur.bind((hote, port))

#En ecoute
socketSimulateur.listen(5)

#Recuperation du port de communication du client
socketClient, infoClient = socketSimulateur.accept()

gen = generateurTrames.generateurTrames("identifiants.txt")

#Creation d'un timer pour l'envoi de trames nulles du capteur de presence toutes les 2 minutes
t = threading.Timer(120, envoiTramesAbsence)
t.start()

print "BIENVENUE DANS L'AUBERGE DU MONSTRE !"
print "\nA travers ce menu, vous pourrez simuler des scenarios"

#Envoi de trames
while True :

    try:
        #Envoi d'une trame parasite
        trame = gen.genericFrame()
        trame = trame.encode()
        socketClient.send(trame)

        print "\n***Choisissez un evenement : (tapez ^C pour sortir)"

        event = 5
        while event > 4 :
            print "1. Quelqu'un entre dans une piece"
            print "2. On allume la lumiere dans un piece"
            print "3. On eteind la lumiere dans une piece"
            print "4. La temperature passe a 24.5 degres"
            event = int(input())

        piece = 4
        while piece > 3 :
            print "\nDans quelle piece?"
            print "1. Couloir"
            print "2. Cuisine"
            print "3. Salon"
            piece = int(input())

        if event not in [2,3,4] :
            
            perso = 4
            while perso > 3 :
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
            
        elif event == 4 : 
            trame = gen.currentTemperature()

        trame = trame.encode()
        print 'Scenario cree, trame envoyee'
        socketClient.send(trame)        


    except KeyboardInterrupt:
        print '\nFermeture de la connexion'
        socketSimulateur.close()

        #Arret du timer
        t.cancel()
        break
