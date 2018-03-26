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

import struct
import utlities

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

my_logger.disabled = True

def udpSocket(message):

    import socket

    UDP_IP = "192.168.1.15"
    UDP_PORT = 19000
    MESSAGE = message
   
    #print "UDP target IP:", UDP_IP
    #print "UDP target port:", UDP_PORT
    #print "message:", MESSAGE
   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()



'''
def udpSocketCreate(host, port, message):

    #UDP_IP = "127.0.0.1"
    #UDP_PORT = 5005
    #MESSAGE = "Hello, World!"

    print "UDP target IP:", host
    print "UDP target port:", port
    print "message:", message

    #sock = socket.socket(socket.AF_INET, # Internet
                         #socket.SOCK_DGRAM) # UDP
    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    #create an INET, STREAMing socket
    try:
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        #sys.exit()

    print 'Socket Created'

    try:
        remote_ip = socket.gethostbyname( host )
        s.connect((host, port))

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    print 'Socket Connected to ' + host + ' on ip ' + remote_ip 

    #Send some data to remote server
    #message = "Test"

    try :
        #Set the whole string
        while True:
            #s.send(message)
            s.sendto(message, (host, port))
            print 'Message sent successfully'
            time.sleep(1)
            print 'Sending...'
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()





def tcpSocketCreate(host, port, message):

    #create an INET, STREAMing socket
    try:
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        #sys.exit()

    print 'Socket Created'

    try:
        remote_ip = socket.gethostbyname( host )
        s.connect((host, port))

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    print 'Socket Connected to ' + host + ' on ip ' + remote_ip 

    #Send some data to remote server
    #message = "Test"

    try :
        #Set the whole string
        while True:
            #s.send(message)
            s.sendto(message, (host, port))
            print 'Message sent successfully'
            time.sleep(1)
            print 'Sending...'
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()


    

def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return ''.join(total_data)

#get reply and print
print recv_timeout(s)

s.close()
'''

presint_Bar = 0
presint_Psi = 0
dispPsi = ""

pres = ""
temp = ""

tempint_Celcious = 0
disptemp = ""


Red = "1"
Green = "2"
Yellow ="3"
Blue = "4"
White = "7"
pres_color = ""
temp_color = ""

nC = ""

dispVar = ""
dispVar1 = ""
dispVar2 = ""
dispVar3 = ""
dispVar4 = ""
dispVar5 = ""
dispVar6 = ""


def displayPresValidation(pres):

    try:

        #Check for the Valid Pres is not 0000
        if pres.strip() != "0000"  :
                        
            
            presint_Psi = utlities.pressureToBarPsiConvertion(pres)
            dispPsi = str(presint_Psi).zfill(3)


                               
            if presint_Psi >= 0 and presint_Psi <= 200:       
                #Staturated PSI value between 121 to 125 Should be Green Color
                if (presint_Psi) <= 135 and presint_Psi >= 120:

                    pres_color = Green
                    #print pres_color
                            
                
                #Staturated PSI value between 114 to below Should be Red Color
                elif presint_Psi < 120 or presint_Psi > 135:
                    pres_color = Red

            else:
                pres_color = Blue
                dispPsi = "---"
                #print "else",pres_color, dispPsi 
                return  pres_color, dispPsi

                                    
        #Check for the Valid Pres is 0000
        else:
            pres_color = Blue
            dispPsi = "---"
        #print "else",pres_color, dispPsi 
        return  pres_color, dispPsi

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Pressure Calculation:%s ",e)
        print ("Failed - Pressure Calculation: ",e)

        return None, None

def displayTempValidation(temp):

    try:
        #Check for the Valid Temp is not 00
        if  temp.strip() != "00" :

            tempint_Celcious  = utlities.temperatureToCelciousConvertion(temp)
            disptemp = str(int(tempint_Celcious)).zfill(3)

            if tempint_Celcious <= 120:     
                #Staturated Temperature Celcious value between 50 to 45 Should be Yellow Color
                if tempint_Celcious <= 40 and tempint_Celcious >= 10:
                    temp_color = Green

                #Staturated Temperature Celcious value is above 50 Should be Red Color   
                elif tempint_Celcious > 40:
                    temp_color = Red
            else:
                temp_color = Blue
                disptemp = "---"
                return  temp_color, disptemp
               
        #Check for the Valid temp is 00
        else:
            temp_color = Blue
            disptemp = "---"

        return  temp_color, disptemp

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Temperature Calculation:%s ",e)
        print ("Failed - Temperature Calculation: ",e)
        return None, None




def displayLEDBoard(vehName, dispCmd, date_time, dispVar):

    nC = White

    startChar = "["
    endChar   = "]"

    display =   "<\\C"+nC+ "----" + ">" + "<\\C"+ nC +"----------" + ">" + \
                "<\\C"+nC+" "+" ---"  +"\\C"+nC+" "+" ---" +"\\C"+nC+" "+" ---" +"\\C"+nC+" "+" ---" +">" +   \
                "<\\C"+nC+" "+" ---"  +"\\C"+nC+" "+" ---" +"\\C"+nC+" "+" ---" +"\\C"+nC+" "+" ---" +">" +   \
                "<\\C"+nC+" "+" ---"  +"\\C"+nC+" "+" ---" +"\\C"+nC+" "+" ---" +"\\C"+nC+" "+" ---" +">" 

    vehName1  = "<\\C"+nC+ "----" + ">"

    dispCmd1  = "<\\C"+ nC +"----------" + ">"
    
    #dispVar1  = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
    #            "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
    #            "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"

    dispCmd = ""

    date_time = ""
    
    try:
        
        if (vehName != None) & (dispVar != None):

            vehN = vehName [4:8] #SND 9457
            #print vehN

            vehNc = "<\\C"+nC+ vehN + ">"
            #print vehNc

            dispc = dispCmd + " " + str(date_time)
            
            dispCmd1  = "<\\C"+ nC + dispc + " " + ">"
         
            #print dispCmd1

        display = startChar + vehNc + dispCmd1 + dispVar + endChar
        #display = startChar + vehNc + dispVar + endChar

        #print display

        udpSocket(display)


    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - displayLEDBoard:%s ",e)
        print ("Failed - displayLEDBoard: ",e)


def displayLEDBoard_Null():
    try:
        dispCmd = ""

        vehName = "--------"

        date_time = ""
        
    
        mylist = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, '00', '00', '00', '00', '00', '00'], \
                  [0, '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00'], \
                  [0, '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00'], \
                  [0, '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00'], \
                  [0, '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00'], \
                  [0, '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00'], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

       
        dispVar = displayLEDBoardParameters(mylist)
    #print dispVar

    #dispVar = "<\\c2 122\\c1 70\\c1 106\\c2 38><\\c1 110\\c1 62\\c3 118\\c1 51><\\c4 ---\\c4 ---\\c7 ---\\c7 --->"
    
  

        displayLEDBoard(vehName, dispCmd, date_time, dispVar)

		
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - displayLEDBoard_Null:%s ",e)
        print ("Failed - displayLEDBoard_Null: ",e)

'''
def displayLEDBoardParameters(mylist):

    

    nC = White

    dispVar =   "<\\C"+nC+" "+"---"  +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +">" +   \
                "<\\C"+nC+" "+"---"  +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +">" +   \
                "<\\C"+nC+" "+"---"  +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +">" 


    dispVar1 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar2 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar3 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar4 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar5 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar6 = nC + " " + "---" + "\\C" + nC + " " + "---"

    try:

        if mylist !=  None:

            #print mylist
            #print len(mylist)
                    
            
            for i in range (2, len(mylist)):
                print i, mylist[i][6]
                
                if mylist[i][6] == '01' :

                    print "SensorID1 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]

                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    dispVar1 = pres_color +" "+ dispPsi + " " + "\\C" + temp_color + disptemp + " "

                    ''
                    dispVar = "<\c"+pres_color+" "+dispPsi+" \c"+temp_color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #if dispVar == "":
                        #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_color+" "+disptemp
                    #else:
                        #dispVar = dispVar + "/c3 "+mylist[i][10]+mylist[i][11]+ "/c4 "+mylist[i][12]+">"
                    ''

                elif mylist[i][6] == '02' :

                    print "SensorID2 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar2 = pres_color + dispPsi + " " + "\\C" + temp_color + disptemp 

                    ''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---" +"\c"+nC+" "+"---"+"\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    ''
                    
                elif mylist[i][6] == '03' :

                    print "SensorID3 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]


                    dispVar3 =  pres_color + " " + dispPsi + " " + "\\C" + temp_color + disptemp + " "
                    
                    ''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---" +"\c"+nC+" "+"---"+"\c"+nC+" "+nC+"\c"+nC+" "+nC+">"+"<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    else:
                        dispVar = dispVar +"<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    ''


                elif mylist[i][6] == '04' :

                    print "SensorID4 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar4 = pres_color + dispPsi + " " + "\\C" + temp_color + disptemp 

                    ''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +       \
                                  "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    ''


                elif mylist[i][6] == '05' :

                    print "SensorID5 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar5 = pres_color + " " + dispPsi + " " + "\\C" + temp_color + disptemp 

                    ''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                                  "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"  +  \
                                  "<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

                    ''

                    
                elif mylist[i][6] == '06' :

                    print "SensorID6 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color, dispPsi = displayPresValidation(pres)
                    #print pres_color, dispPsi 
                    
                    temp_color, disptemp = displayTempValidation(temp)
                    #print temp_color, disptemp
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    dispVar6 = pres_color + dispPsi + " " + "\\C" + temp_color + disptemp 

                    ''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                              "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"  +  \
                              "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp +"\c"+pres_color+" "+dispPsi +"\c"+temp_color+" "+disptemp +">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"+"]"

                    ''
      
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" + "]"

                        #pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

                        #" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

            #dispVar1 = pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
            #dispVar2 = pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

            print dispVar1
            print dispVar2
            print dispVar3
            print dispVar4
            print dispVar5
            print dispVar6
                
            dispVar =   "<\\C" + dispVar1 + "\\C" + dispVar2 + ">"           \
                        "<\\C" + dispVar3 + "\\C" + dispVar4 + ">"           \
                        "<\\C" + dispVar5 + "\\C" + dispVar6 + ">"           
                        
            
            print dispVar

            return dispVar
        
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Temperature Calculation:%s ",e)
        print ("Failed - Temperature Calculation: ",e)

'''

def displayLEDBoardParameters(mylist):

    

    nC = White

    dispVar =   "<\\C"+nC+" "+"---"  +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +">" +   \
                "<\\C"+nC+" "+"---"  +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +">" +   \
                "<\\C"+nC+" "+"---"  +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +"\\C"+nC+" "+"---" +">" 


    dispVar1 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar2 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar3 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar4 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar5 = nC + " " + "---" + "\\C" + nC + " " + "---"
    dispVar6 = nC + " " + "---" + "\\C" + nC + " " + "---"


    pres_color1 = White
    dispPsi1    = "---"
    temp_color1 = White
    disptemp1   = "---"

    pres_color2 = White
    dispPsi2    = "---"
    temp_color2 = White
    disptemp2   = "---"

    pres_color3 = White
    dispPsi3    = "---"
    temp_color3 = White
    disptemp3   = "---"

    pres_color4 = White
    dispPsi4    = "---"
    temp_color4 = White
    disptemp4   = "---"

    pres_color5 = White
    dispPsi5    = "---"
    temp_color5 = White
    disptemp5   = "---"

    pres_color6 = White
    dispPsi6    = "---"
    temp_color6 = White
    disptemp6   = "---"

    try:

        if mylist !=  None:

            #print mylist
            #print len(mylist)
                    
            
            for i in range (2, len(mylist)):
                #print i, mylist[i][6]
                
                if mylist[i][6] == '01' :

                    #print "SensorID1 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]

                    pres_color1, dispPsi1 = displayPresValidation(pres)
                    #print pres_color1, dispPsi1 
                    
                    temp_color1, disptemp1 = displayTempValidation(temp)
                    #print temp_color1, disptemp1
                        
                    #dispVar1 = pres_color +" "+ dispPsi + " " + "\\C" + temp_color + disptemp + " "

                    '''
                    dispVar = "<\c"+pres_color+" "+dispPsi+" \c"+temp_color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #if dispVar == "":
                        #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_color+" "+disptemp
                    #else:
                        #dispVar = dispVar + "/c3 "+mylist[i][10]+mylist[i][11]+ "/c4 "+mylist[i][12]+">"
                    '''

                elif mylist[i][6] == '02' :

                    #print "SensorID2 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color2, dispPsi2 = displayPresValidation(pres)
                    #print pres_color2, dispPsi2
                    
                    temp_color2, disptemp2 = displayTempValidation(temp)
                    #print temp_color2, disptemp2
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #dispVar2 = pres_color + dispPsi + " " + "\\C" + temp_color + disptemp 

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---" +"\c"+nC+" "+"---"+"\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    '''
                    
                elif mylist[i][6] == '03' :

                    #print "SensorID3 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color3, dispPsi3 = displayPresValidation(pres)
                    #print pres_color1, dispPsi1 
                    
                    temp_color3, disptemp3 = displayTempValidation(temp)
                    #print temp_color1, disptemp1
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]


                    #dispVar3 =  pres_color + " " + dispPsi + " " + "\\C" + temp_color + disptemp + " "
                    
                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---" +"\c"+nC+" "+"---"+"\c"+nC+" "+nC+"\c"+nC+" "+nC+">"+"<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    else:
                        dispVar = dispVar +"<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    '''


                elif mylist[i][6] == '04' :

                    #print "SensorID4 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color4, dispPsi4 = displayPresValidation(pres)
                    #print pres_color1, dispPsi1 
                    
                    temp_color4, disptemp4 = displayTempValidation(temp)
                    #print temp_color1, disptemp1
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #dispVar4 = pres_color + dispPsi + " " + "\\C" + temp_color + disptemp 

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +       \
                                  "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"
                    '''


                elif mylist[i][6] == '05' :

                    #print "SensorID5 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color5, dispPsi5 = displayPresValidation(pres)
                    #print pres_color5, dispPsi5
                    
                    temp_color5, disptemp5 = displayTempValidation(temp)
                    #print temp_color5, disptemp5
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #dispVar5 = pres_color + " " + dispPsi + " " + "\\C" + temp_color + disptemp 

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                                  "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"  +  \
                                  "<\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

                    '''

                    
                elif mylist[i][6] == '06' :

                    #print "SensorID6 ",mylist[i][7]+mylist[i][8]+mylist[i][9]
                    pres = mylist[i][10]+mylist[i][11]
                    temp = mylist[i][12]
                    
                    pres_color6, dispPsi6 = displayPresValidation(pres)
                    #print pres_color6, dispPsi6 
                    
                    temp_color6, disptemp6 = displayTempValidation(temp)
                    #print temp_color6, disptemp6
                        
                    
                    #dispVar = "</c"+pres_color+" "+dispPsi+" /c"+temp_Color+" "+disptemp
                    #dispVar = "</c1 "+mylist[i][10]+mylist[i][11]+" /c2 "+mylist[i][12]
                    #dispVar = "</c1 "+k+" /c2 "+mylist[i][12]

                    #dispVar6 = pres_color + dispPsi + " " + "\\C" + temp_color + disptemp 

                    '''
                    if dispVar == "":
                        nC = White
                        dispVar = "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                              "<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">"  +  \
                              "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp +"\c"+pres_color+" "+dispPsi +"\c"+temp_color+" "+disptemp +">"
                    else:
                        dispVar = dispVar +" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp+">"+"]"

                    '''
      
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" +   \
                        #"<\c"+nC+" "+"---"  +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +"\c"+nC+" "+"---" +">" + "]"

                        #pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

                        #" "+ "\c"+pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp

            #dispVar1 = pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp
            #dispVar2 = pres_color+" "+dispPsi+"\c"+temp_color+" "+disptemp


            #pres_color1, dispPsi1 = displayPresValidation(pres)
            #print pres_color1, dispPsi1 
                    
            #temp_color1, disptemp1 = displayTempValidation(temp)
            #print temp_color1, disptemp1

            dispVar1 = pres_color1 + " " + dispPsi1 + " " + "\\C" + pres_color2 + dispPsi2 + " "
            dispVar2 = temp_color1 + disptemp1 + " " + "\\C" + temp_color2 + disptemp2
            dispVar3 = pres_color3 + " " + dispPsi3 + " " + "\\C" + pres_color4 + dispPsi4 + " "
            dispVar4 = temp_color3 + disptemp3 + " " + "\\C" + temp_color4 + disptemp4
            dispVar5 = pres_color5 + " " + dispPsi5 + " " + "\\C" + pres_color6 + dispPsi6 + " "
            dispVar6 = temp_color5 + disptemp5 + " " + "\\C" + temp_color6 + disptemp6 

            #print dispVar1
            #print dispVar2
            #print dispVar3
            #print dispVar4
            #print dispVar5
            #print dispVar6
                
            dispVar =   "<\\C" + dispVar1 + "\\C" + dispVar2 + ">"           \
                        "<\\C" + dispVar3 + "\\C" + dispVar4 + ">"           \
                        "<\\C" + dispVar5 + "\\C" + dispVar6 + ">"           
                        
            
            #print dispVar

            return dispVar

        else:
            print ("Failed - LED Display parameters is None:",mylist)
            my_logger.warning("Failed - LED Display parameters is None: %s",mylist)
            return None
        
    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - LED Display parameters is None:%s %s ",e, mylist)
        print ("Failed - LED Display parameters is None: ",e, mylist)



#main function
if __name__ == "__main__":

    #if(len(sys.argv) < 2) :
        #print 'Usage : python client.py hostname'
        #sys.exit()

    host = "192.168.1.15"
    port = 19000

    message = "Test"
    message1 = "[<\\C70000><\\C21234567fghfhfghfghfghgfhgfh890A ><\\C1 123 \\C2456 \\C3789 \\C4456><\\C1 123 \\C2456 \\C3789 \\C4456><\\C1 123 \\C2456 \\C3789 \\C4456>]"
    #message1 = "[<\\C70000><\\C21234567fghfhfghfghfghgfhgfh890A ><\\C1 123 \\C2 456 \\C3 789 \\C4 456><\\C1 123 \\C2456 \\C3 789 \\C4 456><\\C1 123 \\C2 456 \\C3 789 \\C4 456>]"
    #hex_data = binascii.b2a_hex(message1)

    #print hex_data
    #tcpSocketCreate(host, port, message1)
    #udpSocketCreate(host, port, hex_data)

    #udpSocket(message1)
    #udpSocketReceive()

    dispCmd = "SND"

    vehName = "SND 9406"

    date_time = time.strftime('%H:%M %d/%m/%Y')
    print date_time
    
    mylist = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
              [0, 'a1', '41', '08', '63', '00', '05'], \
              [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '56', '50', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '51', '50', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '40', '50', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '45', '50', '00'], \
              [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '00', '00', '00', '00'], \
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    dispVar = displayLEDBoardParameters(mylist)
    print dispVar

    #dispVar = "<\\c2 122\\c1 70\\c1 106\\c2 38><\\c1 110\\c1 62\\c3 118\\c1 51><\\c4 ---\\c4 ---\\c7 ---\\c7 --->"
    
   
    #while(True):
     #   time.sleep(1)
    #displayLEDBoard(vehName, dispCmd, date_time, dispVar)
    displayLEDBoard_Null()
    
