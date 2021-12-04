import paho.mqtt.client as mqtt
import json
from DataParser import DataParser
import os

# Lighting extremes in Lux
MIN_LIGHT = 500
MAX_LIGHT = 800

# Temperature extremes in celsius
MIN_TEMP = 20
MAX_TEMP = 27

PLANNER_DIR = "/home/dijikshra/Softwares_Custom/Planner/downward/"
PPDL_DIR = "/home/dijikshra/Softwares_Custom/Planner/downward/NewPddl/"

class StateVaribles:

    def __init__(self):
        # All state variables
        self.LdrIndoorData = 0
        self.LdrOutdoorData = 0
        self.TempData = 0
        self.DustBinFull = False
        self.PeopleCount = 0

class ActionVariables:

    def __init__(self):
        self.AcStatus = "OFF"
        self.HeaterStatus = "OFF"
        self.LightStatus = "OFF"
        self.BlindStatus = "CLOSE"
        self.DustbinStatus = "NON-FULL"

class Composition:

    def __init__(self, ipAddress):
        
        self.hardData = DataParser("./Data.json")
        
        self.mqtt_sub =  mqtt.Client("Listener-Composition")
        self.mqtt_pub =  mqtt.Client("Writer-Composition")
        self.ipAddress = ipAddress

        self.stateVariables = StateVaribles()
        self.prevStateVariables = StateVaribles()
        self.actionVariables = ActionVariables()

        # MQTT
        self.mqtt_sub.on_message = self.on_context_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("Context/#", qos =2)
        self.mqtt_pub.connect(self.ipAddress, 1883, 70)
        self.mqtt_pub.loop_start()

    def start(self):
        self.initData()
        self.sendBulkData()
        self.mqtt_sub.loop_forever()

    def initData(self):
        self.actionVariables.AcStatus = self.hardData.getAcStatus()
        self.actionVariables.HeaterStatus = self.hardData.getHeaterStatus()
        self.actionVariables.LightStatus = self.hardData.getLightStatus()
        self.actionVariables.BlindStatus = self.hardData.getBlindStatus()
        self.actionVariables.DustbinStatus = self.hardData.getDustbinStatus()
        if self.actionVariables.DustbinStatus == "NON-FULL":
            self.stateVariables.DustBinFull = False
        else:
            self.stateVariables.DustBinFull = True
        self.stateVariables.PeopleCount = self.hardData.getPeopleCount()
        self.prevStateVariables.PeopleCount = self.stateVariables.PeopleCount

    def saveData(self):
        self.hardData.setAcStatus(self.actionVariables.AcStatus)
        self.hardData.setHeaterStatus(self.actionVariables.HeaterStatus)
        self.hardData.setLightStatus(self.actionVariables.LightStatus)
        self.hardData.setBlindStatus(self.actionVariables.BlindStatus)
        self.hardData.setDustbinStatus(self.actionVariables.DustbinStatus)
        self.hardData.setPeopleCount(self.stateVariables.PeopleCount)

    def sendBulkData(self):
        message = {
            "value": self.actionVariables.AcStatus
        }
        jmsg = json.dumps(message, indent = 4)
        self.mqtt_pub.publish("Composition/User/U38/0/1/AcStatus", self.actionVariables.AcStatus,2, True)

        message["value"] = self.actionVariables.HeaterStatus
        self.mqtt_pub.publish("Composition/User/U38/0/1/HeaterStatus", self.actionVariables.HeaterStatus,2, True)

        message["value"] = self.actionVariables.LightStatus
        self.mqtt_pub.publish("Composition/User/U38/0/1/LightStatus", self.actionVariables.LightStatus,2, True)

        message["value"] = self.actionVariables.BlindStatus
        self.mqtt_pub.publish("Composition/User/U38/0/1/BlindStatus", self.actionVariables.BlindStatus,2, True)

        message["value"] = self.actionVariables.DustbinStatus
        self.mqtt_pub.publish("Composition/User/U38/0/1/DustbinStatus", self.actionVariables.DustbinStatus,2, True)

        message["value"] = self.stateVariables.PeopleCount
        self.mqtt_pub.publish("Composition/User/U38/0/1/PeopleCount", self.stateVariables.PeopleCount,2, True)

    def on_context_message(self, client, userdata, message):
        print("Message topic {}".format(message.topic))
        print(json.loads(message.payload.decode()))
        # Topic = Context/Composition/U38/0/1/State-Variable

        lTopic = message.topic.split("/")
        parsedMessage = json.loads(message.payload.decode())

        if self.updateState(lTopic[5], parsedMessage) == False:
            print("Value not changed")
            return

        isPeopleCountChange = self.checkForPeopleStateChange()

        if isPeopleCountChange == True and self.stateVariables.PeopleCount == 0:
            self.Plan("Light_OFF_Blind_CLOSE.pddl")
            self.TakeAction()
            self.Plan("Heater_OFF_Cooler_OFF.pddl")
            self.TakeAction()
            return

        if isPeopleCountChange == True == False and self.stateVariables.PeopleCount == 0:
            print("No people in the room, no actuation")
            return

        if isPeopleCountChange == True:
            print("Updating people count")
            self.UpdatePeopleCountStateChange()

        if self.checkForLightingStateChange():
            print("UpdateLigtingState")
            self.UpdateLigtingState()

        if self.checkForTempStateChange():
            self.UpdateTempState()

        if self.checkForDustBinStateChange():
            self.UpdateDustBinStateChange()



    def updateState(self, sVariable, data):
        
        isChanged = False
        if sVariable == "LdrIndoor":
            if self.stateVariables.LdrIndoorData != float(data["value"]["Lux"]):
                isChanged = False
            self.stateVariables.LdrIndoorData = float(data["value"]["Lux"])
        elif sVariable == "LdrOutdoor":
            if self.stateVariables.LdrOutdoorData != float(data["value"]["Lux"]):
                isChanged = True
            self.stateVariables.LdrOutdoorData = float(data["value"]["Lux"])
        elif sVariable == "Temperature":
            if self.stateVariables.TempData != float(data["value"]["celsius"]):
                self.mqtt_pub.publish("Composition/User/U38/0/1/Temperature", int(data["value"]["celsius"]),2, True)
                isChanged = True
            self.stateVariables.TempData = float(data["value"]["celsius"])
        elif sVariable == "InfraredSensor":
            if self.stateVariables.DustBinFull != data["value"]["boolean"]:
                isChanged = True
            self.stateVariables.DustBinFull = data["value"]["boolean"]
        elif sVariable == "PeopleCount":
            if self.stateVariables.PeopleCount !=  int(data["value"]):
                isChanged = True
            self.stateVariables.PeopleCount = int(data["value"])

        return isChanged


    def checkForLightingStateChange(self):

        print("checkForLightingStateChange")

        stateChange = False
        """
        if self.stateVariables.LdrIndoorData != self.prevStateVariables.LdrIndoorData:
            stateChange = True
            self.prevStateVariables.LdrIndoorData = self.stateVariables.LdrIndoorData
        """

        if self.stateVariables.LdrOutdoorData != self.prevStateVariables.LdrOutdoorData:
            stateChange = True
            self.prevStateVariables.LdrOutdoorData = self.stateVariables.LdrOutdoorData 
        return stateChange

    def checkForTempStateChange(self):

        stateChange = False
        if self.stateVariables.TempData != self.prevStateVariables.TempData:
            stateChange = True
            self.prevStateVariables.TempData = self.stateVariables.TempData 
        return stateChange

    def checkForDustBinStateChange(self):

        stateChange = False
        if self.stateVariables.DustBinFull != self.prevStateVariables.DustBinFull:
            stateChange = True
            self.prevStateVariables.DustBinFull = self.stateVariables.DustBinFull 
        return stateChange

    def checkForPeopleStateChange(self):

        stateChange = False
        if self.stateVariables.PeopleCount != self.prevStateVariables.PeopleCount:
            stateChange = True
            self.prevStateVariables.PeopleCount = self.stateVariables.PeopleCount 
        return stateChange

    def UpdateLigtingState(self):

        if self.stateVariables.LdrOutdoorData > MIN_LIGHT and self.stateVariables.LdrOutdoorData < MAX_LIGHT:
            self.Plan("Light_OFF_Blind_OPEN.pddl")

        elif self.stateVariables.LdrOutdoorData <= MIN_LIGHT:
            self.Plan("Light_ON_Blind_OPEN.pddl")

        elif self.stateVariables.LdrOutdoorData >= MAX_LIGHT:
            self.Plan("Light_ON_Blind_CLOSE.pddl")

        self.TakeAction()

    def UpdateTempState(self):

        if self.stateVariables.TempData > MIN_TEMP and self.stateVariables.TempData < MAX_TEMP:
            self.Plan("Heater_OFF_Cooler_OFF.pddl")

        elif self.stateVariables.TempData <= MIN_TEMP:
            self.Plan("Heater_ON_Cooler_OFF.pddl")

        elif self.stateVariables.TempData >= MAX_TEMP:
            self.Plan("Heater_OFF_Cooler_ON.pddl")

        self.TakeAction()

    def UpdateDustBinStateChange(self):

            dustBinStatus = "NON-FULL"
            if self.stateVariables.DustBinFull == True:
                dustBinStatus = "FULL"
            if self.actionVariables.DustbinStatus != dustBinStatus:
                self.actionVariables.DustbinStatus = dustBinStatus
                message = {
                    "value": self.actionVariables.DustbinStatus
                }
                jmsg = json.dumps(message, indent = 4)
                self.mqtt_pub.publish("Composition/User/U38/0/1/DustbinStatus", self.actionVariables.DustbinStatus,2, True)
                self.saveData()

    def UpdatePeopleCountStateChange(self):
        message = {
            "value": self.stateVariables.PeopleCount
        }
        jmsg = json.dumps(message, indent = 4)
        self.mqtt_pub.publish("Composition/User/U38/0/1/PeopleCount", self.stateVariables.PeopleCount,2, True)
        self.saveData()

    def autoCreateProblemFile(self, baseDir, problemFileTemplate):

        print("Creating file")

        lightState = "(not (lState l))"
        if self.actionVariables.LightStatus == "ON":
            lightState = "(lState l)"

        blindState = "(not (bState b))"
        if self.actionVariables.BlindStatus == "OPEN":
            blindState = "(bState b)"

        heaterState = "(not (hState h))"
        if self.actionVariables.HeaterStatus == "ON":
            heaterState = "(hState h)"

        coolerState = "(not (cState c))"
        if self.actionVariables.AcStatus == "ON":
            coolerState = "(cState c)"

        ppdlFileTemplate = baseDir+problemFileTemplate
        print(ppdlFileTemplate)
        print(baseDir+"Problem.pddl")
        fin = open(ppdlFileTemplate, "rt")
        fout = open(baseDir+"Problem.pddl", "wt")

        replaceString = lightState+"\n    "+blindState+"\n    "+heaterState+"\n    "+coolerState
        for line in fin:
            fout.write(line.replace('<Placeholder>', replaceString))

        fin.close()
        fout.close()

        print("File created")


    def Plan(self, problemFileTemplate):
        print("Planning - PPL - " + problemFileTemplate)
        self.autoCreateProblemFile(PPDL_DIR, problemFileTemplate)
        command = PLANNER_DIR+"fast-downward.py " +PPDL_DIR+"Domain.pddl "+PPDL_DIR+"Problem.pddl --search \"astar(blind())\""
        print(command)
        os.system(command)


    def TakeAction(self):

        f = open("sas_plan")
        line = f.readline()
        while line.split()[0] != ";":
            self.Action(line.split())
            line = f.readline()
        f.close()
        self.saveData()
        command = "rm "+PPDL_DIR+"Problem.pddl"
        os.system(command)

    def Action(self, action):

        if action[0] == "(lightswitchon":
            self.actionVariables.LightStatus = "ON"
            message = {
                "value": self.actionVariables.LightStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/LightStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/LightStatus", self.actionVariables.LightStatus,2, True)

        elif action[0] == "(lightswitchoff":
            self.actionVariables.LightStatus = "OFF"
            message = {
                "value": self.actionVariables.LightStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/LightStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/LightStatus", self.actionVariables.LightStatus,2, True)

        elif action[0] == "(closeblind":
            self.actionVariables.BlindStatus = "CLOSE"
            message = {
                "value": self.actionVariables.BlindStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/BlindStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/BlindStatus", self.actionVariables.BlindStatus,2, True)

        elif action[0] == "(openblind":
            self.actionVariables.BlindStatus = "OPEN"
            message = {
                "value": self.actionVariables.BlindStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/BlindStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/BlindStatus", self.actionVariables.BlindStatus,2, True)

        elif action[0] == "(heaterswitchon":
            self.actionVariables.HeaterStatus = "ON"
            message = {
                "value": self.actionVariables.HeaterStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/HeaterStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/HeaterStatus", self.actionVariables.HeaterStatus,2, True)

        elif action[0] == "(heaterswitchoff":
            self.actionVariables.HeaterStatus = "OFF"
            message = {
                "value": self.actionVariables.HeaterStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/HeaterStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/HeaterStatus", self.actionVariables.HeaterStatus,2, True)

        elif action[0] == "(coolerswitchon":
            self.actionVariables.AcStatus = "ON"
            message = {
                "value": self.actionVariables.AcStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/AcStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/AcStatus", self.actionVariables.AcStatus,2, True)

        elif action[0] == "(coolerswitchoff":
            self.actionVariables.AcStatus = "OFF"
            message = {
                "value": self.actionVariables.AcStatus
            }
            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Composition/Execution/U38/0/1/AcStatus", jmsg,2, True)
            self.mqtt_pub.publish("Composition/User/U38/0/1/AcStatus", self.actionVariables.AcStatus,2, True)

