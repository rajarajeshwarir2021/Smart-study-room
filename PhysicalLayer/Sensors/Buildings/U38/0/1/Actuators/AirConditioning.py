import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import os

class AirCondition:
    sensor_type = "AirCondition"
    unit = "String"

    def __init__(self):
        self.acStatus = "OFF"


    def setStatus(self, acStatus):
        self.acStatus = acStatus

    def getStatus(self):
        return self.acStatus

class AirConditionControl:

    def __init__(self, ipAddress):
        self.mqtt_sub = mqtt.Client("Listener-AirCondition")
        self.objAirCondition = AirCondition()
        self.ipAddress = ipAddress

    def start(self):
        print("Started {}".format("AirCondition Control"))
        self.mqtt_sub.on_message = self.on_gateway_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("Gateway/Actuator/U38/0/1/AirCondition/#", qos=2)
        self.mqtt_sub.loop_forever()

    def on_gateway_message(self, client, userdata, message):
        parsedMessage = json.loads(message.payload.decode())
        self.objAirCondition.acStatus = parsedMessage["value"]
        command = "echo \""+self.objAirCondition.acStatus+"\" > AirCondition_State.txt"
        os.system(command)
        print("The Aircontioning is switching " + self.objAirCondition.acStatus)

#AirConditionControl("192.168.0.177").start()
        

