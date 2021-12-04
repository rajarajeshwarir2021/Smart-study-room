import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import os

class Lighting:
    sensor_type = "Lighting"
    unit = "String"

    def __init__(self):
        self.lightingStatus = "OFF"

    def setStatus(self, lightingStatus):
        self.lightingStatus = lightingStatus

    def getStatus(self):
        return self.lightingStatus	

class LightingControl:

    def __init__(self, ipAddress):
        self.mqtt_sub = mqtt.Client("Listener-Lighting")
        self.objLighting = Lighting()
        self.ipAddress = ipAddress

    def start(self):
        print("Started {}".format("Lighting Control"))
        self.mqtt_sub.on_message = self.on_gateway_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("Gateway/Actuator/U38/0/1/Lighting/#", qos=2)
        self.mqtt_sub.loop_forever()

    def on_gateway_message(self, client, userdata, message):
        parsedMessage = json.loads(message.payload.decode())
        self.objLighting.lightingStatus = parsedMessage["value"]
        os.system("echo \""+self.objLighting.lightingStatus+"\" > Lighting_State.txt")
        print("The Lighting is switching " + self.objLighting.lightingStatus)

