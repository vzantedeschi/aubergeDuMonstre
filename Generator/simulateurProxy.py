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
port = 13500

#Ouverture d'un port de connexion avec les clients
socketSimulateur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketSimulateur.bind((hote, port))

#En ecoute
socketSimulateur.listen(5)

#Recuperation du port de communication du client
socketClient, infoClient = socketSimulateur.accept()

#Tentative de connexion au proxy pour appareillage
okProxy = True
try :
    socketProxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socketProxy.connect(("134.214.106.23", 5000))
    print("Connexion établie avec la passerelle sur le port {}".format(port))
except socket.error :
    print("Impossible de se connecter au proxy")
    print("L'appareillage ne sera pas possible")
    okProxy = False

gen = generateurTrames.generateurTrames("../identifiants.txt")

#Creation d'un timer pour l'envoi de trames nulles du capteur de presence toutes les 2 minutes
t = threading.Timer(120, envoiTramesAbsence)
t.start()

print "BIENVENUE DANS L'AUBERGE DU MONSTRE !"
print "\nA travers ce menu, vous pourrez simuler des scenarios"

#Envoi de trames
while True :
    try:
        print "\nQue voulez-vous faire?"
        event = 3
        while event > 2 :
            print "1. Appareiller un nouvel appareil"
            print "2. Envoyer des trames pour un scenario"
            event = int(input())

        if event == 1 and okProxy == True :
            print "\nQuelle est la trame de reconnaissance à envoyer?"
            message = raw_input(">> ")
            print "\nPassez l'actionneur en mode Learn-In puis taper sur ""Entree"""
            event = raw_input()
            socketProxy.send( 'A55A6B0550000000FF9F1E0530B1' )
                    
        elif event == 2 :
            while True :

                try:
                    #Envoi d'une trame parasite
                    trame = gen.genericFrame()
                    trame = trame.encode()
                    socketClient.send(trame)

                    print "\n***Choisissez un evenement : (tapez ^C pour sortir)"

                    event = 8
                    while event > 7 :
                        print "1. Quelqu'un entre dans une piece"
                        print "2. On allume la lumiere dans une piece"
                        print "3. On eteint la lumiere dans une piece"
                        print "4. La temperature passe a 24.5 degres"
                        print "5. Une fenetre est ouverte/fermee dans une piece"
                        print "6. L'humidite passe a 52.8 %"
                        print "7. On clique sur l'interrupteur pour rouvrir les volets"
                        event = int(input())

                    piece = 6
                    while piece > 5 :
                        print "\nDans quelle piece?"
                        print "1. Couloir"
                        print "2. Salon"
                        print "3. Cuisine"
                        print "4. Bain"
                        print "5. Chambre"
                        piece = int(input())

                    if event not in [2,3,4,5,6,7] :
                        
                        perso = 4
                        while perso > 3 :
                            print "\nQuel personnage?"
                            print "1. Meduse"
                            print "2. Vampire"
                            print "3. Un inconnu"
                            perso = int(input())

                    if event not in [1,2,3,4,6,7] :

                        mouv = 3
                        while mouv > 2:
                            print "\nOuverte ou fermee?"
                            print "1. Ouverte"
                            print "2. Fermee"
                            mouv = int(input())
                    
                    trame = ""

                    if event == 1 :
                        if perso == 3:
                            if piece == 1:
                                trame = gen.presenceDetected(1)
                                socketClient.send(trame)
                                ## Laisse le temps aux volets de se fermer avant
                                ## que le capteur ne le signale
                                time.sleep(10)
                                trame = gen.contactFenetreFermee(1)
                            elif piece == 2:
                                trame = gen.presenceDetected(2)
                                socketClient.send(trame)
                                time.sleep(10)
                                trame = gen.contactFenetreFermee(2)
                            elif piece == 3:
                                trame = gen.presenceDetected(2)
                                socketClient.send(trame)
                                time.sleep(10)
                                trame = gen.contactFenetreFermee(2)
                            elif piece == 4:
                                trame = gen.presenceDetected(4)
                                socketClient.send(trame)
                                time.sleep(10)
                                trame = gen.contactFenetreFermee(4)
                            elif piece == 5:
                                trame = gen.presenceDetected(5)
                                socketClient.send(trame)
                                time.sleep(10)
                                trame = gen.contactFenetreFermee(5)
                        else :
                            if piece == 1:
                                trame = gen.rfidDetected(perso,1)
                            elif piece == 2:
                                trame = gen.rfidDetected(perso,2)
                            elif piece == 3:
                                trame = gen.rfidDetected(perso,3)
                            elif piece == 4:
                                trame = gen.rfidDetected(perso,4)
                            elif piece == 5:
                                trame = gen.rfidDetected(perso,5)
                            trame = trame.encode()
                            socketClient.send(trame)
                            time.sleep(3)
                            if piece == 1:
                                trame = gen.presenceDetected(1)
                            elif piece == 2:
                                trame = gen.presenceDetected(2)
                            elif piece == 3:
                                trame = gen.presenceDetected(3)
                            elif piece == 4:
                                trame = gen.presenceDetected(4)
                            elif piece == 5:
                                trame = gen.presenceDetected(5)
                                
                    elif event == 2 :
                        if piece == 1:
                            trame = gen.pressON()
                        elif piece == 2:
                            print "Pas de capteurs dans cette piece"
                        elif piece == 3:
                            print "Pas de capteurs dans cette piece"
                    elif event == 3 :
                        if piece == 1:
                            trame = gen.pressOFF()
                        elif piece == 2:
                            print "Pas de capteurs dans cette piece"
                        elif piece == 3:
                            print "Pas de capteurs dans cette piece"
                    
                    elif event == 4 :
                        if piece == 1:
                            trame = gen.currentTemperature(1)
                        elif piece == 2:
                            trame = gen.currentTemperature(2)
                        elif piece == 3:
                            trame = gen.currentTemperature(3)
                        elif piece == 4:
                            trame = gen.currentTemperature(4)
                        elif piece == 5:
                            trame = gen.currentTemperature(5)

                    elif event == 5 and mouv == 1 :
                        if piece == 1:
                            trame = gen.contactFenetreOuverte(1)
                        elif piece == 2:
                            trame = gen.contactFenetreOuverte(2)
                        elif piece == 3:
                            trame = gen.contactFenetreOuverte(3)
                        elif piece == 4:
                            trame = gen.contactFenetreOuverte(4)
                        elif piece == 5:
                            trame = gen.contactFenetreOuverte(5)

                    elif event == 5 and mouv == 2 :
                        if piece == 1:
                            trame = gen.contactFenetreFermee(1)
                        elif piece == 2:
                            trame = gen.contactFenetreFermee(2)
                        elif piece == 3:
                            trame = gen.contactFenetreFermee(3)
                        elif piece == 4:
                            trame = gen.contactFenetreFermee(4)
                        elif piece == 5:
                            trame = gen.contactFenetreFermee(5)

                    elif event == 6 :
                        if piece == 1:
                            trame = gen.currentHumidite(1)
                        elif piece == 2:
                            trame = gen.currentHumidite(2)
                        elif piece == 3:
                            trame = gen.currentHumidite(3)
                        elif piece == 4:
                            trame = gen.currentHumidite(4)
                        elif piece == 5:
                            trame = gen.currentHumidite(5)

                    ## Réouverture des volets par interrupteur
                    ## Actuellement tous les interrupteurs ouvrent les volets, il faudra changer ça
                    elif event == 7 :
                        if piece == 1:
                            trame = gen.pressON()
                            socketClient.send(trame)
                            ## Laisse le temps d'ouverture des volets
                            time.sleep(10)
                            trame = gen.contactFenetreOuverte()
                        elif piece == 2:
                            print "Pas de capteurs dans cette piece"
                        elif piece == 3:
                            print "Pas de capteurs dans cette piece"

                    trame = trame.encode()
                    print 'Scenario cree, trame envoyee'
                    socketClient.send(trame)        


                except KeyboardInterrupt:
                    print '\nFermeture de la connexion'
                    break
            
    except KeyboardInterrupt:
        print '\nFermeture de la connexion'
        socketSimulateur.close()

        #Arret du timer
        t.cancel()
        break
