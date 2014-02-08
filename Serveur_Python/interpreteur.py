#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trame
import datetime


### plus nécessaire si on lit un fichier
def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

Capteurs = enum('TEMP', 'RFID', 'PRES','FEN','INTR')

class Interpretation:
  
  def __init__(self, trame):
  
    if(trame.valide):
      self.id = trame.idBytes
      self.annee = trame.date.year
      self.mois = trame.date.month
      self.jour = trame.date.day
      self.heure = trame.heure.hour*3600 + trame.heure.minute*60 + trame.heure.second

      #verification du type du capteur grace a l'id
      fic_id = open("../identifiants.txt","r")
	  
      liste = fic_id.readlines()
        
      fic_id.close()
      for capt in liste:
          type, id = capt.split()
          if self.id == int(id,16):
              self.typeCapteur = type
              print self.typeCapteur
      
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
    
    date = datetime.datetime(2014, 1, 12, 18, 59, 30)
    chaine = 'A55A0B07C7FF000D000541550080'
    print chaine
    tr = trame.Trame(chaine, date)

    interpretation = Interpretation(tr)
    
    if(interpretation.donnees == 1):
      print 'detection d\'une presence'
    else:
      print 'rien detecte'
      
    chaine = 'A55A0B07C7FF000F000541550080'
    print chaine
    tr = trame.Trame(chaine, date)

    interpretation = Interpretation(tr)
    
    if(interpretation.donnees == 1):
      print 'detection d\'une presence'
    else:
      print 'rien detecte'
      
     
