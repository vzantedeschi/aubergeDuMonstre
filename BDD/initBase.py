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
        
    #Initialisation conditions
	fic_id = open('../conditions.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    c_nom, desc = l.split('\t')
	    cond = tables.Condition(nom =c_nom, description = desc)
	    cond.save()
        
    #Initialisation actions
	fic_id = open('../actions.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    a_nom, desc = l.split('\t')
	    act = tables.Action(nom =a_nom, description = desc)
	    act.save()
        
    #Initialisation regles
	fic_id = open('../regles.txt',"r")
	liste = fic_id.readlines()
	fic_id.close()

	for l in liste:
	    id, nom, conds, acts= l.split(';', 3)
        
        l_cond = conds.split('\t', conds.count('\t'))
        pb = False
        if pb == False :
            r_conds = [] 
            for elem in l_cond:
                obj =tables.Condition.objects(nom = elem).first()
                if obj == None :
                    pb = True
                    break
                else :
                    r_conds.append(obj)
                    
            l_act = acts.split('\t', acts.count('\t'))
            
        if pb == False :
            #ajoute les conditions de la regle
            r_acts = [] 
            for elem in l_act:
                obj =tables.Action.objects(nom = elem).first()
                if obj == None :
                    pb = True
                    break
                else :
                    r_acts.append(obj)
 
        if pb == False :
            #ajoute les actions de la regle
            regle = tables.Regle( regle_id= id, nom = nom, conditions = r_conds, actions = r_acts)
            regle.save()

        
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
	    personnage = tables.Personne(personne_id=ident, nom=name)
	    personnage.save()

	####### Création d'un superutilisateur pour le paramétrage des règles #######
	admin = tables.Utilisateur(identifiant='administrateur',mot_de_passe='123456')
	admin.save()
	print 'base reinitialisee'

if __name__ == '__main__' :
	initialize()
	import random
	##### Ajout intrus dans le couloir ######
	piece = tables.Piece.objects(name="Couloir").first()
	etat = tables.Etat.objects(piece_id=piece.piece_id).first()
	id = random.randint(10, 100)
	intrus = tables.Personne(personne_id=id,ignore=False)
	intrus.save()
	etat.persosPresents.append(intrus)
	etat.save()
	print "ça y est : " + intrus.nom + " est dans le couloir"
