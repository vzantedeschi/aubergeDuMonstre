    elif (typeInfo == "Donnee.Temperature"):
        #Détermine la commande et mettre "traite" à True        
        tempDonnees = item[u'valeur']
        print tempDonnees

        climActive = etat[u'climActivee']
        print climActive

        db.etat.update({u'_id' : piece_id},{ "$set": {u'temperature' : tempDonnees} },upsert=False,multi=True)
        print '\nCommande suivant un changement de temperature en cours'

        ## Valeur 19 à modifier dans une interface graphique par exemple
        ## La trame crée est fausse, c'est un exemple
        if tempDonnees > 19 and climActive == False :
            print "Activation de la climatisation"
            
            # Modifier l'information de la BDD pour mettre "climActive" à True
            #change = True
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : change} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.climActivee = True
            etatPiece.save()
            
            if connected == True :
                connectProxy.send( 'A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
                
        elif tempDonnees <= 19 and climActive == True :
            print "Desactivation de la climatisation"

            # Modifier l'information de la BDD pour mettre "climActive" à False
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'climActivee' : False} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.climActivee = False
            etatPiece.save()
            
            if connected == True :
                connectProxy.send( 'A55A6B05WWWWWWWWYYYYYYYY30ZZ' )

    elif (typeInfo == "Donnee.Humidite"):
        humDonnees = item[u'valeur']
        print humDonnees

        antiIncendieActive = etat[u'antiIncendieDeclenche']
        print antiIncendieActive

        db.etat.update({u'_id' : piece_id},{ "$set": {u'humidite' : humDonnees}},upsert=False,multi=True)
        print '\nCommande suivant un changement d''humidite en cours'

        ## Valeur 70 à modifier dans une interface graphique par exemple
        ## La trame crée est fausse, c'est un exemple
        if humDonnees < 70 and antiIncendieActive == False:
            print "Activation du systeme anti-incendie"

            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à True
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : True} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.antiIncendieDeclenche = True
            etatPiece.save()
            
            if connected == True :
                connectProxy.send('A55A6B05XXXXXXXXYYYYYYYY30ZZ' )
                                             
        elif humDonnees > 70 and antiIncendieActive == True:
            print "Desactivation du systeme anti-incendie"

            # Modifier l'information de la BDD pour mettre "antiIncendieDeclenche" à False
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'antiIncendieDeclenche' : False} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.antiIncendieDeclenche = False
            etatPiece.save()
            
            if connected == True :
                connectProxy.send('A55A6B05WWWWWWWWYYYYYYYY30ZZ' )
        
    elif (typeInfo == "Donnee.RFID"):
        resident = item[u'resident_id']
        
        print '\nCommande suivant detection RFID en cours'
        rfidDetected = resident
        # Mise en place d'un timer qui indique
        # qu'il n'attend plus une détection de présence au bout
        # de 20 secondes
        timerRFID = threading.Timer(20,RFIDFunc)
        timerRFID.start()

    elif (typeInfo == "Donnee.Interrupteur"):
        print '\nCommande suivant un interrupteur en cours'
        if connected == True :
            intrDonnees = item[u'ouverte']
            if intrDonnees == True:
                print "Ouverture des volets"
                connectProxy.send('A55A6B0550000000FF9F1E0530D1' )
            elif intrDonnees == False:
                print "Fermeture des volets"
                connectProxy.send('A55A6B0570000000FF9F1E0530D1' )

    elif (typeInfo == "Donnee.ContactFen"):
        fenDonnees = item[u'ouverte']
        
        if fenDonnees == False:
            print '\nCommande suivant une fermeture de volets en cours'
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.voletsOuverts = False
            etatPiece.save()
        elif fenDonnees == True:
            print '\nCommande suivant une ouverture de volets en cours'
            #db.etat.update({u'piece_id' : piece_id},{ "$set": {u'voletsOuverts' : fenDonnees} },upsert=False,multi=True)
            etatPiece = tables.Etat.objects(piece_id = piece_id).first()
            etatPiece.voletsOuverts = True
            etatPiece.save()