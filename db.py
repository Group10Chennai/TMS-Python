###############################################################
# TMS Database Connection File
###############################################################

import sqlite3
from sqlite3 import Error
import __main__
from pip._vendor.pkg_resources import null_ns_handler
 
import glob
import logging
import logging.handlers


LOG_FILENAME = '/home/pi/Documents/TMS-Git/TMS-Python/log/loggingRotatingFileExample.log'
'''
# Set up a specific logger with our desired output level
#LOG_FILENAME = 'example.log'
my_logger= logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
#my_logger = logging.getLogger('MyLogger')
#my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=1)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

my_logger.setFormatter(formatter)

my_logger.addHandler(handler)



my_logger = logging.basicConfig(format='%(asctime)s :%(levelname)s: %(message)s',filename=LOG_FILENAME,level=logging.DEBUG)
my_logger = logging.getLogger('MyLogger')
'''


my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)


#def create database connection
def create_db_connection(db_file):
    """Create a database connection to the DB file .db"""
    
    try:
        conn = sqlite3.connect(db_file)
        my_logger.info(" Create a connection to DB ")
        return conn
    except sqlite3.Error as e:
        print ("Failed - Create a connection to DB to the path: ", db_file)
        my_logger.error("Failed - Create a connection to DB to the path: %s", db_file)
        #raise
        return None


    

#Query DB Select Deveice detail by rfiduid
def select_DeviceDetails_by_rfiduid(conn, rfiduid1):
    """
    Query tasks by rfiduid
    param conn: the Connection object
    param rfiduid:
    """
    
    if(rfiduid1 != None):
    #print (" DB select_DeviceDetails_by_id")
    #my_logger.info(" DB select_DeviceDetails_by_id")
        try:
            cur = conn.cursor()
            cur.execute("SELECT vehId, vehName, BUID, RFUID FROM DeviceDetails WHERE RFUID=?",(rfiduid1,))
 
            rows = cur.fetchall()
            vehDetails = None;
            for row in rows:
                if(row != None):
                    vehDetails = row
                    print vehDetails
            if (vehDetails != None):
                
                return vehDetails
            else:
                print ("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available: ",rfiduid1)
                my_logger.warning("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available: %d",(rfiduid1))
                
                return None
    
        except sqlite3.Error as e:
            print ("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available: ",rfiduid1)
            my_logger.error("Failed - Accessing to DB table DeviceDetails by RFID UID - Not Available:  %d, %d ",e, rfiduid1)
            #raise
            return None
    else:
        print ("FFailed - Accessing to DB table DeviceDetails by RFID UID - None: ",rfiduid1)
        my_logger.warning("Failed - Accessing to DB table DeviceDetails by RFID UID - None: %s",(rfiduid1))
                
        return None
    

def select_TyreDetails_by_VehId(conn, VehId1):
    """
    Query tasks by priority
    param conn: the Connection object
    param rfiduid:
    """
    if(VehId1 != None):
        
        TyreDetials = []
        #my_logger.info (" DB select_TireDetails_by_VehId ")
        try:
            cur = conn.cursor()
            cur.execute("SELECT sensorUID, tirePosition FROM TireDetails WHERE vehId=?",(VehId1,))
            
            rows = cur.fetchall()
            TyreDetails = None;
            for row in rows:
                TyreDetails = row
                print TyreDetails
        
            #return TyreDetials
            #return rows

            if (len(rows) != 0):
                print len(rows)
                print rows
                return rows
            else:
                print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: ",VehId1)
                my_logger.warning("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: %d",(VehId1))
                
                return None
    
        except sqlite3.Error as e:
            print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - Not Available: ",VehId1)
            my_logger.error("Failed - sqlite3.Error and Accessing to DB table TyreDetails by Vehicle ID - Not Available: %d, %d ",e, VehId1)
            #raise
            return None
    else:
        print ("Failed - Accessing to DB table TyreDetails by Vehicle ID - None: ",VehId1)
        my_logger.warning("Failed - Accessing to DB table TyreDetails by Vehicle ID - None %s",(VehId1))
                
        return None


def main():
    
    database = "/opt/Aquire/sqlite/Sample.db"
    print (" DB Create a connection ")
    
    #create a connection to database
    conn = create_db_connection(database)

    #tag = "e2000016351702081640767faa"
    tag = None
    vehID = 10
    with conn:
        select_DeviceDetails_by_rfiduid(conn, tag)
        select_TyreDetails_by_VehId(conn, vehID)
        #conn.close()

if __name__ == '__main__':
    main()
