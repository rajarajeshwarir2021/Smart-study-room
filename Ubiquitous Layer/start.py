import paho.mqtt.client as mqtt
import json
import threading, time
from UbiquitousLayer import UbiquitousLayer
import traceback
import sys

class ParseJson:
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

    def getIp(self):
        return self.parsedData["MQTT_BROKER"]

try:
    masterConfig = ParseJson("./Config.json")
except:
    traceback.print_exc()
    sys.exit(1)

ipAddress = masterConfig.getIp()

UbiquitousLayer(ipAddress).start()
