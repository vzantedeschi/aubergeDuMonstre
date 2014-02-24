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
import datetime


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

# try :
    # print 'Attente connexion au proxy'
    # connectProxy.connect((hote, port))
    # print("Connexion établie avec la passerelle sur le port {}".format(port))
    # connected = True
# except socket.error :
    # print("Impossible de se connecter au proxy : Les trames d'actionneurs ne seront pas envoyees")
    # connected = False

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

# def activerActionneur(idPiece, idAct):
#     actionneurs = piece.actionneurs
#     for a in actionneurs : 
#         if a.capteur_type == idAct : 
#             print "----Activation de l'actionneur"
#             # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
#             if connected == True :
#                 print "Envoi au proxy"
#                 connectProxy.send(trameActionneur(actionneurConcerne, True))

def activerActionneur(idAct):
    print "----Activation de l'actionneur"
    # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(idAct, True))
        
def activerActionneur_type(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs: 
        if a.capteur_type == typeActionneur: 
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(a.actionneur_id, True))

# def desactiverActionneur(idPiece, idAct):
#     actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
#     for a in actionneurs : 
#         if a.capteur_type == idAct : 
#             print "----Désactivation de l'actionneur"
#             # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
#             if connected == True :
#                 print "Envoi au proxy"
#                 connectProxy.send(trameActionneur(actionneurConcerne, False)) 
                
def desactiverActionneur(idAct):
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(idAct, False))
            
def desactiverActionneur_type(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece).first().actionneurs
    for a in actionneurs:
        if a.capteur_type == typeActionneur:
            # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
            if connected == True :
                print "Envoi au proxy"
                connectProxy.send(trameActionneur(a.actionneur_id, False))
                
def ouvrirVolets(idPiece):    
    # Allume la prise simulant les volets
    print "*****Verrouillage desactive : volets en cours d'ouverture"
    activerActionneur_type(idPiece, 'VOL')   

def fermerVolets(idPiece):
    # Eteint la prise simulant les volets
    print "*****Verrouillage active : volets en cours de fermeture"
    desactiverActionneur_type(idPiece, 'VOL')
    
def ouvrirPiece(idPiece):    
    # Allume la prise simulant les portes
    print "*****Verrouillage actif : portes en cours d'ouverture"
    activerActionneur_type(idPiece, 'PORTE') 

def fermerPiece(idPiece):
    # Eteint la prise simulant les portes
    print "*****Verrouillage desactive : portes en cours de fermeture"
    desactiverActionneur_type(idPiece, 'PORTE')    
        
def ouvrirRideaux(idPiece):
    print "*****Ouverture des rideaux"
    activerActionneur_type(idPiece, 'RID') 

def fermerRideaux(idPiece):
    print "*****Fermeture des rideaux"
    desactiverActionneur_type(idPiece, 'RID')

def allumerClim(idPiece):
    print "******Allumage de la climatisation"
    activerActionneur_type(idPiece, 'CLIM')

def eteindreClim(idPiece):
    print "******Extinction de la climatisation"
    desactiverActionneur_type(idPiece, 'CLIM')

def allumerAnIn(idPiece):
    print "******Allumage du systeme anti incendie"
    activerActionneur_type(idPiece, 'ANIN')

def eteindreAnIn(idPiece):
    print "******Extinction du systeme anti incendie"
    desactiverActionneur_type(idPiece, 'ANIN')
    
def allumerLum(idPiece):
    print "******Allumage de la lumiere"
    activerActionneur_type(idPiece, 'LUM')

def eteindreLum(idPiece):
    print "*****Extinction de la lumiere"
    desactiverActionneur_type(idPiece, 'LUM')
    
def allumerPrise(idPiece):
    print "******Allumage de la lumiere"
    activerActionneur_type(idPiece, 'PRISE')

def eteindrePrise(idPiece):
    print "******Extinction de la lumiere"
    desactiverActionneur_type(idPiece, 'PRISE')

#----------------------------CONDITIONS--------------------------------------------------------------------------------------------------------     
   
def tempInf(valeur) :
    currentTemp = etat.temperature
    return currentTemp < valeur
    
def tempSup(valeur) : 
    currentTemp = etat.temperature
    return currentTemp > valeur
        
def porteOuv() :
    return etat.portesFermees == False
    
def porteFer() :
    return etat.portesFermees == True

def vampire():
    trouve = False
    for p in etat.persosPresents : 
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
    for p in etat.persosPresents : 
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

    if len(etat.persosPresents ) == 0:
        #s il n y a personne dans la piece il n y a pas d intrus
        return False
        
    trouve = False
    for p in etat.persosPresents : 
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
        
    if tables.Personne.objects(nom="Intrus").first().ignore == True:
        trouve = True
    
    return trouve == False

def sirene() : 
    trouve = False
    for p in etat.persosPresents : 
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
    for p in etat.persosPresents : 
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
    return etat.voletsOuverts == True

def fenFer() : 
    return etat.voletsOuverts == False

def humInf(valeur) : 
    currentHum = etat.humidite
    return currentHum < valeur

def humSup(valeur) : 
    currentHum = etat.humidite
    return currentHum > valeur 

def pasChange(valeur) : 
    return (now - etat.dernierEvenement).total_seconds() > valeur

def mouv() : 
    return (now - etat.dernierMouvement).total_seconds() < 2

def lumEt() :
    return etat.lumiereAllumee == False

def lumAll() :
    return etat.lumiereAllumee == True

def pasBouge(valeur) : 
    return (now - etat.dernierMouvement).total_seconds() > valeur

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
    return etat.climActivee == True

def climEt() :
    return etat.climActivee == False

def eauAll() : 
    return etat.antiIncendieDeclenche == True

def eauEt() : 
    return etat.antiIncendieDeclenche == False

def intAll() : 
    return etat.interrupteurEnclenche == 1

def intEt() :
    return etat.interrupteurEnclenche == -1

def repNon() : 
    pass

def repOui() :
    pass
    #penser à mettre en "prises en compte" les variables utilisées pour trouver les règles


#-----------------------------FIN CONDITIONS--------------------------------------------------------------------------------------------------------
#----------------------------FONCTIONNALITES--------------------------------------------------------------------------------------------------------

def eteintClim():
    eteindreClim(piece_id)
    etat.climActivee = False
    etat.save()
    return 0

def allumeClim(): 
    allumerClim(piece_id)
    etat.climActivee = True
    etat.save()
    return 0 

 
def ouvreVolet():
    ouvrirVolets(piece_id)
    etat.voletsOuverts = True
    etat.save()
    return 0

def fermeVolet():
    fermerVolets(piece_id)
    etat.voletsOuverts = False
    etat.save()
    return 0

def allumeEau(): 
    allumerAnIn(piece_id)
    etat.antiIncendieDeclenche = True
    etat.save()
    return 0
   

def eteintEau():    
    eteindreAnIn(piece_id)
    etat.antiIncendieDeclenche = False
    etat.save()
    return 0 

def allumeLum():  
    allumerLum(piece_id)
    etat.lumiereAllumee = True
    etat.save()
    return 0

def eteintLum(): 
    eteindreLum(piece_id)
    etat.lumiereAllumee = False
    etat.save()
    return 0
        
def allumeInt():      
    allumerPrise(piece_id)
    etat.priseDeclenchee = True
    etat.save()
    return 0
        
def eteintInt():   
    eteindrePrise(piece_id)
    etat.priseDeclenchee =False
    etat.save()
    return 0
        
def fermePiece():
    fermerPiece(piece_id)
    etat.portesFermees = True
    etat.save()

    
def ouvrePiece():
    ouvrirPiece(piece_id)
    etat.portesFermees =False
    etat.save()
    
def question():
    print "Question a faire"

def fermeRideau(): 
    fermerRideaux(piece_id)
    etat.rideauxOuverts = False
    etat.save()
    return 0
        
def ouvreRideau():   
    ouvrirRideaux(piece_id)
    etat.rideauxOuverts = True
    etat.save()
    return 0
        
#----------------------------FIN FONCTIONNALITES--------------------------------------------------------------------------------------------------------
def realisationDemandeAction(actionneurType, actionType):
    if actionType:
        if actionneurType == 'VOL':
            ouvreRideau()
        elif actionneurType == 'CLIM':
            allumeClim()
        elif actionneurType == 'ANIN':
            allumeEau()
        elif actionneurType == 'RID':
            ouvreRideau()
        elif actionneurType == 'LUM':
            allumeLum()
        elif actionneurType == 'PORTE':
            ouvrePiece()
    else:
        if actionneurType == 'VOL':
            fermeRideau()
        elif actionneurType == 'CLIM':
            eteintClim()
        elif actionneurType == 'ANIN':
            eteintEau()
        elif actionneurType == 'RID':
            fermeRideau()
        elif actionneurType == 'LUM':
            eteintLum()
        elif actionneurType == 'PORTE':
            fermePiece()

def commande():
    global rfidDetected
    global piece
    global piece_id
    global etat
    global now

#### INTEGRATION ENVOIS DE L'APPLI WEB ########

    for item in tables.DonneeAppli.objects(traite=False):
        #Recherche des actionneurs de la piece du type demande
        piece_id = item.piece_id
        actionType = item.action_type
        actionneurConcerne = tables.Actionneur.objects(actionneur_id=item.actionneur_id).first()
        realisationDemandeAction(actionneurConcerne.capteur_type, actionType)
        item.traite=True
        item.save()  

    for item in tables.ReponseAppli.objects(traite=False):
        piece_id = item.piece_id
        reponse = item.reponse
        if reponse:
            fermerVolets(piece_id)

        item.traite=True
        item.save()   

    for item in tables.DemandeAppareillage.objects(traite=False):
        ident = item.ident
        type = item.type
        piece = tables.Piece.objects(piece_id = piece_id).first()
        if item.creer :
            print 'création dispositif'
            if item.dispositif == 'Capteur':
                dispo = tables.Capteur(capteur_id = ident, capteur_type = type)
                dispo.save()
                piece.capteurs.append(dispo)
                piece.save()
            elif item.dispositif == 'Actionneur':
                dispo = tables.Actionneur(actionneur_id = ident, capteur_type = type)
                dispo.save()
                piece.actionneurs.append(dispo)
                piece.save()
        else :
            print 'suppression dispositif'
            if item.dispositif == 'Capteur':
                dispo = tables.Capteur.objects.get(capteur_id = ident)
                dispo.delete()
            elif item.dispositif == 'Actionneur':
                dispo = tables.Actionneur.objects.get(actionneur_id = ident)
                dispo.delete()

        item.traite=True
        item.save()

#### FIN INTEGRATION ENVOIS DE L'APPLI WEB ####

    #pour chaque piece de la base
    for piece in tables.Piece.objects:
        piece_id = piece.piece_id
        #récupération état de la pièce concernée
        etat = tables.Etat.objects(piece_id = piece.piece_id).first()
        # print("Etat de la piece concernée")
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
        now = datetime.datetime.now()
        
        

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
            if conditionsRemplies == True : 
                print "regle trouvee : " + r.nom
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
                             }
                enFonctionnement = baseregle[act]()

                i = i + 1
