#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import threading
import time
import signal
import os
import baseRegle

from flask import Flask, render_template, request
import requests
import json

presence = False

app = Flask(__name__)

@app.route('/')
def hello():
    clients = [1, 2, 3]
    return render_template('index.html', clients=clients)

@app.route('/surveillance.html')
def surveillance():
    return render_template('surveillance.html', presence = presence)

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

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
        
        webList = ThreadAppliWebListener()
        webList.start()
        
        # Le checkStatus passe à 1 quand le thread doit lire la BI
        self.checkStatus = 0

        # Aucune puce RFID détectée
        self.rfidDetected = False
        
    def run(self):
        while 1:
            try:
                if self.checkStatus == 1:
                    # Timer avec 2sec de période remettant le checkstatus à 1
                    t = threading.Timer(10,TimerFunc,[self])
                    t.start()

                    # Fais appel à la base de règle pour générer une commande
                    commande = baseRegle.Commande()

                    ### ICI TRAITER LA COMMANDE SELON SON TYPE ###
                    if commande.type == 'RFID' :
                        print 'Commande suivant detection RFID envoyee'
                        self.rfidDetected = True
                        # Mise en place d'un timer qui indique
                        # qu'il n'attend plus une détection de présence au bout
                        # de 20 secondes
                        timerRFID = threading.Timer(20,RFIDFunc,[self])
                        timerRFID.start()
                        
                    elif commande.type == 'PRES' :
                        print 'Commande suivant une intrusion envoyee'
                        presence = True

                        if self.rfidDetected == False :
                            ## ENVOYER A L'APPLI WEB ##

                            ## REPONSE APPLI WEB ##
                            if (True) :
                                ## Allume l'interrupteur simulant les volets ##
                                print "Verrouillage activé : volets en cours de fermeture"
                                self.socket.send( 'A55A6B0570000000FF9F1E0530D1' )

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
