import time
from  datetime import datetime
import json
import paho.mqtt.client as mqtt
from random import random
import threading
from random import uniform

class TemperatureSensor:
    sensor_type = "Temperature"
    unit = "celsius"

    def __init__(self, average_temperature, temperature_variation, min_temp, max_temp):
        self.average_temperature = average_temperature
        self.temperature_variation = temperature_variation
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.value = 0.0


    def sense(self):
        self.value = self.simple_random()
        return self.value

    def simple_random(self):
        value = uniform(self.min_temp, self.max_temp)
        return value

    def complex_random(self):
        value = self.average_temperature * (1 + (self.temperature_variation/100) * (3*random() -1))
        value = max(value, self.min_temp)
        value = min(value, self.max_temp)
        return value
        



class TemperatureNode:

    def __init__(self, ipAddress, interval):
        self.interval = interval
        self.ipAddress = ipAddress

        self.isBackdoorEnable = False
        self.sensorValue = 0.0
        self.mqtt_sub =  mqtt.Client("Backdoor Temperature messages")
        self.mqtt_sub.on_message = self.on_backdoor_message
        self.mqtt_sub.on_connect = self.on_backdoor_connect
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe("/backdoor/U38/0/1/Temperature/#", qos=2)

        self.mqtt_pub = mqtt.Client("Temperature publisher")
        self.mqtt_pub.connect(self.ipAddress, 1883, 70)
        self.mqtt_pub.loop_start()

    def start(self):
        threading.Thread(target=self.startReceiving).start()

        print("Started {}".format("TemperatureNode"))
        ts = TemperatureSensor(20,30,16,35)

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
        print("TemperatureNode :: Backdoor connect")

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

#TemperatureNode("192.168.0.177", 5).start()


