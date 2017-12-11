#lets use httplib2

#import httplib2
import json
import requests
import pprint
import time


def postLiveData(data):

    #url = 'http://172.16.0.151:8080/TMS/api/tms/saveTPMSLatestData'
    url = 'https://qas.placer.in/TMS/api/tms/saveTPMSLatestData'

    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=data_json, headers=headers)
    pprint.pprint(response.json())

def prepareJsonString(vehId, mylist):

    tyres = []
    current_milli_time = lambda: int(round(time.time() * 1000))

    for i in range (2, len(mylist)):
        #print i, mylist[i][6]
        position = mylist[i][6]

        if (mylist[i][6] != '0') or (mylist[i][6] != '00'):

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


            sensorId = mylist[i][7] + mylist[i][8] + mylist[i][9]
            pressure = mylist[i][10] + mylist[i][11]
            temp = mylist[i][12]

            # We need tyreId also
	    # If possible get the tyreId from DB By querying sensorId
	    #Otherwise I'll do it from Backend
            tyres.append(prepareTyre(position, sensorId, i, pressure, temp))


    data = {
        "tyres": tyres,
        "device_date_time": current_milli_time(),
        "vehId": vehId
        }

    print data
    postLiveData(data)


def prepareTyre(position, sensorId, tyreId, pressure, temp):
    return {"sensorId": sensorId, "tyreId": tyreId,"position": position, "temp": temp, "pressure": pressure}



if __name__ == "__main__": 
    #main function
    print "Main"
    mylistVar = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                [0, 'a1', '41', '08', '63', '00', '05'], \
                [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '50', '78', '00'], \
                [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '25', '58', '00'], \
                [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '30', '70', '00'], \
                [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '45', '65', '00'], \
                [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '00', '00', '00', '00'], \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    prepareJsonString(2, mylistVar)



