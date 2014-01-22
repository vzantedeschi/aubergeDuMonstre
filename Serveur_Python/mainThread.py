#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threadsDefined
import socket
import trame
import datetime

# Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
hote = 'localhost'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 4000

print "Lancement du Serveur"

############# CONNEXION PASSERELLE ###################
connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    connexion_avec_passerelle.connect((hote, port))
    print("Connexion établie avec la passerelle sur le port {}".format(port))

except socket.error :
    print("Impossible de se connecter au proxy")
    exit()

fic_id = open("../identifiants.txt","r")
identifiants = fic_id.readlines()
fic_id.close()

SYNC_BYTES = "A55A"
H_SEQ = "0B"
identifiants = [int(el,16) for el in identifiants]
        
try: 
	while True:
	    msg_recu = connexion_avec_passerelle.recv(28)	    
	    msg_recu = msg_recu.decode()
	    
	    # Recupere l'identifiant du capteur
	    ident = msg_recu[16:24]
	    
	    # Si le capteur appartient a ceux etudies on traite la trame
	    if int(ident,16) in identifiants :
	        # Recupere la date et l'heure de reception
	        now = datetime.datetime.now()

	        print("Reçu {}".format(msg_recu))

	        # Passage par le parser
	        infosTrame = trame.Trame(msg_recu,now)

	        print ("ID {}".format(hex(infosTrame.idBytes)))
	        print ("DB {}".format(hex(infosTrame.dataBytes)))
	        print ("Heure {}".format(infosTrame.heure))

except KeyboardInterrupt:
	print '\nFermeture de la connection'
	connexion_avec_passerelle.close()

print "Exit main program"
