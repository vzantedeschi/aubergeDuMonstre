#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import pymongo

class Commande():
    def __init__(self):

        typeInfo = 'None'

        ### Examiner la BD ###
        db_connec = mongoengine.connect('GHome_BDD')
        db = db_connec.GHome_BDD
        
        # Risque de nous donner une liste => problèmes
        liste = db.capteur.find({u'traite':False},{u'_cls':1})
        item = None
        # Permet d'examiner les informations nouvelles dans la BDD
        for anItem in liste:
            item = anItem
            print item
            typeInfo = item['_cls']
            print typeInfo
			
        
        ### Il me faut le format des informations de sortie pour savoir
        ### sur quoi faire une condition
        if (typeInfo == "Capteur.Presence"):
            print 'Presence detectee'
            self.type = 'PRES'
            # Il faudrait tester si une trame RFID a été envoyée aussi
            

        elif (typeInfo =="Capteur.Temperature"):
            #Détermine la commande et mettre "traite" à True
            print "température"
            # Si la température passe en-dessous d'un certain seuil, allumer la clim
            
        elif (typeInfo =="Capteur.Humidite"):
            #Détermine la commande et mettre "traite" à True
            print "humidité"
            #Si l'humidité passe en-dessous d'un certain seuil, déclencher le système incendie
            
        elif (typeInfo =="Capteur.RFID"):
            #Détermine la commande et mettre "traite" à True
            print "RFID"

        else:
            print 'Autre type de commande'
            self.type = 'OTHER'
			
        if (item != None):
	    # Modifier l'information de la BDD pour mettre "traite" à True            
	    db.capteur.update({"_id" : item['_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
