import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
import threading
from random import random
from random import uniform

class LdrIndoorSensor:
    sensor_type = "LdrIndoor"
    unit = "Lux"

    def __init__(self, average_light_Intensity, light_Intensity_variation, min_intensity, max_intensity):
        self.average_light_Intensity = average_light_Intensity
        self.light_Intensity_variation = light_Intensity_variation
        self.min_intensity = min_intensity
        self.max_intensity = max_intensity
        self.value = 0.0

    def sense(self):
        self.value = self.simple_random()
        return self.value

    def simple_random(self):
        value = uniform(self.min_intensity, self.max_intensity)
        return value


class LdrIndoorNode:

    def __init__(self, ipAddress, interval):
        self.interval = interval
        self.ipAddress = ipAddress

        self.isBackdoorEnable = False
        self.sensorValue = 0.0
        self.mqtt_sub =  mqtt.Client("Backdoor LdrIndoor messages")
        self.mqtt_sub.on_message = self.on_backdoor_message
        self.mqtt_sub.on_connect = self.on_backdoor_connect
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("/backdoor/U38/0/1/LdrIndoor/#", qos=2)

        self.mqtt_pub = mqtt.Client("Indoor light publisher")
        self.mqtt_pub.connect(self.ipAddress, 1883, 70)
        self.mqtt_pub.loop_start()

    def start(self):
        threading.Thread(target=self.startReceiving).start()

        print("Started {}".format("LdrIndoorNode"))
        ts = LdrIndoorSensor(20,30,0,1000)

        while True:
            if self.isBackdoorEnable == False:
                self.sensorValue = ts.sense()
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
        print("LdrIndoorNode :: Backdoor connect")

    def on_backdoor_message(self, client, userdata, message):
        print("=======================================")
        print(message.payload.decode())
        parsedMessage = json.loads(message.payload.decode())
        self.isBackdoorEnable = parsedMessage["Enabler"] == "True"
        if self.isBackdoorEnable == True:
            msgVal = parsedMessage["value"]
            self.sensorValue = float(msgVal)
           

    def startReceiving(self):
        self.mqtt_sub.loop_forever()

#LdrIndoorNode("192.168.0.177", 5).start()
