#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import pymongo

class Commande():
    def __init__(self):

        typeInfo = 'None'

		##premier test : est ce qu il y a du mouvement depuis peu de temps ?
        ### ICI EXAMINER LA BDD ###
        db_connec = mongoengine.connect('GHome_BDD')
        db = db_connec.GHome_BDD
        
        # Risque de nous donner une liste => problèmes
        liste = db.capteur.find({u'traite':False},{u'_cls':1})
        
        # Permet d'examiner les informations nouvelles dans la BDD
        for item in liste:
            print item
            typeInfo = item['_cls']
            print typeInfo
        
        ### Il me faut le format des informations de sortie pour savoir
        ### sur quoi faire une condition
        if (typeInfo == "Capteur.Presence"):
            print 'Presence detectee'
            self.type = 'PRES'
            
            # Modifier l'information de la BDD pour mettre "traite" à True            
            db.capteur.update({"_id" : item['_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
        else:
            print 'Autre type de commande'
            self.type = 'OTHER'
