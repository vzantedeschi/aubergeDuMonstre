----------------------------------------------------------------------------
pour lancer le serveur mongodb qui va gerer la base dans un terminal 
----------------------------------------------------------------------------

0. vous pouvez suivre ces instructions pour avoir les commandes sous windows (et ne pas devoir aller tout le temps dans le bin)

http://tuts.syrinxoon.net/tuts/installation-et-bases-de-mongodb

(1.) si vous n avez pas fait l installation pour lancer la commande de o� vous voulez allez dans mongodb/bin 

2. sous C:\ cr�er un dossier vide data et dans celui-ci creer un dossier vide db

3. executer la ligne mongod

cela permettra de rassembler toute les database dans le dossier correspondant

4. pour vous connecter sur ce serveur sans utiliser le code prenez un nouveau terminal, (allez au bin au besoin) et tapez mongo


----------------------------------------------------------------------------
Le mat�riel compl�mentaire � installer apr�s ces premiers essais.
----------------------------------------------------------------------------
�tape 0 : 
dans panneau de configuration -> Syst�me -> param�tre syst�mes avanc�s
-> variables d'environnement -> variables syst�me
ajouter une variable PYTHONPATH valant C:\Python27\Lib;C:\Python27;C:\Python27\DLLs;C:\Python27\lib-tk



a. installer Setuptools => 

http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools


b. installer Pip => 

http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip


�tape 1 :
dans le dossier Python27, dans script, faire 

pip install mongoengine

si cette ligne ne marche pas utiliser

easyinstall -U mongoengine





