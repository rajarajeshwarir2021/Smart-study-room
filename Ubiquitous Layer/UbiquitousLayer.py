import paho.mqtt.client as mqtt
import json
from UbiquitousLayerDB import UbiquitousLayerDB
import collections
import time
from  datetime import datetime

class UbiquitousLayer:

    def __init__(self, ipAddress):

        self.UbiquitousLayerDBobj = UbiquitousLayerDB()
        self.mqtt_sub =  mqtt.Client("Listener-UbiquitousLayer")
        self.mqtt_pub =  mqtt.Client("Writer-UbiquitousLayer")
        self.ipAddress = ipAddress

        self.mqtt_sub.on_message = self.on_message
        self.mqtt_sub.connect(self.ipAddress, 1883, 70)
        self.mqtt_sub.subscribe([("Gateway/Context/#",2),("Composition/Execution/#",2)])

        self.mqtt_pub.connect(self.ipAddress, 1883, 70)
        self.mqtt_pub.loop_start()
        
        self.Out_Us_queue = collections.deque()
        self.In_Us_queue = collections.deque()

        self.pepIterator = 0
        self.pepOutdoor = 0
        self.pepIndoor = 0

    def on_message(self, client, userdata, message):

        lTopic = message.topic.split("/")
        
        if lTopic[1] == "Context":
            self.updateSensorParam(message)
        elif lTopic[1] == "Execution":
            self.updateActuatorParam(message)
        else:
            print("Invalid-Command")

    def updateSensorParam(self, message):
        parsedMessage = json.loads(message.payload.decode())
        lTopic = message.topic.split("/")

        print(lTopic)
        print(parsedMessage)

        sensorVal = lTopic[5]
        
        if sensorVal == "LdrIndoor":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Sensor/U38/0/1/LdrIndoor/'", str(parsedMessage["value"]["Lux"]))
        elif sensorVal == "LdrOutdoor":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Sensor/U38/0/1/LdrOutdoor/'", str(parsedMessage["value"]["Lux"]))
        elif sensorVal == "Temperature":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Sensor/U38/0/1/Temperature/'", str(parsedMessage["value"]["celsius"]))
        elif sensorVal == "Ultrasonic_Outdoor_Sensor":
            val = "False"
            if parsedMessage["value"]["boolean"] == True:
                val = "True"
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Sensor/U38/0/1/Ultrasonic_Outdoor_Sensor/'", str(parsedMessage["value"]["boolean"]))

            self.Out_Us_queue.append(val)
            if len(self.Out_Us_queue) > 3:
                self.Out_Us_queue.popleft()
          
            if self.checkValidTransition(self.Out_Us_queue):
                self.pepIterator = self.pepIterator + 1
                self.pepOutdoor = self.pepIterator
                self.updatePeopleCount()
 
        elif sensorVal == "Ultrasonic_Indoor_Sensor":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Sensor/U38/0/1/Ultrasonic_Indoor_Sensor/'", str(parsedMessage["value"]["boolean"]))
            val = "False"
            if parsedMessage["value"]["boolean"] == True:
                val = "True"
            self.In_Us_queue.append(val)
            if len(self.In_Us_queue) > 3:
                self.In_Us_queue.popleft()
          
            if self.checkValidTransition(self.In_Us_queue):
                self.pepIterator = self.pepIterator + 1
                self.pepIndoor = self.pepIterator
                self.updatePeopleCount()

        elif sensorVal == "InfraredSensor":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Sensor/U38/0/1/InfraredSensor/'", str(parsedMessage["value"]["boolean"]))
 
        jmsg = json.dumps(parsedMessage, indent = 4)
        self.mqtt_pub.publish("Context/Composition/U38/0/1/" + sensorVal, jmsg,2)


    def checkValidTransition(self, container):
        if len(container) == 3 and container[0] == "False" and container[1] == "True" and container[2] == "False":
            return True
        return False

    def updatePeopleCount(self):
        if self.pepIterator == 2:
            print("Person In/Out complete transition")
            peopleCount = int(self.UbiquitousLayerDBobj.read_data("'U38/0/1/PeopleCount/'")[2])
            if self.pepOutdoor == 2:
                peopleCount = peopleCount - 1
            elif self.pepIndoor == 2:
                peopleCount = peopleCount + 1

            print("Person Count = " + str(peopleCount))
            self.UbiquitousLayerDBobj.write_data("Simulated", "'U38/0/1/PeopleCount/'", str(peopleCount))
            self.pepIterator = 0
            self.pepOutdoor = 0
            self.pepIndoor = 0
            dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
            message = {
                "timestamp":dt,
                "value":peopleCount
            }

            jmsg = json.dumps(message, indent = 4)
            self.mqtt_pub.publish("Context/Composition/U38/0/1/PeopleCount", jmsg,2)

    def updateActuatorParam(self, message):
        parsedMessage = json.loads(message.payload.decode())
        lTopic = message.topic.split("/")
        actuator = lTopic[5]
        
        if actuator == "AirCondition":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Actuator/U38/0/1/AirCondition/'", str(parsedMessage["value"]))
        elif actuator == "Blinds":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Actuator/U38/0/1/Blinds/'", str(parsedMessage["value"]))
        elif actuator == "Heater":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Actuator/U38/0/1/Heater/'", str(parsedMessage["value"]))
        elif actuator == "Lighting":
            self.UbiquitousLayerDBobj.write_data(parsedMessage["timestamp"], "'Actuator/U38/0/1/Lighting/'", str(parsedMessage["value"]))

        jmsg = json.dumps(parsedMessage, indent = 4)
        self.mqtt_pub.publish("Execute/Gateway/U38/0/1/" + actuator, jmsg,2)


    def start(self):
        self.mqtt_sub.loop_forever()


