import os
import sys
import traceback
import json
import threading
from Gateway.Gateway import Gateway

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


Service = sys.argv[1] 
"""  
buildingName = sys.argv[2]
floor = sys.argv[3]
room = sys.argv[4]
"""

buildingName = "U38"
floor = "0"
room = "1"

try:
    masterConfig = ParseJson("./Config.json")
except:
    traceback.print_exc()
    sys.exit(1)

ipAddress = masterConfig.getIp()

print(ipAddress)

def sensorActuatorStart():
    os.system("python3 Sensors/Buildings/" + buildingName + "/" + floor +"/" + room +"/start_script.py " + ipAddress)

def gatewayStart():
    Gateway(ipAddress).startSense()

if Service == "start":
    threading.Thread(target=sensorActuatorStart).start()
    threading.Thread(target=gatewayStart).start()
