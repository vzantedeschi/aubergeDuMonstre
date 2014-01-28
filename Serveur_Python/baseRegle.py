#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Commande():
    def __init__(self):

		##premier test : est ce qu il y a du mouvement depuis peu de temps ?
        ### ICI EXAMINER LA BDD ###

        ### Il me faut le format des informations de sortie pour savoir
        ### sur quoi faire une condition
        if (True):
            print 'Présence détectée'
            self.type = 'PRES'
            # je met d'autre informations qu'on pourrait trouver dans la BDD
            self.piece = 'piece1'
            self.heure = 'heure1'
        else:
            print 'autre type de commande'
            self.type = 'OTHER'
