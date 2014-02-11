#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import pymongo
import time
import sys
sys.path.append('../BDD')
import tables

class Commande():
    def __init__(self):

        typeInfo = 'None'

        ### Examiner la BD ###
        db_connec = mongoengine.connect('GHome_BDD')
        db = db_connec.GHome_BDD
        
        liste = db.devices.find({u'traite':False})
        item = None

        # Permet d'examiner les informations nouvelles dans la BDD
        for anItem in liste:
            item = anItem
            print "\n"
            print item
            typeInfo = item[u'_cls']
        
        ### Il me faut le format des informations de sortie pour savoir
        ### sur quoi faire une condition
        if (typeInfo == "Devices.Presence"):
            print 'Presence detectee'
            self.type = 'PRES'

        elif (typeInfo == "Devices.Temperature"):
            #Détermine la commande et mettre "traite" à True
            print "Temperature"
            self.type = 'TEMP'
            
            self.val = item[u'valeur']
            print self.val

            self.piece_id = item[u'piece_id']
            print self.piece_id
            
            pieces = tables.Piece.objects
            for p in pieces :
                if self.piece_id == p.piece_id :
                    etats = db.etat.find({u'_cls':"Etat.Clim", u'piece_id': item[u'piece_id']})
                    for elem in etats:
                        print elem

            self.climActive = elem[u'climActivee']
            print self.climActive

        elif (typeInfo == "Devices.Humidite"):
            print "Humidite"
            self.type = 'HUMID'
            
            self.val = item[u'valeur']
            print self.val

            self.piece_id = item[u'piece_id']
            print self.piece_id
            
            pieces = tables.Piece.objects
            for p in pieces :
                if self.piece_id == p.piece_id :
                    etats = db.etat.find({u'_cls':"Etat.AntiIncendie", u'piece_id': item[u'piece_id']})
                    for elem in etats:
                        print elem

            self.antiIncendieActive = elem[u'antiIncendieDeclenche']
            print self.antiIncendieActive
            
        elif (typeInfo =="Devices.RFID"):
            print "RFID"
            self.type = 'RFID'
            self.resident = item[u'resident_id']
            print self.resident

        elif (typeInfo =="Devices.Interrupteur"):
            print "Interrupteur"
            self.type = 'INTR'

        else:
            print 'Autre type de commande'
            self.type = 'OTHER'
            
        if (item != None):
            # Modifier l'information de la BDD pour mettre "traite" à True            
            db.devices.update({"_id" : item[u'_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
