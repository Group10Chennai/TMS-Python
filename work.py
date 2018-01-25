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
import display
import apiupdate
import bluetoothctl
import BtAutoPair
#import push

import datetime

import glob
import logging
import logging.handlers



LOG_FILENAME = '/home/pi/Documents/TMS-Git/log/loggingRotatingFileExample.log'

my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)

'''
#Creating Object for bluetoothctl
autopair = BtAutoPair.BtAutoPair()
autopair.enable_pairing()

bl = bluetoothctl.Bluetoothctl()
'''

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

dispVar = ""

tup1=()
_DBSensorID = []
_DBLocation = []

BluetoothSocketVariable= []
DBSensorVariable=[]


database = "/opt/Aquire/sqlite/TPMS.db"
TID1 = "e2000016351702081640767f"
#tag_id = "e2000016351702081640767f" #24
#vehID = 32
#BUID = '00:13:EF:C0:02:1E' #17
#BUID = '00:13:EF:C0:01:4D' #17
BUID = '00:13:EF:C0:01:3C' #


# Start Query the DB with RFID TID
def db_DeviceDetails_by_rfiduid(conn, tag_id):

    try:
        #print("Create a database connection to the DB file .db")
        #conn = db.create_db_connection(database)
        #print tag_id
        #print("Query the database to read Vehicle Details by RFUID")
        #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, "RFID 1")

        if(conn != None): 
            #with conn:
            if conn:
                vehDetail = db.select_DeviceDetails_by_rfiduid(conn, tag_id)
                if (vehDetail != None):
                    #Check vehID 
                    if(vehDetail[0] != 0):
                        vehID = vehDetail[0]
                    else:
                        my_logger.warning ("Failed - vehID is Not Available", vehDetail[0])
                        
                    #Check vehName
                    if(vehDetail[1] != None):
                        vehName = vehDetail[1].strip()
                    else:
                        my_logger.warning ("Failed - vehName is Not Available", vehDetail[1].strip())
                        
                    #Check BUID and Mac Address Length
                    if((vehDetail[2] != None) &(len(vehDetail[2].strip()) == 17)):
                        BUID = vehDetail[2].strip()
                    else:
                        my_logger.warning ("Failed - BUID is Not Available", vehDetail[2])
                        
                    #Check RFUID and tagid Length
                    if((vehDetail[3] != None) & (len(vehDetail[3].strip()) == 24)):
                        RFUID = vehDetail[3].strip()
                    else:
                        my_logger.warning ("Failed - BUID is Not Available", vehDetail[2])
                        
                    
                    if(vehID, vehName, BUID, RFUID != None):                   
                        my_logger.info ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s are Available", vehID, vehName, BUID, RFUID)
                        print ("If vehID : %s, vehName : %s, BUID : %s, RFUID : %s are Available", vehID, vehName, BUID, RFUID)
                        #Add Response Class
                        return vehID, vehName, BUID, RFUID
                        #return  vehDetail
                    else:
                        my_logger.warning ("Failed - If vehID : %s, vehName : %s, BUID : %s, RFUID : %s  are NONE", vehID, vehName, BUID, RFUID) 
                        #Add Response Class
                        return None                
                else:
                    my_logger.warning ("Failed - db.select_DeviceDetails_by_rfiduid vehDetail None : %s." , vehDetail) 
                    #Add Response Class
                    return None
                #print vehID, vehName, BUID, RFUID       
        else:
            my_logger.warning ("Failed - Connection to DB is None " )
            return None
    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Failed - Bluetooth Parse data Attribute Value not Avalable:",e)

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
def db_DeviceDetails_by_vehID(DBconn, vehID1):

    #print("Create a database connection to the DB file .db")
    #conn = db.create_db_connection(database)
    
    #print vehID
    print("Query the database to read Tyre Details by vehID")
    #vehDetail = db.select_DeviceDetails_by_rfiduid(conn, vehID)
    DBTyreDetail = []

    try:
        
        #with DBconn:
        if DBconn:
            TyreDetail = db.select_TyreDetails_by_VehId(DBconn, vehID1)

            DBtotalTyres = len(TyreDetail)
            print DBtotalTyres
        else:
            my_logger.warning("Failed - db_DeviceDetails_by_vehID - DBconn: %s ", data)
            print ("Failed - db_DeviceDetails_by_vehID - DBconn:  ", data)
            return None
        
        if TyreDetail is not None:
            for DBi in range(1, DBtotalTyres+1):

                if(DBi == 1):
                    
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
                    DBTyreDetail.append(SID1)
                    DBTyreDetail.append(L1)
                    
                    if DBi == int(DBtotalTyres):
                        
                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 2):

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
                    DBTyreDetail.append(SID2)
                    DBTyreDetail.append(L2)
                    
                    if DBi == int(DBtotalTyres):
                        
                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 3):

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
                    DBTyreDetail.append(SID3)
                    DBTyreDetail.append(L3)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 4):
                    
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
                    DBTyreDetail.append(SID4)
                    DBTyreDetail.append(L4)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 5):

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
                    DBTyreDetail.append(SID5)
                    DBTyreDetail.append(L5)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi == 6):

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
                    DBTyreDetail.append(SID6)
                    DBTyreDetail.append(L6)
                    
                    if DBi == int(DBtotalTyres):

                        print DBTyreDetail
                        return DBTyreDetail

                elif(DBi > 6):
                    my_logger.warning("Failed - DB Select TyreDetails by VehId in DBtotalTyres is more than 6: %s, %s ",DBi, DBtotalTyres)
                    print ("Failed - DB Select TyreDetails by VehId in DBtotalTyres is more than 6:",DBi, DBtotalTyres)
                    return None   
                    

        elif TyreDetail is None:
            my_logger.warning("Failed - DB Select TyreDetails by VehId in TyreDetail is None: %s",TyreDetail)
            print ("Failed - DB Select TyreDetails by VehId in TyreDetail is None:",TyreDetail)
            return None 

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - DB Select TyreDetails by VehId is not available: %s, %s ",e, VehId)
        print ("Failed - DB Select TyreDetails by VehId is not available:",e, VehId)
        return None
        
        #print("Close a database connection to the DB file .db")
        #DBconn.close()
    

# Start Connecting the Socket by BUID
def Connect_Socket_Bluetooth_by_BUID( conn):

    #print("Create a Bluetooth connection")
    #conn = blecontroller.connect_ble(BUID)
   
    #blecontroller.Tpms_Tire_SET_Position1(SID1, L1)
    print("Query the Bluetooth Controller to set TyreNo, Sensor ID")
    print "Connect_Socket_Bluetooth_by_BUID 1"
    #data = blecontroller.Query_Tpms_SET_TireID(conn)
    try:
        if(conn != None):
            print("Query the Bluetooth Controller with 63 to read All TyreNo, Sensor ID, Pressure and Temp")
            TPMSID1 = blecontroller.TpmsTireDataPosition()

            if(TPMSID1 != None):
            
                print("Query the Bluetooth Controller to read TyreNo, Sensor ID, Pressure and Temp")
                data, BLEstatus = blecontroller.Query_TpmsTireDataPosition(conn, TPMSID1)
                print ("hexstr = binascii.b2a_hex(data)", binascii.b2a_hex(data))
                if(data != None) and (BLEstatus == "Success"):

                    print("Parse the hex data string TyreNo, Sensor ID, Pressure and Temp")    
                    
                    BluetoothSocketVariable1 = blecontroller.ParseBluetoothTyre(data.strip())

                    #print "Connect_Socket_Bluetooth_by_BUID in loop ", BluetoothSocketVariable1
                    #print "Connect_Socket_Bluetooth_by_BUID in loop2 with BLEstatus ", BluetoothSocketVariable1, BLEstatus

                    return BluetoothSocketVariable1, BLEstatus
                
                else:
                    my_logger.warning("Failed - BT Query Data not Available from the Bluetooth Controller: %s ", data)
                    print ("Failed - BT Query Data not Available from the Bluetooth Controller:", data)
                    return None, "Failed"
            else:
                my_logger.warning("Failed - BT Query the Bluetooth Controller with 63 to read All is None: %s, %s ",e, TPMSID1)
                print ("Failed - BT Query the Bluetooth Controller with 63 to read All is None:",e, TPMSID1)
                return None, "Failed"
            
        else:
            my_logger.warning("Failed - BT Query the Bluetooth Controller BTConnection is None: %s",conn)
            print ("Failed - BT Query the Bluetooth Controller BTConnection is None:",conn)
            return None, "Failed"

    except:
            e = sys.exc_info()[0]
            my_logger.error("Failed - BT Query the Bluetooth Controller with 63 to read All is None: %s, %s ",e, TPMSID1)
            print ("Failed - BT Query the Bluetooth Controller with 63 to read All is None:",e, TPMSID1)
            return None, "Failed"
    #print("Compare DB Sensor UID, tirePosition with Bluetooth TyreNo, TyreID")

    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID()

    
# Start Configuring the Bluetooth Controller Based on the DB Parameters   
def configure_BTController(bleConn, DBSensorVariable):

    try:

        print "DBSensorVariable", DBSensorVariable

        for i in range(0,len(DBSensorVariable),2):

            #Check 01 Location and Related Sensor ID
            
            #print "in DBSensorVariable[i] ",( DBSensorVariable[i+1], DBSensorVariable[i])

            #print "BluetoothSocketVariable SensorID Not Assigned"
            RetValConf = assignNewSensorToBTC(bleConn, DBSensorVariable[i+1], DBSensorVariable[i])
            time.sleep(0.3)
            
            if RetValConf == "aa":
                continue
            else:
                my_logger.warning("Failed - BT Query the Bluetooth Controller to configure Sensor ID, Location - RetValConf is None or FF: %s, %s, %s",DBSensorVariable[i+1], DBSensorVariable[i], RetValConf)
                print ("Failed - BT Query the Bluetooth Controller to configure Sensor ID, Location - RetValConf is None or FF: ",DBSensorVariable[i+1], DBSensorVariable)
                #return None

           
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: %s ",e)
        print ("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e)

        return None

           
def compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(conn, DBSensorVariable, BluetoothSocketVariable):

    print "compare_DBSensorUID_DBLocation_BTyreNo_BTyreID DBSensorVariable",DBSensorVariable
    print "compare_DBSensorUID_DBLocation_BTyreNo_BTyreID BluetoothSocketVariable",BluetoothSocketVariable
    
    #BTtotalTyres = int(BluetoothSocketVariable[0])
    #print "Total Tyres:", BTtotalTyres
    try:
        
        #if (DBSensorVariable is not None) and (BluetoothSocketVariable is not None):
        if (DBSensorVariable is not None):
            #Check the DBSensorVariable and find the DBSensorID, DBLocation 
            for i in range(len(DBSensorVariable)):

                #Check 01 Location and Related Sensor ID
                if(DBSensorVariable[i] == "01"):
                    _DBSensorID1 =  DBSensorVariable[i-1]
                    _DBLocation1 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation1, _DBSensorID1
                    
                #Check 02 Location and Related Sensor ID
                elif(DBSensorVariable[i] == "02"):
                    _DBSensorID2 =  DBSensorVariable[i-1]
                    _DBLocation2 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation2, _DBSensorID2

                #Check 03 Location and Related Sensor ID
                elif(DBSensorVariable[i] == "03"):
                    _DBSensorID3 =  DBSensorVariable[i-1]
                    _DBLocation3 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation3, _DBSensorID3

                #Check 04 Location and Related Sensor ID
                elif(DBSensorVariable[i] == "04"):
                    _DBSensorID4 =  DBSensorVariable[i-1]
                    _DBLocation4 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation4, _DBSensorID4

                #Check 05 Location and Related Sensor ID
                elif(DBSensorVariable[i] == "05"):
                    _DBSensorID5 =  DBSensorVariable[i-1]
                    _DBLocation5 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation5, _DBSensorID5

                #Check 06 Location and Related Sensor ID
                elif(DBSensorVariable[i] == "06"):
                    _DBSensorID6 =  DBSensorVariable[i-1]
                    _DBLocation6 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation6, _DBSensorID6

        
            '''
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
            '''
        else:
            my_logger.warning("Failed - DBSensorVariable is None %s",DBSensorVariable)
            print ("Failed - DBSensorVariable is None",DBSensorVariable)
            return None

            
        mylist = BluetoothSocketVariable
        #print mylist

       
        

        
        if (mylist != None):
            print "1: mylist != None and conn != None)"
            for i in range (2, len(mylist)):
                #print i, mylist[i][6]

                '''
                print "Location ", mylist[2][6]
                print "Location ", mylist[3][6]
                print "Location ", mylist[4][6]
                print "Location ", mylist[5][6]
                print "Location ", mylist[6][6]
                print "Location ", mylist[7][6]
                '''
                
                if mylist[i][6] == '01' :

                    print "SensorID1 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    _BTLocation1 = mylist[i][6]
                    _BTSensorID1 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                    

                elif mylist[i][6] == '02' :

                    print "SensorID2 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    _BTLocation2 = mylist[i][6]
                    _BTSensorID2 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                    

                elif mylist[i][6] == '03' :

                    print "SensorID3 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    _BTLocation3 = mylist[i][6]
                    _BTSensorID3 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                    

                elif mylist[i][6] == '04' :

                    print "SensorID4 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    _BTLocation4 = mylist[i][6]
                    _BTSensorID4 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                    

                elif mylist[i][6] == '05' :

                    print "SensorID5 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    _BTLocation5 = mylist[i][6]
                    _BTSensorID5 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                    

                elif mylist[i][6] == '06' :

                    print "SensorID6 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    _BTLocation6 = mylist[i][6]
                    _BTSensorID6 = mylist[i][7]+mylist[i][8]+mylist[i][9]


            print "2: mylist != None and conn != None)"    
            #Compare Sensor ID and location 
            for v in range(len(DBSensorVariable)):
                
                #for v in range(len(BluetoothSocketVariable)):
                for i in range (2, len(mylist)):
                
                    #Check 01 Location and Related Sensor ID
                    if(DBSensorVariable[v] == "01"):
                        _DBSensorID1 =  DBSensorVariable[v-1]
                        _DBLocation1 =  DBSensorVariable[v]

                        if(mylist[i][6] == "01"):
                            #print "in BluetoothSocketVariable[v] ",_DBLocation1, _DBSensorID1

                            _BTLocation1 = mylist[i][6]
                            _BTSensorID1 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                            #print "in BluetoothSocketVariable[v] ",_BTLocation1, _BTSensorID1
                            
                            if(_BTSensorID1 != None):
                                
                                if(_DBSensorID1 == _BTSensorID1):
                                    #print "in if ", _BTLocation1, _BTSensorID1
                                    print ("BTSensorID1 and DBSensorID1 are Same", _BTSensorID1, _DBSensorID1)
                                    RetVal = "Success"
                                    #continue
                                elif (_DBSensorID1 != _BTSensorID1):
                                    #print "in else ", _BTLocation1, _BTSensorID1
                                    print ("BTSensorID1 and DBSensorID1 are Not Same", _BTSensorID1, _DBSensorID1)
                                    RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)

                                    if RetVal == "aa":
                                        RetVal = "Success"
                                        print "Successfully Assigned Sensor"
                                        continue
                                    else:
                                        return None
                            else:
                                print "BluetoothSocketVariable SensorID Not Assigned"
                                RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                                if RetVal == "aa":
                                    RetVal = "Success"
                                    print "Successfully Assigned Sensor"
                                    continue
                                else:
                                   return None

                        '''
                        #elif (mylist[i][6] != "01") or (mylist[i][6] == '0'):
                        elif (mylist[i][6] == '0'):
                            #print "in None",_BTLocation1, _BTSensorID1
                            RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                            if RetVal == "aa":
                                RetVal = "Success"
                                print "Successfully Assigned Sensor"
                                continue
                            else:
                                return None

                        '''

                    #Check 02 Location and Related Sensor ID
                    elif(DBSensorVariable[v] == "02"):
                        _DBSensorID2 =  DBSensorVariable[v-1]
                        _DBLocation2 =  DBSensorVariable[v]

                        if(mylist[i][6] == "02"):
                            #print "in BluetoothSocketVariable[v] ",_DBLocation2, _DBSensorID2

                            _BTLocation2 = mylist[i][6]
                            _BTSensorID2 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                            #print "in BluetoothSocketVariable[v] ",_BTLocation2, _BTSensorID2
                            
                            if(_BTSensorID2  != None):
                                
                                if(_DBSensorID2 == _BTSensorID2):
                                    #print "in if ", _BTLocation2, _BTSensorID2
                                    print ("BTSensorID2 and DBSensorID2 are Same", _BTSensorID2, _DBSensorID2)
                                    RetVal = "Success"
                                    continue
                                elif (_DBSensorID2 != _BTSensorID2):
                                    #print "in else ", _BTLocation2, _BTSensorID2
                                    print ("BTSensorID2 and DBSensorID2 are Not Same", _BTSensorID2, _DBSensorID2)
                                    RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)

                                    if RetVal == "aa":
                                        RetVal = "Success"
                                        print "Successfully Assigned Sensor"
                                        continue
                                    else:
                                        return None
                            else:
                                print "BluetoothSocketVariable SensorID Not Assigned"
                                RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                                if RetVal == "aa":
                                    RetVal = "Success"
                                    print "Successfully Assigned Sensor"
                                    continue
                                else:
                                    return None
                        '''    
                        #elif (mylist[i][6] != "02") or (mylist[i][6] == '0'):
                        elif (mylist[i][6] == '0'):
                            #print "in None",_BTLocation2, _BTSensorID2
                            RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                            if RetVal == "aa":
                                RetVal = "Success"
                                print "Successfully Assigned Sensor"
                                continue
                            else:
                                return None
                        '''

                    #Check 03 Location and Related Sensor ID
                    elif(DBSensorVariable[v] == "03"):
                        _DBSensorID3 =  DBSensorVariable[v-1]
                        _DBLocation3 =  DBSensorVariable[v]

                        if(mylist[i][6] == "03"):
                            #print "in BluetoothSocketVariable[v] ",_DBLocation3, _DBSensorID3

                            _BTLocation3 = mylist[i][6]
                            _BTSensorID3 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                            #print "in BluetoothSocketVariable[v] ",_BTLocation3, _BTSensorID3
                            
                            if(_BTSensorID3 != None):
                                
                                if(_DBSensorID3 == _BTSensorID3):
                                    #print "in if ", _BTLocation3, _BTSensorID3
                                    print ("BTSensorID3 and DBSensorID3 are Same", _BTSensorID3, _DBSensorID3)
                                    RetVal = "Success"
                                    continue
                                elif (_DBSensorID3 != _BTSensorID3):
                                    #print "in else ", _BTLocation3, _BTSensorID3
                                    print ("BTSensorID3 and DBSensorID3 are Not Same", _BTSensorID3, _DBSensorID3)
                                    RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)

                                    if RetVal == "aa":
                                        RetVal = "Success"
                                        print "Successfully Assigned Sensor"
                                        continue
                                    else:
                                        return None
                            else:
                                print "BluetoothSocketVariable SensorID Not Assigned"
                                RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                                if RetVal == "aa":
                                    RetVal = "Success"
                                    print "Successfully Assigned Sensor"
                                    continue
                                else:
                                    return None


                        '''    
                        #elif (mylist[i][6] != "03") or (mylist[i][6] == '0'):
                        elif (mylist[i][6] == '0'):
                            #print "in None",_BTLocation3, _BTSensorID3
                            RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                            if RetVal == "aa":
                                RetVal = "Success"
                                print "Successfully Assigned Sensor"
                                continue
                            else:
                                return None
                        '''
                            

                    #Check 04 Location and Related Sensor ID
                    elif(DBSensorVariable[v] == "04"):
                        _DBSensorID4 =  DBSensorVariable[v-1]
                        _DBLocation4 =  DBSensorVariable[v]

                        if(mylist[i][6] == "04"):
                            #print "in BluetoothSocketVariable[v] ",_DBLocation4, _DBSensorID4

                            _BTLocation4 = mylist[i][6]
                            _BTSensorID4 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                            #print "in BluetoothSocketVariable[v] ",_BTLocation4, _BTSensorID4
                            
                            if(_BTSensorID4 != None):
                                
                                if(_DBSensorID4 == _BTSensorID4):
                                    #print "in if ", _BTLocation4, _BTSensorID4
                                    print ("BTSensorID4 and DBSensorID4 are Same", _BTSensorID4, _DBSensorID4)
                                    RetVal = "Success"
                                    continue
                                elif (_DBSensorID4 != _BTSensorID4):
                                    #print "in else ", _BTLocation4, _BTSensorID4
                                    print ("BTSensorID4 and DBSensorID4 are Not Same", _BTSensorID4, _DBSensorID4)
                                    RetVal = assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)

                                    if RetVal == "aa":
                                        RetVal = "Success"
                                        print "Successfully Assigned Sensor"
                                        continue
                                    else:
                                        return None
                            else:
                                print "BluetoothSocketVariable SensorID Not Assigned"
                                RetVal = assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)

                                if RetVal == "aa":
                                    RetVal = "Success"
                                    print "Successfully Assigned Sensor"
                                    continue
                                else:
                                    return None

                        '''        
                        #elif (mylist[i][6] != "04") or (mylist[5][6] == '00'):
                        elif (mylist[i][6] == '0'):
                            #print "in None",_BTLocation4, _BTSensorID4
                            RetVal = assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)

                            if RetVal == "aa":
                                RetVal = "Success"
                                print "Successfully Assigned Sensor"
                                continue
                            else:
                                return None
                        '''

                    #Check 05 Location and Related Sensor ID
                    elif(DBSensorVariable[v] == "05"):
                        _DBSensorID5 =  DBSensorVariable[v-1]
                        _DBLocation5 =  DBSensorVariable[v]

                        if(mylist[i][6] == "05"):
                            #print "in BluetoothSocketVariable[v] ",_DBLocation5, _DBSensorID5

                            _BTLocation5 = mylist[i][6]
                            _BTSensorID5 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                            #print "in BluetoothSocketVariable[v] ",_BTLocation5, _BTSensorID5
                            
                            if(_BTSensorID5 != None):
                                
                                if(_DBSensorID5 == _BTSensorID5):
                                    #print "in if ", _BTLocation5, _BTSensorID5
                                    print ("BTSensorID5 and DBSensorID5 are Same", _BTSensorID5, _DBSensorID5)
                                    RetVal = "Success"
                                    continue

                                elif (_DBSensorID5 != _BTSensorID5):
                                    #print "in else ", _BTLocation5, _BTSensorID5
                                    print ("BTSensorID5 and DBSensorID5 are Not Same", _BTSensorID5, _DBSensorID5)
                                    RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)

                                    if RetVal == "aa":
                                        RetVal = "Success"
                                        print "Successfully Assigned Sensor"
                                        continue
                                    else:
                                        return None
                            else:
                                print "BluetoothSocketVariable SensorID Not Assigned"
                                RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)

                                if RetVal == "aa":
                                    RetVal = "Success"
                                    print "Successfully Assigned Sensor"
                                    continue
                                else:
                                    return None
                        '''            
                        #elif (mylist[i][6] == None):
                        #elif (mylist[i][6] != "05") or (mylist[i][6] == '0'):
                        elif (mylist[i][6] == '0') and (_BTSensorID5 == ""):
                            #print "in None",_BTLocation5, _BTSensorID5
                            RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)

                            if RetVal == "aa":
                                RetVal = "Success"
                                print "Successfully Assigned Sensor"
                                continue
                            else:
                                return None
                        '''
                            


                    #Check 06 Location and Related Sensor ID
                    elif(DBSensorVariable[v] == "06"):
                        _DBSensorID6 =  DBSensorVariable[v-1]
                        _DBLocation6 =  DBSensorVariable[v]

                        if(mylist[i][6] == "06"):
                            #print "in BluetoothSocketVariable[v] ",_DBLocation6, _DBSensorID6

                            _BTLocation6 = mylist[i][6]
                            _BTSensorID6 = mylist[i][7]+mylist[i][8]+mylist[i][9]
                            #print "in BluetoothSocketVariable[v] ",_BTLocation6, _BTSensorID6
                            
                            if(_BTSensorID6 != None):
                                
                                if(_DBSensorID6 == _BTSensorID6):
                                    #print "in if ", _BTLocation6, _BTSensorID6
                                    print ("BTSensorID6 and DBSensorID6 are Same", _BTSensorID6, _DBSensorID6)
                                    RetVal = "Success"
                                    continue
                                elif (_DBSensorID6 != _BTSensorID6):
                                    #print "in else ", _BTLocation6, _BTSensorID6
                                    print ("BTSensorID6 and DBSensorID6 are Not Same", _BTSensorID6, _DBSensorID6)
                                    RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                                    if RetVal == "aa":
                                        RetVal = "Success"
                                        print "Successfully Assigned Sensor"
                                        continue
                                    else:
                                        return None
                            else:
                                #print "BluetoothSocketVariable SensorID Not Assigned"
                                print ("BTSensorID6 and DBSensorID6 are Not Same", _BTSensorID6, _DBSensorID6)
                                RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                                if RetVal == "aa":
                                    RetVal = "Success"
                                    print "Successfully Assigned Sensor"
                                    continue
                                else:
                                    return None
                        '''
                        #elif (mylist[i][6] != "06") or (mylist[i][6] == '0'):
                        elif (mylist[i][6] == '0') and (_BTSensorID6 == ""):
                            #print "in None",_BTLocation6, _BTSensorID6
                            RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                            if RetVal == "aa":
                                RetVal = "Success"
                                print "Successfully Assigned Sensor"
                                continue
                            else:
                                return None
                        '''

                            
            '''
            #Check the Missed tyre form BluetoothSocketVariable
            MissedTyre = [i for i in DBSensorVariable if i not in mylist]

            print "Missed Tyre", MissedTyre

            if MissedTyre is not None:
                
                for BTtyre in MissedTyre:
                    
                    if BTtyre == "01":
                        print "assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)"
                        RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)
                        
                        if RetVal is "aa":
                            print "SucceSsfully Assigned a Missed Sensor"
                            #continue
                        else:
                            return None
                        
                    elif BTtyre == "02":
                        print "assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)"
                        RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)
                        
                        if RetVal is "aa":
                            #continue
                            print "SucceSsfully Assigned a Missed Sensor"
                        else:
                            return None
                        
                    elif BTtyre == "03":
                        print "assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)"
                        RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)
                        
                        if RetVal is "aa":
                            print "SucceSsfully Assigned a Missed Sensor"
                            #continue
                        else:
                            return None
                        
                    elif BTtyre == "04":
                        print "assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)"
                        RetVal = assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)
                        
                        if RetVal is "aa":
                            print "SucceSsfully Assigned a Missed Sensor"
                            #continue
                        else:
                            return None
                        
                    elif BTtyre == "05":
                        print "assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)"
                        RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)
                        
                        if RetVal is "aa":
                            print "SucceSsfully Assigned a Missed Sensor"
                            #continue
                        else:
                            return None

                    elif BTtyre == "06":
                        print "assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)"
                        RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                        if RetVal is "aa":
                            print "SucceSsfully Assigned a Missed Sensor"
                            #continue
                        else:
                            return None
            
            '''

            
            print "Inside After For Compare (mylist != None and conn != None)", RetVal

            return RetVal
             
        elif (mylist == None and conn != None):

            print "Inside (mylist == None and conn != None):"
            #To configure all sensor to Bluetooth Controller
            for i in range(len(DBSensorVariable)):

                #Check 01 Location and Related Sensor ID
                if(DBSensorVariable[i] == "01"):
                    _DBSensorID1 =  DBSensorVariable[i-1]
                    _DBLocation1 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] To Assign BT",_DBLocation1, _DBSensorID1
                    RetVal = assignNewSensorToBTC(conn, _DBLocation1, _DBSensorID1)

                    if RetVal == "aa":
                        RetVal = "Success"
                        print "Successfully Assigned Sensor"
                        continue
                    else:
                        return None
                    
                #Check 02 Location and Related Sensor ID
                if(DBSensorVariable[i] == "02"):
                    _DBSensorID2 =  DBSensorVariable[i-1]
                    _DBLocation2 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation2, _DBSensorID2
                    RetVal = assignNewSensorToBTC(conn, _DBLocation2, _DBSensorID2)

                    if RetVal == "aa":
                        RetVal = "Success"
                        print "Successfully Assigned Sensor"
                        continue
                    else:
                        return None

                #Check 03 Location and Related Sensor ID
                if(DBSensorVariable[i] == "03"):
                    _DBSensorID3 =  DBSensorVariable[i-1]
                    _DBLocation3 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation3, _DBSensorID3
                    RetVal = assignNewSensorToBTC(conn, _DBLocation3, _DBSensorID3)

                    if RetVal == "aa":
                        RetVal = "Success"
                        print "Successfully Assigned Sensor"
                        continue
                    else:
                        return None

                #Check 04 Location and Related Sensor ID
                if(DBSensorVariable[i] == "04"):
                    _DBSensorID4 =  DBSensorVariable[i-1]
                    _DBLocation4 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation4, _DBSensorID4
                    RetVal = assignNewSensorToBTC(conn, _DBLocation4, _DBSensorID4)

                    if RetVal == "aa":
                        RetVal = "Success"
                        print "Successfully Assigned Sensor"
                        continue
                    else:
                        return None

                #Check 05 Location and Related Sensor ID
                if(DBSensorVariable[i] == "05"):
                    _DBSensorID5 =  DBSensorVariable[i-1]
                    _DBLocation5 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation5, _DBSensorID5
                    RetVal = assignNewSensorToBTC(conn, _DBLocation5, _DBSensorID5)

                    if RetVal == "aa":
                        RetVal = "Success"
                        print "Successfully Assigned Sensor"
                        continue
                    else:
                        return None

                #Check 06 Location and Related Sensor ID
                if(DBSensorVariable[i] == "06"):
                    _DBSensorID6 =  DBSensorVariable[i-1]
                    _DBLocation6 =  DBSensorVariable[i]
                    print "in DBSensorVariable[i] ",_DBLocation6, _DBSensorID6
                    RetVal = assignNewSensorToBTC(conn, _DBLocation6, _DBSensorID6)

                    if RetVal == "aa":
                        RetVal = "Success"
                        print "Successfully Assigned Sensor"
                        continue
                    else:
                        return None

        
                
        #print DBSensorVariable[0]
        #print BluetoothSocketVariable[0]

            print "After elif (mylist != None and conn != None)"       
            return RetVal
        
        else:
            print ("Failed - mylist and Bluetooth conn are None:",mylist,conn)
            my_logger.warning("Failed - mylist and Bluetooth conn are None: %s %s",mylist,conn)
            return None

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - compare_DBSensorUID_DBLocation_BTyreNo_BTyreID:%s, %s, %s ",e, DBSensorVariable, BluetoothSocketVariable)
        print ("Failed - compare_DBSensorUID_DBLocation_BTyreNo_BTyreID: ",e, DBSensorVariable, BluetoothSocketVariable)
        return None
                
    
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
                    #print data
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
                
rows = 8
columns= 16
mylist = [['0' for x in range(columns)] for x in range(rows)]

vehID = 0
vehName = ""
BUID = ""
RFUID = ""
dbConn = ""

dispCommand = "Sarojini Nagar Depot"

#function for java
def javaFun_start(tag_id):
    tag_id1 = tag_id
    print "Work.py is executing"
    print tag_id1

def javaFun_end():
    tag_id1 = None
    print tag_id1


def fun_VehName(vehName):

    try:

        print(" fun_VehName Function " + vehName)

        if (vehName != None):

            print(" fun_VehName Function " + vehName)

            if(database!=None):
                dbConn = db.create_db_connection(database)
                print(" Database Function " + vehName)

                if(dbConn != None):
                    #Get the Device Detail by vehNo from GUI
                    #vehID, vehName, BUID, RFUID = db_DeviceDetails_by_rfiduid(dbConn, tag_id)
                    vehDetails1 = db.select_DeviceDetails_by_vehName(dbConn, vehName)

                    if(vehDetails1 != None):
                        print("Query the Database to read Tyre Details, Sensor ID, Position by vehID")
                            
                        #vehID = vehDetails1[0]
                        #vehName = vehDetails1[1]
                        #BUID = vehDetails1[2]
                        RFUID = vehDetails1[3]
                        

                        print RFUID

                        return RFUID
                    else:
                        my_logger.warning("Failed - vehDetails1 : %s",vehDetails1)
                        print("Failed - vehDetails1 : ",vehDetails1)
                        return None
                else:
                    dbConn.close()
                    my_logger.warning("Failed - dbConn : %s",dbConn)
                    print("Failed - dbConn : ",dbConn)
                    return None

            else:
                my_logger.warning("Failed - database : %s",database)
                print("Failed - database : ",database)
                return None
                
        else:
            my_logger.warning("Failed - vehName : %s",vehName)
            print("Failed - vehName : ",vehName)
            return None
        
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - GUI Attribute to Set (vehName) None:%s, %s ",e, vehName )
        print ("Failed - GUI Attribute to Set (vehName) None: ",e, vehName )

        return None
    



def bluetoothctlObjectPair(BUID):

    #BUID = "00:13:EF:C0:01:24"   
    try:

        #Creating Object for bluetoothctl
        autopair = BtAutoPair.BtAutoPair()
        autopair.enable_pairing()

        bl = bluetoothctl.Bluetoothctl()
        
        #Creating Object for BtAutoPair
        #print("Init bluetooth...")  

        if BUID != None:

            print "BUID :", BUID

            #check for Paired Bluetooth MAC Address
            paired = bl.get_paired_devices()
                    
            #for i in range(len(paired)):
                #print i, ":",  paired[i]

            #check for Paired Bluetooth MAC Address with new BUID 
            paired_valid = any(keyword in BUID for keyword in paired)
            #print paired_valid

            if paired_valid == False:
                
                print("Ready!")
                bl.start_scan()
                print("Scanning for 10 seconds...")

                for i in range(0, 10):
                    print(i)
                    time.sleep(1)

                print("Searching for discoverable 10 times...")

                for i in range(0, 10): 

                    #check for discoverable Bluetooth MAC Address in Nearby Device
                    discover = bl.get_discoverable_devices()

                    #check for discoverable Bluetooth MAC Address in Nearby Device with BUID
                    discover_valid = any(keyword in BUID for keyword in discover)
                    #print discover_valid

                    if discover_valid == True:
                        break
                    if discover_valid == False:
                        continue
                        

                #for i in range(len(discover)):
                    #print "Discover Device", i, ":",  discover[i]

                if discover_valid == True:

                    print("Pairing for 10 seconds...")
                    #Pair the New BUID
                    pair = bl.pair(BUID)

                    if pair == True:
                        
                        my_logger.error("Success - Successfully Paird with the New BUID: %s ", BUID )
                        print ("Success - Successfully Paird with the New BUID: ", BUID )
                        return "Success"
                    else:
                        
                        my_logger.error("Failed - Not Paird with the New BUID: %s ", BUID )
                        print ("Failed - Not Paird with the New BUID: ", BUID )
                        return None 
                else:
                    
                    my_logger.error("Failed - Not Availabel in Discoverable devices list BUID: %s ", BUID )
                    print ("Failed - Not Availabel in Discoverable devices list BUID: ", BUID )
                    return None
                    

            elif paired_valid == True:
                #print "Already Paired in the System:", BUID
                my_logger.error("Success - Successfully Already Paired in the System: %s ", BUID )
                print ("Success - Successfully Already Paired in the System: ", BUID )
                return "Success"

            else:
                my_logger.error("Failed - Not Availabel or Error value in Paired devices list BUID: %s ", BUID )
                print ("Failed - Not Availabel or Error value in Paired devices list BUID: ", BUID )
                return None    
                

        else:
            my_logger.error("Failed - BluetoothctlObjectPair BUID is None: %s ", BUID )
            print ("Failed - BluetoothctlObjectPair BUID is None: ", BUID )
            return None    
            
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - BluetoothctlObjectPair:%s, %s ",e, BUID )
        print ("Failed - BluetoothctlObjectPair: ",e, BUID )

        return None


def fun_main(RFIDTID):
    
    
    try:
        print(" Main Function " + RFIDTID, len( RFIDTID ) )
        if (RFIDTID == None) or (RFIDTID == ""):

            print("RFID Module Read TAG ID Function")

            tag_id = rfid.RFIDUHFQueryTag()

        elif(RFIDTID != None) and (RFIDTID != ""):
            
            tag_id = RFIDTID
            
        
        print "tag_id", tag_id
        
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
                            #print dbConn
                            DBSensorVariable = db_DeviceDetails_by_vehID(dbConn, vehID)                        

                            #print DBSensorVariable
                            dbConn.close()

                            if DBSensorVariable == None:
                                my_logger.warning ("Vehicle ID Related Sensors is None :%s ", DBSensorVariable)
                                return None, "Vehicle ID Related Sensors is None "+DBSensorVariable, vehID, "Failed"
                                    
                        else:
                            my_logger.warning ("Failed - Vehicle ID not Available or None Function :%s ", vehID)
                            return None, "Failed - Vehicle ID not Available or None "+ vehID , "Failed"


                        #Query DB Device Detail to read vehID, vehName, BUID, RFUID
                        if (BUID != None):
                            print("Connect socket RFCOMM to Bluetooth Controller by BUID")                 
                            print("Create a Bluetooth connection")

                            #Creating Object for bluetoothctl
                            RetValBLE = bluetoothctlObjectPair(BUID)

                            if RetValBLE == "Success":                                

                                bleConn = blecontroller.connect_ble(BUID)

                                if bleConn != None:
                                    print ("Success - Trying to connect Bluetooth BUID", BUID, bleConn)

                                    BluetoothSocketVariable, BLEstatus = Connect_Socket_Bluetooth_by_BUID(bleConn)                                  

                                    if(BluetoothSocketVariable != None and BLEstatus == "Success"):
                                            
                                        #RetValCompare = configure_BTController(bleConn, DBSensorVariable)
                                        RetValCompare = compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(bleConn, DBSensorVariable, BluetoothSocketVariable)
                                        #RetValCompare = compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(bleConn, DBSensorVariable, None)

                                        if RetValCompare != None:
                                            print ("Success - Trying to connect Bluetooth vehName", vehName, vehID, "Success")
                                            return bleConn, vehName, vehID, "Success"

                                        else:
                                            print ("Failed - RetValCompare is None", RetValCompare)
                                            my_logger.warning ("Failed - RetValCompare is None : %s", RetValCompare)
                                            return None, "Failed - RetValCompare is None", None, "Failed"

                                    else:
                                        print ("Failed - BluetoothSocketVariable is None", BluetoothSocketVariable)
                                        my_logger.warning ("Failed - BluetoothSocketVariable is None : %s", BluetoothSocketVariable)
                                        return None, "Failed - BluetoothSocketVariable is None", None, "Failed"

                                else:
                                    print ("Failed - Trying to connect Bluetooth BUID", BUID, bleConn)
                                    my_logger.warning ("Failed - Trying to connect Bluetooth BUID: %s %s", BUID, bleConn)
                                    bleConn.close()
                                    return None, "Failed - Trying to connect Bluetooth BUID ", None, "Failed"

                            else:
                                print ("Failed - bluetoothctlObjectPair in None: ", BUID)
                                my_logger.warning ("Failed - bluetoothctlObjectPair in None %s: ", BUID)
                                return None, "Failed - bluetoothctlObjectPair in None: ", None, "Failed"
                                
                        else:
                            print ("Failed - Trying to connect Bluetooth BUID is None")
                            my_logger.warning ("Failed - Trying to connect Bluetooth BUID is None")
                            bleConn.close()
                            return None, "Failed - Trying to connect Bluetooth BUID in None " +BUID, None, "Failed"

                            
                    else:
                        my_logger.warning ("Failed - RFID Tag ID is not available in DB :%s ", tag_id)
                        return None, "Failed - RFID Tag ID is not available in DB "+ tag_id, None, "Failed"
                else:
                    dbConn.close()
                    my_logger.warning ("Failed - No DB Connection ")
                    return None, "Failed - No DB Connection ", None, "Failed"
            else: 
                my_logger.warning ("Failed - Database path Not Available ")
                return None, "Failed - Database path Not Available ", None, "Failed"
        else:
         #   my_logger.warning ("Failed - RFID Tag ID is not available in DB %s: ", tag_id)
            print ("Failed - RFID Tag ID is not available in DB %s: ", tag_id)
            return None, "Failed - No TagId Connection ", None, "Failed"

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Main Function Crashed:fun_main(RFIDTID) %s ",e)
        print ("Failed - Main Function Crashed:fun_main(RFIDTID) ",e)
        #dbConn.close()
        
        return None, "Failed - Main Function Crashed:fun_main(RFIDTID) ", None, "Failed"

    

def fun_main_Bluetooth(bleConn, vehName, vehID, loop, status):

    #print "fun_main_Bluetooth(blecon)", bleConn, vehName
    
    try:
        
        if(bleConn != None):                           

            #print("Configure BT SensorUID, tirePosition based on DB Before ")


            #Return value is Success or aa                       
            if (status == "Success" ):
                    
                mylist, status = Connect_Socket_Bluetooth_by_BUID(bleConn)

                if (mylist != None) and (status == "Success"):

                    #print("Configure BT SensorUID, tirePosition based on DB After ", mylist)
                    time.sleep(0.2)
                    #bleConn.close()
                                    
                    #Dummy
                    #mylist = [  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                    #            [0, 'a1', '41', '08', '63', '00', '05'], \
                    #            [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '50', '78', '00'], \
                    #            [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '25', '58', '00'], \
                    #            [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '30', '70', '00'], \
                    #            [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '45', '65', '00'], \
                    #            [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '00', '00', '00', '00'], \
                    #            [0, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]

                            
                    return mylist, vehName, "Success"

                else:
                    my_logger.warning ("Failed - Connect_Socket_Bluetooth_by_BUID is None %s %s", mylist, status)
                    print ("Failed - Connect_Socket_Bluetooth_by_BUID is None", mylist, status)
                    return None, "Failed - Connect_Socket_Bluetooth_by_BUID is None", "Failed" 
                                
            else:
                my_logger.warning ("Failed - fun_main_Bluetooth status: %s", status)
                print ("Failed - fun_main_Bluetooth status: ", status)
                return None, "Failed - fun_main_Bluetooth status:", "Failed"   
        else:
            my_logger.warning ("Failed - bleConn  not Available or None Function : ")
            bleConn.close()
            return None, "Failed - bleConn  not Available or None Function : ", "Failed"
            
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Main Function Crashed:%s ",e)
        print ("Failed - Main Function Crashed: ",e)

        return None, "Failed - Main Function Crashed: " , "Failed"
        #return ("Failed - Main Function Crashed: " +e)


def display_Parameter_LED(mylist, vehName, vehID, date_time):

    #Current date and time
    #t = datetime.utcnow()
    #date_time = time.strftime('%H:%M:%S %d/%m/%Y')
    #date_timeDB = int(datetime.datetime.now().strftime("%s")) * 1000
    print date_time

    try:
        if mylist != None:
            print("displayLEDBoard ")
            #Display this data in LED Display with Commands 
            dispVar = display.displayLEDBoardParameters(mylist)
            print dispVar, vehName
                        
            if dispVar != None:
                                    
                #display.displayLEDBoard(vehName, dispCommand, date_time, dispVar)
                display.displayLEDBoard(vehName, dispCommand, date_time, dispVar)

            else:
                my_logger.warning ("Failed - dispVar  not Available or None: %s", dispVar)
                print ("Failed - dispVar  not Available or None:", dispVar)
                #return None, " dispVar  not Available or None", "Failed"
                            
                #return None, "dispVar  not Available or None", "Failed"
        else:
            my_logger.warning ("Failed - display_Parameter_LED.mylist  not Available or None: %s", mylist)
            print ("Failed - display_Parameter_LED.mylist  not Available or None:", mylist)

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - dispVar  not Available or None :%s ",e)
        print ("Failed - dispVar  not Available or None:%s ",e)

def display_Parameter_API(mylist, vehName, vehID, date_time):        

        DBTyreDetail = []
        date_timeDB = int(datetime.datetime.now().strftime("%s")) * 1000
        #update to the live server            
        try:

            #update to the live server
            RetVal = apiupdate.prepareJsonString(int(vehID), mylist)

            print ("RetVal - RetVal is RetVal : ",RetVal)
            
            '''
            #Data not send to server then it has to Update to the Record data
            if RetVal == None:

                 
                try:
                                    
                    dbConn = db.create_db_connection(database)
                    print ("Success - dbConn is Created : ",dbConn)
                    #with dbConn: 
                    with dbConn:

                        print ("Success - dbConn is Created Inside : ", vehName, vehID, date_timeDB)
                        #Update the Report_data_master Table by VehId
                        report_data_master_id = db.update_Report_data_master_by_VehId(dbConn, vehID, date_timeDB)
                        print ("Success - report_data_master_id is Created : ", vehID,report_data_master_id)
                        print ("Success - dbConn is Created : ",dbConn)
                        
                        #Query the TyreId and SensorUID by unsig VehID
                        TyreDetail = db.select_TyreDetails_tyreId_by_VehId(dbConn, vehID)
                        print ("Success - select_TyreDetails_tyreId_by_VehId is Created : ",TyreDetail)
                        print ("Success - dbConn is Created : ",dbConn)


                        DBtotalTyres = len(TyreDetail)
            
                        if TyreDetail is not None:
                            for DBi in range(0, DBtotalTyres):
                                    
                                Tyre_row = TyreDetail[DBi]

                                SID = Tyre_row[1]
                                    
                                T = Tyre_row[0]          
                                        
                                #print SID1, L1
                                DBTyreDetail.append(T)
                                DBTyreDetail.append(SID)
      
                            
                            print DBTyreDetail

                        print ("Success - dbConn is Created : ",dbConn)

                        #update the Report_data_master_child Table by report_data_master_id               
                        ret = db.update_Report_data_child_by_report_data_master_id(dbConn, report_data_master_id, vehID, mylist, DBTyreDetail)
                        #update_Report_data_child_by_report_data_master_id(conn, report_data_master_id, vehID, mylist, DBTyreDetail)

                        print ("Success - dbConn is Created : ",dbConn, ret)
                        #dbConn.close()

                    #else:
                        #dbConn.close()
                        #my_logger.error("Failed - dbConn is None :%s ",dbConn)
                        #print ("Failed - dbConn is None : ",dbConn)

                except:
                    e = sys.exc_info()[0]
                    my_logger.error("Failed - display_Parameter_API :%s ",e)
                    print ("Failed - display_Parameter_API ",e)

                    #return None, "dispVar  not Available or None", "Failed"
            
            elif RetVal == "Success":
                my_logger.error("Success - prepareJsonString : ")
                print ("Success - prepareJsonStringis None : ")

            '''

            if RetVal == None:

                database = "/opt/Aquire/sqlite/TPMS.db"
                conn = db.create_db_connection(database)

                                
                with conn:
                    
                    print ("Success - dbConn is Created conn: ",conn)
                    

                    db.update_Report_data_master_by_VehId(conn, vehID, date_timeDB)

                    
                    print "report_data_master_id"
                    report_data_master_id = db.select_Report_data_master_report_data_master_id_by_VehId(conn, vehID)
                        
                    

                    print "report_data_master_id", report_data_master_id
                    

                    TyreDetail = db.select_TyreDetails_tyreId_by_VehId(conn, vehID)

                    
                    
                    DBtotalTyres = len(TyreDetail)

                    if TyreDetail is not None:
                        for DBi in range(0, DBtotalTyres):
                                
                            Tyre_row = TyreDetail[DBi]

                            SID = Tyre_row[1]
                                
                            T = Tyre_row[0]          
                                    
                            #print SID1, L1
                            DBTyreDetail.append(T)
                            DBTyreDetail.append(SID)
              
                                    
                        print DBTyreDetail
                                               
                                       
                    #print TyreIDL
                    #for i in range (len(TyreIDL)):
                        #print TyreIDL[i]

                    #print "report_data_master_id", report_data_master_id
                    DBStatus = db.update_Report_data_child_by_report_data_master_id(conn, report_data_master_id, vehID, mylist, DBTyreDetail)


                    if DBStatus == "Success":

                        time.sleep(0.10)
                        conn.close()
                    

            else:
                print ("Failed - dbConn is Error conn: ")
                 
        except:
            e = sys.exc_info()[0]
            my_logger.error("Failed - prepareJsonString :%s ",e)
            print ("Failed - prepareJsonString ",e)

            #return None, "dispVar  not Available or None", "Failed"
                        
        
    
        '''               
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

                    RetValCompare = compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(bleConn, DBSensorVariable, BluetoothSocketVariable)
                else:
                    my_logger.warning ("DBSensorVariable and BluetoothSocketVariable not Available or None Function : %s %s", DBSensorVariable, BluetoothSocketVariable)
            else:
                my_logger.warning ("Bluetooth ID not connected or Host Not Available or None Function : ")
        else:
            my_logger.warning ("Bluetooth ID not Available or None Function : %s", BUID)
          
        #Query DB Device Detail to read vehID, vehName, BUID, RFUID
        if RetValCompare is not None:
            BluetoothSocketVariableFinal = Connect_Socket_Bluetooth_by_BUID(bleConn)    
            print BluetoothSocketVariableFinal
        ''



    
    update_Latest_data_by_VehId(conn, 2, '2015-01-04', '2015-01-06',2)
    
           
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Main Function Crashed:%s ",e)
        print ("Failed - Main Function Crashed: ",e)

        return None
    '''
   
    
       
    #DBSensorVariable = (u'SensorUID 15', '01', u'SensorUID 14', '02', u'SensorUID 22', '03', u'SensorUID 21', '04', u'SensorUID 20', '06', u'SensorUID 19', '05')
    #DBSensorVariable = (u'ba6b09', '01', u'ba6d6d', '02', u'56a8cb', '03', u'56a6be', '04', u'56a781', '05', u'56a7c5', '06')
    #BluetoothSocketVariable = ('01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00', '06', '56a7c5', '000000', '00')
    #DBSensorVariable = (u'ba6b09', '01', u'56a8cb', '03', u'ba6d6d', '02', u'56a6be', '04', u'56a781', '06', u'56a7c5', '05')
    #BluetoothSocketVariable = (5, '01', 'ba6b09', '000000', '00', '02', 'ba6d6d', '000000', '00', '03', '56a8cb', '000000', '00', '04', '56a6be', '000000', '00', '05', '56a781', '000000', '00')
    #BluetoothSocketVariable = ( )
    #compare_DBSensorUID_DBLocation_BTyreNo_BTyreID(DBSensorVariable, BluetoothSocketVariable)
    
    #print("After While Loop Connect socket RFCOMM to Bluetooth Controller by BUID")
    #bleConn.close()

import threading
if __name__ == "__main__":  

    

    #def printit():
        #threading.Timer(5.0, printit).start()
        #print "Hello, World!"
        #fun()
    #printit()
    loop = True
    vehName = "9406"
    tagId = fun_VehName(vehName)
    print tagId
    bleConn, vehName, vehID, status = fun_main(tagId)

    #mylist, vehName, BLEStatus = fun_main_Bluetooth(bleConn)


    if ((bleConn != None) and (status == "Success")):
        print ("1111",status)
        #while loop == True:

        mylist, vehName, BLEStatus = fun_main_Bluetooth(bleConn, vehName, vehID, loop, status)
        print BLEStatus, vehName

        time.sleep(2)
            
        if BLEStatus == "Failed":
            loop = False
                           

    #print v1
    #print v2
    #print v3
    
        
