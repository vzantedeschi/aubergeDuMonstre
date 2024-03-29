#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import mongoengine
import datetime
import trame
import interpreteur
sys.path.append('../BDD')
import tables
import initBase


########### CONNEXION BDD ###############
db_connec = mongoengine.connect('GHome_BDD')

initBase.initialize()

############# CONNEXION PASSERELLE ###################
connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
            
try :
    hote = '134.214.106.23'
    port = 5000
    connexion_avec_passerelle.connect((hote, port))
    print("Connexion etablie avec la passerelle sur le port {}".format(port))
    print ("\n")
    connected = True
except socket.error :
    print("Impossible de se connecter au proxy")
    print ("\n")

    try :
        hote = 'localhost'
        port = 13900
        connexion_avec_passerelle.connect((hote, port))
        print("Connexion etablie avec le simulateur sur le port {}".format(port))
        print ("\n")   
    except socket.error :
        print("Impossible de se connecter au simulateur")
        print ("\n")
        if connected == False:
            exit()

# Process qui va vérifier les trames provenant de la passerelle       
try: 
    while True:
        #récupération identifiants dans la base
        identifiants = [i.capteur_id for i in tables.Capteur.objects(interpreter=True)]
        nouveaux = [i.capteur_id for i in tables.Capteur.objects(interpreter=False)]
        nouveaux.append(int("0021CBE3",16))
        msg_recu = connexion_avec_passerelle.recv(28)       
        msg_recu = msg_recu.decode()
        print "\n"
        print msg_recu
        
        # Recupere l'identifiant du capteur
        ident = msg_recu[16:24] 
        print str(int(ident,16))
        
        # Si le capteur appartient a ceux etudiés on traite la trame
        if int(ident,16) in identifiants :
            # Recupere la date et l'heure de reception
            now = datetime.datetime.now()

            print("Recu {}".format(msg_recu))

            # Passage par le parser
            infosTrame = trame.Trame(msg_recu)          

            if infosTrame.valide == True :
                print ("\n")
                print ("ID {}".format(hex(infosTrame.idBytes)))
                print ("DB ", infosTrame.dataBytes)
                print ("Heure {}".format(now.time()))
                print ("\n")

                if infosTrame.eepSent == False :
                    # Interprète les informations contenues dans la Trame
                    interpreteur.interpretation(infosTrame,now)

        if int(ident,16) in nouveaux :
            print 'trame de confirmation reçue'
            now = datetime.datetime.now()
            capteur = tables.Capteur.objects(capteur_id = int(ident,16)).first()
            pieces = tables.Piece.objects()
            for p in pieces:
                for c in p.capteurs:
                    if c.capteur_id == int(ident,16):
                        piece_id = p.piece_id
            if capteur and piece_id:
                conf = tables.ConfirmationAppareillage(piece_id = piece_id, date = now, traite = True,ident=int(ident,16))
                capteur.interpreter = True;
                capteur.save();
                conf.save();


except KeyboardInterrupt:
    print '\nFermeture de la connexion'
    connexion_avec_passerelle.close()

print "Exit main program"
