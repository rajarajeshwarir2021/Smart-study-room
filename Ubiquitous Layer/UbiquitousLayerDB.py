#!/usr/bin/python

import sqlite3
import time
import datetime

class UbiquitousLayerDB:

    def __init__(self):
        self.conn = sqlite3.connect('UbiquitousLayer.db')
        self.Lt = self.conn.cursor() # a cursor for the database

        self.LdrIndoorData = "0"
        self.LdrOutdoorData = "0"
        self.TempData = "0"
        self.UsIndoorData = "False"
        self.UsOutdoorData = "False"
        self.InfraredData = "False"
   
        self.AcStatus = "OFF"
        self.HeaterStatus = "OFF"
        self.LightStatus = "OFF"
        self.BlindStatus = "CLOSE"

        self.PeopleCount = "0"


        self.Lt.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Data' ''')
        if self.Lt.fetchone()[0]==1: 
            self.readCompleteData()
        else:
            self.Lt.execute('CREATE TABLE IF NOT EXISTS Data(Datestmp TEXT,Topic TEXT,Data TEXT )') # creating a table
            result = self.Lt.fetchone()
            self.Reset_data()

    def Reset_data(self):
        unix = int( time.time())
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Sensor/U38/0/1/LdrIndoor/','1'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Sensor/U38/0/1/LdrOutdoor/','1'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Sensor/U38/0/1/Temperature/','1'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Sensor/U38/0/1/Ultrasonic_Indoor_Sensor/','False'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Sensor/U38/0/1/Ultrasonic_Outdoor_Sensor/','False'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Sensor/U38/0/1/InfraredSensor/','1'))

        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Actuator/U38/0/1/AcStatus/','OFF'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Actuator/U38/0/1/HeaterStatus/','OFF'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Actuator/U38/0/1/LightStatus/','OFF'))
        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'Actuator/U38/0/1/BlindStatus/','CLOSE'))

        self.Lt.execute("INSERT INTO Data(Datestmp,Topic,Data)VALUES (?,?,?)",(date,'U38/0/1/PeopleCount/','0'))

        self.conn.commit()


    def write_data(self, date, topic, data):
        print("Update Data SET Data =\"" + data + "\" WHERE Topic =" + topic )
        print("Update Data SET Datestmp =\"" + date + "\" WHERE Topic =" + topic )
        self.Lt.execute("Update Data SET Data =\"" + data + "\" WHERE Topic =" + topic )
        print("write_data1")
        self.Lt.execute("Update Data SET Datestmp =\"" + date + "\" WHERE Topic =" + topic )
        print("write_data2")
        self.conn.commit()

    def read_data(self, topic):
        self.Lt.execute("SELECT * FROM Data WHERE Topic =" + topic )
        result = self.Lt.fetchone()
        return result

    def closeDb(self):
        self.Lt.close()
        self.conn.close()

    def readCompleteData(self):

        self.LdrIndoorData = self.read_data("'Sensor/U38/0/1/LdrIndoor/'")[2]
        self.LdrOutdoorData = self.read_data("'Sensor/U38/0/1/LdrOutdoor/'")[2]
        self.TempData = self.read_data("'Sensor/U38/0/1/Temperature/'")[2]
        self.UsIndoorData = self.read_data("'Sensor/U38/0/1/Ultrasonic_Indoor_Sensor/'")[2]
        self.UsOutdoorData = self.read_data("'Sensor/U38/0/1/Ultrasonic_Outdoor_Sensor/'")[2]
        self.InfraredData = self.read_data("'Sensor/U38/0/1/InfraredSensor/'")[2]
   
        self.AcStatus = self.read_data("'Actuator/U38/0/1/AcStatus/'")[2]
        self.HeaterStatus = self.read_data("'Actuator/U38/0/1/HeaterStatus/'")[2]
        self.LightStatus = self.read_data("'Actuator/U38/0/1/LightStatus/'")[2]
        self.BlindStatus = self.read_data("'Actuator/U38/0/1/BlindStatus/'")[2]

        self.PeopleCount = self.read_data("'U38/0/1/PeopleCount/'")[2]
        print("Read Complete Data")
 

"""
x = sensorDatabase()
x.write_data("sdsd", "'Sensor/U38/0/1/LdrIndoor/'", "100")
print(x.read_data("'Sensor/U38/0/1/LdrIndoor/'")[2])
x.write_data("sdsd", "'Sensor/U38/0/1/LdrIndoor/'", "110")
print(x.read_data("'Sensor/U38/0/1/LdrIndoor/'")[2])

"""

