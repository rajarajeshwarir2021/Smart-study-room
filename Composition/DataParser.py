import paho.mqtt.client as mqtt
import json
import threading, time
import traceback
import sys

class DataParser:
    """
    This class reads the configuration file and parses it according to the services offered.
    """

    def __init__(self, filePath):
        """
        Constructor of the class
        """
        self.jsonFileName = filePath
        self.parsedData = self.parseJson()

    def parseJson(self):
        """
        json parser
        """
        with open(self.jsonFileName) as f_in:
            return json.load(f_in)

    def writeJson(self, data):
        with open(self.jsonFileName, 'w') as outfile:
            json.dump(data, outfile)

    def getHeaterStatus(self):
        return self.parsedData["HeaterStatus"]

    def getLightStatus(self):
        return self.parsedData["LightStatus"]

    def getDustbinStatus(self):
        return self.parsedData["DustbinStatus"]

    def getAcStatus(self):
        return self.parsedData["AcStatus"]

    def getBlindStatus(self):
        return self.parsedData["BlindStatus"]

    def getPeopleCount(self):
        return int(self.parsedData["PeopleCount"])

    def setHeaterStatus(self, sString):
        self.parsedData["HeaterStatus"] = sString
        self.writeJson(self.parsedData)

    def setLightStatus(self, sString):
        self.parsedData["LightStatus"] = sString
        self.writeJson(self.parsedData)

    def setDustbinStatus(self, sString):
        self.parsedData["DustbinStatus"] = sString
        self.writeJson(self.parsedData)

    def setAcStatus(self, sString):
        self.parsedData["AcStatus"] = sString
        self.writeJson(self.parsedData)

    def setBlindStatus(self, sString):
        self.parsedData["BlindStatus"] = sString
        self.writeJson(self.parsedData)

    def setPeopleCount(self, val):
        self.parsedData["PeopleCount"] = str(val)
        self.writeJson(self.parsedData)
