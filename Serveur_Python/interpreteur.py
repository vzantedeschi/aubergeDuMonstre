#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trame
import datetime


### plus nécessaire si on lit un fichier
def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

Capteurs = enum('TEMP', 'HUMID', 'RFID', 'PRES','FEN','INTR')

class Interpretation:
  
  def __init__(self, trame):
  
    if(trame.valide):
      self.id = trame.idBytes
      self.date = trame.date
      self.heure = trame.heure
      
      #verification du type du capteur grace a l'id (qd la bdd sera faite)

      #### Peut être fait en utilisant le format de fichier et de lecture du
      #### générateur de trames (fichier contenant le type de capteur)
      
      #self.typeCapteur = Capteurs.PRES #a supprimer plus tard

      fic_id = open("identifiants.txt","r")
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
        self.donnees = not((trame.dataBytes & 0x00000002) >> 1)
"""	
      elif self.typeCapteur == Capteurs.TEMP:
	#recuperation de la temperature
      elif self.typeCapteur == Capteurs.HUMID:
	#recuperation du taux d'humidite
      elif self.typeCapteur == Capteurs.RFID:
	#recuperation des donnees rfid
"""

if __name__ == "__main__" :
    print '#################TESTS UNITAIRES##################'
    
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
      
     