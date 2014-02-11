#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import threading
import time
import signal
import os
import baseRegle
import socket

from flask import Flask, render_template, request
import requests
import json

presence = False

app = Flask(__name__)

@app.route('/')
def hello():
    clients = [1, 2, 3]
    return render_template('index.html', clients=clients)

@app.route('/surveillance')
def surveillance():
    return render_template('surveillance.html', presence = presence)

@app.route('/controle')
def controle():
    return render_template('controle.html')

@app.route('/presence')
def get_presence():
    global presence
    presence = not presence
    return json.dumps(presence)

## Functions Server ##

def TimerFunc(thread):
    thread.checkStatus = 1

def RFIDFunc(thread):
    thread.rfidDetected = False

## Threads ##
        
class ThreadAppliWebListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        app.run(threaded=True)
            
class ThreadCommand(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        
        # Le checkStatus passe à 1 quand le thread doit lire la BI
        self.checkStatus = 0

        # Aucune puce RFID détectée
        self.rfidDetected = False
        
    def run(self):
        hote = '134.214.106.23'
        port = 5000
        try :
            self.socket.connect((hote, port))
            self.connected = True
        except socket.error :
            print("Impossible de se connecter au proxy : Les trames d'actionneurs ne seront pas envoyees")

        webList = ThreadAppliWebListener()
        webList.start()

        while True :
            try :
                if self.checkStatus == 1:
                    # Timer avec 2sec de période remettant le checkstatus à 1
                    t = threading.Timer(10,TimerFunc,[self])
                    t.start()

                    # Fais appel à la base de règle pour générer une commande
                    commande = baseRegle.Commande()

                    ### ICI TRAITER LA COMMANDE SELON SON TYPE ###
                    if commande.type == 'RFID' :
                        print 'Commande suivant detection RFID en cours'
                        self.rfidDetected = True
                        # Mise en place d'un timer qui indique
                        # qu'il n'attend plus une détection de présence au bout
                        # de 20 secondes
                        timerRFID = threading.Timer(20,RFIDFunc,[self])
                        timerRFID.start()
                        
                    elif commande.type == 'PRES' :
                        print 'Commande suivant une presence en cours'
                        presence = True

                        if self.rfidDetected == False :
                            ## ENVOYER A L'APPLI WEB ##

                            ## REPONSE APPLI WEB ##
                            if (True) :
                                # Allume l'interrupteur simulant les volets
                                print "Verrouillage active : volets en cours de fermeture"
                                # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
                                if self.connected == True :
                                    self.socket.send( 'A55A6B0570000000FF9F1E0530D1' )
                                    
                    elif commande.type == 'TEMP' :
                        print 'Commande suivant un changement de temperature en cours'

                        ## Valeur 19 à modifier dans une interface graphique par exemple
                        if commande.val > 19 :
                            print "Activation de la climatisation"
                            if self.connected == True :
                                self.socket.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
                                
                    elif commande.type == 'HUMID' :
                        print 'Commande suivant un changement de humidite en cours'

                        ## Valeur 70 à modifier dans une interface graphique par exemple
                        if commande.val < 70 :
                            print "Activation du systeme anti-incendie"
                            if self.connected == True :
                                self.socket.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )

                    elif commande.type == 'OTHER':
                        print 'Pas de commande implementee'
                        presence = False

                    # Met le checkstatus à 0 pour éviter de reparcourir la BI
                    self.checkStatus = 0
            except KeyboardInterrupt:
                t.cancel()
                break
            
if __name__ == '__main__':
    app.run(debug=True)
