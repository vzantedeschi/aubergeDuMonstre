#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
import sys
import tables

def addCapteur() :
	print 'ajouté à la base'

def addActionneur() :
	print 'ajouté à la base'

def initialize() :
	db = connect('GHome_BDD')
	db.drop_database('GHome_BDD')

	#Initialisation pièces
	fic_id = open('../pieces.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    pi, nom = l.split()
	    pi = int(pi)
	    piece = tables.Piece(piece_id = pi, name = nom)
	    piece.save()
	    etat = tables.Etat(piece_id = piece.piece_id, persosPresents = [])
	    etat.save()

	#Initialisation capteurs
	fic_id = open('../capteurs.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    pi, typeC, ident = l.split()
	    pi = int(pi)
	    ident = int(ident,16)
	    capteur = tables.Capteur(capteur_id = ident, capteur_type = typeC)
	    capteur.save()

	    piece = tables.Piece.objects(piece_id = pi).first()
	    if piece == None :
			piece = tables.Piece(piece_id = pi, name = "")
			piece.save()
			etat = tables.Etat(piece_id = pi, persosPresents = [])
			etat.save()

	    piece.capteurs.append(capteur)
	    piece.save()

	#Initialisation actionneurs
	fic_id = open('../actionneurs.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    pi, typeA, ident = l.split()
	    pi = int(pi)
	    ident = int(ident,16)
	    actionneur = tables.Actionneur(actionneur_id = ident, capteur_type = typeA)
	    actionneur.save()

	    piece = tables.Piece.objects(piece_id = pi).first()
	    if piece == None :
			piece = tables.Piece(piece_id = pi, name = "")
			piece.save()
			etat = tables.Etat(piece_id = pi, persosPresents = [])
			etat.save()

	    piece.actionneurs.append(actionneur)
	    piece.save()

	#Initialisation des personnages
	fic_id = open('../personnages.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    ident, name = l.split()
	    ident = int(ident,16)
	    personnage = tables.Personne(personne_id = ident, nom = name)
	    personnage.save()

        pieces = tables.Piece.objects

	print 'base reinitialisee'

if __name__ == '__main__' :
	initialize()

	##### Ajout intrus dans le couloir ######
	piece = tables.Piece.objects(name="Couloir").first()
	print piece.piece_id
	etat = tables.Etat.objects(piece_id=piece.piece_id).first()
	intrus = tables.Personne.objects(nom="Intrus").first()
	etat.persosPresents.append(intrus)
	etat.save()
	print "ça y est : un intrus est dans le couloir"