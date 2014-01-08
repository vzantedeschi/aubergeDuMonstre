import socket
import select

#Mettre ici l'adresse IP de la passerelle EnOcean
hote = '134.214.106.23'
# Mettre ici le port de la passerelle sur lequel se connecter.
port = 5000

connexion_avec_passerelle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_passerelle.connect((hote, port))
print("Connexion �tablie avec le serveur sur le port {}".format(port))

# Client est de type socket
msg_recu = connexion_avec_passerelle.recv(1024)
# Peut planter si le message contient des caract�res sp�ciaux
msg_recu = msg_recu.decode()
print("Re�u {}".format(msg_recu))
