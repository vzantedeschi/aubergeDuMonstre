#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import threading
import time
import signal
import os
import baseRegle
sys.path.append('../ghome web/')
import web

## Functions ##

def TimerFunc(thread):
    thread.checkStatus = 1

## Threads ##
        
class ThreadAppliWebListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "Web Listener"
            
class ThreadCommand(threading.Thread):

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
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
                        web.surveillance(True)

                        ## ENVOYER A L'APPLI WEB ##
                    elif commande.type == 'OTHER':
                        print 'pas de commande implementee'
                        web.surveillance(False)
                        ## TODO

                    # Met le checkstatus à 0 pour éviter de reparcourir la BI
                    self.checkStatus = 0
            except KeyboardInterrupt:
                t.cancel()
                break
