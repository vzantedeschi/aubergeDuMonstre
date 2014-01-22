#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
                
class ThreadAppliWebListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"
            
class ThreadCommand(threading.Thread):

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
        
    def run(self):
        #création des threads
        #threadTimer = ThreadTimer()
        #threadTimer.start()
        
        #thread de test pour envoi de trame
        #threadSender = ThreadSender(self.socket)
        #threadSender.start()
        print "Send a message 1"
        #trame de test"
        #self.socket.send('A55A6B0570000000FF9F1E0430D0')
        
        print "Send a message 2"
        #trame de test"
        self.socket.send('A55A6B05500000000021CBE230BE')

        print "Send a message 3"
        #trame de test"
        self.socket.send('A55A6B0550000000FF9F1E0430B0')
        
        #while 1:
            #Lire la BI et agir (envoi de commandes) toutes les XX secondes
            #
            #time.sleep(1)
            #

class ThreadTimer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"

class ThreadSender(threading.Thread):

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
        
    def run(self):
        print "bonjour"
