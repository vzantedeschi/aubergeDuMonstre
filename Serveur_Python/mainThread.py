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

# Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
hote = 'localhost'

# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000
port = 12900

print "Lancement du Serveur"

############# CONNEXION PASSERELLE ###################
connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    connexion_avec_passerelle.connect((hote, port))
    print("Connexion établie avec la passerelle sur le port {}".format(port))

except socket.error :
    print("Impossible de se connecter au proxy")
    exit()

########### CONNEXION BDD ###############
db_connec = mongoengine.connect('GHome_BDD')
db = db_connec.GHome_BDD

########### INITIALISATION BDD #############
#now = datetime.datetime.now()
capteur_presence1 = tables.Presence(capteur_id = "00054155", date = 0, traite = True)
#capteur_presence1 = {capteur_id:"00054155",date:"0",traite:"True"}
collection = db.presenc
collection.save(capteur_presence1)

fic_id = open("../identifiants.txt","r")
identifiants = fic_id.readlines()
fic_id.close()

identifiants = [int(el,16) for el in identifiants]

threadCommand = threadsDefined.ThreadCommand(connexion_avec_passerelle)
threadCommand.start()

#Process qui va vérifier les trames provenant de la passerelle       
try: 
    while True:
        msg_recu = connexion_avec_passerelle.recv(28)       
        msg_recu = msg_recu.decode()
        print msg_recu
        
        # Recupere l'identifiant du capteur
        ident = msg_recu[16:24] 
        
        # Si le capteur appartient a ceux etudiés on traite la trame
        if int(ident,16) in identifiants :
            # Recupere la date et l'heure de reception
            now = datetime.datetime.now()

            print("Reçu {}".format(msg_recu))

            # Passage par le parser
            infosTrame = trame.Trame(msg_recu,now)

            print ("ID {}".format(hex(infosTrame.idBytes)))
            print ("DB {}".format(hex(infosTrame.dataBytes)))
            print ("Heure {}".format(infosTrame.heure))

            # Insère la trame dans la BI
            trameInterpretee = interpreteur.Interpretation(infosTrame)
            ### ICI METTRE DANS LA BDD ###
            if trameInterpretee.typeCapteur == 'PRES':
                    capteur_presence = tables.Presence(capteur_id = trameInterpretee.id, date = trameInterpretee.date, traite = False)
                    db.presence.save(capteur_presence)

            # Met le checkStatus du thread de commande à 1
            threadCommand.checkStatus = 1
            # Note : il est possible que l'on se retrouve avec deux
            # timers au lieu d'un avec cet appel... => double check de la BI

except KeyboardInterrupt:
    print '\nFermeture de la connexion'
    connexion_avec_passerelle.close()

print "Exit main program"
