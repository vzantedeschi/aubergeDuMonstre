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
	fic_id = open('pieces.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    pi, nom = l.split()
	    pi = int(pi)
	    piece = tables.Piece(piece_id = pi, name = nom)
	    piece.save()

	#Initialisation capteurs
	fic_id = open('capteurs.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    pi, typeC, ident = l.split()
	    pi = int(pi)
	    ident = int(ident,16)
	    capteur = tables.Capteur(capteur_id = ident, capteur_type = typeC, annee = 0, mois = 0, jour = 0, heure = 0, traite = True)
	    capteur.save()

	    piece = tables.Piece.objects(piece_id = pi).first()
	    if piece == None :
			piece = tables.Piece(piece_id = pi, name = "")
			piece.save()

	    piece.capteurs.append(capteur)
	    piece.save()

	print 'base réinitialisée'

if __name__ == '__main__' :
	initialize()

