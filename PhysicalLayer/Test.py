import paho.mqtt.client as mqtt
import json
import time
from  datetime import datetime

mqtt_pub =  mqtt.Client("Writer")
mqtt_pub.connect("192.168.0.177", 1883, 70)
mqtt_pub.loop_start()
t = True
while t == True:


    dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
    """
    message = {
        "timestamp": dt,
        "value": {
            "boolean" : False
         }
    }

    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Gateway/Context/U38/0/1/Ultrasonic_Indoor_Sensor", jmsg,2)
    time.sleep(3)

    message = {
        "timestamp": dt,
        "value": {
            "boolean" : False
         }
    }

    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Gateway/Context/U38/0/1/Ultrasonic_Outdoor_Sensor", jmsg,2)
    time.sleep(3)

    message = {
        "timestamp": dt,
        "value": {
            "boolean" : True
         }
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Gateway/Context/U38/0/1/Ultrasonic_Outdoor_Sensor", jmsg,2)
    time.sleep(3)

    message = {
        "timestamp": dt,
        "value": {
            "boolean" : False
         }
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Gateway/Context/U38/0/1/Ultrasonic_Outdoor_Sensor", jmsg,2)
    time.sleep(3)


    message = {
        "timestamp": dt,
        "value": {
            "boolean" : True
         }
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Gateway/Context/U38/0/1/Ultrasonic_Indoor_Sensor", jmsg,2)
    time.sleep(3)

    message = {
        "timestamp": dt,
        "value": {
            "boolean" : False
         }
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Gateway/Context/U38/0/1/Ultrasonic_Indoor_Sensor", jmsg,2)
    time.sleep(3)
    """

    message = {
        "value": "OFF"
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("Execute/Gateway/U38/0/1/Blinds/", jmsg,2)
    time.sleep(1)


    t =  False
