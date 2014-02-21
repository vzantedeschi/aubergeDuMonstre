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
    rfidDetected = 0

def calcCheckSum(trame):
    checksum = 0
    i = 0
    while i < len(trame) :
        c = trame[i:i+2]
        i += 2
        checksum += int(c, 16)

    checksum &= 0xFF
    return hex(checksum)[2:4]

def trameActionneur(actionneurId, activation):
    sync = 'A55A'
    message = '6B0550000000'
    if activation:
        message = '6B0570000000'
    message += format(actionneurId, '08x')
    message += "30"
    checksum = calcCheckSum(message)
    return sync + message + checksum



def activerActionneur(idAct):
    print "Activation de l'actionneur"
    # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(idAct, True))
        
def activerActionneur_type(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs:
        if a.capteur_type == typeActionneur:
            print "Activation de l'actionneur"
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
            connectProxy.send(trameActionneur(a.actionneur_id, True))

def desactiverActionneur(idAct):
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(idAct, False))
            
def desactiverActionneur_type(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs:
        if a.capteur_type == typeActionneur:
            print "Desactivation de l'actionneur"
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(a.actionneur_id, False))

def ouvrirVolets(idPiece):    
    # Allume l'interrupteur simulant les volets
    print "Verrouillage actif : volets en cours d'ouverture"
    activerActionneur_type(idPiece, 'VOL')        

def fermerVolets(idPiece):
    # Allume l'interrupteur simulant les volets
    print "Verrouillage actif : volets en cours de fermeture"
    desactiverActionneur_type(idPiece, 'VOL')   

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
            print ("Intrus est dans la piece :",piece_id)

            # Un seul intrus dans la maison en même temps sinon => comment savoir si un
            # intrus qui rentre dans une pièce est un nouveau (générer nouvel id) ou un qui
            # vient de changer de pièce (enlever id de la pièce précédente)

            # Si l'intrus est dans la pièce 1 'Couloir', il n'est plus ignoré

            if piece_id == 1:
                persoAjoute = tables.Personne.objects(nom = "Intrus").first()
                persoAjoute.ignore = False
                persoAjoute.save()

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
            etatAChanger = tables.Etat.objects(piece_id = piece_id)
            etatAChanger.climActivee = True
            etatAChanger.save()
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : True} },upsert=False,multi=True)

            if connected == True :
                connectProxy.send( 'A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
                
        elif tempDonnees <= 19 and climActive == True :
            print "Desactivation de la climatisation"

            # Modifier l'information de la BDD pour mettre "climActive" à False
            etatAChanger = tables.Etat.objects(piece_id = piece_id)
            etatAChanger.climActivee = False
            etatAChanger.save()
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)

            if connected == True :
                connectProxy.send( 'A55A6B05WWWWWWWWYYYYYYYY30ZZ' )

    elif (typeInfo == "Donnee.Humidite"):
        
        humDonnees = item[u'valeur']
        print humDonnees

        antiIncendieActive = etat[u'antiIncendieDeclenche']
        print antiIncendieActive

        db.etat.update({u'piece_id' : piece_id},{ "$set": {u'humidite' : humDonnees} },upsert=False,multi=True)
        print '\nCommande suivant un changement d''humidite en cours'

        ## Valeur 70 à modifier dans une interface graphique par exemple
        ## La trame crée est fausse, c'est un exemple
        if humDonnees < 70 and antiIncendieActive == False:
            print "Activation du systeme anti-incendie"

            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à True
            etatAChanger = tables.Etat.objects(piece_id = piece_id)
            etatAChanger.antiIncendieDeclenche = True
            etatAChanger.save()
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : True} },upsert=False,multi=True)

            if connected == True :
                connectProxy.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
        elif humDonnees > 70 and antiIncendieActive == True:
            print "Desactivation du systeme anti-incendie"

            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
            etatAChanger = tables.Etat.objects(piece_id = piece_id)
            etatAChanger.antiIncendieDeclenche = False
            etatAChanger.save()
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)

            if connected == True :
                connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
    

        
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
            print "Ouverture des volets"
            connectProxy.send('A55A6B0570000000FF9F1E0530D1' )

    elif (typeInfo == "Donnee.ContactFen"):
        fenDonnees = item[u'ouverte']
        
        if fenDonnees == False:
            print '\nCommande suivant une fermeture de volets en cours'
            etatAChanger = tables.Etat.objects(piece_id = piece_id)
            etatAChanger.voletsOuverts = False
            etatAChanger.save()
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
        elif fenDonnees == True:
            print '\nCommande suivant une ouverture de volets en cours'
            etatAChanger = tables.Etat.objects(piece_id = piece_id)
            etatAChanger.voletsOuverts = True
            etatAChanger.save()
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)


#### ESSAI INTEGRATION ENVOIS DE L'APPLI WEB ########
    elif(typeInfo == "Donnee.DonneeAppli"):
        #Recherche des actionneurs de la piece du type demande
        actionneur_id = item[u'actionneur_id']
        actionType = item[u'action_type']      
        if actionType:
            activerActionneur(actionneur_id)
        else:
            desactiverActionneur(actionneur_id)

    elif(typeInfo == "Donnee.ReponseAppli"):
        reponse = item[u'reponse']
        if reponse:
            fermerVolets(piece_id)


#### FIN ESSAI INTEGRATION ENVOIS DE L'APPLI WEB ####


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
