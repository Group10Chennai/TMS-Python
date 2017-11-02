################################################################
# TMS Integration -09-2017
################################################################

import serial
import binascii
import sys
import string
import bluetooth
from bluetooth import*
import bluetooth._bluetooth as _bt
import socket
import subprocess
import time


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

Tyredata = []
T = []
tyreDetail = []

# TPMS Bluetooth FMS request TPMS to send all recorded tyres data
def TpmsTireDataPosition():

    try:  
        #TpmsModuleQuery = ['\xAA', '\x41', '\xA1', '\x07', '\x63', '\x00']
        TpmsModuleQuery = ['AA', '41', 'A1', '07', '63', '00']
        #TpmsModuleQuery = ["AA", "41", "A1", "07", "63", "00"]

        #TpmsModuleQueryID = "AA41A1076300"
        if(TpmsModuleQuery != None):
            
            #print TpmsModuleQuery
            TpmsCksm = TpmsCalcChecksum(TpmsModuleQuery)
            
            TpmsModuleQueryID = ''.join(TpmsModuleQuery)
            #print TpmsModuleQuery
            
            #print TpmsCksm
            if(TpmsCksm != None):
                #Append checksum to the Query List
                TPMSQueryAllTyre = TpmsModuleQueryID + TpmsCksm
                TPMSQueryAllTyre = TPMSQueryAllTyre.strip()
                print TPMSQueryAllTyre
            else:
                my_logger.warning("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                print("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                return None

            my_hex_TPMS = TPMSQueryAllTyre.decode('hex')
            #print my_hex_TPMS       
            #print binascii.b2a_hex(my_hex_TPMS)

            #serial.write(my_hex_TPMS)

            return  my_hex_TPMS

        else:
            my_logger.warning("Failed - Bluetooth Query Command Value not Avalable: %s",TpmsModuleQuery)
            print("Failed - Bluetooth Query Command Value not Avalable: ",TpmsModuleQuery)
            return None

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Command Value Error: %s, %s ",e, TpmsModuleQuery)
        print ("Failed - Bluetooth Query Command Value Error:",e, TpmsModuleQuery)

        return None


def Tpms_Tire_SET_Position1(L1, SID1):

    TpmsSET1 = ['AA', '41', 'A1', '0E', '63']

    try:  
    
        if(L1, SID1 != None):
            TpmsSET1.append(L1)
            TpmsSET1.append(SID1[0:2])
            TpmsSET1.append(SID1[2:4])
            TpmsSET1.append(SID1[4:6])
                
            TpmsSET1.append('00')
            TpmsSET1.append('00')
            TpmsSET1.append('00')
            TpmsSET1.append('00')
        else:
            my_logger.warning("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: %s, %s",L1, SID1)
            print ("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: ",L1, SID1)
            return None

        if(TpmsSET1 != None):
            #print TpmsSET1
            TpmsCksm = TpmsCalcChecksum(TpmsSET1)
            #print TpmsCksm

            TpmsSET = ''.join(TpmsSET1)
            #print TpmsSET
            
            if(TpmsCksm != None):
                #Append checksum to the Query List
                TPMSQueryAddTyre = TpmsSET+(TpmsCksm)
                #print TPMSQueryAddTyre
            else:
                my_logger.warning("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                print("Failed - Bluetooth Query checksum not Avalable: ",TpmsCksm)
                return None
            
            my_hex_TPMS = TPMSQueryAddTyre.decode('hex')
            #print my_hex_TPMS       
            print binascii.b2a_hex(my_hex_TPMS)

            return my_hex_TPMS
        
        else:
            my_logger.warning("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: %s, %s, %s",L1, SID1, TpmsSET1)
            print ("Failed - Bluetooth Query to SET Tyre Position1(Location, Sensor ID) not Avalable: ",L1, SID1, TpmsSET1)
            return None
        
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: %s, %s, %s",e, L1, SID1 )
        print ("Failed - Bluetooth Query Attribute to Set (Location, Sensor ID) None: ",e, L1, SID1 )

        return None 
    

# TPMS Bluetooth to SET Tyre Data
def Tpms_SET_TireID(conn, TPMSET):

    #TPMSID1 = TpmsTireDataPosition()
    #print binascii.b2a_hex(TPMSET)
    
    print "performing Bluetooth Communication..."
    #s.send(TPMSID1)

    #while True:
    #s.send(my_hex)

    if(conn != None):
        
        if(TPMSET != None):
            #print "TPMSET :",binascii.b2a_hex(TPMSET)
        
            while(True):
                try:
                    conn.send(TPMSET)
            
                    time.sleep(1)

                    data = conn.recv(1024)

                    hex_data = binascii.b2a_hex(data)
                    RcvResponse =  hex_data[10:12]
                    print RcvResponse
                    
                    if (RcvResponse == "aa"):
                        print binascii.b2a_hex(data)
                        return RcvResponse
                        break;
                    else:
                        print ("Failed - Bluetooth Send and Receive Communication RcvResponse is Not Valuable aa:",data)
                        my_logger.warning("Failed - Bluetooth Send and Receive Communication RcvResponse is Not Valuable aa: %s",data)
                        #conn.close()
                        return None
                   
                    
                except bluetooth.btcommon.BluetoothError as e:
                    print ("Failed - Bluetooth Send and Receive Communication bluetooth.btcommon.BluetoothError",e)
                    my_logger.error ("Failed - Bluetooth Send and Receive Communication bluetooth.btcommon.BluetoothError",e)  
                    #conn.close()
                    time.sleep(2)
                    return None
                    pass
        else:
            print ("Failed - Bluetooth Send and Receive Communication Query Command is None:",TPMSET)
            my_logger.warning("Failed - Bluetooth Send and Receive Communication Query Command is None: %s",TPMSET)
            #conn.close()
            return None
    else:
        print ("Failed - Bluetooth Send and Receive Communication Bluetooth Connection is None:",TPMSET)
        my_logger.warning("Failed - Bluetooth Send and Receive Communication Bluetooth Connection is None: %s",TPMSET)
        #conn.close()
        return None
    
    
    
    
#    s.close()

#    return data     


#convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''

   

# TPMS Bluetooth Calculate Checksum
def TpmsCalcChecksum(TpmsModuleQuery1):

    try:
        count = len(TpmsModuleQuery1)
        #print TpmsModuleQuery1
        
        i = 0
        cksm = 0
        if(TpmsModuleQuery1 != None):
            
            while (i < count-1):
                #print(TpmsModuleQuery1[i])
                #val = binascii.b2a_hex(TpmsModuleQuery1[i])
                val = TpmsModuleQuery1[i].decode("hex")
                #cksm += int (val, 16)
                cksm += int(TpmsModuleQuery1[i], 16)
                #print cksm
                #i += 1
            
                cksm1 = hex(cksm).split('x')[-1]
                #cksm1 = hex(cksm)
                #print cksm1
                i += 1
            
            #print cksm1
            high, low = cksm1[:1], cksm1[1:3]
            #print(high, low)

            return low
        else:
            my_logger.warning("Failed - Bluetooth Query Command for Checksum is Not Available: %s", TpmsModuleQuery1)
            print ("Failed - Bluetooth Query Command for Checksum is Not Available: ", TpmsModuleQuery1)
            return None
    
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Bluetooth Query Command for Checksum Query is Not Available:%s %s ",e, TpmsModuleQuery1)
        print ("Failed - Bluetooth Query Command for Checksum Query is Not Available: ", e,TpmsModuleQuery1)
        return None


def connect_ble(BUID1):
    
    print "performing inquiry..."
    #serverMACAddress = '00:13:EF:C0:02:1E'
    port = 1
    
      
    '''
    nearby_devices = bluetooth.discover_devices(duration=4, lookup_names = True, flush_cache=True)

    print "found %d devices" % len(nearby_devices)

    for addr, name in nearby_devices:
        print "  %s - %s" % (addr, name)
    '''
    if(BUID1 != None):
        while(True):        
            print BUID1
            try:
                print "performing Bluetooth Socket Creation..."
                bleCon = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                #return bleCon
                break;

            except bluetooth.btcommon.BluetoothError as e:
                my_logger.error("Failed - Bluetooth Socket Creation: %s", e)
                print ("Failed - Bluetooth Socket Creation: ", e)
                #bleCon.close()
                time.sleep(2)
                #return None
                pass 

        print "trying to connect to %s on 0x%X" % (BUID1, port)

        if(bleCon is not None):
            while(True):
                try:
                    bleCon.connect((BUID1, port))
                        
                    print "connected to %s on 0x%X" % (BUID1, port)
                    print "performing Bluetooth Communication..."
                    return bleCon
                    break;

                except bluetooth.btcommon.BluetoothError as e:
                    print ("Failed Trying to connect on %s on 0x%X" % (BUID1, port),e)
                    my_logger.error("Failed - Trying to connect %s",e)  
                    time.sleep(2)
                    bleCon.close()
                    return None
                    pass
                    
                #except _bt.error as e:
                    #raise BluetoothError(str(e))
                    #my_logger.error(e)  
                    #bleCon.close()
                    #pass
                    #return None
            
        #except Error as e:
            #my_logger.error(e)  
            #return None
        else:
            my_logger.warning("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID1)
            print ("Failed - Bluetooth Connection Socket is Not Avalable: %s", BUID1)
            return None
            
    else:
        my_logger.warning("Failed - Bluetooth MAC Address is Not Avalable: %s", BUID1)
        print("Failed - Bluetooth MAC Address is Not Avalable: %s", BUID1)
        return None

    '''
    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Bluetooth Query Attribute Value not Avalable:",e)

        return None
    '''

#def Query_Tpms_SET_TireID(s):


    

def Query_TpmsTireDataPosition(s, TPMSID1):
    
    #TPMSID1 = TpmsTireDataPosition()
    print binascii.b2a_hex(TPMSID1)
    
    #print "performing Bluetooth Communication..."
    #s.send(TPMSID1)
    
    #while True:
    #s.send(my_hex)
    if(s != None):
        if(TPMSID1 != None):
        
            while(True):
                try:
                    s.send(TPMSID1)
            
                    time.sleep(1)

                    data = s.recv(1024)

                    print binascii.b2a_hex(data)
                    return data
                    break;
                    
                except bluetooth.btcommon.BluetoothError as e:
                    print ("Failed - Bluetooth Send and Receive Communication bluetooth.btcommon.BluetoothError",e)
                    my_logger.error ("Failed - Bluetooth Send and Receive Communication bluetooth.btcommon.BluetoothError",e)  
                    s.close()
                    time.sleep(2)
                    return None
                    pass
        else:
            print ("Failed - Bluetooth Send and Receive Communication Query Command is None:",TPMSID1)
            my_logger.warning("Failed - Bluetooth Send and Receive Communication Query Command is None: %s",TPMSID1)
            s.close()
            return None
    else:
        print ("Failed - Bluetooth Send and Receive Communication Bluetooth Connection is None:",TPMSID1)
        my_logger.warning("Failed - Bluetooth Send and Receive Communication Bluetooth Connection is None: %s",TPMSID1)
        s.close()
        return None

#from parse import *


def ParseBluetoothTyre(data):

    #hexstr = "aaa14108630005fcaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081"
    #hexstr = "aaa14108630006fdaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081aaa1410f63000656a7c500000000c6"
    # ok, figure the fixed fields we've pulled out and type convert them
    #fixed_fields = list(m.groups())
    #for n in m:
        #if n in type_conversions:
            #fixed_fields[n] = type_conversions[n](fixed_fields[n], m)
        #print n
    #fixed_fields = tuple(fixed_fields[n] for n in self._fixed_fields)

    #data = 'From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008'
    #atpos = data.find('aa')
    #print atpos
    #word = 'banana'
    #count = 0
    #for letter in data:
        #if letter == 'aa':
            #count = count + 1
    #print count

    hexstr = binascii.b2a_hex(data)
    
    totalTyres = int(hexstr[12:14])
    
    for tyre in range (1, totalTyres+1):
        #print tyre
        if tyre is 1:
            if(hexstr[16:18] =="aa"):
                
                Tyre1No = hexstr[28:30]
                    
                if(int(Tyre1No) == tyre):

                    Tyre1ID = hexstr[30:36]
                    Tyre1Presure = hexstr[36:42]
                    Tyre1Temp = hexstr[42:44]
                    
                    print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp

                else:
                    Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp = None
            else:
                Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp = None
        

        elif tyre is 2:
            if(hexstr[46:48] =="aa"):

                Tyre2No = hexstr[58:60]
                
                if (int(Tyre2No) == tyre):
                    Tyre2ID = hexstr[60:66]
                    Tyre2Presure = hexstr[66:72]
                    Tyre2Temp = hexstr[72:74]
                    print tyre, Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp

                else:
                    Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp = None
            else:
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp = None
        

        elif tyre is 3:
            if(hexstr[76:78] =="aa"):
                    
                Tyre3No = hexstr[88:90]
                    
                if(int(Tyre3No) == tyre):
                        
                    Tyre3ID = hexstr[90:96]
                    Tyre3Presure = hexstr[96:102]
                    Tyre3Temp = hexstr[102:104]
                    print tyre, Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp

                else:
                    Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp = None
            else:
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp = None
        

        elif tyre is 4:
            if(hexstr[106:108] =="aa"):
                    
                Tyre4No = hexstr[118:120]
                if(int(Tyre4No) == tyre):
                        
                    Tyre4ID = hexstr[120:126]
                    Tyre4Presure = hexstr[126:132]
                    Tyre4Temp = hexstr[132:134]
                    print tyre, Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp

                else:
                    Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp = None
            else:
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp = None
        

        elif tyre is 5:
            if(hexstr[136:138] =="aa"):
                    
                Tyre5No = hexstr[148:150]
                if(int(Tyre5No) == tyre):
                        
                    Tyre5ID = hexstr[150:156]
                    Tyre5Presure = hexstr[156:162]
                    Tyre5Temp = hexstr[162:164]
                    print tyre, Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp
                    
                else:
                    Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp = None
            else:
                Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp = None
        

        elif tyre is 6:
            if(hexstr[166:168] =="aa"):
                    
                Tyre6No = hexstr[178:180]
                    
                if(int(Tyre6No) == tyre):
                        
                    Tyre6ID = hexstr[180:186]
                    Tyre6Presure = hexstr[186:192]
                    Tyre6Temp = hexstr[192:194]
                    print tyre, Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp

                else:
                    Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = None
            else:
                Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = None

        else:
            Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = None



    if (totalTyres == 1):
        
        print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp
        return tyreTyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp
    
    elif (totalTyres == 2):

        print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,\
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp
        return tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp

    elif (totalTyres == 3):

        print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp, \
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp
        return tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp

    elif (totalTyres == 4):

        print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp
        return tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp

    elif (totalTyres == 5):
       
        print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
        return tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
                

    elif (totalTyres == 6):

        print tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
        return tyre, Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp, \
                Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,\
                Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,\
                Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,\
                Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,\
                Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
        
    #return (Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp, Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp)    
        
'''
    try:
        if(data != None):

            hexstr = binascii.b2a_hex(data)
            #hexstr = "aaa14108630006fdaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081aaa1410f63000656a7c500000000c6"
            #aaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081"

            hexstr = "aaa14108630005fcaaa1410f630001ba6b09000000002d"
            string1 = "Hello"
            #totalTyres = int(hexstr[12:14])
            #print totalTyres
            #for tyre in range (1, totalTyres+1):
            #for(i in string1):
                #print i

 
            #if(totalTyres = 0):
                #print totalTyres
                #print tyre
                
                if(hexstr[16:18] =="aa"):
                    
                    Tyre1No = hexstr[28:30]
                    
                    if(int(Tyre1No) == tyre):
                        Tyre1ID = hexstr[30:36]
                        Tyre1Presure = hexstr[36:42]
                        Tyre1Temp = hexstr[42:44]
                        print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp
                    else:
                        #print "else : ",Tyre1No,tyre
                        Tyre1No = None
                else:

                    Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp = None
                
                if(hexstr[46:48] =="aa"):
                    
                    Tyre2No = hexstr[58:60]
                    
                    if (int(Tyre2No) == tyre):
                        Tyre2ID = hexstr[60:66]
                        Tyre2Presure = hexstr[66:72]
                        Tyre2Temp = hexstr[72:74]
                        print Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp
                    else:
                        
                        #print "else : ",int(Tyre2No),tyre
                        Tyre2No = None
                else:
                    
                    Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp = None
                
                if(hexstr[76:78] =="aa"):
                    
                    Tyre3No = hexstr[88:90]
                    if(int(Tyre3No) == tyre):
                        
                        Tyre3ID = hexstr[90:96]
                        Tyre3Presure = hexstr[96:102]
                        Tyre3Temp = hexstr[102:104]
                        print Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp
                    else:
                        #print "else : ",int(Tyre3No),tyre
                        Tyre3No = None
                else:
                    Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp = None


                if(hexstr[106:108] =="aa"):
                    
                    Tyre4No = hexstr[118:120]
                    if(int(Tyre4No) == tyre):
                        
                        Tyre4ID = hexstr[120:126]
                        Tyre4Presure = hexstr[126:132]
                        Tyre4Temp = hexstr[132:134]
                        print Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp
                    else:
                        #print "else : ",int(Tyre4No),tyre
                        Tyre4No = None
                else:
                    Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp = None

                if(hexstr[136:138] =="aa"):
                    
                    Tyre5No = hexstr[148:150]
                    if(int(Tyre5No) == tyre):
                        
                        Tyre5ID = hexstr[150:156]
                        Tyre5Presure = hexstr[156:162]
                        Tyre5Temp = hexstr[162:164]
                        print Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp
                    else:
                        #print "else : ",int(Tyre5No),tyre
                        Tyre5No = None
                else:
                    Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp = None

                
                if(hexstr[166:168] =="aa"):
                    
                    Tyre6No = hexstr[178:180]
                    
                    if(int(Tyre6No) == tyre):
                        
                        Tyre6ID = hexstr[180:186]
                        Tyre6Presure = hexstr[186:192]
                        Tyre6Temp = hexstr[192:194]
                        print Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
                    else:
                        #print "else : ",int(Tyre6No),tyre
                        Tyre6No = None
                else:
                    print Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
                    Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp = None
                    
                
        
            return (Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp, Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp)
            
        else:
            #my_logger.warning("Failed - Bluetooth ParseBluetoothTyre data Not Avalable: %s", data)
            print("Failed - Bluetooth ParseBluetoothTyre data Not Avalable:", data)
            return None

    except:
        e = sys.exc_info()[0]
        #my_logger.error(e)
        print ("Bluetooth Parse data Attribute Value not Avalable:",e)
        return None
'''
  
'''

def ParseBluetoothTyre(data):

    try:
        if(data != None):

            hexstr = binascii.b2a_hex(data)
            #hexstr = "aaa14108630006fdaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081aaa1410f63000656a7c500000000c6"
            

            Tyre1No = hexstr[28:30]
            Tyre1ID = hexstr[30:36]
            Tyre1Presure = hexstr[36:42]
            Tyre1Temp = hexstr[42:44]
            print Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp
            
            Tyre2No = hexstr[58:60]
            Tyre2ID = hexstr[60:66]
            Tyre2Presure = hexstr[66:72]
            Tyre2Temp = hexstr[72:74]
            print Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp

            Tyre3No = hexstr[88:90]
            Tyre3ID = hexstr[90:96]
            Tyre3Presure = hexstr[96:102]
            Tyre3Temp = hexstr[102:104]
            print Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp

            Tyre4No = hexstr[118:120]
            Tyre4ID = hexstr[120:126]
            Tyre4Presure = hexstr[126:132]
            Tyre4Temp = hexstr[132:134]
            print Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp

            Tyre5No = hexstr[148:150]
            Tyre5ID = hexstr[150:156]
            Tyre5Presure = hexstr[156:162]
            Tyre5Temp = hexstr[162:164]
            print Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp

            Tyre6No = hexstr[178:180]
            Tyre6ID = hexstr[180:186]
            Tyre6Presure = hexstr[186:192]
            Tyre6Temp = hexstr[192:194]
            print Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp
        
            return (Tyre1No, Tyre1ID, Tyre1Presure, Tyre1Temp,Tyre2No, Tyre2ID, Tyre2Presure, Tyre2Temp,Tyre3No, Tyre3ID, Tyre3Presure, Tyre3Temp,Tyre4No, Tyre4ID, Tyre4Presure, Tyre4Temp,Tyre5No, Tyre5ID, Tyre5Presure, Tyre5Temp,Tyre6No, Tyre6ID, Tyre6Presure, Tyre6Temp)

        else:
            my_logger.warning("Failed - Bluetooth ParseBluetoothTyre data Not Avalable: %s", data)
            print("Failed - Bluetooth ParseBluetoothTyre data Not Avalable:", data)
            return None

    except:
        e = sys.exc_info()[0]
        my_logger.error(e)
        print ("Bluetooth Parse data Attribute Value not Avalable:",e)
        return None
'''
def fun():

    data = "aaa14108630006fdaaa1410f630001ba6b09000000002daaa1410f630002ba6d6d0000000094aaa1410f63000356a8cb00000000caaaa1410f63000456a6be00000000bcaaa1410f63000556a7810000000081aaa1410f63000656a7c500000000c6"
    hexstr = binascii.b2a_hex(data)

    TPMSID1 = "aa41a1076300f6"
    
    BUID1 = '00:13:EF:C0:02:1E'
    #TpmsTireDataPosition()
    #s = connect_ble(BUID1)

    SID6, L6 = "56a7c5", "06"
    SID2, L2 = "ba6b75", "02"
    #Tpms_Tire_SET_Position1(L6, SID6)
    #Tpms_Tire_SET_Position1(L2, SID2)

    #Tpms_SET_TireID(conn, TMSSET)

    
    
    ParseBluetoothTyre(data)

    #Query_TpmsTireDataPosition(s, TPMSID1)

    

    
    

if __name__ == "__main__":  
    
    fun()
