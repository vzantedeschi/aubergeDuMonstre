#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
import sys
import tables
import datetime

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
        etat = tables.Etat(piece_id = piece.piece_id,
                            rideauxOuverts = True,
                            antiIncendieDeclenche = False,
                            climActivee = False,
                            portesFermees = False,
                            voletsOuverts = True,
                            priseDeclenchee = False,
                            lumiereAllumee = False,
                            temperature = 19,
                            humidite =71,
                            dernierEvenement = datetime.datetime.now(),
                            dernierMouvement = datetime.datetime.now(),  
                            interrupteurEnclenche = 0,
                            persosPresents = [])
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
        c_nom, desc = l.split(',')
        listeConditions = c_nom.split()
        if len(listeConditions) > 1 :
            condition = listeConditions[0]
            valeur = listeConditions[1]
        else :
            condition = c_nom
            valeur = None
            
        cond = tables.ConditionGenerique(nom = condition, valeur=valeur, description = desc)
        cond.save()
        
    #Initialisation actions
    fic_id = open('../actions.txt',"r")
    liste = fic_id.readlines()
    fic_id.close()

    for l in liste:
        a_nom, desc = l.split(',')
        act = tables.ActionGenerique(nom =a_nom, description = desc)
        act.save()
        
    #Initialisation regles
    fic_id = open('../regles.txt',"r")
    liste = fic_id.readlines()
    fic_id.close()
    taille = len(liste)
    for l in liste:
        id, nom, conds, acts, rebut = l.split(';')
        l_cond = conds.split(',', conds.count(','))
        pb = False
        if pb == False :
            r_conds = [] 
            for elem in l_cond :
                listeConditions = elem.split()
                if len(listeConditions) > 1 :
                    condition = listeConditions[0]
                    valeur = listeConditions[1]
                else :
                    condition = elem
                    valeur = None
                
                obj = tables.Condition.objects(nom = condition).first()
                if obj == None :
                    print 'condition ' + elem +' ne correspond a rien'
                    pb = True
                    break
                else :
                    if valeur != None:
                        newCond = tables.Condition(nom= condition, valeur=valeur, description = cond.description)
                    else:
                        newCond = tables.Condition(nom= condition, description = cond.description)
                    r_conds.append(newCond)
                    
            l_act = acts.split(',', acts.count(','))
            
        if pb == False :
            #ajoute les conditions de la regle
            r_acts = [] 
            for elem in l_act:
            
                listeActions = elem.split()
                if len(listeActions) > 1 :
                    action = listeActions[0]
                    valeur = listeActions[1]
                else :
                    action = elem
                obj =tables.Action.objects(nom = action).first()  
                if obj == None :
                    print 'action ' + elem +' ne correspond a rien'
                    pb = True
                    break
                else :
                    r_acts.append(obj)
        if pb == False :
            #ajoute les actions de la regle
            for cond in r_conds:
                cond.save()
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
            etat = tables.Etat(piece_id = pi, 
                                rideauxOuverts = True,
                                antiIncendieDeclenche = False,
                                climActivee = False,
                                portesFermees = False,
                                voletsOuverts = False,
                                priseDeclenchee = False,
                                lumiereAllumee = False,
                                temperature = 19,
                                humidite =71,
                                dernierEvenement = datetime.datetime.now(),
                                dernierMouvement = datetime.datetime.now(),
                                interrupteurEnclenche = 0,
                                persosPresents = [])
            etat.save()

        piece.actionneurs.append(actionneur)
        piece.save()

    #Initialisation des personnages et des utilisateurs
    fic_id = open('../personnages.txt',"r")
    liste = fic_id.readlines()
    fic_id.close()

    for l in liste:
        ident, name = l.split()
        ident = int(ident,16)
        print ident
        personnage = tables.Personne(personne_id=ident, nom=name)
        personnage.save()
        user = tables.Utilisateur(identifiant=name, secret_hash='IFODJI2973', salt='2')
        user.save()

    # Création d'un type intrus dans la base des personnages
    personnage = tables.Personne(personne_id = 0, nom = "Intrus", ignore = False)
    personnage.save()

    ####### Création d'un superutilisateur #######
    admin = tables.Utilisateur(identifiant='administrateur',secret_hash='IFODJI2973', salt='2')
    admin.save()

    print 'base reinitialisee'

if __name__ == '__main__' :
    initialize()
    import random
    ##### Ajout intrus dans le couloir ######
    #piece = tables.Piece.objects(name="Couloir").first()
    #etat = tables.Etat.objects(piece_id=piece.piece_id).first()
    #id = random.randint(10, 100)
    #intrus = tables.Personne(personne_id=id,ignore=False)
    #intrus.save()
    #etat.persosPresents.append(intrus)
    #etat.save()
    #print "ça y est : " + intrus.nom + " est dans le couloir"
