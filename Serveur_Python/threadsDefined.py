#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import requests
import json

import sys
import threading
import time
import signal
import os
import baseRegle
import socket
import mongoengine
import pymongo

presence = False

    
def TimerFunc(thread):
    thread.checkStatus = 1
    
class ThreadCommand(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # La variable "connected" servira à savoir au cour du programme si on peut
        # envoyer des trames aux actionneurs ou si on s'en tient à des affichages écran
        # dans le cas où l'on n'a pas accès au réseau GHome
        self.connected = False
        
        # Le checkStatus passe à 1 quand le thread doit lire la BI
        self.checkStatus = 0

        # Aucune puce RFID détectée
        self.rfidDetected = False
        self.Terminated = False
        
    def run(self):
        db_connec = mongoengine.connect('GHome_BDD')
        db = db_connec.GHome_BDD
        self.checkStatus = 1
        t = threading.Timer(2,TimerFunc,[self])
        baseRegle.connect()

        while not self.Terminated:
            try :
                if self.checkStatus == 1:
                    # Timer avec 2sec de période remettant le checkstatus à 1         
                    threading.Timer(2, TimerFunc, [self]).start()
                    self.checkStatus = 0

                    
                    # Fais appel à la base de règle 
                    retour = baseRegle.commande()

                    ### ICI TRAITER LA COMMANDE SELON SON TYPE ###
                    #if commande.type == 'RFID' :
                    #    print 'Commande suivant detection RFID en cours'
                    #    self.rfidDetected = True
                        # Mise en place d'un timer qui indique
                        # qu'il n'attend plus une détection de présence au bout
                        # de 20 secondes
                    #    timerRFID = threading.Timer(20,RFIDFunc,[self])
                    #    timerRFID.start()
                        
                    # elif commande.type == 'PRES' :
                        # print 'Commande suivant une presence en cours'
                        # presence = True

                        # if self.rfidDetected == False :
                            ## ENVOYER A L'APPLI WEB ##

                            ## REPONSE APPLI WEB ##
                            # if (True) :
                                # Allume l'interrupteur simulant les volets
                                # print "Verrouillage active : volets en cours de fermeture"
                                # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
                                # if self.connected == True :
                                    # print "Envoi au proxy"
                                    # self.socket.send( 'A55A6B0550000000FF9F1E0530B1' )
                                    
                    # elif commande.type == 'TEMP' :
                        # print 'Commande suivant un changement de temperature en cours'

                        ## Valeur 19 à modifier dans une interface graphique par exemple
                        ## La trame crée est fausse, c'est un exemple
                        # if commande.val > 19 and commande.climActive == False :
                            # print "Activation de la climatisation"
                            # Modifier l'information de la BDD pour mettre "climActive" à True
                            # db.etat.update({"_cls" : "Etat.Clim", u'piece_id' : commande.piece_id},{ "$set": {u'climActivee' : True} },upsert=False,multi=True)
                            # if self.connected == True :
                                # self.socket.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
                        # elif commande.val <= 19 and commande.climActive == True :
                            # print "Desactivation de la climatisation"
                            # if self.connected == True :
                                # self.socket.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
                                
                    # elif commande.type == 'HUMID' :
                        # print 'Commande suivant un changement d''humidite en cours'

                        ## Valeur 70 à modifier dans une interface graphique par exemple
                        ## La trame crée est fausse, c'est un exemple
                        # if commande.val < 70 and commande.antiIncendieActive == False:
                            # print "Activation du systeme anti-incendie"
                            # if self.connected == True :
                                # self.socket.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
                        # elif commande.val > 70 and commande.antiIncendieActive == True:
                            # print "Desactivation du systeme anti-incendie"
                            # if self.connected == True :
                                # self.socket.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )

                    # elif commande.type == 'INTR' :
                        # print 'Commande suivant un interrupteur en cours'
                        # if self.connected == True :
                            # print "Ouverture des volets"
                            # self.socket.send('A55A6B0570000000FF9F1E0530D1' )

                    # elif commande.type == 'OTHER':
                        # print 'Pas de commande implementee'

                    # Met le checkstatus à 0 pour éviter de reparcourir la BI
                    
            except KeyboardInterrupt:
                self.Terminated = True
                t.cancel()
                break

if __name__ == '__main__':
    app.run(debug=True)





