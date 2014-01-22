import datetime
SIZE = 28

class Trame:
    """Classe contenant les informations d'une trame 
    Parsage effectue dans le constructeur.
    
    Attributs :
        - syncBytes (int)
        - hSeq (int)
        - length (int)
        - org (int)
        - dataBytes (int) dans le bon ordre
        - idBytes (int) changement (avant de type string) !!!
        - status (int)
        - checksum (int)
        - teachIn (bool) vrai si EEP envoye
        - valide (bool) vrai si la trame est composee de 28 caracteres hexadecimaux
        - date (datetime.date)
        - heure (datetime.time)

        Si la trame n'est pas valide, tous les attributs valent None sauf valide (False)
        
    """
    def __init__(self, trame, temps):
        self.teachIn = False
        self.valide = True
             
        if (trame != None) and (len(trame) == SIZE):    
            #recuperation des donnees
            try:
                self.syncBytes = int(trame[0:4], 16)
                hSeqAndLength = int(trame[4:6], 16)
                self.hSeq = (hSeqAndLength >> 5)
                self.length = hSeqAndLength & 0x1f
                self.org = int(trame[6:8], 16)
                
                #### a priori pas utile d'inverser l'ordre des octets ####
                """#remise en ordre des octets DATA_BYTES
                dataByte0 = trame[8:10] #utile pour le mode
                db = "%s%s%s%s" % (trame[14:16], trame[12:14], trame[10:12], dataByte0)  """   
                
                dataByte0 = trame[14:16] #utile pour le mode
                db = "%s%s%s%s" % (trame[8:10], trame[10:12], trame[12:14], dataByte0)
                self.dataBytes = int(db, 16)    
                
                self.idBytes = int(trame[16:24], 16)
                self.status = int(trame[24:26], 16)
                self.checksum = int(trame[26:28], 16)
                self.date = temps.date()
                self.heure = temps.time()
                
                #verification du mode (normal ou teach-in)
                bit3 = (int(dataByte0, 16) >> 3) & 1
                bit7 = (int(dataByte0, 16) >> 7) & 1
                if (bit3 == 0) and (bit7 == 1):
                    self.teachIn = True
            
            except (ValueError, AttributeError):
                self.valide = False
                    
        else:
            self.valide = False
            
        if not(self.valide):
            #on met a None les attributs si la trame n'est pas valide
            self.syncBytes = None
            self.hSeq = None
            self.length = None
            self.org = None
            self.dataBytes = None
            self.idBytes = None
            self.status = None
            self.checksum = None
            self.teachIn = None
            self.date = None
            self.heure = None
