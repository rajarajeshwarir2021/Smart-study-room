import paho.mqtt.client as mqtt
import json
import threading, time

class Gateway:

    def __init__(self, ipAddress):
        print("Gateway started")
        self.mqtt_sub =  mqtt.Client("Listener-Gateway")
        self.mqtt_pub =  mqtt.Client("Writer-Gateway")
        self.ipAddress = ipAddress

        self.mqtt_sub.on_message = self.on_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe([("Sensor/U38/0/1/#",2),("Execute/#",2)])
        #self.mqtt_sub.subscribe([("Sensor/U38/0/1/Ultrasonic_Outdoor_Sensor/#",2),("Sensor/U38/0/1/Ultrasonic_Indoor_Sensor/#",2)])

        self.mqtt_pub.connect(self.ipAddress, 1883, 70)


    def startSense(self):
        self.mqtt_pub.loop_start()
        self.mqtt_sub.loop_forever()


    def on_message(self, client, userdata, message):
        lTopic = message.topic.split("/")
        parsedMessage = json.loads(message.payload.decode())
        jmsg = json.dumps(parsedMessage, indent = 4)
        if str(lTopic[0]) == "Sensor":
            print("Gateway/Context/" + lTopic[1] + "/" + lTopic[2] + "/" + lTopic[3] + "/" + lTopic[4] + "/")
            self.mqtt_pub.publish("Gateway/Context/" + lTopic[1] + "/" + lTopic[2] + "/" + lTopic[3] + "/" + lTopic[4] + "/", jmsg,2)
        elif lTopic[0] == "Execute":
            self.mqtt_pub.publish("Gateway/Actuator/" + lTopic[2] + "/" + lTopic[3] + "/" + lTopic[4] + "/" + lTopic[5] + "/", jmsg,2)
        else:
            print("Invalid gateway sub")

#Gateway("192.168.0.177").startSense()

