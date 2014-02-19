#TODO
#factoriser la ligne if connected == True : 
#changer la valeur de enFonctionnement en cas d'erreur
enFonctionnement == 0

while enFonctionnement==0 : 

    baseregle = {"allumeClim" : allumeClim,
                 "eteintClim" : eteintClim,
                 "ouvreVolet" : ouvreVolet,
                 "fermeVolet" : fermeVolet, 
                 "allumeLum" : allumeLum, 
                 "eteintLum" : eteintLum,
                 "allumeInt" : allumeInt,
                 "eteintInt" : eteintInt,
                 "fermePiece" : fermePiece, 
                 "ouvrePiece" : ouvrePiece,
                 "question" : question, 
                 "allumeEau" : allumeEau, 
                 "eteintEau" : eteintEau, 
                 "fermeRideau" : fermeRideau, 
                 "ouvreRideau" : ouvreRideau,
                 "notifierRes" : notifierRes
                 }
 
    def eteintClim():
        print "Desactivation de la climatisation"

        # Modifier l'information de la BDD pour mettre "climActive" à False
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.climActivee = False
        etatPiece.save()
                
        if connected == True :
            connectProxy.send( 'A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
        elif connected ==False    
            enFonctionnement == 1

    def allumeClim():
        print "Activation de la climatisation"
                
        # Modifier l'information de la BDD pour mettre "climActive" à True
        #change = True
        #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : change} },upsert=False,multi=True)
        etatPiece = tables.Etat.objects(piece_id = piece_id).first()
        etatPiece.climActivee = True
        etatPiece.save()
                
        if connected == True :
            connectProxy.send( 'A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
        elif connected ==False    
            enFonctionnement == 1
     
    def ouvreVolet():
        print '\nCommande suivant un interrupteur en cours'
            if connected == True :
                intrDonnees = item[u'ouverte']
                if intrDonnees == True:
                    print "Ouverture des volets"
                    connectProxy.send('A55A6B0550000000FF9F1E0530D1' )
            elif connected ==False    
                enFonctionnement == 1

def fermeVolet():
        if connected == True :
            intrDonnees = item[u'ouverte']
            if intrDonnees == False:
                print "Fermeture des volets"
                connectProxy.send('A55A6B0570000000FF9F1E0530D1' )
        elif connected ==False    
                enFonctionnement == 1

def allumeEau(): 
         print "Activation du systeme anti-incendie"

            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à True
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : True} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.antiIncendieDeclenche = True
            etatPiece.save() 
            
    def eteintEau(): 
        print "Desactivation du systeme anti-incendie"

            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.antiIncendieDeclenche = False
            etatPiece.save()
            
            if connected == True :
                connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
                
    def allumeLum():
    def eteintLum():
    def allumeInt():
    def eteintInt():
    def fermePiece():
    def ouvrePiece():
    def question():
    def fermeRideau(): 
    def ouvreRideau(): 
    def notifierRes():
                    
    baseregle[num]()