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
import threadsDefined


########### CONNEXION BDD ###############
db_connec = mongoengine.connect('GHome_BDD')

initBase.initialize()

############# CONNEXION PASSERELLE ###################
connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
    
    # print "\nOu voulez-vous vous connecter?"
    
    # passerelleChoisie = 3
    # while passerelleChoisie > 2 :
        # print "1. Passerelle EnOcean"
        # print "2. Simulateur Proxy"
        # passerelleChoisie = int(input())

    # if passerelleChoisie == 1:
        # try :
            # hote = '134.214.106.23'
            # port = 5000
            # connexion_avec_passerelle.connect((hote, port))
            # print("Connexion etablie avec la passerelle sur le port {}".format(port))
            # connected = True
            
        # except socket.error :
            # print("Impossible de se connecter au proxy")
            # exit()
    # else :
        # print "\nSur quelle adresse IP? (localhost autorisé)"
        # hote = raw_input(">> ")
        # print "\nSur quel port?"
        # port = int(input())
        # port = 13800
        # try :
            # connexion_avec_passerelle.connect((hote, port))
            # print("Connexion établie avec la passerelle sur le port {}".format(port))
            # connected = True
            
        # except socket.error :
            # print("Impossible de se connecter au proxy")
            # exit()
            
try :
    #hote = '134.214.106.23'
    #port = 5000
    #connexion_avec_passerelle.connect((hote, port))
    #print("Connexion etablie avec la passerelle sur le port {}".format(port))
    print ("\n")
    #connected = True
   
except socket.error :
    print("Impossible de se connecter au proxy")
    print ("\n")

try :
    hote = 'localhost'
    port = 13700
    connexion_avec_passerelle.connect((hote, port))
    print("Connexion etablie avec le simulateur sur le port {}".format(port))
    print ("\n")
   
except socket.error :
    print("Impossible de se connecter au simulateur")
    print ("\n")
    if connected == False:
        exit()

threadCommand = threadsDefined.ThreadCommand()
threadCommand.start()

# Process qui va vérifier les trames provenant de la passerelle       
try: 
    while True:
        #récupération identifiants dans la base
        identifiants = [i.capteur_id for i in tables.Capteur.objects(interpreter=True)]
        nouveaux = [i.capteur_id for i in tables.Capteur.objects(interpreter=False)]
        msg_recu = connexion_avec_passerelle.recv(28)       
        msg_recu = msg_recu.decode()
        print "\n"
        print msg_recu
        
        # Recupere l'identifiant du capteur
        ident = msg_recu[16:24] 
        
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

        elif int(ident,16) in nouveaux :
            print 'trame de confirmation reçue'
            now = datetime.datetime.now()
            capteur = tables.Capteur.objects(capteur_id = ident).first()
            pieces = tables.Piece.objects()
            for p in pieces :
                if capteur in p.capteurs :
                    piece_id = p.piece_id
                    break
            conf = tables.ConfirmationAppareillage(piece_id = piece_id, date = now, traite = True,ident=ident)
            capteur.interpreter = True;
            capteur.save();
            conf.save();


except KeyboardInterrupt:
    print '\nFermeture de la connexion'
    connexion_avec_passerelle.close()

print "Exit main program"
