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
rfidDetected = False

hote = '134.214.106.23'
port = 5000
## Functions Server ##
db_connec = mongoengine.connect('GHome_BDD')
db = db_connec.GHome_BDD

def RFIDFunc():
    rfidDetected = False

def commande(item):
    global rfidDetected
    #récupération type de donnée
    typeInfo = item[u'_cls']
    #récupération de l'id de la pièce concernée
    piece_id = item[u'piece_id']
    print piece_id
    #récupération état de la pièce concernée
    etat = tables.Etat.objects(piece_id = piece_id).first()
    print etat

    ### Il me faut le format des informations de sortie pour savoir
    ### sur quoi faire une condition
    if (typeInfo == "Donnee.Presence"):
        print 'Commande suivant une présence en cours'

        if rfidDetected == False :
            # TODO : mise à jour état pièce

            ## REPONSE APPLI WEB ##
            if (True) :
                # Allume l'interrupteur simulant les volets
                print "Verrouillage active : volets en cours de fermeture"
                # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
                if connected == True :
                    print "Envoi au proxy"
                    connectProxy.send( 'A55A6B0550000000FF9F1E0530B1' )

    elif (typeInfo == "Donnee.Temperature"):
        #Détermine la commande et mettre "traite" à True
        print "Temperature"
        
        tempDonnees = item[u'valeur']
        print tempDonnees

        climActive = etat[u'climActivee']
        print climActive

        db.etat.update({u'piece_id' : piece_id},{ "$set": {u'temperature' : tempDonnees} },upsert=False,multi=True)
        print 'Commande suivant un changement de temperature en cours'

        ## Valeur 19 à modifier dans une interface graphique par exemple
        ## La trame crée est fausse, c'est un exemple
        if tempDonnees > 19 and climActive == False :
            print "Activation de la climatisation"
            # Modifier l'information de la BDD pour mettre "climActive" à True
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : True} },upsert=False,multi=True)
            if connected == True :
                connectProxy.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
        elif tempDonnees <= 19 and climActive == True :
            print "Desactivation de la climatisation"
            # Modifier l'information de la BDD pour mettre "climActive" à False
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)
            if connected == True :
                connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )

    elif (typeInfo == "Donnee.Humidite"):
        print "Humidite"
        type = 'HUMID'
        
        humDonnees = item[u'valeur']
        print humDonnees

        antiIncendieActive = etat[u'antiIncendieDeclenche']
        print antiIncendieActive

        print 'Commande suivant un changement d''humidite en cours'

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
            if connected == True :
                connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
    
        db.etat.update({u'piece_id' : piece_id},{ "$set": {u'humidite' : humDonnees} },upsert=False,multi=True)
        
    elif (typeInfo == "Donnee.RFID"):
        print "RFID"
        resident = item[u'resident_id']
        print resident

        print 'Commande suivant detection RFID en cours'
        rfidDetected = True
        # Mise en place d'un timer qui indique
        # qu'il n'attend plus une détection de présence au bout
        # de 20 secondes
        timerRFID = threading.Timer(20,RFIDFunc)
        timerRFID.start()

    elif (typeInfo == "Donnee.Interrupteur"):
        print "Interrupteur"
        print 'Commande suivant un interrupteur en cours'
        if connected == True :
            print "Ouverture des volets"
            connectProxy.send('A55A6B0570000000FF9F1E0530D1' )

    else:
        print 'Autre type de commande'
        print 'Pas de commande implementee'
        
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
        liste = db.donnee.find({u'traite':False})
        for item in liste:
            print type(item)
            print "\n"
            print item
            commande(item)
        else :
            #s'il n'y a pas de données à traiter
            print 'Aucune nouvelle donnée'
            time.sleep(1)
    except KeyboardInterrupt:
        t.cancel()
        break
