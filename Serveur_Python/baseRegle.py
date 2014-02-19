#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import time
import pymongo
import sys
import socket
import threading
sys.path.append('../BDD')
import tables

## Variables globales ##
connectProxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# La variable "connected" servira à savoir au cour du programme si on peut
# envoyer des trames aux actionneurs ou si on s'en tient à des affichages écran
# dans le cas où l'on n'a pas accès au réseau GHome
connected = False

# Aucune puce RFID détectée
rfidDetected = 0

hote = '134.214.106.23'
port = 5000
## Functions Server ##
db_connec = mongoengine.connect('GHome_BDD')
db = db_connec.GHome_BDD

def RFIDFunc():
    global rfidDetected
    rfidDetected = 0
    print '\nRFID DETECTED REMIS A 0'

def commande(item):
    global rfidDetected
    #récupération type de donnée
    typeInfo = item[u'_cls']
    #récupération de l'id de la pièce concernée
    piece_id = item[u'piece_id']
    #récupération état de la pièce concernée
    etat = tables.Etat.objects(piece_id = piece_id).first()
    print("\nEtat de la piece concernée")
    print("Numero :",etat.piece_id)
    print("Rideaux ouverts :",etat.rideauxOuverts)
    print("Systeme anti-incendie declenchee :",etat.antiIncendieDeclenche)
    print("Climatisation activee :",etat.climActivee)
    print("Portes fermees :",etat.portesFermees)
    print("Volets ouverts :",etat.voletsOuverts)
    print("Prise allumee :",etat.priseDeclenchee)
    print("Temperature :",etat.temperature)
    print("Humidite :",etat.humidite)
    print("Personnages presents :",etat.persosPresents)
    print '\n'

    if (typeInfo == "Donnee.Presence"):
        print '\nCommande suivant une presence en cours'

        if rfidDetected == 0 :
            # TODO : mise à jour état pièce

            ## REPONSE APPLI WEB ##
            if (True) :
                # Allume l'interrupteur simulant les volets
                print "Verrouillage active : volets en cours de fermeture"
                # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
                if connected == True :
                    print "Envoi au proxy"
                    connectProxy.send( 'A55A6B0550000000FF9F1E0530B1' )
                    
        elif rfidDetected == 1 :
            print ("Meduse est dans la piece :",piece_id)
            pieceConcernee = tables.Etat.objects(piece_id = piece_id).first()

            persoAjoute = tables.Personne.objects(personne_id = rfidDetected).first()

            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.persosPresents.append(persoAjoute)
            etatPiece.save()        

            ## Enlever le perso des autres pieces
            listePieces = tables.Etat.objects
            for p in listePieces :
                if p.piece_id != piece_id:
                    etatAChanger = tables.Etat.objects(piece_id = p.piece_id).first()
                    if persoAjoute in etatAChanger.persosPresents:
                        etatAChanger.persosPresents.remove(persoAjoute)
                        etatAChanger.save()

            # Remettre rfidDetected a 0
            rfidDetected = 0

        elif rfidDetected == 2 :
            print ("Vampire est dans la piece :",piece_id)
            pieceConcernee = tables.Etat.objects(piece_id = piece_id).first()
            
            persoAjoute = tables.Personne.objects(personne_id = rfidDetected).first()

            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.persosPresents.append(persoAjoute)
            etatPiece.save()        

            ## Enlever le perso des autres pieces
            listePieces = tables.Etat.objects
            for p in listePieces :
                if p.piece_id != piece_id:
                    etatAChanger = tables.Etat.objects(piece_id = p.piece_id).first()
                    if persoAjoute in etatAChanger.persosPresents:
                        etatAChanger.persosPresents.remove(persoAjoute)
                        etatAChanger.save()

            # Remettre rfidDetected a 0
            rfidDetected = 0

    elif (typeInfo == "Donnee.Temperature"):
        #Détermine la commande et mettre "traite" à True        
        tempDonnees = item[u'valeur']
        print tempDonnees

        climActive = etat[u'climActivee']
        print climActive

        db.etat.update({u'_id' : piece_id},{ "$set": {u'temperature' : tempDonnees} },upsert=False,multi=True)
        print '\nCommande suivant un changement de temperature en cours'

        ## Valeur 19 à modifier dans une interface graphique par exemple
        ## La trame crée est fausse, c'est un exemple
        if tempDonnees > 19 and climActive == False :
            print "Activation de la climatisation"
            # Modifier l'information de la BDD pour mettre "climActive" à True
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : True} },upsert=False,multi=True)
            if connected == True :
                connectProxy.send( 'A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
        elif tempDonnees <= 19 and climActive == True :
            print "Desactivation de la climatisation"
            # Modifier l'information de la BDD pour mettre "climActive" à False
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)
            if connected == True :
                connectProxy.send( 'A55A6B05WWWWWWWWYYYYYYYY30ZZ' )

    elif (typeInfo == "Donnee.Humidite"):
        type = 'HUMID'
        
        humDonnees = item[u'valeur']
        print humDonnees

        antiIncendieActive = etat[u'antiIncendieDeclenche']
        print antiIncendieActive

        print '\nCommande suivant un changement d''humidite en cours'

        ## Valeur 70 à modifier dans une interface graphique par exemple
        ## La trame crée est fausse, c'est un exemple
        if humDonnees < 70 and antiIncendieActive == False:
            print "Activation du systeme anti-incendie"
            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à True
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : True} },upsert=False,multi=True)
            if connected == True :
                connectProxy.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
        elif humDonnees > 70 and antiIncendieActive == True:
            print "Desactivation du systeme anti-incendie"
            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
            if connected == True :
                connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
    
        db.etat.update({u'piece_id' : piece_id},{ "$set": {u'humidite' : humDonnees} },upsert=False,multi=True)
        
    elif (typeInfo == "Donnee.RFID"):
        resident = item[u'resident_id']
        
        print '\nCommande suivant detection RFID en cours'
        rfidDetected = resident
        # Mise en place d'un timer qui indique
        # qu'il n'attend plus une détection de présence au bout
        # de 20 secondes
        timerRFID = threading.Timer(20,RFIDFunc)
        timerRFID.start()

    elif (typeInfo == "Donnee.Interrupteur"):
        print '\nCommande suivant un interrupteur en cours'
        if connected == True :
            intrDonnees = item[u'ouverte']
            if intrDonnees == True:
                print "Ouverture des volets"
                connectProxy.send('A55A6B0550000000FF9F1E0530D1' )
            elif intrDonnees == False:
                print "Fermeture des volets"
                connectProxy.send('A55A6B0570000000FF9F1E0530D1' )

    elif (typeInfo == "Donnee.ContactFen"):
        fenDonnees = item[u'ouverte']
        
        if fenDonnees == False:
            print '\nCommande suivant une fermeture de volets en cours'
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
        elif fenDonnees == True:
            print '\nCommande suivant une ouverture de volets en cours'
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)

    else:
        print '\nPas de commande implementee'
        
    if (item != None):
        # Modifier l'information de la BDD pour mettre "traite" à True            
        db.donnee.update({"_id" : item[u'_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
      
try :
    print 'Attente connexion au proxy'
    connectProxy.connect((hote, port))
    print("Connexion établie avec la passerelle sur le port {}".format(port))
    connected = True
except socket.error :
    print("Impossible de se connecter au proxy : Les trames d'actionneurs ne seront pas envoyees")

while True :
    try :
        # Permet d'examiner les informations nouvelles dans la BDD
        liste = db.donnee.find({u'traite':False}).sort("_id", 1)
        for item in liste:
            print "\n"
            print item
            commande(item)
        else :
            #s'il n'y a pas de données à traiter
            print 'Aucune nouvelle donnee'
            time.sleep(2)
    except KeyboardInterrupt:
        break
