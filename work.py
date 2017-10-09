################################################################
# TPMS Integration -09-2017
################################################################

import serial
import binascii
import sys
import bluetooth
from bluetooth import*
import socket
import time
import sqlite3
from sqlite3 import Error
import __main__
from pip._vendor.pkg_resources import null_ns_handler

import db
import rfid
import blecontroller
from blecontroller import *

#Variable Decleration
s = 'hello'
data = []
rfidTID_hex = []
rfidTID = []
cksm = []
vehID = 0
vehName = ""
BUID = ""
RFUID = ""
#tag_id = ""

tup1=()
_DBSensorID = []
_DBLocation = []


database = "/opt/Aquire/sqlite/Sample.db"
TID1 = "e2000016351702081640767f"
tag_id = "e2000016351702081640767f"
vehID = 32
BUID = '00:13:EF:C0:02:1E'



# Start Query the DB with RFID TID
def db_DeviceDetails_by_rfiduid():

    print("Create a database connection to the DB file .db")
    conn = db.create_db_connection(database)
    
    #print tag_id
    print("Query the database to read Vehicle Details by RFUID")
    #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, "RFID 1")

    with conn:
        vehDetail = db.select_DeviceDetails_by_rfiduid(conn, tag_id)

    if (vehDetail != None):
        vehID = vehDetail[0]
        vehName = vehDetail[1]
        BUID = vehDetail[2]
        RFUID = vehDetail[3]

        #print vehID, vehName, BUID, RFUID

    return vehID, vehName, BUID, RFUID
'''

# Start Query the DB with vehID to get Tyre Details
def db_DeviceDetails_by_vehID(vehID1):

    print("Create a database connection to the DB file .db")
    conn = db.create_db_connection(database)
    
    #print vehID
    print("Query the database to read Tyre Details by vehID")
    #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, vehID)

    with conn:
        TyreDetail = db.select_TyreDetails_by_VehId(conn, 24)
        #print TyreDetail
    if (TyreDetail != None):

     
        if(TyreDetail[0] != None):
            Tyre_row1 = TyreDetail[0]

            SID1, L1 = Tyre_row1[0], Tyre_row1[1]
            print SID1, L1
            
        if(TyreDetail[1] != None):
            Tyre_row2 = TyreDetail[1]

            SID2, L2 = Tyre_row2[0], Tyre_row2[1]
            print SID2, L2
            
        if(TyreDetail[2] != None):
            Tyre_row3 = TyreDetail[2]

            SID3, L3 = Tyre_row3[0], Tyre_row3[1]
            print SID3, L3

        if(TyreDetail[3] != None):
            Tyre_row4 = TyreDetail[3]

            SID4, L4 = Tyre_row4[0], Tyre_row4[1]
            print SID4, L4

        if(TyreDetail[4] != None):
            Tyre_row5 = TyreDetail[4]

            SID5, L5 = Tyre_row5[0], Tyre_row5[1]
            print SID5, L5

        if(TyreDetail[5] != None):
            Tyre_row6 = TyreDetail[5]

            SID6, L6 = Tyre_row6[0], Tyre_row6[1]
            print SID6, L6
       
        
    
    print("Close a database connection to the DB file .db")
    conn.close()
    
    #return vehID, vehName, BUID, RFUID

'''

# Start Query the DB with vehID to get Tyre Details
# Assign Location  by value
# FL = 01, FR = 02, RLO = 03, RLI = 04, RRI = 05, RRO = 06
def db_DeviceDetails_by_vehID(vehID1):

    print("Create a database connection to the DB file .db")
    conn = db.create_db_connection(database)
    
    #print vehID
    print("Query the database to read Tyre Details by vehID")
    #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, vehID)

    with conn:
        TyreDetail = db.select_TyreDetails_by_VehId(conn, vehID1)
        #print TyreDetail
    if (TyreDetail != None):

     
        if(TyreDetail[0] != None):
            Tyre_row1 = TyreDetail[0]

            SID1 = Tyre_row1[0]
            
            if Tyre_row1[1] == "FL":
                L1 = "01"
            elif Tyre_row1[1] == "FR":
                L1 = "02"
            elif Tyre_row1[1] == "RLO":
                L1 = "03"
            elif Tyre_row1[1] == "RLI":
                L1 = "04"
            elif Tyre_row1[1] == "RRO":
                L1 = "05"
            elif Tyre_row1[1] == "RRI":
                L1 = "06"
                
            #print SID1, L1
            
        if(TyreDetail[1] != None):
            Tyre_row2 = TyreDetail[1]

            SID2 = Tyre_row2[0]

            if Tyre_row2[1] == "FL":
                L2 = "01"
            elif Tyre_row2[1] == "FR":
                L2 = "02"
            elif Tyre_row2[1] == "RLO":
                L2 = "03"
            elif Tyre_row2[1] == "RLI":
                L2 = "04"
            elif Tyre_row2[1] == "RRO":
                L2 = "05"
            elif Tyre_row2[1] == "RRI":
                L2 = "06"
                
            #print SID2, L2
            
        if(TyreDetail[2] != None):
            Tyre_row3 = TyreDetail[2]

            SID3 = Tyre_row3[0]

            if Tyre_row3[1] == "FL":
                L3 = "01"
            elif Tyre_row3[1] == "FR":
                L3 = "02"
            elif Tyre_row3[1] == "RLO":
                L3 = "03"
            elif Tyre_row3[1] == "RLI":
                L3 = "04"
            elif Tyre_row3[1] == "RRO":
                L3 = "05"
            elif Tyre_row3[1] == "RRI":
                L3 = "06"
                
            #print SID3, L3

        if(TyreDetail[3] != None):
            Tyre_row4 = TyreDetail[3]

            SID4 = Tyre_row4[0]

            if Tyre_row4[1] == "FL":
                L4 = "01"
            elif Tyre_row4[1] == "FR":
                L4 = "02"
            elif Tyre_row4[1] == "RLO":
                L4 = "03"
            elif Tyre_row4[1] == "RLI":
                L4 = "04"
            elif Tyre_row4[1] == "RRO":
                L4 = "05"
            elif Tyre_row4[1] == "RRI":
                L4 = "06"
                
            #print SID4, L4

        if(TyreDetail[4] != None):
            Tyre_row5 = TyreDetail[4]

            SID5 = Tyre_row5[0]

            if Tyre_row5[1] == "FL":
                L5 = "01"
            elif Tyre_row5[1] == "FR":
                L5 = "02"
            elif Tyre_row5[1] == "RLO":
                L5 = "03"
            elif Tyre_row5[1] == "RLI":
                L5 = "04"
            elif Tyre_row5[1] == "RRO":
                L5 = "05"
            elif Tyre_row5[1] == "RRI":
                L5 = "06"
                
            #print SID5, L5

        if(TyreDetail[5] != None):
            Tyre_row6 = TyreDetail[5]

            SID6 = Tyre_row6[0]

            if Tyre_row6[1] == "FL":
                L6 = "01"
            elif Tyre_row6[1] == "FR":
                L6 = "02"
            elif Tyre_row6[1] == "RLO":
                L6 = "03"
            elif Tyre_row6[1] == "RLI":
                L6 = "04"
            elif Tyre_row6[1] == "RRO":
                L6 = "05"
            elif Tyre_row6[1] == "RRI":
                L6 = "06"
                
            #print SID6, L6
       
        
    
    print("Close a database connection to the DB file .db")
    conn.close()
    return SID1, L1, SID2, L2, SID3, L3, SID4,L4, SID5,L5, SID6,L6
     
# Start Connecting the Socket by BUID
def Connect_Socket_Bluetooth_by_BUID( conn):

    #print("Create a Bluetooth connection")
    #conn = blecontroller.connect_ble(BUID)
   
    #blecontroller.Tpms_Tire_SET_Position1(SID1, L1)
    #print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
    #data = blecontroller.Query_Tpms_SET_TireID(conn)

    print("Query the Bluetooth Controller with 63 to read All TyreNo, Sensor ID, Pressure and Temp")
    TPMSID1 = blecontroller.TpmsTireDataPosition()

    print("Query the Bluetooth Controller to read TyreNo, Sensor ID, Pressure and Temp")
    data = blecontroller.Query_TpmsTireDataPosition(conn, TPMSID1)

    print("Parse the hex data string TyreNo, Sensor ID, Pressure and Temp")    
    Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
    Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
    Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
    Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
    Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
    Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = blecontroller.ParseBluetoothTyre(data)

    ''' 
    print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
          Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
          Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
          Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
          Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
          Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp

    '''
    #print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID()
    

    return Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
           Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
           Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
           Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
           Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
           Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp



           

def compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(conn, DBSensorVariable, BluetoothSocketVariable):

    print DBSensorVariable
    print BluetoothSocketVariable
    
    for i in range(len(DBSensorVariable)):
        
        for v in range(len(BluetoothSocketVariable)):                  

            #Check 01 Location and Related Sensor ID
            if(DBSensorVariable[i] == "01"):
                _DBSensorID1 =  DBSensorVariable[i-1]
                _DBLocation1 =  DBSensorVariable[i]

                if(BluetoothSocketVariable[v] == "01"):
                    #print "in BluetoothSocketVariable[v] ",_DBLocation1, _DBSensorID1

                    _BTLocation1 = BluetoothSocketVariable[v]
                    _BTSensorID1 = BluetoothSocketVariable[v+1]
                    #print "in BluetoothSocketVariable[v] ",_BTLocation1, _BTSensorID1
                    
                    if(BluetoothSocketVariable[v+1] != None):
                        
                        if(_DBSensorID1 == BluetoothSocketVariable[v+1]):
                            #print "in if ", _BTLocation1, _BTSensorID1
                            print "BluetoothSocketVariable BTSensorID and DBSensorVariable DBSensorID are Same"
                        elif (_DBSensorID1 != BluetoothSocketVariable[v+1]):
                            #print "in else ", _BTLocation1, _BTSensorID1
                            assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                    else:
                        print "BluetoothSocketVariable SensorID Not Assigned"
                        assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                    
                elif (BluetoothSocketVariable[v] == None):
                    #print "in None",_BTLocation1, _BTSensorID1
                    assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)


            #Check 02 Location and Related Sensor ID
            if(DBSensorVariable[i] == "02"):
                _DBSensorID2 =  DBSensorVariable[i-1]
                _DBLocation2 =  DBSensorVariable[i]

                if(BluetoothSocketVariable[v] == "02"):
                    #print "in BluetoothSocketVariable[v] ",_DBLocation2, _DBSensorID2

                    _BTLocation2 = BluetoothSocketVariable[v]
                    _BTSensorID2 = BluetoothSocketVariable[v+1]
                    #print "in BluetoothSocketVariable[v] ",_BTLocation2, _BTSensorID2
                    
                    if(BluetoothSocketVariable[v+1] != None):
                        
                        if(_DBSensorID2 == BluetoothSocketVariable[v+1]):
                            #print "in if ", _BTLocation2, _BTSensorID2
                            print "BluetoothSocketVariable BTSensorID and DBSensorVariable DBSensorID are Same"
                        elif (_DBSensorID2 != BluetoothSocketVariable[v+1]):
                            #print "in else ", _BTLocation2, _BTSensorID2
                            assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                    else:
                        print "BluetoothSocketVariable SensorID Not Assigned"
                        assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                    
                elif (BluetoothSocketVariable[v] == None):
                    #print "in None",_BTLocation2, _BTSensorID2
                    assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                    

            #Check 03 Location and Related Sensor ID
            if(DBSensorVariable[i] == "03"):
                _DBSensorID3 =  DBSensorVariable[i-1]
                _DBLocation3 =  DBSensorVariable[i]

                if(BluetoothSocketVariable[v] == "03"):
                    #print "in BluetoothSocketVariable[v] ",_DBLocation3, _DBSensorID3

                    _BTLocation3 = BluetoothSocketVariable[v]
                    _BTSensorID3 = BluetoothSocketVariable[v+1]
                    #print "in BluetoothSocketVariable[v] ",_BTLocation3, _BTSensorID3
                    
                    if(BluetoothSocketVariable[v+1] != None):
                        
                        if(_DBSensorID3 == BluetoothSocketVariable[v+1]):
                            #print "in if ", _BTLocation3, _BTSensorID3
                            print "BluetoothSocketVariable BTSensorID and DBSensorVariable DBSensorID are Same"
                        elif (_DBSensorID3 != BluetoothSocketVariable[v+1]):
                            #print "in else ", _BTLocation3, _BTSensorID3
                            assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                    else:
                        print "BluetoothSocketVariable SensorID Not Assigned"
                        assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                    
                elif (BluetoothSocketVariable[v] == None):
                    #print "in None",_BTLocation3, _BTSensorID3
                    assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)


            #Check 04 Location and Related Sensor ID
            if(DBSensorVariable[i] == "04"):
                _DBSensorID4 =  DBSensorVariable[i-1]
                _DBLocation4 =  DBSensorVariable[i]

                if(BluetoothSocketVariable[v] == "04"):
                    #print "in BluetoothSocketVariable[v] ",_DBLocation4, _DBSensorID4

                    _BTLocation4 = BluetoothSocketVariable[v]
                    _BTSensorID4 = BluetoothSocketVariable[v+1]
                    #print "in BluetoothSocketVariable[v] ",_BTLocation4, _BTSensorID4
                    
                    if(BluetoothSocketVariable[v+1] != None):
                        
                        if(_DBSensorID4 == BluetoothSocketVariable[v+1]):
                            #print "in if ", _BTLocation4, _BTSensorID4
                            print "BluetoothSocketVariable BTSensorID and DBSensorVariable DBSensorID are Same"
                        elif (_DBSensorID4 != BluetoothSocketVariable[v+1]):
                            #print "in else ", _BTLocation4, _BTSensorID4
                            assignNewSensorToBTC(_conn, DBLocation4, _DBSensorID4)
                    else:
                        print "BluetoothSocketVariable SensorID Not Assigned"
                        assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                    
                elif (BluetoothSocketVariable[v] == None):
                    print "in None",_BTLocation4, _BTSensorID4
                    assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                    

            #Check 05 Location and Related Sensor ID
            if(DBSensorVariable[i] == "05"):
                _DBSensorID5 =  DBSensorVariable[i-1]
                _DBLocation5 =  DBSensorVariable[i]

                if(BluetoothSocketVariable[v] == "05"):
                    #print "in BluetoothSocketVariable[v] ",_DBLocation5, _DBSensorID5

                    _BTLocation5 = BluetoothSocketVariable[v]
                    _BTSensorID5 = BluetoothSocketVariable[v+1]
                    #print "in BluetoothSocketVariable[v] ",_BTLocation5, _BTSensorID5
                    
                    if(BluetoothSocketVariable[v+1] != None):
                        
                        if(_DBSensorID5 == BluetoothSocketVariable[v+1]):
                            #print "in if ", _BTLocation5, _BTSensorID5
                            print "BluetoothSocketVariable BTSensorID and DBSensorVariable DBSensorID are Same"
                        elif (_DBSensorID5 != BluetoothSocketVariable[v+1]):
                            #print "in else ", _BTLocation5, _BTSensorID5
                            assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)
                    else:
                        print "BluetoothSocketVariable SensorID Not Assigned"
                        assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)
                    
                elif (BluetoothSocketVariable[v] == None):
                    #print "in None",_BTLocation5, _BTSensorID5
                    assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)


            #Check 06 Location and Related Sensor ID
            if(DBSensorVariable[i] == "06"):
                _DBSensorID6 =  DBSensorVariable[i-1]
                _DBLocation6 =  DBSensorVariable[i]

                if(BluetoothSocketVariable[v] == "06"):
                    #print "in BluetoothSocketVariable[v] ",_DBLocation6, _DBSensorID6

                    _BTLocation6 = BluetoothSocketVariable[v]
                    _BTSensorID6 = BluetoothSocketVariable[v+1]
                    #print "in BluetoothSocketVariable[v] ",_BTLocation6, _BTSensorID6
                    
                    if(BluetoothSocketVariable[v+1] != None):
                        
                        if(_DBSensorID6 == BluetoothSocketVariable[v+1]):
                            #print "in if ", _BTLocation6, _BTSensorID6
                            print "BluetoothSocketVariable BTSensorID and DBSensorVariable DBSensorID are Same"
                        elif (_DBSensorID6 != BluetoothSocketVariable[v+1]):
                            #print "in else ", _BTLocation6, _BTSensorID6
                            assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)
                    else:
                        print "BluetoothSocketVariable SensorID Not Assigned"
                        assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)
                    
                elif (BluetoothSocketVariable[v] == None):
                    #print "in None",_BTLocation6, _BTSensorID6
                    assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)
    
                    
    
    #print DBSensorVariable[0]
    #print BluetoothSocketVariable[0]

def assignNewSensorToBTC(conn, location, sensorUID):

    print ("assignNewSensorToBTC", location, sensorUID)
    

    TPMSET = blecontroller.Tpms_Tire_SET_Position1(location, sensorUID)
    print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
    data = blecontroller.Tpms_SET_TireID(conn, TPMSET)
    print data
    
    
def fun():
    print("Main Function")

    #print("RFID Module Read TAG ID Function")
    #tag_id = rfid.RFIDUHFQueryTag()
    
#    vehID, vehName, BUID, RFUID = db_DeviceDetails_by_rfiduid()

    #print "Main: ", vehID, vehName, BUID, RFUID
    #vehID=24
    if (vehID != None):
        print("Query the Database to read Tyre Details, Sensor ID, Position by vehID")
        '''
        SID1,L1, SID2,L2, SID3,L3,\
        SID4,L4, SID5,L5, SID6,L6 = db_DeviceDetails_by_vehID(vehID)

        print SID1,L1, SID2,L2, SID3,L3,\
              SID4,L4, SID5,L5, SID6,L6
        '''

        DBSensorVariable = db_DeviceDetails_by_vehID(vehID)

        #print DBSensorVariable

    
    if (BUID != None):
        print("Connect socket RFCOMM to Bluetooth Controller by BUID")
        '''
        Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
        Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
        Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
        Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
        Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
        Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = Connect_Socket_Bluetooth_by_BUID(BUID)

        print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
        Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
        Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
        Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
        Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
        Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
        '''
        print("Create a Bluetooth connection")
        conn = blecontroller.connect_ble(BUID)
        
        BluetoothSocketVariable = Connect_Socket_Bluetooth_by_BUID(conn)

        #print BluetoothSocketVariable
        
       
    #DBSensorVariable = (u'SensorUID 15', '01', u'SensorUID 14', '02', u'SensorUID 22', '03', u'SensorUID 21', '04', u'SensorUID 20', '06', u'SensorUID 19', '05')
    #BluetoothSocketVariable = ('01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')
    #DBSensorVariable = (u'ba6b09', '01', u'56a8cb', '03', u'ba6d6d', '02', u'56a6be', '04', u'56a781', '06', u'56a7c5', '05')
    #BluetoothSocketVariable = ('01', 'ba6b01', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')

    print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

    compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(conn, DBSensorVariable, BluetoothSocketVariable)

    
    print("After While Loop Connect socket RFCOMM to Bluetooth Controller by BUID")
    conn.close()

if __name__ == "__main__":  
    
    fun()
    
        
