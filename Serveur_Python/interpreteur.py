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
  
  if(trame.valide):
    db_connec = mongoengine.connect('GHome_BDD')

    id = trame.idBytes

    # a quelle piece correspond ce capteur v2
    # !!!solution temporaire : il doit y avoir une façon plus propre et directe
    print 'Piece concernee'
    capteur = tables.Capteur.objects(capteur_id = id).first()
    typeCapteur = capteur.capteur_type
    pieces = tables.Piece.objects
    for p in pieces :
      if capteur in p.capteurs :
        print "piece ", p.piece_id, "  : ", p.name
        print "\n"
        break

    piece_id = p.piece_id
      
    #stockage des donnes selon le type du capteur
    if typeCapteur == 'PRES':
      #recuperation de DB0.1 donnant la presence
      trame.dataBytes = int (trame.dataBytes, 16)
      #si l'avant dernier bit est a 0 alors c est une presence, si il est a 1 c est une absence
      donnees = not((trame.dataBytes & 0x00000002) >> 1)
      #print (trame.dataBytes)

      if donnees == 1:
        capteur_presence = tables.Presence(piece_id = piece_id, date = now, traite = False)
        capteur_presence.save()
        
    elif typeCapteur == 'TEMP':
      # Recuperation de la temperature
      tempBytes = int(trame.dataBytes[4:6], 16)
      humBytes = int(trame.dataBytes[2:4], 16) 
      tempBytes = float(tempBytes)
      humBytes = float(humBytes)
      tempDonnees = ((tempBytes)*40)/250
      humDonnees = ((humBytes)*100)/250
      print ("Temperature : ", tempDonnees)
      print ("Humidite : " , humDonnees)

      capteur_temperature = tables.Temperature(piece_id = piece_id, date = now, traite = False, valeur = tempDonnees)
      capteur_temperature.save()
      capteur_humidite = tables.Humidite(piece_id = piece_id, date = now, traite = False, valeur = humDonnees)
      capteur_humidite.save()
        
    elif typeCapteur == 'RFID':
        # Recuperation des donnees rfid
        # On fixe que l'octet DB.0 porte l'information de la puce RFID
        perso = int(trame.dataBytes[6:8],16)
        print ("Puce RFID : ", perso)

        capteur_rfid = tables.RFID(piece_id =piece_id, date = now, traite = False, resident_id = perso)
        capteur_rfid.save()

    elif typeCapteur == 'INTR':
        capteur_interrupteur = tables.Interrupteur(piece_id = piece_id, date = now, traite = False)
        capteur_interrupteur.save()

    elif typeCapteur == 'FEN':
        fenBytes = int(trame.dataBytes[7:8], 16)
        print ("fenBytes : ",fenBytes)
        if fenBytes == 8:
          capteur_fenetre = tables.ContactFen(piece_id = piece_id, date = now, traite = False, ouverte = True)
        elif fenBytes == 9:
          capteur_fenetre = tables.ContactFen(piece_id = piece_id, date = now, traite = False, ouverte = False)
          
        capteur_fenetre.save()

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
      
     
