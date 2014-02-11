#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import pymongo
import time

class Commande():
    def __init__(self):

        typeInfo = 'None'

        ### Examiner la BD ###
        db_connec = mongoengine.connect('GHome_BDD')
        db = db_connec.GHome_BDD
        
        liste = db.etat.find({u'traite':False})
        item = None

        # Permet d'examiner les informations nouvelles dans la BDD
        for anItem in liste:
            item = anItem
            print item
            typeInfo = item[u'_cls']
            print typeInfo
        
        ### Il me faut le format des informations de sortie pour savoir
        ### sur quoi faire une condition
        if (typeInfo == "Etat.Presence"):
            print 'Presence detectee'
            self.type = 'PRES'

        elif (typeInfo == "Etat.Temperature"):
            #Détermine la commande et mettre "traite" à True
            print "Temperature"
            self.type = 'TEMP'
            self.val = item[u'valeur']
            print self.val

        elif (typeInfo == "Etat.Humidite"):
            print "Humidite"
            self.type = 'HUMID'
            self.val = item[u'valeur']
            print self.val
            
        elif (typeInfo =="Etat.RFID"):
            print "RFID"
            self.type = 'RFID'
            self.resident = item[u'resident_id']
            print self.resident

        else:
            print 'Autre type de commande'
            self.type = 'OTHER'
            
        if (item != None):
            # Modifier l'information de la BDD pour mettre "traite" à True            
            db.etat.update({"_id" : item[u'_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
