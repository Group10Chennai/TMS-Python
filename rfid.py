###############################################################
# TMS RFID Serial Integration -09-2017
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

import glob
import logging
import logging.handlers


#Serial Enable
serial = serial.Serial("/dev/ttyS0", baudrate = 9600, timeout = 0.2)



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

TID1 = "e2000016351702081640767f"


#RFID Query Tag
def RFIDUHFQueryTag():

    try:

        QueryTag = "040001DB4B"

        my_hex = QueryTag.decode('hex')
        #print my_hex        
        print binascii.b2a_hex(my_hex)

#        while True:
        serial.write(my_hex)
        #serial.write("Hello World")

        #print " ".join(hex(ord(n)) for n in my_hex)


    
        data = serial.readline()
        #print data
    
        if(data[3] == '\x01'):
       
        
            #rfid = binascii.b2a_hex(data)
            rfidTID_hex = binascii.b2a_hex(data)
            #print rfidTID_hex
            rfidTID = rfidTID_hex [12:36]
            #RFID TAG ID Data
            print rfidTID

            if rfidTID == TID1:
                print "Hello"

            return rfidTID
           

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - RFID Query Tag %s, %s:",e, QueryTag)
        print ("Failed - RFID Query Tag :",e, QueryTag)
        return None

if __name__ == "__main__":  
    
    RFIDUHFQueryTag()
