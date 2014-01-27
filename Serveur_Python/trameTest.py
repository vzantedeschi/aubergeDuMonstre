#Tests unitaires pour la classe Trame (parsage de la trame)

import trame
import unittest
import datetime

class TestTrameValide(unittest.TestCase):

    def testTrDonnees(self):
        #teste une trame d'envoi de donnees (mode normal)
        test = "A55A0B070084990F0004E9570001"
        date = datetime.datetime(2014, 1, 12, 18, 59, 30)
        
        result = trame.Trame(test, date)
        self.assertEquals(result.syncBytes, 0xA55A)
        self.assertEquals(result.hSeq, 0)
        self.assertEquals(result.length, 11)
        self.assertEquals(result.org, 0x07)
        self.assertEquals(result.dataBytes, 0x0084990F)
        self.assertEquals(result.idBytes, 0x0004E957)
        self.assertEquals(result.status, 0x00)
        self.assertEquals(result.checksum, 0x01)
        self.assertEquals(result.eepSent, False)
        self.assertEquals(result.valide, True)
        self.assertEquals(result.date, date.date())
        self.assertEquals(result.heure, date.time())
    
    def testTreepSent(self):
    #teste une trame en mode teach-in
        test = "A55A0B07100802870004E9570088"
        date = datetime.datetime(2014, 1, 12, 18, 59, 30)
        
        result = trame.Trame(test, date)

        self.assertEquals(result.syncBytes, 0xA55A)
        self.assertEquals(result.hSeq, 0)
        self.assertEquals(result.length, 11)
        self.assertEquals(result.org, 0x07)
        self.assertEquals(result.dataBytes, 0x10080287)
        self.assertEquals(result.idBytes, 0x0004E957)
        self.assertEquals(result.status, 0x00)
        self.assertEquals(result.checksum, 0x88)
        self.assertEquals(result.eepSent, True)
        self.assertEquals(result.valide, True)
        self.assertEquals(result.date, date.date())
        self.assertEquals(result.heure, date.time())
    
class TestTrameBadInput(unittest.TestCase):
    def testTrLongueurInvalide(self):
        """le parsage doit echouer avec une trame de longueur != 28 caracteres (valide == False)"""
        tests = ["AN5A0B0710802870004E957008", ""\
                 "A95A0B0%10802870004E9570088A"]
        date = datetime.datetime(2014, 1, 12, 18, 59, 30)
        for test in tests:
            result = trame.Trame(test, date)
            self.assertEquals(result.syncBytes, None)
            self.assertEquals(result.hSeq, None)
            self.assertEquals(result.length, None)
            self.assertEquals(result.org, None)
            self.assertEquals(result.dataBytes, None)
            self.assertEquals(result.idBytes, None)
            self.assertEquals(result.status, None)
            self.assertEquals(result.checksum, None)
            self.assertEquals(result.eepSent, None)
            self.assertEquals(result.valide, False)
            self.assertEquals(result.date, None)
            self.assertEquals(result.heure, None)
        
    def testTrNone(self):
        """le parsage doit echouer avec None (valide == False)"""
        test = None
        date = datetime.datetime(2014, 1, 12, 18, 59, 30)
        
        result = trame.Trame(test, date)
        self.assertEquals(result.syncBytes, None)
        self.assertEquals(result.hSeq, None)
        self.assertEquals(result.length, None)
        self.assertEquals(result.org, None)
        self.assertEquals(result.dataBytes, None)
        self.assertEquals(result.idBytes, None)
        self.assertEquals(result.status, None)
        self.assertEquals(result.checksum, None)
        self.assertEquals(result.eepSent, None)
        self.assertEquals(result.valide, False)
        self.assertEquals(result.date, None)
        self.assertEquals(result.heure, None)
    
    def testTrCaracInvalide(self):
        """le parsage doit echouer qd la trame n'est pas convertible en 
        hexadecimal (valide == False)"""
        tests = ["AN5A0B0710802870004E9570088", "A95A0B07108028700ZRE9570088"\
                 "A95A0B0%10802870004E9570088"]
        date = datetime.datetime(2014, 1, 12, 18, 59, 30)
        
        for test in tests:
            result = trame.Trame(test, date)
            self.assertEquals(result.syncBytes, None)
            self.assertEquals(result.hSeq, None)
            self.assertEquals(result.length, None)
            self.assertEquals(result.org, None)
            self.assertEquals(result.dataBytes, None)
            self.assertEquals(result.idBytes, None)
            self.assertEquals(result.status, None)
            self.assertEquals(result.checksum, None)
            self.assertEquals(result.eepSent, None)
            self.assertEquals(result.valide, False)
            self.assertEquals(result.date, None)
            self.assertEquals(result.heure, None)
            
    def testDateInvalide(self):
        test = "A55A0B070084990F0004E9570001"
        date = 4
        
        result = trame.Trame(test, date)
        self.assertEquals(result.syncBytes, None)
        self.assertEquals(result.hSeq, None)
        self.assertEquals(result.length, None)
        self.assertEquals(result.org, None)
        self.assertEquals(result.dataBytes, None)
        self.assertEquals(result.idBytes, None)
        self.assertEquals(result.status, None)
        self.assertEquals(result.checksum, None)
        self.assertEquals(result.eepSent, None)
        self.assertEquals(result.valide, False)
        self.assertEquals(result.date, None)
        self.assertEquals(result.heure, None)


if __name__ == "__main__":
  unittest.main()
  """ttv = TestTrameValide()
  ttv.testTrDonnees()
  ttv.testTreepSent()

  ttbi = TestTrameBadInput()
  ttbi.testTrLongueurInvalide()
  ttbi.testTrNone()
  ttbi.testTrCaracInvalide()
  ttbi.testDateInvalide()"""
