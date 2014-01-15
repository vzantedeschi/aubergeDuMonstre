L�architecture du serveur python se structure autour d�un syst�me multi-threads.

Nous aurons deux threads d��coute (listeners) destin�s � recevoir les trames envoy�es par la passerelle EnOcean d�une part et par l�application 
Web (tablette) d�autre part.

A la r�ception d�une trame, ces threads utiliseront le parser pour trier les informations, rejetteront imm�diatement les trames incorrectes 
puis feront passer ces informations dans la base d�informations (architecture plus d�taill�e de celle-ci � demander � V et A) avant 
d�envoyer un signal � s1 � au thread Command.

Le thread Command cr�e est � l�origine d�un Timer qui renvoi � chaque cycle un signal � s1 � d�fini qui a faire r�agir le thread Command 
(par un handler) et qui le force � faire appel au moteur de r�gles.

Le moteur de r�gle examine la base d�information o� sont stock�es les informations contenues dans les trames re�ues 
(�ventuellement un historique de ces informations si cela est n�cessaire � l�interpr�tation d�une r�gle) et � partir d�un 
ensemble de pr�-conditions d�finies statiquement, choisi une ou plusieurs commandes (ie une information � encoder au sein d�une trame) et 
le thread Command cr�e alors autant de threads Sender que de commandes � envoyer (celles-ci peuvent �tre envoy�es � la passerelle ou � 
l�application Web).

A la r�ception d�une commande, le Sender encode la commande (ie l�information dans une trame compr�hensible par le syst�me EnOcean ou selon le formalisme choisit pour l�application Web (� d�finir avec M) puis envoie l�information sur le port de communication.

Note : Les ports des diff�rentes machines, les identifiants des capteurs, les r�gles de d�cision des commandes doivent �tre d�finies 
statiquement dans le programme ou dans un fichier.

Note : Penser � r�armer le Timer � chaque fin de boucle.

