#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
import sys
import tables

db = connect('GHome_BDD')

def addCapteur() :
	print 'ajouté à la base'

def addActionneur() :
	print 'ajouté à la base'

def initialize() :
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

        #Initialisation de l'état des pièces
        for p in pieces :
                etat = tables.Etat(piece_id = p.piece_id, rideauxOuverts = True,antiIncendieDeclenche = False,climActivee = False,portesFermees = False,voletsOuverts = True,priseDeclenchee = False,persosPresents = [])
                etat.save()

	print 'base reinitialisee'

if __name__ == '__main__' :
	initialize()

