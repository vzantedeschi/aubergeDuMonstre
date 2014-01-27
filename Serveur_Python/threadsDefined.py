#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import signal
import os

## Functions ##

def TimerFunc(thread):
    thread.checkStatus = 1

## Threads ##
        
class ThreadAppliWebListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        # Termine le thread en même temps que le main
        self.setDaemon(True)
        
    def run(self):
        while 1:
            print "Web Listener"
            
class ThreadCommand(threading.Thread):

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.setDaemon(True)
        
        # le checkStatus passe à 1 quand le thread doit lire la BI
        self.checkStatus = 0
        print self.checkStatus
        
    def run(self):
        
        while 1:
            if self.checkStatus == 1:
                #Timer avec 2sec de période remettant le checkstatus à 1
                t = threading.Timer(2,TimerFunc,[self])
                t.start()

                #inspecte la BI

                self.checkStatus = 0
       
        #print "Envoi de message"
        #trame de test"
        #self.socket.send('A55A6B05100000000021CBE3205F')

class ThreadSender(threading.Thread):

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.setDaemon(True)
        
    def run(self):
        print "Sender"
