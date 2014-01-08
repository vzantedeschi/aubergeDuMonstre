import socket
import select

#Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000

connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_passerelle.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

trame = "A55A3B0510020024000000042024"
trame2 = "A55A0B05000000000021CC072024"
trameEteindre = "A55A3B05700000000021CC0730A4"
trame1 = trameEteindre.encode()
connexion_avec_passerelle.send(trame1)

while 1:
    # Client est de type socket
    msg_recu = connexion_avec_passerelle.recv(224)
    # Peut planter si le message contient des caractères spéciaux
    msg_recu = msg_recu.decode()
    ident = msg_recu[16:24]
    print ident
    if ident == "0021CC07" :
        print("Reçu {}".format(msg_recu))
        
        
