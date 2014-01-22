import trame
import datetime

def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

Capteurs = enum('TEMP', 'HUMID', 'RFID', 'PRES')

class Interpretation:
  
  def __init__(self, trame):
  
    if(trame.valide):
      self.id = trame.idBytes
      self.date = trame.date
      self.heure = trame.heure
      
      #verification du type du capteur grace a l'id (qd la bdd sera faite)
      self.typeCapteur = Capteurs.PRES #a supprimer plus tard
      
      #stockage des donnes selon le type du capteur
      if self.typeCapteur == Capteurs.PRES:
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
      
     