# 

class generateurTrames():

    def __init__(self, identifiants):
    	fic_id = open(identifiants,"r")
    	liste = fic_id.readlines()
    	self.enteteTrames = 'A55A0B'
    	fic_id.close()

	for capt in liste:
		type, id = capt.split()

		if (type == 'fenetre') :
			self.fenetre = id

		elif (type == 'interrupteur') :
			self.interrupteur = id

		elif (type == 'presence') :
			self.presence = id

    #Generation des trames de l'interrupteur
    def pressON(self) :
    	message = "051000000000"
    	queueTrame = "2024"
    	return self.enteteTrames + message + queueTrame

    def pressOFF(self) :
    	message = "053000000000"
    	queueTrame = "2024"
    	return self.enteteTrames + message + queueTrame

    def getCapteurs(self) :
    	print "liste des capteurs en memoire :"
    	print "capteur d'ouverture fenetre ", self.fenetre
    	print "capteur de detection de presence ", self.presence
    	print "interrupteur sans fils ", self.interrupteur 

if __name__ == "__main__" :
	print '#################TESTS UNITAIRES##################'

	gen = generateurTrames("identifiants.txt")

	print '\n***Test 1 : Lecture fichier des identifiants***'
	gen.getCapteurs()

	print '\n***Test 2 : interrupteur : allumer/eteindre***'
	print "allumer => ", gen.pressON()
	print "eteindre => ", gen.pressOFF()