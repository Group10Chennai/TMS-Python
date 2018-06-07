#lets use httplib2

#import httplib2
import json
import requests
import pprint
import time
import sys
import display

import glob
import logging
import logging.handlers


'''
LOG_FILENAME = '/home/pi/Documents/TMS-Git/log/loggingRotatingFileExample.log'

my_logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s :')
hdlr.setFormatter(formatter)
my_logger.addHandler(hdlr) 
my_logger.setLevel(logging.DEBUG)
'''

#my_logger.disabled = True

def postLiveData(data):

    try:
        
        #url = 'http://172.16.0.151:8080/TMS/api/tms/saveTPMSLatestData'
        #url = 'https://qas.placer.in/TMS/api/tms/saveTPMSLatestData'
        url = 'https://tpms-api.placer.in/TMS/api/tms/saveTPMSLatestData'

        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=data_json, headers=headers)
        #pprint.pprint(response.json())
        apiResp = response.json()

        if(apiResp.get('displayMsg') == "Success"):
            return "Success"
        else:
            return None
        
        #print data_json
        #return "Success"

    except:
        errObj = traceback.format_exc()
        #e = sys.exc_info()[0]
        #my_logger.error("Failed - postLiveData(data) None or Not Connected to URL: %s ",errObj)
        #print ("Failed - postLiveData(data) None or Not Connected to URL: ",errObj)

        return None

'''
def prepareJsonString(vehId, mylist):

    tyres = []
    current_milli_time = lambda: int(round(time.time() * 1000))
    for i in range (2, len(mylist)):

        print i, mylist[i][6]
        position = mylist[i][6]

        if (mylist[i][6] != 0) or (mylist[i][6] != 00):

            if mylist[i][6] == '01':
                position = "FL"
            if mylist[i][6] == '02':
                position = "FR"
            if mylist[i][6] == '03':
                position = "RLO"
            if mylist[i][6] == '04':
                position = "RLI"
            if mylist[i][6] == '05':
                position = "RRI"
            if mylist[i][6] == '06':
                position = "RRO"

            sensorUID = mylist[i][7] + mylist[i][8] + mylist[i][9]
            pressure = mylist[i][10] + mylist[i][11]
            temp = mylist[i][12]

            # We need tyreId also
            # If possible get the tyreId from DB By querying sensorId
            #Otherwise I'll do it from Backend
            tyres.append(prepareTyre(position, sensorUID, pressure, temp))

    data = {
        "tyres": tyres,
        "device_date_time": current_milli_time(),
        "vehId": vehId
        }

    print data
    postLiveData(data)

'''




def prepareJsonString(vehId, mylist):

    tyres = []

    pres_color = ""
    dispPsi = ""
    temp_color = ""
    disptemp = ""

    current_milli_time = lambda: int(round(time.time() * 1000))
    
    #print mylist
    try:
        
        for i in range (2, len(mylist)):

            #print i, mylist[i][6]
            
                            
            if mylist[i][6] == '01':
                position = "FL"

                sensorUID = (mylist[i][7] + mylist[i][8] + mylist[i][9])
                pressure = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])
                status = (mylist[i][13])
                
                pres_color, dispPsi = display.displayPresValidation(pressure)

                temp_color, disptemp = display.displayTempValidation(temp)
                
                if dispPsi == "---":
                    pressure = "0000"
                    dispPsi = str(pressure)
                if disptemp == "---":
                    temp = "00"
                    disptemp = str(temp)
                
                #print "URL Update", sensorUID, dispPsi, temp, status

                # We need tyreId also
                # If possible get the tyreId from DB By querying sensorId
                #Otherwise I'll do it from Backend

                tyres.append(prepareTyre(position, sensorUID, dispPsi, disptemp, status))
                
            if mylist[i][6] == '02':
                
                position = "FR"

                sensorUID = (mylist[i][7] + mylist[i][8] + mylist[i][9])
                pressure = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])
                status = (mylist[i][13])
                
                pres_color, dispPsi = display.displayPresValidation(pressure)

                temp_color, disptemp = display.displayTempValidation(temp)
                
                if dispPsi == "---":
                    pressure = "0000"
                    dispPsi = str(pressure)
                if disptemp == "---":
                    temp = "00"
                    disptemp = str(temp)
                
                #print "URL Update", sensorUID, dispPsi, temp, status

                # We need tyreId also
                # If possible get the tyreId from DB By querying sensorId
                #Otherwise I'll do it from Backend

                tyres.append(prepareTyre(position, sensorUID, dispPsi, disptemp, status))
                
            if mylist[i][6] == '03':
                position = "RLO"

                sensorUID = (mylist[i][7] + mylist[i][8] + mylist[i][9])
                pressure = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])
                status = (mylist[i][13])
                
                pres_color, dispPsi = display.displayPresValidation(pressure)

                temp_color, disptemp = display.displayTempValidation(temp)
                
                if dispPsi == "---":
                    pressure = "0000"
                    dispPsi = pressure
                if disptemp == "---":
                    temp = "00"
                    disptemp = temp
                
                #print "URL Update", sensorUID, dispPsi, temp, status

                # We need tyreId also
                # If possible get the tyreId from DB By querying sensorId
                #Otherwise I'll do it from Backend

                tyres.append(prepareTyre(position, sensorUID, dispPsi, disptemp, status))
                
            if mylist[i][6] == '04':
                position = "RLI"

                sensorUID = (mylist[i][7] + mylist[i][8] + mylist[i][9])
                pressure = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])
                status = (mylist[i][13])
                
                pres_color, dispPsi = display.displayPresValidation(pressure)

                temp_color, disptemp = display.displayTempValidation(temp)
                
                if dispPsi == "---":
                    pressure = "0000"
                    dispPsi = pressure
                if disptemp == "---":
                    temp = "00"
                    disptemp = temp

                #print "URL Update", sensorUID, dispPsi, temp, status

                # We need tyreId also
                # If possible get the tyreId from DB By querying sensorId
                #Otherwise I'll do it from Backend

                tyres.append(prepareTyre(position, sensorUID, dispPsi, disptemp, status))

                
            if mylist[i][6] == '05':
                position = "RRI"

                sensorUID = (mylist[i][7] + mylist[i][8] + mylist[i][9])
                pressure = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])
                status = (mylist[i][13])
                
                pres_color, dispPsi = display.displayPresValidation(pressure)

                temp_color, disptemp = display.displayTempValidation(temp)
                
                if dispPsi == "---":
                    pressure = "0000"
                    dispPsi = pressure
                if disptemp == "---":
                    temp = "00"
                    disptemp = temp

                #print "URL Update", sensorUID, dispPsi, temp, status

                # We need tyreId also
                # If possible get the tyreId from DB By querying sensorId
                #Otherwise I'll do it from Backend

                tyres.append(prepareTyre(position, sensorUID, dispPsi, disptemp, status))

                
            if mylist[i][6] == '06':
                position = "RRO"

                sensorUID = (mylist[i][7] + mylist[i][8] + mylist[i][9])
                pressure = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])
                status = (mylist[i][13])
                
                pres_color, dispPsi = display.displayPresValidation(pressure)

                temp_color, disptemp = display.displayTempValidation(temp)

                if dispPsi == "---":
                    pressure = "0000"
                    dispPsi = pressure
                if disptemp == "---":
                    temp = "00"
                    disptemp = temp

                #print "URL Update", sensorUID, dispPsi, temp, status

                # We need tyreId also
                # If possible get the tyreId from DB By querying sensorId
                #Otherwise I'll do it from Backend

                tyres.append(prepareTyre(position, sensorUID, dispPsi, disptemp, status))

            '''   
            sensorUID = mylist[i][7] + mylist[i][8] + mylist[i][9]
            pressure = mylist[i][10] + mylist[i][11]
            temp = mylist[i][12]
            status = mylist[i][13]
            
            pres_color, dispPsi = display.displayPresValidation(pressure)

            temp_color, disptemp = display.displayTempValidation(temp)

            print "URL Update", sensorUID, dispPsi, temp, status

            # We need tyreId also
            # If possible get the tyreId from DB By querying sensorId
            #Otherwise I'll do it from Backend

            tyres.append(prepareTyre(position, sensorUID, pressure, temp, status))
            '''

        data =  {
                "tyres": tyres,
                "device_date_time": current_milli_time(),
                "vehId": vehId
                }

        #print data
        PostRet = postLiveData(data)

        if PostRet == "Success":

            return "Success"

        else:
            return None

    except:
        e = sys.exc_info()[0]
        #my_logger.error("Failed - prepareJsonString(vehId, mylist) None:%s, %s ",e, "Failed")
       #print ("Failed - prepareJsonString(vehId, mylist) None: ",e, "Failed")

        return None
        
def prepareTyre(position, sensorUID, pressure, temp, status):
    
    return {"sensorUID": sensorUID, "position": position, "pressure": pressure, "temp": temp, "status": status }


#main function
if __name__ == "__main__":
    mylistVar = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 'a1', '41', '08', '63', '00', '05'], \
                  [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '50', '78', '00'], \
                  [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '25', '58', '00'], \
                  [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '30', '70', '00'], \
                  [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '45', '65', '00'], \
                  [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '00', '00', '00', '00'], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    prepareJsonString(2, mylistVar)



