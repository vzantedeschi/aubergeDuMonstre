#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threadsDefined
import socket
import trame
import datetime
import interpreteur
import pymongo
import mongoengine
sys.path.append('../BDD')
import tables

############# CONNEXION PASSERELLE ###################
connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
while connected == False:
    
    print "\nOu voulez-vous vous connecter?"
    
    passerelleChoisie = 3
    while passerelleChoisie > 3 :
        print "1. Passerelle EnOcean"
        print "2. Simulateur Proxy"
        passerelleChoisie = int(input())

    if passerelleChoisie == 1:
        try :
            hote = '134.214.106.23'
            port = 5000
            connexion_avec_passerelle.connect((hote, port))
            print("Connexion etablie avec la passerelle sur le port {}".format(port))
            connected = True
            
        except socket.error :
            print("Impossible de se connecter au proxy")
            exit()
    else :
        print "\nSur quelle adresse IP? (localhost autorisé)"
        hote = raw_input(">> ")
        #print "\nSur quel port?"
        #port = int(input())
        port = 13800
        try :
            connexion_avec_passerelle.connect((hote, port))
            print("Connexion établie avec la passerelle sur le port {}".format(port))
            connected = True
            
        except socket.error :
            print("Impossible de se connecter au proxy")
            exit()
    
print 'ok'       
########### CONNEXION BDD ###############
db_connec = mongoengine.connect('GHome_BDD')

#récupération identifiants dans la base
identifiants = tables.Capteur.objects
identifiants = map(lambda i : i.capteur_id, identifiants)
print identifiants

#
#
#
# TESTS POUR ENVOI TRAME (APPAREILLAGE) #
#connexion_avec_passerelle.send( 'A55A6B0570000000FF9F1E0530D1' )
#
#
#
#

#threadCommand = threadsDefined.ThreadCommand()
#threadCommand.start()

# Process qui va vérifier les trames provenant de la passerelle       
try: 
    while True:
        print 'reception'
        msg_recu = connexion_avec_passerelle.recv(28)       
        msg_recu = msg_recu.decode()
        print msg_recu
        
        # Recupere l'identifiant du capteur
        ident = msg_recu[16:24] 
        
        # Si le capteur appartient a ceux etudiés on traite la trame
        if int(ident,16) in identifiants :
            # Recupere la date et l'heure de reception
            now = datetime.datetime.now()

            print("Recu {}".format(msg_recu))

            # Passage par le parser
            infosTrame = trame.Trame(msg_recu,now)          

            if infosTrame.valide == True :
                print ("ID {}".format(hex(infosTrame.idBytes)))
                print ("DB ", infosTrame.dataBytes)
                print ("Heure {}".format(infosTrame.heure))
                
                if infosTrame.eepSent == False :
                    # Interprète les informations contenues dans la Trame
                    trameInterpretee = interpreteur.Interpretation(infosTrame)
                    
                    # a quelle piece correspond ce capteur
                    # !!!solution temporaire : il doit y avoir une façon plus propre et directe
                    print 'Pièce concernée'
                    capteur = tables.Capteur.objects(capteur_id = trameInterpretee.id).first()
                    pieces = tables.Piece.objects
                    for p in pieces :
                        if capteur in p.capteurs :
                            print "piece ", p.piece_id, "  : ", p.name

                    ### INSERTION DANS LA BDD ###
                    if trameInterpretee.typeCapteur == 'PRES':
                        if trameInterpretee.donnees == 1:
                            capteur_presence = tables.Presence(capteur_id = trameInterpretee.id, capteur_type = "PRES", annee = trameInterpretee.annee, mois = trameInterpretee.mois, jour = trameInterpretee.jour, heure = trameInterpretee.heure, traite = False)
                            capteur_presence.save()
                            
                    elif trameInterpretee.typeCapteur == 'TEMP':
                        capteur_temperature = tables.Temperature(capteur_id =trameInterpretee.id, annee = trameInterpretee.annee, mois = trameInterpretee.mois, jour = trameInterpretee.jour, heure = trameInterpretee.heure, valeur = trameInterpretee.tempDonnees, traite = False)
                        capteur_humidite = tables.Humidite(capteur_id =trameInterpretee.id, annee = trameInterpretee.annee, mois = trameInterpretee.mois, jour = trameInterpretee.jour, heure = trameInterpretee.heure, valeur = trameInterpretee.humDonnees, traite = False)
                        capteur_temperature.save()
                        capteur_humidite.save()
                        print "1 = temp"
                        
                    elif trameInterpretee.typeCapteur == 'RFID':
                        #capteur_rfid = tables.RFID(capteur_id =trameInterpretee.id, annee = trameInterpretee.annee, mois = trameInterpretee.mois, jour = trameInterpretee.jour, heure = trameInterpretee.heure, valeur = trameInterpretee, traite = False)
                        print "3 = rfid"

                    # Met le checkStatus du thread de commande à 1
                    #threadCommand.checkStatus = 1
                    # Note : il est possible que l'on se retrouve avec deux
                    # timers au lieu d'un avec cet appel... => double check de la BI

except KeyboardInterrupt:
    print '\nFermeture de la connexion'
    connexion_avec_passerelle.close()

print "Exit main program"
