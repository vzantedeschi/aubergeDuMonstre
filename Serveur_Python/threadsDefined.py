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



## Functions ##

def TimerFunc(thread):
    thread.checkStatus = 1

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
                    if commande.type == 'PRES':
                        print 'commande suivant une intrusion envoyee'
                        presence = True

                        ## ENVOYER A L'APPLI WEB ##
                    elif commande.type == 'OTHER':
                        print 'pas de commande implementee'
                        presence = False
                        ## TODO

                    # Met le checkstatus à 0 pour éviter de reparcourir la BI
                    self.checkStatus = 0
            except KeyboardInterrupt:
                t.cancel()
                break
if __name__ == '__main__':
    app.run(debug=True)