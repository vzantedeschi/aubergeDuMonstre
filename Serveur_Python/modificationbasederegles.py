#Je viens de m'en rendre compte, là, vers 11h55 que Cyprien et Éloise ont ajouté ça : 
def trameActionneur(actionneur, activation):
    sync = 'A55A'
    message = 'B0550000000'
    if activation:
        message = 'B0570000000'
    message += actionneurConcerne.actionneur_id
    status = "30"
    checksum = calcCheckSum(message)
    queueTrame = status + checksum
    return sync + message + queueTrame

def activerActionneur(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece.first().actionneurs
    actionneurConcerne = actionneursPiece.objects(capteur_type = typeActionneur]).first()
    print "Activation de l'actionneur"
    # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(actionneurConcerne, True))

def desactiverActionneur(idPiece, typeActionneur):
    actionneurs = tables.Piece.objects(piece_id = idPiece.first().actionneurs
    actionneurConcerne = actionneursPiece.objects(capteur_type = typeActionneur]).first()
    print "Desactivation de l'actionneur"
    # Test si nous sommes effectivement connectés à la passerelle avant d'envoyer une trame d'actionneur
    if connected == True :
        print "Envoi au proxy"
        connectProxy.send(trameActionneur(actionneurConcerne, False))

def ouvrirVolets(idPiece):    
    # Allume l'interrupteur simulant les volets
    print "Verrouillage actif : volets en cours d'ouverture"
    activerActionneur(idPiece, 'ContactFen')        

def fermerVolets(idPiece):
    # Allume l'interrupteur simulant les volets
    print "Verrouillage actif : volets en cours d'ouverture"
    desactiverActionneur(idPiece, 'ContactFen')  

#TODO
#factoriser la ligne if connected == True : 
#connected permet de verifier si on est bien connecté au proxy...
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
        if connected == True :
            #envoi de la trame 
            print "Desactivation de la climatisation"
            connectProxy.send( 'A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
            # Modifier l'information de la BDD pour mettre "climActive" à False
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.climActivee = False
            etatPiece.save()
        elif connected ==False    
            enFonctionnement == 1

    def allumeClim():        
        if connected == True :
            #envoi de la trame
            print "Activation de la climatisation"
            connectProxy.send( 'A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
            # Modifier l'information de la BDD pour mettre "climActive" à True
            #change = True
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : change} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.climActivee = True
            etatPiece.save()
        elif connected ==False    
            enFonctionnement == 1
     
    def ouvreVolet():
        print '\nCommande suivant un interrupteur en cours'
            if connected == True :
                #envoi de la trame
                print "Ouverture des volets"
                connectProxy.send('A55A6B0550000000FF9F1E0530D1')
                #Mettre à jour l'état de la pièce dans la BDD
                #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
                etatPiece = tables.Etat.objects(piece_id = piece_id).first()
                etatPiece.voletsOuverts = True
                etatPiece.save()
            elif connected ==False    
                enFonctionnement == 1

    def fermeVolet():
            if connected == True :
                print "Fermeture des volets"
                connectProxy.send('A55A6B0570000000FF9F1E0530D1')
                #Mettre à jour l'état de la mpièce dans la BDD
                #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
                etatPiece = tables.Etat.objects(piece_id = piece_id).first()
                etatPiece.voletsOuverts = False
                etatPiece.save()
            elif connected ==False    
                enFonctionnement == 1

    def allumeEau(): 
        #pas d'envoi de trame pour l'instant
        #if connected ==True :
            print "Activation du systeme anti-incendie"
            #connectProxy.send('traaaaame')
            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à True
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : True} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.antiIncendieDeclenche = True
            etatPiece.save() 
        elif connected ==False    
                enFonctionnement == 1        

    def eteintEau(): 
        if connected == True :    
            print "Desactivation du systeme anti-incendie"
            connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ')
            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.antiIncendieDeclenche = False
            etatPiece.save()
        elif connected ==False    
                enFonctionnement == 1 

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