#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
                
class ThreadAppliWebListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"
            
class ThreadCommand(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            #Lire la BI et agir (envoi de commandes) toutes les XX secondes
            #
            time.sleep(1)
            #

class ThreadTimer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"

class ThreadSender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"