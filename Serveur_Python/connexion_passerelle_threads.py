import socket
import select
import threading
import sys
import time

# Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000

connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_passerelle.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

# Ici il faut mettre en mémoire les valeurs des identifiants des capteurs utilisés
# et éventuellement les constantes (Sync Bytes, H_SEQ)
fic_id = open("../identifiants.txt","r")
identifiants = fic_id.readlines()
fic_id.close()
for identifiant in identifiants:
    print identifiant

SYNC_BYTES = "A55A"
H_SEQ = "0"

# Créer un thread qui reçoit les messages provenant de la passerelle.
class ThreadPasserelleRecv(threading.Thread):
    
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        while 1:
            #attendre une trame et l'afficher
            trameRecue = self.connexion.recv(1024)
            message = "%s" % (trameRecue)
            print message
            #traiter la trame et enregistrer l'information dans la BI
            #
            #Parser
            #
            #
        
class ThreadTraitementBaseInformation(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        while 1:
            #Lire la BI et agir (envoi de commandes) toutes les XX secondes
            #
            time.sleep(1)
            
