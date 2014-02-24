#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trame
import datetime
import sys
import mongoengine
sys.path.append('../BDD')
import tables


### plus nécessaire si on lit un fichier
def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

Capteurs = enum('TEMP', 'RFID', 'PRES','FEN','INTR')

def interpretation(trame, now):
  idIntrus = 13
  
  while tables.Personne.objects(personne_id=idIntrus).first() != None: 
    idIntrus = idIntrus+1 

  if(trame.valide):
    db_connec = mongoengine.connect('GHome_BDD')

    id = trame.idBytes
    

    # a quelle piece correspond ce capteur v2
    # !!!solution temporaire : il doit y avoir une façon plus propre et directe
    print 'Piece concernee'
    capteur = tables.Capteur.objects(capteur_id = id).first()
    typeCapteur = capteur.capteur_type
    print typeCapteur
    pieces = tables.Piece.objects
    for p in pieces :
      if capteur in p.capteurs :
        print "piece ", p.piece_id, "  : ", p.name
        print "\n"
        break

    piece_id = p.piece_id
    etatPiece = tables.Etat.objects(piece_id = piece_id).first()
    date = now
      
    #stockage des donnes selon le type du capteur
    if typeCapteur == 'PRES':
      #recuperation de DB0.1 donnant la presence
      trame.dataBytes = int (trame.dataBytes, 16)
      #si l'avant dernier bit est a 0 alors c est une presence, si il est a 1 c est une absence
      donnees = not((trame.dataBytes & 0x00000002) >> 1)
      #print (trame.dataBytes)

      if donnees == 1:
      # cela signifie qu'il y a une presence
        if len(etatPiece.persosPresents) == 0:
          newPerso = tables.Personne( personne_id=idIntrus , name ="Intrus", ignore = False)
          newPerso.save()
          etatPiece.persosPresents.append(newPerso)
        capteur_presence = tables.Presence(piece_id = piece_id, date = date, traite = False)
        capteur_presence.save()
        etatPiece.dernierEvenement = date
        etatPiece.dernierMouvement = date
        etatPiece.save()
        
    elif typeCapteur == 'TEMP' :
      # Recuperation de la temperature
      tempBytes = int(trame.dataBytes[4:6], 16)
      humBytes = int(trame.dataBytes[2:4], 16) 
      tempBytes = float(tempBytes)
      humBytes = float(humBytes)
      tempDonnees = ((tempBytes)*40)/250
      humDonnees = ((humBytes)*100)/250
      print ("Temperature : ", tempDonnees)
      print ("Humidite : " , humDonnees)
      capteur_temperature = tables.Temperature(piece_id = piece_id, date = date, traite = False, valeur = tempDonnees)
      capteur_temperature.save()
      capteur_humidite = tables.Humidite(piece_id = piece_id, date = date, traite = False, valeur = humDonnees)
      capteur_humidite.save()
      etatPiece.temperature = tempDonnees
      etatPiece.humidite = humDonnees
      etatPiece.dernierEvenement = date
      etatPiece.save() 

    elif typeCapteur == 'RFID':
        # Recuperation des donnees rfid
        # On fixe que l'octet DB.0 porte l'information de la puce RFID
        perso = int(trame.dataBytes[6:8],16)
        print ("Puce RFID : ", perso)
        capteur_rfid = tables.RFID(piece_id =piece_id, date = now, traite = False, resident_id = perso)
        capteur_rfid.save()
        piecePrecedente = None

        personneEnMouvement = tables.Personne.objects(personne_id=perso).first()
        #on cherche l'ancienne piece du personnage
        for pieceCherchee in tables.Etat.objects:
          for p in pieceCherchee.persosPresents:
            if p.personne_id == perso:
              piecePrecedente = pieceCherchee
              break
            if piecePrecedente != None:
              break
        #quand on le trouve, on l'enlève de la piece
        if piecePrecedente != None:
          piecePrecedente.persosPresents.remove(personneEnMouvement)              
        
        #on met le personnage dans la nouvelle piece
        etatPiece.persosPresents.append(personneEnMouvement)
        etatPiece.dernierEvenement = date
        etatPiece.save()

    elif typeCapteur == 'INTR':
        intrDonnees = int(trame.dataBytes[0:1],16)
        print ("donnees :",intrDonnees)
        if intrDonnees == 5 or intrDonnees == 1:
          capteur_interrupteur = tables.Interrupteur(piece_id = piece_id, date = date, traite = False, ouverte = True)
          etatPiece.interrupteurEnclenche = 1
        elif intrDonnees == 7 or intrDonnees == 3:
          capteur_interrupteur = tables.Interrupteur(piece_id = piece_id, date = date, traite = False, ouverte = False)
          etatPiece.interrupteurEnclenche = -1
        capteur_interrupteur.save()
        etatPiece.dernierEvenement = date
        etatPiece.save()  
        

    elif typeCapteur == 'FEN':
        fenBytes = int(trame.dataBytes[7:8], 16)
        print ("fenBytes : ",fenBytes)
        if fenBytes == 8:
          capteur_fenetre = tables.ContactFen(piece_id = piece_id, date = date, traite = False, ouverte = True)
          etatPiece.voletsOuverts = True
        elif fenBytes == 9:
          capteur_fenetre = tables.ContactFen(piece_id = piece_id, date = date, traite = False, ouverte = False)
          etatPiece.voletsOuverts = False
          
        capteur_fenetre.save()
        
        etatPiece.dernierEvenement = date
        etatPiece.save()  
        

if __name__ == "__main__" :
    print '################# TESTS UNITAIRES ##################'
    initBase.initialize()
    chaine = 'A55A0B07C7FF000D000541550080'
    print chaine
    tr = trame.Trame(chaine)

    interpretation = Interpretation(tr)
    
    if(interpretation.donnees == 1):
      print 'detection d\'une presence'
    else:
      print 'rien detecte'
      
    chaine = 'A55A0B07C7FF000F000541550080'
    print chaine
    tr = trame.Trame(chaine)

    interpretation = Interpretation(tr)
    
    if(interpretation.donnees == 1):
      print 'detection d\'une presence'
    else:
      print 'rien detecte'
      
     
