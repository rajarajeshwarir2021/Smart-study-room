import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import os

class Heater:
    sensor_type = "Heater"
    unit = "String"

    def __init__(self):
        self.heaterStatus = "OFF"

    def setStatus(self, heaterStatus):
        self.heaterStatus = heaterStatus

    def getStatus(self):
        return self.heaterStatus

class HeaterControl:

    def __init__(self, ipAddress):
        self.mqtt_sub = mqtt.Client("Listener-Heater")
        self.objHeater = Heater()
        self.ipAddress = ipAddress

    def start(self):
        print("Started {}".format("Heater Control"))
        self.mqtt_sub.on_message = self.on_gateway_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("Gateway/Actuator/U38/0/1/Heater/#", qos=2)
        self.mqtt_sub.loop_forever()


    def on_gateway_message(self, client, userdata, message):
        parsedMessage = json.loads(message.payload.decode())
        self.objHeater.heaterStatus = parsedMessage["value"]
        os.system("echo \""+self.objHeater.heaterStatus+"\" > Heater_State.txt")
        print("The Heater is switching " + self.objHeater.heaterStatus)


