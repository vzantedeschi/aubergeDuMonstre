#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trame
import datetime
import sys
import mongoengine
sys.path.append('../BDD')
import tables
import initBase

### plus nécessaire si on lit un fichier
def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

Capteurs = enum('TEMP', 'RFID', 'PRES','FEN','INTR')

class Interpretation:
  
  def __init__(self, trame):
  
    if(trame.valide):
      db_connec = mongoengine.connect('GHome_BDD')

      self.id = trame.idBytes

      # a quelle piece correspond ce capteur v2
      # !!!solution temporaire : il doit y avoir une façon plus propre et directe
      print 'Pièce concernée'
      capteur = tables.Capteur.objects(capteur_id = self.id).first()
      self.typeCapteur = capteur.capteur_type
      pieces = tables.Piece.objects
      for p in pieces :
        if capteur in p.capteurs :
            print "piece ", p.piece_id, "  : ", p.name

      self.piece_id = p.piece_id
      
      #stockage des donnes selon le type du capteur
      if self.typeCapteur == 'PRES':
        #recuperation de DB0.1 donnant la presence
        trame.dataBytes = int (trame.dataBytes, 16)
        #si l avant dernier bit est a 0 alors c est une presence, si il est a 1 c est une absence
        self.donnees = not((trame.dataBytes & 0x00000002) >> 1)
        #print (trame.dataBytes)
        
      elif self.typeCapteur == 'TEMP':
        # Recuperation de la temperature
        tempBytes = int(trame.dataBytes[4:6], 16) 
        humBytes = int(trame.dataBytes[2:4], 16) 
        tempBytes = float(tempBytes)
        humBytes = float(humBytes)
        self.tempDonnees = ((tempBytes)*40)/250
        self.humDonnees = ((humBytes)*100)/250
        print ("Temperature : ", self.tempDonnees)
        print ("Humidite : " , self.humDonnees)
        
      elif self.typeCapteur == 'RFID':
          # Recuperation des donnees rfid
          # On fixe que l'octet DB.0 porte l'information de la puce RFID
          self.perso = int(trame.dataBytes[6:8],16)
          print ("Puce RFID : ", self.perso)
          

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
      
     
