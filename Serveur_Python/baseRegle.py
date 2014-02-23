#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mongoengine
import time
import pymongo
import sys
import socket
import threading
sys.path.append('../BDD')
import tables


## Variables globales ##
connectProxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# La variable "connected" servira à savoir au cour du programme si on peut
# envoyer des trames aux actionneurs ou si on s'en tient à des affichages écran
# dans le cas où l'on n'a pas accès au réseau GHome
connected = False

# Aucune puce RFID détectée
rfidDetected = 0

hote = '134.214.106.23'
port = 5000
## Functions Server ##
db_connec = mongoengine.connect('GHome_BDD')
db = db_connec.GHome_BDD

def RFIDFunc():
    rfidDetected = 0

def calcCheckSum(trame):
    checksum = 0
    i = 0
    while i < len(trame) :
        c = trame[i:i+2]
        i += 2
        checksum += int(c, 16)

    checksum &= 0xFF
    return hex(checksum)[2:4]

def trameActionneur(actionneurId, activation):
    sync = 'A55A'
    message = '6B0550000000'
    if activation:
        message = '6B0570000000'
    message += format(actionneurId, '08x')
    message += "30"
    checksum = calcCheckSum(message)
    return sync + message + checksum

def activerActionneur(idPiece, idAct):
    actionneurs = piece.actionneurs
    for a in actionneurs : 
        if a.capteur_type == idAct : 
            print "Activation de l'actionneur"
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(actionneurConcerne, True))

def activerActionneur(idAct):
    print "Activation de l'actionneur"
    # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(idAct, True))
        
def activerActionneur_type(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs: 
        if a.capteur_type == typeActionneur: 
            print "Activation de l'actionneur"
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(a.actionneur_id, True))

def desactiverActionneur(idPiece, idAct):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs : 
        if a.capteur_type == idAct : 
            print "Désactivation de l'actionneur"
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(actionneurConcerne, False)) 
                
def desactiverActionneur(idAct):
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(idAct, False))
            
def desactiverActionneur_type(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs:
        if a.capteur_type == typeActionneur:
            print "Desactivation de l'actionneur"
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(a.actionneur_id, False))
                
def ouvrirVolets(idPiece):    
    # Allume la prise simulant les volets
    print "Verrouillage actif : volets en cours d'ouverture"
    activerActionneur_type(idPiece, 'VOL')        

def fermerVolets(idPiece):
    # Eteint la prise simulant les volets
    print "Verrouillage desactive : volets en cours de fermeture"
    desactiverActionneur_type(idPiece, 'VOL')
    
#----------------------------CONDITIONS--------------------------------------------------------------------------------------------------------     
   
def tempInf(valeur) :
    currentTemp = tables.Etat.temperature
    if currentTemp < valeur : 
        return "tempInf" 
    
def ouvrirRideaux(idPiece):
    print "Ouverture des rideaux"
    activerActionneur_type(idPiece, 'RID') 

def fermerRideaux(idPiece):
    print "Fermeture des rideaux"
    desactiverActionneur_type(idPiece, 'RID')

def allumerClim(idPiece):
    print "Allumage de la climatisation"
    activerActionneur_type(idPiece, 'CLIM')

def eteindreClim(idPiece):
    print "Extinction de la climatisation"
    desactiverActionneur_type(idPiece, 'CLIM')

def allumerAnIn(idPiece):
    print "Allumage du systeme anti incendie"
    activerActionneur_type(idPiece, 'ANIN')

def eteindreAnIn(idPiece):
    print "Extinction du systeme anti incendie"
    desactiverActionneur_type(idPiece, 'ANIN')

def commande(item):
    global rfidDetected
    #récupération type de donnée
    typeInfo = item[u'_cls']
    #récupération de l'id de la pièce concernée
    piece_id = item[u'piece_id']
    #récupération état de la pièce concernée
    etat = tables.Etat.objects(piece_id = piece_id).first()
    print("\nEtat de la piece concernée")
    print("Numero :",etat.piece_id)
    print("Rideaux ouverts :",etat.rideauxOuverts)
    print("Systeme anti-incendie declenchee :",etat.antiIncendieDeclenche)
    print("Climatisation activee :",etat.climActivee)
    print("Portes fermees :",etat.portesFermees)
    print("Volets ouverts :",etat.voletsOuverts)
    print("Prise allumee :",etat.priseDeclenchee)
    print("Temperature :",etat.temperature)
    print("Humidite :",etat.humidite)
    print("Personnages presents :",etat.persosPresents)
    print '\n'

    if (typeInfo == "Donnee.Presence"):
        print '\nCommande suivant une presence en cours'

        if rfidDetected == 0 :
            print ("Intrus est dans la piece :",piece_id)

            # Un seul intrus dans la maison en même temps sinon => comment savoir si un
            # intrus qui rentre dans une pièce est un nouveau (générer nouvel id) ou un qui
            # vient de changer de pièce (enlever id de la pièce précédente)

            # Si l'intrus est dans la pièce 1 'Couloir', il n'est plus ignoré

            if piece_id == 1:
                persoAjoute = tables.Personne.objects(nom = "Intrus").first()
                persoAjoute.ignore = False
                persoAjoute.save()

            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.persosPresents.append(persoAjoute)
            etatPiece.save()        

            ## Enlever le perso des autres pieces
            listePieces = tables.Etat.objects
            for p in listePieces :
                if p.piece_id != piece_id:
                    etatAChanger = tables.Etat.objects(piece_id = p.piece_id).first()
                    if persoAjoute in etatAChanger.persosPresents:
                        etatAChanger.persosPresents.remove(persoAjoute)
                        etatAChanger.save()
                            
        elif rfidDetected == 1 :
            print ("Meduse est dans la piece :",piece_id)
            pieceConcernee = tables.Etat.objects(piece_id = piece_id).first()

            persoAjoute = tables.Personne.objects(personne_id = rfidDetected).first()

def tempSup(valeur) : 
    currentTemp = tables.Etat.temperature
    if currentTemp > valeur :
        return "tempSup"
        
def porteOuv() :
    return tables.Etat.portesFermees == False
    
def porteFer() :
    return tables.Etat.portesFermees == True

def vampire():
    trouve = False
    for p in tables.Etat.persosPresents : 
        fic_id = open('../personnages.txt',"r")
        liste = fic_id.readlines()
        fic_id.close()

        for l in liste:
            ident, name = l.split()
            ident = int(ident,16)
            if name == "Vampire" :                            
                if p.personne_id  == ident :
                    trouve = True
                    break                            
        if trouve == True : 
            break
    return trouve                        

def meduse ():
    trouve = False
    for p in tables.Etat.persosPresents : 
        fic_id = open('../personnages.txt',"r")
        liste = fic_id.readlines()
        fic_id.close()

        for l in liste:
            ident, name = l.split()
            ident = int(ident,16)
            if name == "Meduse" :                            
                if p.personne_id  == ident :
                    trouve = True
                    break                            
        if trouve == True : 
            break
    return trouve 
    
def intrus() :
    trouve = False
    for p in tables.Etat.persosPresents : 
        fic_id = open('../personnages.txt',"r")
        liste = fic_id.readlines()
        fic_id.close()

        for l in liste:
            ident, name = l.split()
            ident = int(ident,16)                           
            if p.personne_id  == ident :
                trouve = True
                break                            
        if trouve == True : 
            break
    return trouve == False

def sirene() : 
    trouve = False
    for p in tables.Etat.persosPresents : 
        fic_id = open('../personnages.txt',"r")
        liste = fic_id.readlines()
        fic_id.close()

        for l in liste:
            ident, name = l.split()
            ident = int(ident,16)
            if name == "Sirene" :                            
                if p.personne_id  == ident :
                    trouve = True
                    break                            
        if trouve == True : 
            break
    return trouve 

def invite() : 
    trouve = False
    for p in tables.Etat.persosPresents : 
        fic_id = open('../personnages.txt',"r")
        liste = fic_id.readlines()
        fic_id.close()

        for l in liste:
            ident, name = l.split()
            ident = int(ident,16)
            if name == "Invite" :                            
                if p.personne_id  == ident :
                    trouve = True
                    break                            
        if trouve == True : 
            break
    return trouve 

def fenOuv() : 
    return tables.Etat.voletsOuverts == True

def fenFer() : 
    return tables.Etat.voletsOuverts == False

def humInf(valeur) : 
    currentHum = tables.Etat.humidite
    if currentHum < valeur :
        return "humInf"

def humSup(valeur) : 
    currentHum = tables.Etat.humidite
    if currentHum > valeur :
        return "humSup"

def pasChange() : 
    pass

def mouv() : 
    pass

def lumEt() :
    return tables.Etat.lumiereAllumee == False

def lumAll() :
    return tables.Etat.lumiereAllumee == True

def pasBouge() : 
    pass

#Les id des pieces sont-ils dans pieces.txt ou dans nom_piece.txt, les deux fichiers ne correspondent pas.
def dansCuisine() :
    if piece.name == "Cuisine" :                                               
        return True
    return False
    
def dansChambre() : 
    if piece.name == "Chambre" :                            
        return True
    return False

def dansSalon() : 
    if piece.name == "Salon" :                            
        return True
    return False 

def dansCouloir(): 
    if piece.name == "Couloir" :                            
        return True
    return False
    
def dansBain() : 
    if piece.name == "Bain" :                            
        return True
    return False
    
def dansPiece() : 
    if piece.name == valeur :                            
        return True
    return False
    
def climAll() :
    return tables.Etat.climActivee == True

def climEt() :
    return tables.Etat.climActivee == False

def eauAll() : 
    return tables.Etat.antiIncendieDeclenche == True

def eauEt() : 
    return tables.Etat.antiIncendieDeclenche == False

def intAll() : 
    return tables.Etat.priseDeclenchee == True

def intEt() :
    return tables.Etat.priseDeclenchee == False

def repNon() : 
    pass

def repOui() :
    pass
    #penser à mettre en "prises en compte" les variables utilisées pour trouver les règles

#-----------------------------FIN CONDITIONS--------------------------------------------------------------------------------------------------------
#----------------------------FONCTIONNALITES--------------------------------------------------------------------------------------------------------

def eteintClim():
    if connected == True :
        #envoi de la trame 
        print "Desactivation de la climatisation"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "climActive" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.climActivee = False
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1

def allumeClim():        
    if connected == True :
        #envoi de la trame
        print "Activation de la climatisation"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "climActive" à True
        #change = True
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : change} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.climActivee = True
        etatPiece.save()
        return 0 
    elif connected ==False :    
        return 1
 
def ouvreVolet():
    if connected == True :
        print "ouverture des volets"
        ouvrirVolets(piece_id)
        #Mettre à jour l'état de la pièce dans la BDD
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.voletsOuverts = True
        etatPiece.save()
        return 0
    elif connected ==False :    
        return 1

def fermeVolet():
        if connected == True :
            print "Fermeture des volets"
            fermerVolets(piece_id)
            #Mettre à jour l'état de la mpièce dans la BDD
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.voletsOuverts = False
            etatPiece.save()
            return 0
        elif connected ==False :   
            return 1 

def allumeEau(): 
    #pas d'envoi de trame pour l'instant
    if connected ==True :
        print "Activation du systeme anti-incendie"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à True
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : True} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.antiIncendieDeclenche = True
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1        

def eteintEau(): 
    if connected == True :    
        print "Desactivation du systeme anti-incendie"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.antiIncendieDeclenche = False
        etatPiece.save()
        return 0 
    elif connected ==False :   
        return 1 

def allumeLum():
    if connected == True :    
        print "Allumer la lumière"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.lumiereAllumee = True
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1

def eteintLum():
    if connected == True :    
        print "Éteindre la lumière"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.lumiereAllumee = False
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1
        
def allumeInt():
    if connected == True :    
        print "Allumer la prise"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.priseDeclenchee = True
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1
        
def eteintInt():
    if connected == True :    
        print "Éteindre la prise"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.priseDeclenchee =False
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1
        
def fermePiece():
    pass
    #fermeture porte ou fermeture portes fenetres?
    
def ouvrePiece():
    pass
    
def question():
    pass

def fermeRideau():
    if connected == True :    
        print "Fermer le rideau"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.rideauxOuverts = False
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1
        
def ouvreRideau(): 
    if connected == True :    
        print "Ouvrir le rideau"
        activerActionneur(idPiece, capteur_id)
        # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.rideauxOuverts = True
        etatPiece.save()
        return 0
    elif connected ==False :   
        return 1
        
def notifierRes():
    pass 

#----------------------------FIN FONCTIONNALITES--------------------------------------------------------------------------------------------------------

def commande():
    print "appel de la base de regle"
    global rfidDetected
    #pour chaque piece de la base
    for piece in tables.Piece.objects:
        piece_id = piece.piece_id
        #récupération état de la pièce concernée
        etat = tables.Etat.objects(piece_id = piece.piece_id).first()
        # print("\nEtat de la piece concernée")
        # print("Numero :",etat.piece_id)
        # print("Rideaux ouverts :",etat.rideauxOuverts)
        # print("Systeme anti-incendie declenchee :",etat.antiIncendieDeclenche)
        # print("Climatisation activee :",etat.climActivee)
        # print("Portes fermees :",etat.portesFermees)
        # print("Volets ouverts :",etat.voletsOuverts)
        # print("Prise allumee :",etat.priseDeclenchee)
        # print("Temperature :",etat.temperature)
        # print("Humidite :",etat.humidite)
        # print("Personnages presents :",etat.persosPresents)
        #a ajouter : dernier changement en date
        #               interrupteur (changements jusqu a la base)
        #               reponse utilisateur eventuelle
        
        print '\n'

        # ------partie deplacer les personnages dans les donnees -------------------------------
 
        # ------fin partie deplacer les personnages dans les donnees -------------------------------   
        # ------partie recherche des regles ---------------------------------------------
        #récupération des regles de la base de donnees
        regles = tables.Regle.objects
        reglesRemplies = []
        #on applique la premiere regle qui marche ***********
        #uneQuiMarche = False
        #i = 0
        #while uneQuiMarche == False and i < len(regles):
        # fin on applique la premiere regle qui marche ***********
        #on applique toutes les regles qui marchent ***********
        for r in regles:
            conditionsRemplies = True
            i=0
            #on vérifie si la regle r remplit les conditions
            while conditionsRemplies == True and i < len(r.conditions) :
                    
                switchCondition = {"tempInf" : tempInf,
                                   "tempSup" : tempSup,
                                   "porteOuv" : porteOuv,
                                   "porteFer"  : porteFer,
                                   "vampire" : vampire,
                                   "meduse" : meduse,
                                   "intrus" : intrus,
                                   "sirene" : sirene,
                                   "invite" : invite,
                                   "fenOuv" : fenOuv,
                                   "fenFer" : fenFer,
                                   "humInf" : humInf,
                                   "humSup" : humSup,
                                   "pasChange" : pasChange,
                                   "mouv" : mouv,
                                   "lumEt" : lumEt,
                                   "lumAll" : lumAll,
                                   "pasBouge" : pasBouge,
                                   "dansCuisine" : dansCuisine,
                                   "dansChambre" : dansChambre,
                                   "dansSalon" : dansSalon,
                                   "dansCouloir" : dansCouloir,
                                   "dansBain" : dansBain,
                                   "dansPiece" : dansPiece,
                                   "climAll" : climAll,
                                   "climEt" : climEt,
                                   "eauAll" : eauAll,
                                   "eauEt" : eauEt,
                                   "intAll" : intAll,
                                   "intEt" : intEt,
                                   "repNon" : repNon,
                                   "repOui" : repOui}
                                   
                nomCondition = r.conditions[i].nom
                valeurCondition = r.conditions[i].valeur
                
                if valeurCondition != None: 
                    conditionsRemplies = switchCondition[nomCondition](valeurCondition)
                else :
                    conditionsRemplies = switchCondition[nomCondition]()
                
                i = i + 1
            
            #si r verifie les conditions on l ajoute a la liste des regles a appliquer
            if conditionsRemplies : 
                reglesRemplies.append(r)
            
                    
        
        # fin on applique toutes les regles qui marchent ***********
            
        # ------fin partie recherche des regles ---------------------------------------------
        # ------partie execution des regles trouvees -----------------------------------
        for r in reglesRemplies :
            enFonctionnement = 0
            i =0
            while enFonctionnement==0 and i < len(r.actions) :
            
                act = r.actions[i].nom
                baseregle = {"allumeClim" : allumeClim,
                             "eteintClim" : eteintClim,
                             "ouvreVolet" : ouvreVolet,
                             "fermeVolet" : fermeVolet, 
                             "allumeLum" : allumeLum, 
                             "eteintLum" : eteintLum,
                             "allumeInt" : allumeInt,
                             "eteintInt" : eteintInt,
                             "fermePiece" : fermePiece, 
                             "ouvrePiece" : ouvrePiece,
                             "question" : question, 
                             "allumeEau" : allumeEau, 
                             "eteintEau" : eteintEau, 
                             "fermeRideau" : fermeRideau, 
                             "ouvreRideau" : ouvreRideau,
                             "notifierRes" : notifierRes
                             }
                enFonctionnement = baseregle[act]()
                i = i + 1
        
    # ------fin partie execution des regles trouvees -----------------------------------

### ESSAI INTEGRATION ENVOIS DE L'APPLI WEB ########
    # if(typeInfo == "Donnee.DonneeAppli"):
        ##Recherche des actionneurs de la piece du type demande
        # capteurType = item[u'actionneur_id']
        # actionType = item[u'action_type']      
        # if actionType:
            # activerActionneur(actionneur_id)
        # else:
            # desactiverActionneur(actionneur_id)

    # elif(typeInfo == "Donnee.ReponseAppli"):
        # reponse = item[u'reponse']
        # if reponse:
            # fermerVolets(piece_id)


### FIN ESSAI INTEGRATION ENVOIS DE L'APPLI WEB ####


    # else:
        # print '\nPas de commande implementee'
        
    # if (item != None):
        ## Modifier l'information de la BDD pour mettre "traite" à True            
        # db.donnee.update({"_id" : item[u'_id']},{ "$set": {u'traite' : True} },upsert=False,multi=True)
      
# try :
    # print 'Attente connexion au proxy'
    # connectProxy.connect((hote, port))
    # print("Connexion établie avec la passerelle sur le port {}".format(port))
    # connected = True
# except socket.error :
    # print("Impossible de se connecter au proxy : Les trames d'actionneurs ne seront pas envoyees")

# while True :
    # try :
        ## Permet d'examiner les informations nouvelles dans la BDD
        # liste = db.donnee.find({u'traite':False}).sort("_id", 1)
        # for item in liste:
            # print "\n"
            # print item
            # commande(item)
        # else :
            ##s'il n'y a pas de données à traiter
            # print 'Aucune nouvelle donnee'
            # time.sleep(2)
    # except KeyboardInterrupt:
        # break
