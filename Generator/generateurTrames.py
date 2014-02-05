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
                self.fenetre = id

            elif (type == 'INTR') :
                self.interrupteur = id

            elif (type == 'PRES') :
                self.presence = id

            elif (type == 'TEMP') :
                self.temperature = id

    #Generation des trames parasites
    def genericFrame(self) :
        org = "05"
        dataBytes = "23000000"
        idBytes = "00000000"
        message = org+dataBytes+idBytes
        status = "20"
        checksum = "53"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames de l'interrupteur
    def pressON(self) :
        org = "05"
        dataBytes = "10000000"
        idBytes = self.interrupteur
        message = org+dataBytes+idBytes
        status = "20"
        # checksum est censé être l'addition des octets en hexadécimal sur un octet de HSEQ à status
        #checksum = hex(int(org,16)+int(status,16)+int("10",16)+int(idBytes[0:2],16)+int(idBytes[2:4],16)+int(idBytes[4:6],16)+int(idBytes[6:8],16))
        #print checksum
        checksum = "03"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def pressOFF(self) :
        org = "05"
        dataBytes = "30000000"
        idBytes = self.interrupteur
        message = org+dataBytes+idBytes
        status = "20"
        checksum = "23"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    #Generation des trames du capteur de presence
    def presenceDetected(self) :
        org = "07"
        dataBytes = "B7D6000D"
        idBytes = self.presence
        message = org+dataBytes+idBytes
        status = "00"
        checksum = "47"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    def nothingDetected(self) :
        org = "07"
        dataBytes = "B9B3000F"
        idBytes = self.presence
        message = org+dataBytes+idBytes
        status = "00"
        checksum = "28"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame

    
    #Generation des trames du capteur de température
    def currentTemperature(self) : 
        org = "07"
        dataBytes = "2284990F"
        idBytes = self.temperature
        message = org+dataBytes+idBytes
        status = "00"
        checksum = "01"
        queueTrame = status+checksum
        return self.enteteTrames + message + queueTrame
        
    def getCapteurs(self) :
        print "liste des capteurs en memoire :"
        print "capteur d'ouverture fenetre ", self.fenetre
        print "capteur de detection de presence ", self.presence
        print "interrupteur sans fils ", self.interrupteur 
        print "capteur de temperature ", self.temperature
    

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