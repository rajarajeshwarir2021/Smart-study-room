import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import random
import threading

class InfraredSensor:
    sensor_type = "InfraredSensor"
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

class InfraredSensorNode:

    def __init__(self, ipAddress, interval):
        self.interval = interval
        self.prev_Value = False
        self.isFirstMsg = True
        self.ipAddress = ipAddress

        self.isBackdoorEnable = False
        self.sensorValue = False
        self.mqtt_sub =  mqtt.Client("Backdoor Infrared messages")
        self.mqtt_sub.on_message = self.on_backdoor_message
        self.mqtt_sub.on_connect = self.on_backdoor_connect
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("/backdoor/U38/0/1/Infrared/#", qos=2)

        self.mqtt_pub = mqtt.Client("InfraredSensor publisher")
        self.mqtt_pub.connect(self.ipAddress, 1883, 70)
        self.mqtt_pub.loop_start()

    def start(self):
        threading.Thread(target=self.startReceiving).start()

        print("Started {}".format("InfraredSensorNode"))
        ts = InfraredSensor(0.8)

        while True:
            if self.isBackdoorEnable == False:
                self.sensorValue = ts.sense()
            if self.isFirstMsg==True or self.prev_Value != self.sensorValue:
                self.isFirstMsg = False
                self.prev_Value = self.sensorValue
                dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
                message = {
                    "timestamp":dt,
                    "value":{
                        ts.unit: self.sensorValue
                    }
                }
                jmsg = json.dumps(message, indent = 4)
                self.mqtt_pub.publish("Sensor/U38/0/1/" + ts.sensor_type, jmsg,2)
            time.sleep(self.interval)

    def on_backdoor_connect(self, client, userdata, message):
        print("InfraredSensorNode :: Backdoor connect")

    def on_backdoor_message(self, client, userdata, message):
        print("=======================================")
        print(message.payload.decode())
        parsedMessage = json.loads(message.payload.decode())
        self.isBackdoorEnable = parsedMessage["Enabler"] == "True"
        if self.isBackdoorEnable == True:
            msgVal = parsedMessage["value"]
            self.sensorValue = msgVal == "True"
           

    def startReceiving(self):
        self.mqtt_sub.loop_forever()

#InfraredSensorNode("192.168.0.177", 5).start()
