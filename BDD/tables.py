#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import datetime

class Capteur():
	capteur_id = mongoengine.IntField(required=True)
	date = mongoengine.IntField(required = True)
	traite = mongoengine.BooleanField(required = True)
	meta = {'allow_inheritance': True}
		
class Actionneur():
	actionneur_id = mongoengine.IntField(required=True)
	date = mongoengine.IntField(required = True)
	meta = {'allow_inheritance': True}

class Piece(mongoengine.Document):
	piece_id = mongoengine.IntField(required=True)
	name = mongoengine.StringField(required = True)
	actionneurs = mongoengine.SortedListField(mongoengine.ReferenceField(Capteur), ordering='date')
	capteurs = mongoengine.SortedListField(mongoengine.ReferenceField(Actionneur), ordering='date')
	
class Personne(mongoengine.Document):
	personne_id = mongoengine.IntField(required=True)
	nom = mongoengine.StringField(required = False)
	
class Presence(Capteur, mongoengine.Document):
	pass
	
class Temperature(Capteur, mongoengine.Document):
	valeur = mongoengine.IntField(required = True)

class Humidite(Capteur, mongoengine.Document):
	valeur = mongoengine.IntField(required = True)	

class RFID (Capteur, mongoengine.Document):
	resident_id = mongoengine.StringField(required = True)

class FermetureRideau(Actionneur, mongoengine.Document):
	rideauOuvert = mongoengine.BooleanField(required = True)

class AntiIncendie (Actionneur, mongoengine.Document):
	antiIncendieDeclenche = mongoengine.BooleanField(required = True)

class Clim(Actionneur, mongoengine.Document):
	climActivee = mongoengine.BooleanField(required = True)

class FermeturePorte (Actionneur, mongoengine.Document):
	porteFermee = mongoengine.BooleanField(required = True)

class FermetureVolet(Actionneur, mongoengine.Document):
	voletOuvert = mongoengine.BooleanField(required = True)

class Interrupteur (Actionneur, mongoengine.Document):
	interrupteurDeclenche = mongoengine.BooleanField(required = True)



