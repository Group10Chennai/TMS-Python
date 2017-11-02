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

import glob
import logging
import logging.handlers


LOG_FILENAME = '/home/pi/Documents/TMS-Git/TMS-Python/log/loggingRotatingFileExample.log'

my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)



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

BluetoothSocketVariable= []
DBSensorVariable=[]


database = "/opt/Aquire/sqlite/Sample.db"
TID1 = "e2000016351702081640767f"
tag_id = "e2000016351702081640767f" #24
#vehID = 32
BUID = '00:13:EF:C0:02:1E' #17



# Start Query the DB with RFID TID
def db_DeviceDetails_by_rfiduid(conn, tag_id):

    try:
        #print("Create a database connection to the DB file .db")
        #conn = db.create_db_connection(database)
        #print tag_id
        #print("Query the database to read Vehicle Details by RFUID")
        #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, "RFID 1")

        if(conn != None): 
            with conn:
                vehDetail = db.select_DeviceDetails_by_rfiduid(conn, tag_id)
                if (vehDetail != None):
                    #Check vehID 
                    if(vehDetail[0] != 0):
                        vehID = vehDetail[0]
                    else:
                        my_logger.warning ("vehID is Not Available", vehDetail[0])
                        
                    #Check vehName
                    if(vehDetail[1] != None):
                        vehName = vehDetail[1].strip()
                    else:
                        my_logger.warning ("vehName is Not Available", vehDetail[1].strip())
                        
                    #Check BUID and Mac Address Length
                    if((vehDetail[2] != None) &(len(vehDetail[2].strip()) == 17)):
                        BUID = vehDetail[2].strip()
                    else:
                        my_logger.warning ("BUID is Not Available", vehDetail[2])
                        
                    #Check RFUID and tagid Length
                    if((vehDetail[3] != None) & (len(vehDetail[3].strip()) == 24)):
                        RFUID = vehDetail[3].strip()
                    else:
                        my_logger.warning ("BUID is Not Available", vehDetail[2])
                        
                    
                    if(vehID, vehName, BUID, RFUID != None):                   
                        my_logger.info ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s are Available", vehID, vehName, BUID, RFUID)
                        print ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s are Available", vehID, vehName, BUID, RFUID)
                        #Add Response Class
                        return vehID, vehName, BUID, RFUID
                        #return  vehDetail
                    else:
                        my_logger.warning ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s  are NONE", vehID, vehName, BUID, RFUID) 
                        #Add Response Class
                        return None                
                else:
                    my_logger.warning ("db.select_DeviceDetails_by_rfiduid vehDetail None : %s." , vehDetail) 
                    #Add Response Class
                    return None
                #print vehID, vehName, BUID, RFUID       
        else:
            my_logger.warning ("Connection to DB is None " )
            return None
    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Bluetooth Parse data Attribute Value not Avalable:",e)

        return None
    
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
def db_DeviceDetails_by_vehID(conn, vehID1):

    #print("Create a database connection to the DB file .db")
    #conn = db.create_db_connection(database)
    
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
            elif Tyre_row1[1] == "RRI":
                L1 = "05"
            elif Tyre_row1[1] == "RRO":
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
            elif Tyre_row2[1] == "RRI":
                L2 = "05"
            elif Tyre_row2[1] == "RRO":
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
            elif Tyre_row3[1] == "RRI":
                L3 = "05"
            elif Tyre_row3[1] == "RRO":
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
            elif Tyre_row4[1] == "RRI":
                L4 = "05"
            elif Tyre_row4[1] == "RRO":
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
            elif Tyre_row5[1] == "RRI":
                L5 = "05"
            elif Tyre_row5[1] == "RRO":
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
            elif Tyre_row6[1] == "RRI":
                L6 = "05"
            elif Tyre_row6[1] == "RRO":
                L6 = "06"
                
            #print SID6, L6
       
        
    
    print("Close a database connection to the DB file .db")
    conn.close()
    return SID1, L1, SID2, L2, SID3, L3, SID4,L4, SID5,L5, SID6,L6
'''     
# Start Connecting the Socket by BUID
def Connect_Socket_Bluetooth_by_BUID( conn):

    #print("Create a Bluetooth connection")
    #conn = blecontroller.connect_ble(BUID)
   
    #blecontroller.Tpms_Tire_SET_Position1(SID1, L1)
    #print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
    #data = blecontroller.Query_Tpms_SET_TireID(conn)
    if(conn != None):
        try:
            print("Query the Bluetooth Controller with 63 to read All TyreNo, Sensor ID, Pressure and Temp")
            TPMSID1 = blecontroller.TpmsTireDataPosition()

            if(TPMSID1 != None):
            
                print("Query the Bluetooth Controller to read TyreNo, Sensor ID, Pressure and Temp")
                data = blecontroller.Query_TpmsTireDataPosition(conn, TPMSID1)

                if(data != None):

                    print("Parse the hex data string TyreNo, Sensor ID, Pressure and Temp")    
                    Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
                    Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                    Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                    Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                    Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                    Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = blecontroller.ParseBluetoothTyre(data)

                    print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
                           Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                           Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                           Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                           Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                           Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp

                    return Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
                           Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                           Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                           Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                           Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                           Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
                

                else:
                    my_logger.warning ("Data not Available from the Bluetooth Controller: ")
                    return None
            else:
                my_logger.warning ("Data not Available from the Bluetooth Controller: ")
                return None
            
        except Error as e:
            my_logger.error(e) 
            return None
    '' 
    print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
          Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
          Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
          Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
          Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
          Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp

    ''
    #print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID()
    

    
'''
# Start Connecting the Socket by BUID
def Connect_Socket_Bluetooth_by_BUID( conn):

    #print("Create a Bluetooth connection")
    #conn = blecontroller.connect_ble(BUID)
   
    #blecontroller.Tpms_Tire_SET_Position1(SID1, L1)
    #print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
    #data = blecontroller.Query_Tpms_SET_TireID(conn)
    if(conn != None):
        try:
            print("Query the Bluetooth Controller with 63 to read All TyreNo, Sensor ID, Pressure and Temp")
            TPMSID1 = blecontroller.TpmsTireDataPosition()

            if(TPMSID1 != None):
            
                print("Query the Bluetooth Controller to read TyreNo, Sensor ID, Pressure and Temp")
                data = blecontroller.Query_TpmsTireDataPosition(conn, TPMSID1)

                if(data != None):

                    print("Parse the hex data string TyreNo, Sensor ID, Pressure and Temp")    
                    
                    BluetoothSocketVariable1 = blecontroller.ParseBluetoothTyre(data)

                    print BluetoothSocketVariable1

                    return BluetoothSocketVariable1
                
                else:
                    my_logger.warning ("Data not Available from the Bluetooth Controller: ")
                    return None
            else:
                my_logger.warning ("Data not Available from the Bluetooth Controller: ")
                return None
            
        except Error as e:
            my_logger.error(e) 
            return None
    
    #print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID()
    

 
'''
           
def compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(conn, DBSensorVariable, BluetoothSocketVariable):

    print DBSensorVariable
    print BluetoothSocketVariable

    totalTyres = int(BluetoothSocketVariable[0])
    print "Total Tyres:", totalTyres
    
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
                    #print "in None",_BTLocation4, _BTSensorID4
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
                    print "in BluetoothSocketVariable[v] ",_DBLocation6, _DBSensorID6

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

'''


           
def compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(conn, DBSensorVariable, BluetoothSocketVariable):

    print DBSensorVariable
    print BluetoothSocketVariable
    
    BTtotalTyres = int(BluetoothSocketVariable[0])
    print "Total Tyres:", BTtotalTyres

    if (DBSensorVariable is not None) and (BluetoothSocketVariable is not None):

        #Check the DBSensorVariable and find the DBSensorID, DBLocation 
        for i in range(len(DBSensorVariable)):
            
            if(DBSensorVariable[i] == "01"):
                _DBSensorID1 =  DBSensorVariable[i-1]
                _DBLocation1 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation1, _DBSensorID1
                
            #Check 02 Location and Related Sensor ID
            if(DBSensorVariable[i] == "02"):
                _DBSensorID2 =  DBSensorVariable[i-1]
                _DBLocation2 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation2, _DBSensorID2

            #Check 03 Location and Related Sensor ID
            if(DBSensorVariable[i] == "03"):
                _DBSensorID3 =  DBSensorVariable[i-1]
                _DBLocation3 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation3, _DBSensorID3

            #Check 04 Location and Related Sensor ID
            if(DBSensorVariable[i] == "04"):
                _DBSensorID4 =  DBSensorVariable[i-1]
                _DBLocation4 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation4, _DBSensorID4

            #Check 05 Location and Related Sensor ID
            if(DBSensorVariable[i] == "05"):
                _DBSensorID5 =  DBSensorVariable[i-1]
                _DBLocation5 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation5, _DBSensorID5

            #Check 06 Location and Related Sensor ID
            if(DBSensorVariable[i] == "06"):
                _DBSensorID6 =  DBSensorVariable[i-1]
                _DBLocation6 =  DBSensorVariable[i]
                print "in DBSensorVariable[i] ",_DBLocation6, _DBSensorID6

    
    
        #Check the BluetoothSocketVariable and find the BTSensorID, BTLocation    
        for v in range(len(BluetoothSocketVariable)):

            if(BluetoothSocketVariable[v] == "01"):

                _BTLocation1 = BluetoothSocketVariable[v]
                _BTSensorID1 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation1, _BTSensorID1

            if(BluetoothSocketVariable[v] == "02"):
                        
                _BTLocation2 = BluetoothSocketVariable[v]
                _BTSensorID2 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation2, _BTSensorID2

            if(BluetoothSocketVariable[v] == "03"):
                        
                _BTLocation3 = BluetoothSocketVariable[v]
                _BTSensorID3 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation3, _BTSensorID3

            if(BluetoothSocketVariable[v] == "04"):
                        
                _BTLocation4 = BluetoothSocketVariable[v]
                _BTSensorID4 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation4, _BTSensorID4

            if(BluetoothSocketVariable[v] == "05"):
                        
                _BTLocation5 = BluetoothSocketVariable[v]
                _BTSensorID5 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation5, _BTSensorID5

            if(BluetoothSocketVariable[v] == "06"):
                        
                _BTLocation6 = BluetoothSocketVariable[v]
                _BTSensorID6 = BluetoothSocketVariable[v+1]
                print "in BluetoothSocketVariable[v] ",_BTLocation6, _BTSensorID6

        
                
        #Compare Sensor ID and location 
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
                        #print "in None",_BTLocation4, _BTSensorID4
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
                        print "in BluetoothSocketVariable[v] ",_DBLocation6, _DBSensorID6

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


        #Check the Missed tyre form BluetoothSocketVariable
        MissedTyre = [i for i in DBSensorVariable if i not in BluetoothSocketVariable]

        print MissedTyre

        if MissedTyre is not None:
            
            for BTtyre in MissedTyre:
                
                if BTtyre == "01":
                    assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                    print "assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)"
                    
                elif BTtyre == "02":
                    assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                    print "assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)"
                    
                elif BTtyre == "03":
                    assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                    print "assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)"
                    
                elif BTtyre == "04":
                    assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                    print "assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)"
                    
                elif BTtyre == "05":
                    assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)
                    print "assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)"

                elif BTtyre == "06":
                    assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)
                    print "assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)"

        
                  
    
    #print DBSensorVariable[0]
    #print BluetoothSocketVariable[0]
    
    else:
        print ("Failed - Bluetooth and DB Sensor Variable are None:",DBSensorVariable, BluetoothSocketVariable)
        my_logger.warning("Failed - Bluetooth DB Sensor Variable are None: %s %s",DBSensorVariable, BluetoothSocketVariable)
        #return None

def assignNewSensorToBTC(conn, location, sensorUID):

    print ("assignNewSensorToBTC", location, sensorUID)
    
    try:
        if(conn != None):
            if(location is not None) and (sensorUID is not None):
            
                TPMSET = blecontroller.Tpms_Tire_SET_Position1(location, sensorUID)

                if(TPMSET != None):
                    
                    print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
                    data = blecontroller.Tpms_SET_TireID(conn, TPMSET)
                    #conn.close()
                    print data
                    return data

                else:
                    my_logger.warning("Failed - Bluetooth Query to Send and Receive Command Not Available: %s",TMSSET)
                    print("Failed - Bluetooth Query to Send and Receive Command Not Available: %s",TMSSET)
                    return None
            else:
                my_logger.warning("Failed - Bluetooth Query to assignNewSensorToBTC(Location, Sensor ID) not Avalable: %s, %s",location, sensorUID)
                print ("Failed - Bluetooth Query to assignNewSensorToBTC(Location, Sensor ID) not Avalable: ",location, sensorUID)
                return None
        else:
            
            my_logger.warning("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID)
            print ("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID)
            return None


    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None:%s, %s, %s ",e, location, sensorUID )
        print ("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e, location, sensorUID )

        return None
                
    
    
def fun():
    print("Main Function")
    
    try:
        #print("RFID Module Read TAG ID Function")
        #tag_id = rfid.RFIDUHFQueryTag()
    
        if(tag_id != None):
            print("Create a database connection to the DB file .db")
            if(database!=None):
                dbConn = db.create_db_connection(database)
                if(dbConn != None):
                    #vehID, vehName, BUID, RFUID = db_DeviceDetails_by_rfiduid(dbConn, tag_id)
                    vehDetails = db_DeviceDetails_by_rfiduid(dbConn, tag_id)
                    #print("Create a database connection to the DB file--- ", vehDetails)
                    
                    if(vehDetails != None):
                        print("Query the Database to read Tyre Details, Sensor ID, Position by vehID")

                        vehID = vehDetails[0]
                        vehName = vehDetails[1]
                        BUID = vehDetails[2]
                        RFUID = vehDetails[3]

                        #Query DB DeviceDetail in VehDetails Table to read vehID, vehName, BUID, RFUID
                        if(vehID != None):
                            DBSensorVariable = db_DeviceDetails_by_vehID(dbConn, vehID)                        

                            #print DBSensorVariable
                            dbConn.close()
                        else:
                            my_logger.warning ("Vehicle ID not Available or None Function : ", vehID)
                    else:
                       my_logger.warning ("RFID Tag ID is not available in DB : ", tag_id)
                else:
                    my_logger.warning ("No DB Connection ")
            else: 
                my_logger.warning ("Database path Not Available ")
        else:
            my_logger.warning ("RFID Tag ID is not available in DB : ", tag_id)
            
                        
        #Query DB Device Detail to read vehID, vehName, BUID, RFUID
        if (BUID != None):
            print("Connect socket RFCOMM to Bluetooth Controller by BUID")                 
            print("Create a Bluetooth connection")
            bleConn = blecontroller.connect_ble(BUID)
            
            if(bleConn != None):                           
                BluetoothSocketVariable = Connect_Socket_Bluetooth_by_BUID(bleConn)

                #print BluetoothSocketVariable

                if(( DBSensorVariable != None) and (BluetoothSocketVariable != None)):
                    print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

                    compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(bleConn, DBSensorVariable, BluetoothSocketVariable)
                else:
                    my_logger.warning ("DBSensorVariable and BluetoothSocketVariable not Available or None Function : ", DBSensorVariable, BluetoothSocketVariable)
            else:
                my_logger.warning ("Bluetooth ID not connected or Host Not Available or None Function : ")
        else:
            my_logger.warning ("Bluetooth ID not Available or None Function : ", BUID)
          
                            
    
            
           
    except Error as e:
        #print (e)
        my_logger.error(e)
        #raise   
        return None 

   
    
       
    #DBSensorVariable = (u'SensorUID 15', '01', u'SensorUID 14', '02', u'SensorUID 22', '03', u'SensorUID 21', '04', u'SensorUID 20', '06', u'SensorUID 19', '05')
    #DBSensorVariable = (u'ba6b09', '01', u'ba6d6d', '02', u'56a8cb', '03', u'56a6be', '04', u'56a781', '05', u'56a7c5', '06')
    #BluetoothSocketVariable = ('01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')
    #DBSensorVariable = (u'ba6b09', '01', u'56a8cb', '03', u'ba6d6d', '02', u'56a6be', '04', u'56a781', '06', u'56a7c5', '05')
    #BluetoothSocketVariable = (5, '01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00')
    #BluetoothSocketVariable = ( )
    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(DBSensorVariable, BluetoothSocketVariable)
    
    #print("After While Loop Connect socket RFCOMM to Bluetooth Controller by BUID")
    #bleConn.close()

if __name__ == "__main__":  
    
    fun()
    
        
