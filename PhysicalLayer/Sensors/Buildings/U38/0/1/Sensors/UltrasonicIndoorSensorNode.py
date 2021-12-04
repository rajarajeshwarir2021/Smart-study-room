import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import random
import threading

class UltrasonicIndoorSensor:
    sensor_type = "Ultrasonic_Indoor_Sensor"
    unit = "boolean"

    def __init__(self, prob):
        self.prob = prob
        self.value = False


    def sense(self):
        if random.random() > self.prob:
            self.value = True
        else:
            self.value = False
        return self.value


class UltrasonicIndoorSensorNode:

    def __init__(self, ipAddress, interval):
        self.interval = interval
        self.prev_Value = False
        self.isFirstMsg = True
        self.ipAddress = ipAddress

        self.isBackdoorEnable = False
        self.sensorValue = False
        self.mqtt_sub =  mqtt.Client("Backdoor Indoor_US messages")
        self.mqtt_sub.on_message = self.on_backdoor_message
        self.mqtt_sub.on_connect = self.on_backdoor_connect
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("backdoor/U38/0/1/Ultrasonic_Indoor_Sensor/#", qos=2)

        self.mqtt_pub = mqtt.Client("Ultrasonic_Indoor_Sensor publisher")
        self.mqtt_pub.connect(self.ipAddress, 1883, 70)
        self.mqtt_pub.loop_start()

    def start(self):
        threading.Thread(target=self.startReceiving).start()

        print("Started {}".format("UltrasonicIndoorSensor"))
        ts = UltrasonicIndoorSensor(0.8)

        while True:
            if self.isBackdoorEnable == False:
                self.sensorValue = ts.sense()
            if self.isBackdoorEnable!= True and (self.isFirstMsg==True or self.prev_Value != self.sensorValue):
                self.isFirstMsg = False
                self.prev_Value = self.sensorValue
                dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
                messageCustom = {
                    "timestamp":dt,
                    "value":{
                        ts.unit: self.sensorValue
                    }
                }
                jmsg = json.dumps(messageCustom, indent = 4)
                self.mqtt_pub.publish("Sensor/U38/0/1/Ultrasonic_Indoor_Sensor", jmsg,2)
            time.sleep(self.interval)

    def on_backdoor_connect(self, client, userdata, message):
        print("UltrasonicIndoorSensorNode :: Backdoor connect")

    def on_backdoor_message(self, client, userdata, message):
        print("=======================================")
        print(message.payload.decode())
        parsedMessage = json.loads(message.payload.decode())
        print(parsedMessage)
        self.isBackdoorEnable = parsedMessage["Enabler"] == "True"
        print(self.isBackdoorEnable)
        if self.isBackdoorEnable == True:
            msgVal = parsedMessage["value"]
            self.sensorValue = msgVal == "True"
            self.prev_Value = self.sensorValue
            dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
            messageCustom = {
                "timestamp":"Simulated",
                "value":{
                    "boolean": self.sensorValue
                }
            }
            jmsg = json.dumps(messageCustom, indent = 4)
            self.mqtt_pub.publish("Sensor/U38/0/1/Ultrasonic_Indoor_Sensor", jmsg,2)
           

    def startReceiving(self):
        self.mqtt_sub.loop_forever()



#UltrasonicIndoorSensorNode("192.168.0.177", 5).start()

#UltrasonicIndoorSensorNode(2).start()
