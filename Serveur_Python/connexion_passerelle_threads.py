import socket
import select
import threading
import sys
import time
import datetime


# Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000

connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_passerelle.connect((hote, port))
print("Connexion �tablie avec le serveur sur le port {}".format(port))

# Ici il faut mettre en m�moire les valeurs des identifiants des capteurs utilis�s
# et �ventuellement les constantes (Sync Bytes, H_SEQ)
fic_id = open("../identifiants.txt","r")
identifiants = fic_id.readlines()
fic_id.close()
for identifiant in identifiants:
    print identifiant

SYNC_BYTES = "A55A"
H_SEQ = "0"

# Cr�er un thread qui re�oit les messages provenant de la passerelle.
class ThreadPasserelleRecv(threading.Thread):
    
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        while 1:
            #attendre une trame
            trameRecue = self.connexion.recv(224)
            
            msg_recu = msg_recu.decode()
            
            #r�cup�re l'identifiant du capteur
            ident = msg_recu[16:24]
            print ident
            
            #Si le capteur appartient � ceux �tudi�s on traite la trame
            if ident in identifiants
                #R�cup�re la date et l'heure de reception
                now = datetime.datetime.now()

                #traiter la trame et enregistrer l'information dans la BI
                #
                #Parser
                #
                #Met A J BI
        
class ThreadTraitementBaseInformation(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        while 1:
            #Lire la BI et agir (envoi de commandes) toutes les XX secondes
            #
            time.sleep(1)
            #
