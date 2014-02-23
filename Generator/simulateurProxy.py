#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import sys
import time
import random
import threading
import generateurTrames
import mongoengine
sys.path.append('../BDD')
import tables

def envoiTramesAbsence():
    trame = gen.nothingDetected()
    trame = trame.encode()
    socketClient.send(trame)

class ThreadSimuActionneurs(threading.Thread):
    # Simulation de la reponse des capteurs suite a l'activation d'un actionneur
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        #récupération infos actionneurs dans la base
        actionneurs = tables.Actionneur.objects
        actionneursId = map(lambda i : i.actionneur_id, actionneurs)

        continuer = True
        while continuer:
            continuer = False
            # Reception des trames d'actionneurs
            #msg_recu = socketProxy.recv(28)       
            #msg_recu = msg_recu.decode()
            # Pour tester
            msg_recu = 'A55A6B0570000000FF9F1E0530D1'
            # Recupere l'identifiant
            ident = msg_recu[16:24] 
            ident = int(ident,16)

            if ident in actionneursId:
                bitAction = msg_recu[8]
                # Piece concernee
                piece = tables.Piece.objects(__raw__={u'actionneurs':{u'$elemMatch':{u'$id':ident}}}).first().piece_id
                # Type Capteur concerne
                typeCapteur = tables.Actionneur.objects(actionneur_id=ident).first().capteur_type
                if typeCapteur == 'VOL':
                    if bitAction == '5':
                        trameGen = gen.contactVoletFerme(piece)
                    elif bitAction == '7':
                        print "trame envoyee"
                        trameGen = gen.contactVoletOuvert(piece)
                elif typeCapteur == 'FEN':
                    if bitAction == '5':
                        trameGen = gen.contactFenetreFermee(piece)
                    elif bitAction == '7':
                        trameGen = gen.contactFenetreOuverte(piece)

                trameGen = trameGen.encode()
                socketClient.send(trameGen) 

                


hote = 'localhost'
port = 13700

#Connexion a la BDD
db_connec = mongoengine.connect('GHome_BDD')
db = db_connec.GHome_BDD

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

tsa = ThreadSimuActionneurs()
tsa.start()

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

                    event = 5
                    while event > 4 :
                        print "1. Quelqu'un entre dans une piece"
                        print "2. On ouvre/ferme les volets dans une piece"
                        print "3. La temperature passe a 24.5 degres dans une piece"
                        print "4. L'humidite passe a 52.8 % dans une piece"
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

                    if event == 1 :
                        
                        perso = 4
                        while perso > 3 :
                            print "\nQuel personnage?"
                            print "1. Meduse"
                            print "2. Vampire"
                            print "3. Un inconnu"
                            perso = int(input())

                    if event == 2 :

                        mouv = 3
                        while mouv > 2:
                            print "\nOuvert ou ferme?"
                            print "1. Ouvert"
                            print "2. Ferme"
                            mouv = int(input())
                    
                    trame = ""

                    ## capteurs de présence et rfid
                    if event == 1 :
                        if perso == 3:
                            if piece == 1:
                                trame = gen.presenceDetected(1)
                                socketClient.send(trame)
                                ## Laisse le temps aux volets de se fermer avant
                                ## que le capteur ne le signale
                                #time.sleep(10)
                                #trame = gen.contactVoletFerme(1)
                            elif piece == 2:
                                trame = gen.presenceDetected(2)
                                socketClient.send(trame)
                                #time.sleep(10)
                                #trame = gen.contactVoletFerme(2)
                            elif piece == 3:
                                trame = gen.presenceDetected(2)
                                socketClient.send(trame)
                                #time.sleep(10)
                                #trame = gen.contactVoletFerme(2)
                            elif piece == 4:
                                trame = gen.presenceDetected(4)
                                socketClient.send(trame)
                                #time.sleep(10)
                                #trame = gen.contactVoletFerme(4)
                            elif piece == 5:
                                trame = gen.presenceDetected(5)
                                socketClient.send(trame)
                                #time.sleep(10)
                                #trame = gen.contactVoletFerme(5)
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

                    ## Interrupteur Généraux (NOT GENERATED)            
                    elif event == 6 :
                        if piece == 1:
                            trame = gen.pressON(1)
                        elif piece == 2:
                            trame = gen.pressON(2)
                        elif piece == 3:
                            trame = gen.pressON(3)
                        elif piece == 4:
                            trame = gen.pressON(4)
                        elif piece == 5:
                            trame = gen.pressON(5)
                            
                    elif event == 7 :
                        if piece == 1:
                            trame = gen.pressOFF(1)
                        elif piece == 2:
                            trame = gen.pressOFF(2)
                        elif piece == 3:
                            trame = gen.pressOFF(3)
                        elif piece == 4:
                            trame = gen.pressOFF(4)
                        elif piece == 5:
                            trame = gen.pressOFF(5)

                    ## capteur température
                    elif event == 3 :
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

                    ## Contacteur pour fenêtre (NOT GENERATED)
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

                    ## capteur humidité
                    elif event == 4 :
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

                    ## ouverture des volets par interrupteur
                    elif event == 2 and mouv == 1:
                        if piece == 1:
                            trame = gen.ouvreVolet(1)
                            socketClient.send(trame)
                            ## Laisse le temps d'ouverture des volets
                            time.sleep(10)
                            trame = gen.contactVoletOuvert(1)
                        elif piece == 2:
                            trame = gen.ouvreVolet(2)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletOuvert(2)
                        elif piece == 3:
                            trame = gen.ouvreVolet(3)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletOuvert(3)
                        elif piece == 4:
                            trame = gen.ouvreVolet(4)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletOuvert(4)
                        elif piece == 5:
                            trame = gen.ouvreVolet(5)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletOuvert(5)

                    ## fermeture des volets par interrupteur
                    elif event == 2 and mouv == 2:
                        if piece == 1:
                            trame = gen.fermeVolet(1)
                            socketClient.send(trame)
                            ## Laisse le temps d'ouverture des volets
                            time.sleep(10)
                            trame = gen.contactVoletFerme(1)
                        elif piece == 2:
                            trame = gen.fermeVolet(2)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletFerme(2)
                        elif piece == 3:
                            trame = gen.fermeVolets(3)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletFerme(3)
                        elif piece == 4:
                            trame = gen.fermeVolet(4)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletFerme(4)
                        elif piece == 5:
                            trame = gen.fermeVolet(5)
                            socketClient.send(trame)
                            time.sleep(10)
                            trame = gen.contactVoletFerme(5)

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
