import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import os

class Blinds:
    sensor_type = "Blinds"
    unit = "String"

    def __init__(self):
        self.blindsStatus = "CLOSE"

    def setStatus(self, blindsStatus):
        self.blindsStatus = blindsStatus

    def getStatus(self):
        return self.blindsStatus	

class BlindsControl:

    def __init__(self, ipAddress):
        self.mqtt_sub = mqtt.Client("Listener-Blinds")
        self.objBlinds = Blinds()
        self.ipAddress = ipAddress

    def start(self):
        print("Started {}".format("Blinds Control"))
        self.mqtt_sub.on_message = self.on_gateway_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 71)
        self.mqtt_sub.subscribe("Gateway/Actuator/U38/0/1/Blinds/#", qos=2)
        self.mqtt_sub.loop_forever()


    def on_gateway_message(self, client, userdata, message):
        parsedMessage = json.loads(message.payload.decode())
        self.objBlinds.blindsStatus = parsedMessage["value"]
        os.system("echo \""+self.objBlinds.blindsStatus+"\" > Blinds_State.txt")
        print("The Blind is " + self.objBlinds.blindsStatus)

