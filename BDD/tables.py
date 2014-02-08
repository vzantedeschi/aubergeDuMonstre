#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import datetime

class Capteur(mongoengine.Document):
	capteur_id = mongoengine.StringField(primary_key=True)
	capteur_type = mongoengine.StringField(required=True)
	annee = mongoengine.IntField(required = True)
	mois = mongoengine.IntField(required = True)
	jour = mongoengine.IntField(required = True)
	heure = mongoengine.IntField(required = True)
	traite = mongoengine.BooleanField(required = True)
	meta = {'allow_inheritance': True}
		
class Actionneur(mongoengine.Document):
	actionneur_id = mongoengine.IntField(required=True)
	annee = mongoengine.IntField(required = True)
	mois = mongoengine.IntField(required = True)
	jour = mongoengine.IntField(required = True)
	heure = mongoengine.IntField(required = True)
	meta = {'allow_inheritance': True}

class Piece(mongoengine.Document):
	piece_id = mongoengine.IntField(required=True)
	name = mongoengine.StringField(required = True)
	actionneurs = mongoengine.SortedListField(mongoengine.ReferenceField('Actionneur'))
	capteurs = mongoengine.SortedListField(mongoengine.ReferenceField('Capteur'))
	
class Personne(mongoengine.Document):
	personne_id = mongoengine.IntField(required=True)
	nom = mongoengine.StringField(required = False)
	
class Presence(Capteur):
	pass
	
class Temperature(Capteur):
	valeur = mongoengine.FloatField(required = True)

class Humidite(Capteur):
	valeur = mongoengine.FloatField(required = True)	

class RFID (Capteur):
	resident_id = mongoengine.StringField(required = True)

class FermetureRideau(Actionneur):
	rideauOuvert = mongoengine.BooleanField(required = True)

class AntiIncendie (Actionneur):
	antiIncendieDeclenche = mongoengine.BooleanField(required = True)

class Clim(Actionneur):
	climActivee = mongoengine.BooleanField(required = True)

class FermeturePorte (Actionneur):
	porteFermee = mongoengine.BooleanField(required = True)

class FermetureVolet(Actionneur):
	voletOuvert = mongoengine.BooleanField(required = True)

class Interrupteur (Actionneur):
	interrupteurDeclenche = mongoengine.BooleanField(required = True)




