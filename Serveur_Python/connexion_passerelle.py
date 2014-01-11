import socket
import select

#Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000

connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_passerelle.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

trameIntOn = "A55A0B05100000000021CC073044"
trameIntOff = "A55A0B05300000000021CC073064"

trameIDMoodleAllumer = "A55A5B0510000000FF9F1E033044"

trameIDMoodleEteindre = "A55A5B0530000000FF9F1E033064"

trame1 = trameIDMoodleEteindre.encode()
connexion_avec_passerelle.send(trame1)

while 1:
    # Client est de type socket
    msg_recu = connexion_avec_passerelle.recv(28)
    # Peut planter si le message contient des caractères spéciaux
    msg_recu = msg_recu.decode()
    ident = msg_recu[16:24]
    print ident
    if ident == "0021CC07" :
        print("Reçu {}".format(msg_recu))
    if ident == "00893386" :
        print("Reçu {}".format(msg_recu))
    if ident == "00054155" :
        print("Reçu {}".format(msg_recu))
        
        
