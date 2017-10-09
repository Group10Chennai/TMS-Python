###############################################################
# TMS Database Connection File
###############################################################

import sqlite3
from sqlite3 import Error
import __main__
from pip._vendor.pkg_resources import null_ns_handler

#def create database connection
def create_db_connection(db_file):
    """Create a database connection to the DB file .db"""
    try:
        conn = sqlite3.connect(db_file)
        print (" Create a connection to DB ")
        return conn
    except Error as e:
        print (e)
        
    return None


    

#Query DB Select Deveice detail by rfiduid
def select_DeviceDetails_by_rfiduid(conn, rfiduid1):
    """
    Query tasks by rfiduid
    param conn: the Connection object
    param rfiduid:
    """
    print (" DB select_DeviceDetails_by_id")
    cur = conn.cursor()
    cur.execute("SELECT vehId, vehName, BUID, RFUID FROM DeviceDetails WHERE RFUID=?",(rfiduid1,))
 
    rows = cur.fetchall()
    vehDetails = None;
    for row in rows:
        vehDetails = row
        #print vehDetails
          
    return vehDetails

def select_TyreDetails_by_VehId(conn, VehId1):
    """
    Query tasks by priority
    param conn: the Connection object
    param rfiduid:
    """
    TyreDetials = []
    print (" DB select_TireDetails_by_VehId ")
    cur = conn.cursor()
    cur.execute("SELECT sensorUID, tirePosition FROM TireDetails WHERE vehId=?",(VehId1,))
 
    rows = cur.fetchall()
    TyreDetails = None;
    for row in rows:
        TyreDetails = row
        #print TyreDetails
        
    #return TyreDetials
    return rows


def main():
    
    database = "/opt/Aquire/sqlite/Sample.db"
    print (" DB Create a connection ")
    
    #create a connection to database
    conn = create_db_connection(database)

    tag = "RFUID 1"
    vehID = 24
    with conn:
        #select_DeviceDetails_by_rfiduid(conn, tag)
        select_TyreDetails_by_VehId(conn, vehID)

if __name__ == '__main__':
    main()
