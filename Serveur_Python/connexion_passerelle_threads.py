import socket
import select
import threading
import sys
import time
import datetime

import trame

def passe_hex(elem):
    return int(elem,16)

# Ici il faut mettre en mémoire les valeurs des identifiants des capteurs utilisés
# et éventuellement les constantes (Sync Bytes, H_SEQ)
fic_id = open("../identifiants.txt","r")
identifiants = fic_id.readlines()
fic_id.close()
#Test
identifiants = map(passe_hex,identifiants)
for identifiant in identifiants:
    print identifiant

SYNC_BYTES = "A55A"
H_SEQ = "0B"

# Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000

# Créer un thread qui reçoit les messages provenant de la passerelle.
class ThreadPasserelleListener(threading.Thread):
    
    def __init__(self,hote,port):
        threading.Thread.__init__(self)

        ############# CONNEXION PASSERELLE ###################
        
        self.connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_avec_passerelle.connect((hote, port))
        
        print("Connexion établie avec la passerelle sur le port {}".format(port))
        ######################################################
        
    def run(self):
        
        while 1:
            # Attendre une trame
            msg_recu = self.connexion_avec_passerelle.recv(28)
            
            msg_recu = msg_recu.decode()
            
            # Récupère l'identifiant du capteur
            ident = msg_recu[16:24]
            print ident
            
            # Si le capteur appartient à ceux étudiés on traite la trame
            if int(ident,16) in identifiants:
                # Récupère la date et l'heure de reception
                now = datetime.datetime.now()

                print("Reçu {}".format(msg_recu))

                # Passage par le parser
                infosTrame = trame.Trame(msg_recu,now)

                print ("ID {}".format(hex(infosTrame.idBytes)))
                print ("DB {}".format(hex(infosTrame.dataBytes)))
                print ("Heure {}".format(infosTrame.heure))
                
class ThreadAppliWebListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"
            
class ThreadCommand(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            #Lire la BI et agir (envoi de commandes) toutes les XX secondes
            #
            time.sleep(1)
            #

class ThreadTimer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"

class ThreadSender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            print "bonjour"

###########################################################
print "Serveur Python lancé"

PasserelleListener = ThreadPasserelleListener(hote,port)
PasserelleListener.start()

print "Exit main program"
