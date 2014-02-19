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
	name = StringField(required=True)
	actionneurs = SortedListField(ReferenceField('Actionneur'))
	capteurs = SortedListField(ReferenceField('Capteur'))
	
class Personne(Document):
	personne_id = IntField(unique=True)	
	nom = StringField(default="Intrus")
	ignore = BooleanField(default=True)

class Etat(Document):
    piece_id = IntField(primary_key=True)
    rideauxOuverts = BooleanField(default=True)
    antiIncendieDeclenche = BooleanField(default=False)
    climActivee = BooleanField(default=False)
    portesFermees = BooleanField(default=False)
    voletsOuverts = BooleanField(default=True)
    priseDeclenchee = BooleanField(default=False)
    temperature = IntField()
    humidite = IntField()
    persosPresents = SortedListField(ReferenceField('Personne'))

class Donnee(Document) :
	piece_id = IntField(required=True)
	date = DateTimeField(required=True)
	traite = BooleanField(required=True)
	meta = {'allow_inheritance': True}

## Les classes héritant de Donnee sont les données récupérées des trames reçues
class Presence(Donnee):
	pass

class Interrupteur(Donnee):
        ouverte = BooleanField(required = True)
	
class Temperature(Donnee):
	valeur = FloatField(required=True)

class Humidite(Donnee):
	valeur = FloatField(required=True)

class ContactFen(Donnee):
	ouverte = BooleanField(required=True)

class RFID (Donnee):
	resident_id = IntField(required=True)


## Donnees recues par l'appli web (actionneurs)
class DonneeAppli(Document) :
	traite = BooleanField(required=True)
	piece_id = IntField(required=True) #piece concernee
	capteur_type = StringField(required=True) #type de capteur concerne
	meta = {'allow_inheritance': True}

## Reponse envoyee suite a la detection d'un intrus
class ReponseAppli(DonneeAppli):
	reponse = BooleanField(required=True)

if __name__ == '__main__' :

	import time
	db = connect('GHome_BDD')
	db.drop_database('GHome_BDD')

	for i in range(10) :
		etat = Etat(piece_id = i)
		etat.save()

	liste = Etat.objects

	for l in liste :
		print 'piece ' + str(l.piece_id) + ' climActivee : ' + str(l.climActivee)

	db.drop_database('GHome_BDD')

