#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
import datetime

class Capteur(Document):
	capteur_id = IntField(primary_key=True)
	capteur_type = StringField(required=True)
		
class Actionneur(Document):
	actionneur_id = IntField(primary_key=True)
	capteur_type = StringField(required=True)

class Piece(Document):
	piece_id = IntField(primary_key=True)
	name = StringField(required = True)
	actionneurs = SortedListField(ReferenceField('Actionneur'))
	capteurs = SortedListField(ReferenceField('Capteur'))
	
class Personne(Document):
	personne_id = IntField(primary_key=True)
	nom = StringField(required = False)

class Etat(Document) :
	piece_id = IntField(required = True)
	date = DateTimeField(required = True)
	traite = BooleanField(required = True)
	meta = {'allow_inheritance': True}

class Presence(Etat):
	pass
	
class Temperature(Etat):
	valeur = FloatField(required = True)

class Humidite(Etat):
	valeur = FloatField(required = True)	

class RFID (Etat):
	resident_id = IntField(required = True)

class FermetureRideau(Etat):
	rideauOuvert = BooleanField(required = True)

class AntiIncendie (Etat):
	antiIncendieDeclenche = BooleanField(required = True)

class Clim(Etat):
	climActivee = BooleanField(required = True)

class FermeturePorte (Etat):
	porteFermee = BooleanField(required = True)

class FermetureVolet(Etat):
	voletOuvert = BooleanField(required = True)

class Interrupteur (Etat):
	interrupteurDeclenche = BooleanField(required = True)


if __name__ == '__main__' :

	import time
	# Test trie par date d'insertion
	db = connect('GHome_BDD')
	db.drop_database('GHome_BDD')

	for i in range(10) :
		etat = Clim(piece_id = 1, date = datetime.datetime.now(), traite = False, climActivee = True)
		etat.save()
		time.sleep(1)

	liste = Etat.objects(piece_id = 1).order_by('-date')

	for l in liste :
		print 'etat : ' + str(l.date)

	db.drop_database('GHome_BDD')

