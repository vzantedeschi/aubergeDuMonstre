#!/usr/bin/env python
# -*- coding: utf-8 -*-

class generateurTrames():

    def __init__(self, identifiants):
        fic_id = open(identifiants,"r")
        liste = fic_id.readlines()
        
        syncBytes = "A55A"
        h_seq_length = "0B"
        self.enteteTrames = syncBytes + h_seq_length
        
        fic_id.close()

        for capt in liste:
            type, id = capt.split()

            if (type == 'FEN') :
                self.porte = id

            elif (type == 'FEN2') :
                self.porte2 = id
                
            elif (type == 'FEN3') :
                self.porte3 = id
                
            elif (type == 'FEN4') :
                self.porte4 = id
                
            elif (type == 'FEN5') :
                self.porte5 = id

            elif (type == 'PRES') :
                self.presence = id

            elif (type == 'PRES2') :
                self.presence2 = id

            elif (type == 'PRES3') :
                self.presence3 = id

            elif (type == 'PRES4') :
                self.presence4 = id

            elif (type == 'PRES5') :
                self.presence5 = id

            elif (type == 'VOL') :
                self.volet = id

            elif (type == 'VOL2') :
                self.volet2 = id

            elif (type == 'VOL3') :
                self.volet3 = id

            elif (type == 'VOL4') :
                self.volet4 = id

            elif (type == 'VOL5') :
                self.volet5 = id

            elif (type == 'TEMP') :
                self.temperature = id
                self.humidite = id

            elif (type == 'TEMP2') :
                self.temperature2 = id
                self.humidite2 = id

            elif (type == 'TEMP3') :
                self.temperature3 = id
                self.humidite3 = id

            elif (type == 'TEMP4') :
                self.temperature4 = id
                self.humidite4 = id

            elif (type == 'TEMP5') :
                self.temperature5 = id
                self.humidite5 = id

            elif (type == 'RFID') :
                self.rfid = id

            elif (type == 'RFID2') :
                self.rfid2 = id

            elif (type == 'RFID3') :
                self.rfid3 = id

            elif (type == 'RFID4') :
                self.rfid4 = id

            elif (type == 'RFID5') :
                self.rfid5 = id
                
            elif (type == 'INTR') :
                self.interrupteur = id

            elif (type == 'INTR2') :
                self.interrupteur2 = id

            elif (type == 'INTR3') :
                self.interrupteur3 = id

            elif (type == 'INTR4') :
                self.interrupteur4 = id

            elif (type == 'INTR5') :
                self.interrupteur5 = id

            elif (type == 'INFE') :
                self.intrVolet = id

            elif (type == 'INFE2') :
                self.intrVolet2 = id
                
            elif (type == 'INFE3') :
                self.intrVolet3 = id
                
            elif (type == 'INFE4') :
                self.intrVolet4 = id
                
            elif (type == 'INFE5') :
                self.intrVolet5 = id

    #Generation des trames parasites
    def genericFrame(self) :
        org = "05"
        dataBytes = "23000000"
        idBytes = "00000000"
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "58"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames de l'interrupteur
    def pressON(self,piece) :
        org = "05"
        dataBytes = "10000000"

        if piece == 1:
            idBytes = self.interrupteur
        elif piece ==2:
            idBytes = self.interrupteur2
        elif piece ==3:
            idBytes = self.interrupteur3
        elif piece ==4:
            idBytes = self.interrupteur4
        elif piece ==5:
            idBytes = self.interrupteur5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "13"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def pressOFF(self,piece) :
        org = "05"
        dataBytes = "30000000"

        if piece == 1:
            idBytes = self.interrupteur
        elif piece ==2:
            idBytes = self.interrupteur2
        elif piece ==3:
            idBytes = self.interrupteur3
        elif piece ==4:
            idBytes = self.interrupteur4
        elif piece ==5:
            idBytes = self.interrupteur5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "33"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames de l'interrupteur pour volet
    def fermeVolet(self,piece) :
        org = "05"
        dataBytes = "30000000"

        if piece == 1:
            idBytes = self.intrVolet
        elif piece ==2:
            idBytes = self.intrVolet2
        elif piece ==3:
            idBytes = self.intrVolet3
        elif piece ==4:
            idBytes = self.intrVolet4
        elif piece ==5:
            idBytes = self.intrVolet5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "04"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def ouvreVolet(self,piece) :
        org = "05"
        dataBytes = "10000000"

        if piece == 1:
            idBytes = self.intrVolet
        elif piece ==2:
            idBytes = self.intrVolet2
        elif piece ==3:
            idBytes = self.intrVolet3
        elif piece ==4:
            idBytes = self.intrVolet4
        elif piece ==5:
            idBytes = self.intrVolet5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "04"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames du capteur de presence
    def presenceDetected(self,piece) :
        org = "07"
        dataBytes = "B7D6000D"
        
        if piece == 1:
            idBytes = self.presence
        elif piece ==2:
            idBytes = self.presence2
        elif piece ==3:
            idBytes = self.presence3
        elif piece ==4:
            idBytes = self.presence4
        elif piece ==5:
            idBytes = self.presence5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "6C"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def nothingDetected(self) :
        org = "07"
        dataBytes = "B9B3000F"
        idBytes = self.presence
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "4D"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame
 
    #Generation des trames du capteur de température
    def currentTemperature(self,piece,dbytes) : 
        org = "07"
        dataBytes = dbytes
        
        if piece == 1:
            idBytes = self.temperature
        elif piece == 2:
            idBytes = self.temperature2
        elif piece == 3:
            idBytes = self.temperature3
        elif piece == 4:
            idBytes = self.temperature4
        elif piece == 5:
            idBytes = self.temperature5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "A7"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames du capteur d'humidité
    def currentHumidite(self,piece,dbytes) : 
        org = "07"
        dataBytes = dbytes
        
        if piece == 1:
            idBytes = self.humidite
        elif piece ==2:
            idBytes = self.humidite2
        elif piece ==3:
            idBytes = self.humidite3
        elif piece ==4:
            idBytes = self.humidite4
        elif piece ==5:
            idBytes = self.humidite5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "A7"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames du capteur de porte
    def contactPorteOuverte(self,piece) :
        org = "07"
        dataBytes = "00000008"
        
        if piece == 1:
            idBytes = self.porte
        elif piece ==2:
            idBytes = self.porte2
        elif piece ==3:
            idBytes = self.porte3
        elif piece ==4:
            idBytes = self.porte4
        elif piece ==5:
            idBytes = self.porte5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "82"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def contactPorteFermee(self,piece) :
        org = "07"
        dataBytes = "00000009"
        
        if piece == 1:
            idBytes = self.porte
        elif piece ==2:
            idBytes = self.porte2
        elif piece ==3:
            idBytes = self.porte3
        elif piece ==4:
            idBytes = self.porte4
        elif piece ==5:
            idBytes = self.porte5
        
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "81"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames du capteur de volet
    def contactVoletOuvert(self,piece) :
        org = "07"
        dataBytes = "00000008"
        
        if piece == 1:
            idBytes = self.volet
        elif piece ==2:
            idBytes = self.volet2
        elif piece ==3:
            idBytes = self.volet3
        elif piece ==4:
            idBytes = self.volet4
        elif piece ==5:
            idBytes = self.volet5
            
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "82"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def contactVoletFerme(self,piece) :
        org = "07"
        dataBytes = "00000009"
        
        if piece == 1:
            idBytes = self.volet
        elif piece ==2:
            idBytes = self.volet2
        elif piece ==3:
            idBytes = self.volet3
        elif piece ==4:
            idBytes = self.volet4
        elif piece ==5:
            idBytes = self.volet5
        
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "81"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames de puces rfid
    def rfidDetected(self,perso,porte) :
        org = "07"
        dataBytes = "0000000"+str(perso)
        
        if porte == 1:
            idBytes = self.rfid
        elif porte ==2:
            idBytes = self.rfid2
        elif porte ==3:
            idBytes = self.rfid3
        elif porte ==4:
            idBytes = self.rfid4
        elif porte ==5:
            idBytes = self.rfid5
           
        message = org+dataBytes+idBytes
        status = "30"
        checksum = "00"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame
        
    def getCapteurs(self) :
        print "liste des capteurs en memoire :"
        print "capteur d'ouverture fenetre ", self.fenetre
        print "capteur de detection de presence ", self.presence
        print "interrupteur sans fils ", self.interrupteur 
        print "capteur de temperature ", self.temperature
        print "capteur de puce rfid ", self.rfid
    

if __name__ == "__main__" :
    print '#################TESTS UNITAIRES##################'

    gen = generateurTrames("identifiants.txt")

    print '\n***Test 1 : Lecture fichier des identifiants***'
    gen.getCapteurs()

    print '\n***Test 2 : interrupteur : allumer/eteindre***'
    print "allumer => ", gen.pressON()
    print "eteindre => ", gen.pressOFF()

    print '\n***Test 3 : generation de trames parasites***'
    print "trame => ", gen.genericFrame()

    print '\n***Test 4 : generation de trames du capteur de presence***'
    print "il y a quelqu'un => ", gen.presenceDetected()
    print "il y a personne => ", gen.nothingDetected()

    print '\n***Test 5 : generation de trames du capteur de temperature***'
    print "il fait 24.5 degres => ", gen.currentTemperature()
