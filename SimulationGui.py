from tkinter import *
from tkinter.ttk import Combobox
import json
import paho.mqtt.client as mqtt
import time

window=Tk()

mqtt_pub = mqtt.Client("Backdoor")
mqtt_pub.connect("192.168.0.177", 1883, 70)
mqtt_pub.loop_start()

labelframe = LabelFrame(padx = 10, pady = 20, text="Backdoor Controls")
labelframe.pack(padx=10, pady=5, fill="both", expand="yes")

enableUSsensorOverride = IntVar()
C1 = Checkbutton(labelframe, text = "Enable People Movement Backdoor", variable = enableUSsensorOverride)
C1.place(x=10, y=0)


buildingData =("U38", "P47", "P58")
floorData=("0", "1", "2", "3")
roomData=("1", "2", "3", "4")

cbBuilding=Combobox(labelframe, height = 1, width = 4, values=buildingData)
cbBuilding.place(x=10, y=30)

cbFloor=Combobox(labelframe, height = 1, width = 4, values=floorData)
cbFloor.place(x=110, y=30)

cbRoom=Combobox(labelframe, height = 1, width = 4, values=roomData)
cbRoom.place(x=210, y=30)

def sendUsIndoor(sStatus):
    enabler = "False"
    if enableUSsensorOverride.get() == 1:
        enabler = "True"
    message = {
        "Enabler":enabler,
        "value":sStatus
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("backdoor/U38/0/1/Ultrasonic_Indoor_Sensor/", jmsg,2)
    print("Sending data Indoor")

def sendUsOutdoor(sStatus):
    enabler = "False"
    if enableUSsensorOverride.get() == 1:
        enabler = "True"
    message = {
        "Enabler":enabler,
        "value":sStatus
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("backdoor/U38/0/1/Ultrasonic_Outdoor_Sensor/", jmsg,2)
    print("Sending data Outdoor")

def goInside():
    sendUsOutdoor("False")
    time.sleep(1)
    sendUsOutdoor("True")
    time.sleep(1)
    sendUsOutdoor("False")
    time.sleep(1)
    sendUsIndoor("False")
    time.sleep(1)
    sendUsIndoor("True")
    time.sleep(1)
    sendUsIndoor("False")
    time.sleep(1)

def goOutside():
    sendUsIndoor("False")
    time.sleep(1)
    sendUsIndoor("True")
    time.sleep(1)
    sendUsIndoor("False")
    time.sleep(1)
    sendUsOutdoor("False")
    time.sleep(1)
    sendUsOutdoor("True")
    time.sleep(1)
    sendUsOutdoor("False")
    time.sleep(1)

goInsideBtn=Button(labelframe, text="Go Inside", command=goInside, height = 1, width = 10, fg='black')
goInsideBtn.place(x=10, y=80)

sendOutBtn=Button(labelframe, text="Go Outside", command=goOutside, height = 1, width = 10, fg='black')
sendOutBtn.place(x=150, y=80)

"""
peopleCountText= Label(labelframe, height = 1, text = "Number of People inside are:")
peopleCountText.place(x=10, y=140)

peopleCountBox = Label(labelframe, height=2, width=10, text = "0")
peopleCountBox.place(x=200, y=140)

"""


isOverrideTemp = IntVar()
OverrideTemp = Checkbutton(labelframe, text = "", variable = isOverrideTemp)
OverrideTemp.place(x=10, y=150)

tempText = Label(labelframe, text = "Temp sensor Value")
tempText.place(x=40, y= 150)

tempVal=Text(labelframe, height = 1, width = 4)
tempVal.place(x=200, y= 150)

def sendTempData():
    enabler = "False"
    if isOverrideTemp.get() == 1:
        enabler = "True"
    value = int(tempVal.get("1.0", "end"))
    message = {
        "Enabler": enabler,
        "value":value
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("/backdoor/U38/0/1/Temperature/", jmsg,2)

tempBtn=Button(labelframe, text="Send Data", command=sendTempData, height = 1, width = 10, fg='black')
tempBtn.place(x=250, y=150)

isOverrideLdr = IntVar()
OverrideLdr = Checkbutton(labelframe, text = "", variable = isOverrideLdr)
OverrideLdr.place(x=10, y=190)

lightText = Label(labelframe, text = "Ldr-In sensor Value")
lightText.place(x=40, y= 190)

lightVal=Text(labelframe, height = 1, width = 4)
lightVal.place(x=200, y=190)

def sendLightData():
    enabler = "False"
    if isOverrideLdr.get() == 1:
        enabler = "True"
    value = int(lightVal.get("1.0", "end"))
    message = {
        "Enabler":enabler,
        "value":value
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("/backdoor/U38/0/1/LdrIndoor/", jmsg,2)

lightBtn=Button(labelframe, text="Send Data", command=sendLightData, height = 1, width = 10, fg='black')
lightBtn.place(x=250, y=190)

isOverrideLdrOutdoor = IntVar()
OverrideLdrOutdoor = Checkbutton(labelframe, text = "", variable = isOverrideLdrOutdoor)
OverrideLdrOutdoor.place(x=10, y=230)

ldrOutText = Label(labelframe, text = "Ldr-Out sensor Value")
ldrOutText.place(x=40, y= 230)

ldrOutVal=Text(labelframe, height = 1, width = 4)
ldrOutVal.place(x=200, y= 230)

def sendLdrOutData():
    enabler = "False"
    if isOverrideLdrOutdoor.get() == 1:
        enabler = "True"
    value = int(ldrOutVal.get("1.0", "end"))
    message = {
        "Enabler":enabler,
        "value":value
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("/backdoor/U38/0/1/LdrOutdoor/", jmsg,2)

ldrOutTextBtn=Button(labelframe, text="Send Data", command=sendLdrOutData, height = 1, width = 10, fg='black')
ldrOutTextBtn.place(x=250, y=230)

isOverrideInfrared = IntVar()
OverrideInfrared = Checkbutton(labelframe, text = "", variable = isOverrideInfrared)
OverrideInfrared.place(x=10, y=270)

xText = Label(labelframe, text = "Infrared sensor Value")
xText.place(x=40, y= 270)

#xVal=Text(labelframe, height = 1, width = 4)
#xVal.place(x=200, y= 350)

isInfraredEnable = IntVar()
InfraredEnable = Checkbutton(labelframe, text = "", variable = isInfraredEnable)
InfraredEnable.place(x=200, y=270)

def sendInfraredData():
    enabler = "False"
    if isOverrideInfrared.get() == 1:
        enabler = "True"

    if isInfraredEnable.get() == 1:
        value = "True"
    else:
        value = "False"

    message = {
        "Enabler":enabler,
        "value":value
    }
    jmsg = json.dumps(message, indent = 4)
    mqtt_pub.publish("/backdoor/U38/0/1/Infrared/", jmsg,2)

xTextBtn=Button(labelframe, text="Send Data", command=sendInfraredData, height = 1, width = 10, fg='black')
xTextBtn.place(x=250, y=270)

window.title('Backdoor')
window.geometry("500x400+10+10")
window.mainloop()
