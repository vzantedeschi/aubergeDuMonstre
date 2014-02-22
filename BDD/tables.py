#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib

from mongoengine import *
import datetime

def hash_password(password, salt):
    return hashlib.sha512(salt + hashlib.sha256(password).hexdigest()).hexdigest()

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

class Utilisateur(Document):
	identifiant = StringField(unique=True)

	secret_hash = StringField(required=True)
	salt = StringField(required=True)

	def valider_mot_passe(self, mot):
		return hash_password(mot, self.salt) == self.secret_hash

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
	traite = BooleanField(default=False)
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
class DonneeAppli(Donnee) :
	actionneur_id = IntField(required=True) #type d'actionneur concerne
	action_type = BooleanField(required=True) #allumer = True, eteindre = False

## Reponse envoyee suite a la detection d'un intrus
class ReponseAppli(Donnee):
	reponse = BooleanField(required=True)
    
class Regle(Document):
    regle_id = IntField(required=True)
    nom = StringField(required = True)
    conditions = SortedListField(ReferenceField('Condition'))
    actions = SortedListField(ReferenceField('Action'))
    
class Action(Document):
    nom = StringField(required = True)
    description = StringField(required = True)
    
class Condition(Document):    
    nom = StringField(required = True)
    description = StringField(required = True)

    

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

