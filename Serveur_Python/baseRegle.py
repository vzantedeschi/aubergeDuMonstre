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
        
        liste = db.donnee.find({u'traite':False})
        item = None

        # Permet d'examiner les informations nouvelles dans la BDD
        for anItem in liste:
            item = anItem
            print "\n"
            print item
            typeInfo = item[u'_cls']
        
        ### Il me faut le format des informations de sortie pour savoir
        ### sur quoi faire une condition
        if (typeInfo == "Donnee.Presence"):
            print 'Presence detectee'
            self.type = 'PRES'

        elif (typeInfo == "Donnee.Temperature"):
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
                    etat = tables.Etat.objects(piece_id = self.piece_id).first()
                    print etat

            self.climActive = etat[u'climActivee']
            print self.climActive

            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'temperature' : tempDonnees} },upsert=False,multi=True)

        elif (typeInfo == "Donnee.Humidite"):
            print "Humidite"
            self.type = 'HUMID'
            
            self.val = item[u'valeur']
            print self.val

            self.piece_id = item[u'piece_id']
            print self.piece_id
            
            pieces = tables.Piece.objects
            for p in pieces :
                if self.piece_id == p.piece_id :
                    etat = tables.Etat.objects(piece_id = self.piece_id).first()
                    print etat

            self.antiIncendieActive = etat[u'antiIncendieDeclenche']
            print self.antiIncendieActive
        
            db.etat.update({u'piece_id' : piece_id},{ "$set": {u'humidite' : humDonnees} },upsert=False,multi=True)
            
        elif (typeInfo == "Donnee.RFID"):
            print "RFID"
            self.type = 'RFID'
            self.resident = item[u'resident_id']
            print self.resident

        elif (typeInfo == "Donnee.Interrupteur"):
            print "Interrupteur"
            self.type = 'INTR'

        else:
            print 'Autre type de commande'
            self.type = 'OTHER'
            
        if (item != None):
            # Modifier l'information de la BDD pour mettre "traite" à True            
            db.donnee.update({"_id" : item[u'_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
