
import threading, time
import sys
from Actuators.Heater import HeaterControl
from Actuators.AirConditioning import AirConditionControl
from Actuators.Blinds import BlindsControl
from Actuators.Lighting import LightingControl

from Sensors.TemperatureNode import TemperatureNode
from Sensors.LdrIndoorNode import LdrIndoorNode
from Sensors.LdrOutdoorNode import LdrOutdoorNode
from Sensors.UltrasonicIndoorSensorNode import UltrasonicIndoorSensorNode
from Sensors.UltrasonicOutdoorSensorNode import UltrasonicOutdoorSensorNode
from Sensors.InfraredSensorNode import InfraredSensorNode

ipAddress = sys.argv[1]

print("Starting all the actuator nodes in Room 1, floor 0, building u38")

def heater():
    HeaterControl(ipAddress).start()

def ac():
    AirConditionControl(ipAddress).start()

def blinds():
    BlindsControl(ipAddress).start()

def light():
    LightingControl(ipAddress).start()

def Ldr1():
    LdrIndoorNode(ipAddress, 2).start()

def Ldr2():
    LdrOutdoorNode(ipAddress,2).start()

def Temp():
    TemperatureNode(ipAddress, 2).start()

def Ultr1():
    UltrasonicIndoorSensorNode(ipAddress, 2).start()

def Ultr2():
    UltrasonicOutdoorSensorNode(ipAddress, 2).start()

def Infra():
    InfraredSensorNode(ipAddress, 2).start()

threading.Thread(target=heater).start()
threading.Thread(target=ac).start()
threading.Thread(target=blinds).start()
threading.Thread(target=light).start()


threading.Thread(target=Ldr1).start()
threading.Thread(target=Ldr2).start()
threading.Thread(target=Temp).start()
threading.Thread(target=Ultr1).start()
threading.Thread(target=Ultr2).start()
threading.Thread(target=Infra).start()

