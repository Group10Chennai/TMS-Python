# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form - Copy - Copy.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

import gui1
import utlities
import display
import work
import time
import string


loopStatus = ""
sec = 2
loopStatus = False
RFID_UID = ""

Red = "1"
Green = "2"
Yellow ="3"
Blue = "4"
White = "7"


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 600, 750)
        self.setFixedSize(600, 750)
        self.startUIWindow()

        self.movie = QMovie("/home/pi/Documents/TZcL7Cc.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("My Program")
        self.show()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)



class Ui_Form(object):

    
    pres_color = ""
    dispPsi = ""
    temp_color = ""
    disptemp = ""

    pres_color1 = ""
    temp_color1 = ""
    
    numberString = ""
    t = ""

    GREEN_CLR_TAG = "color: rgb(0, 100, 0);\n"
    BLUE_CLR_TAG = "color: rgb(85, 0, 127);\n"
    RED_CLR_TAG = "color: rgb(255, 59, 20);\n"
    YELLOW_CLR_TAG = "color: rgb(255, 255, 0);\n"
    BROWN_CLR_TAG = "color: rgb(255, 170, 0);\n" # White in LED Display

    #pres_color1 = BROWN_CLR_TAG
    dispPsi    = "---"
    #temp_color1 = BROWN_CLR_TAG
    disptemp   = "---"

    def displayColorSet(self, pres_color):

        if str(pres_color) == '1':
            pres_color1 = self.RED_CLR_TAG
        if str(pres_color) == '2': 
            pres_color1 = self.GREEN_CLR_TAG
        if str(pres_color) == '3':
            pres_color1 = self.YELLOW_CLR_TAG
        if str(pres_color) == '4':
            pres_color1 = self.BLUE_CLR_TAG
        if str(pres_color) == '7':
            pres_color1 = self.BROWN_CLR_TAG
            

        return pres_color1


    
        
    def displayTPData(self, vehName, mylist):

        print "display method ", mylist
        #_translate = QtCore.QCoreApplication.translate

        for i in range (2, len(mylist)):
            print i, mylist[i][6]
            #if (mylist[i][6] != 0) | (mylist[i][6] != 00):

            #pressure = str(utlities.pressureToBarPsiConvertion(str(mylist[i][10] + mylist[i][11])))
            #temp = str(utlities.temperatureToCelciousConvertion(mylist[i][12]))

            #print "Before",pres_color, dispPsi, "color: rgb(255, 170, 0);\n" 
  
            #print "Mid",pres_color, dispPsi, self.pres_color1
            #print "After",pres_color, dispPsi, pres_color1

            
                
            if mylist[i][6] == '01':

                pres = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])

                pres_color, dispPsi = display.displayPresValidation(pres)
                pres_color1 = self.displayColorSet(pres_color)
                print "01 - Pressure", pres_color, dispPsi, pres_color1
                
                temp_color, disptemp = display.displayTempValidation(temp)    
                temp_color1 = self.displayColorSet(temp_color)
                print "01 - Temp", temp_color, disptemp, temp_color1
                
                #position = "FL"
                self.lineEdit_Value_Press_FL.setText((dispPsi))
                self.lineEdit_Value_Press_FL.setStyleSheet(pres_color1)

                self.lineEdit_Value_Temp_FL.setText((disptemp))
                self.lineEdit_Value_Temp_FL.setStyleSheet(temp_color1)

            if mylist[i][6] == '02':

                pres = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])

                pres_color, dispPsi = display.displayPresValidation(pres)                
                pres_color1 = self.displayColorSet(pres_color)
                print "02 - Pressure", pres_color, dispPsi, pres_color1
                
                temp_color, disptemp = display.displayTempValidation(temp)    
                temp_color1 = self.displayColorSet(temp_color)
                print "02 - Temp", temp_color, disptemp, temp_color1
                
                #position = "FR"
                self.lineEdit_Value_Press_FR.setText((dispPsi))
                self.lineEdit_Value_Press_FR.setStyleSheet(pres_color1)

                self.lineEdit_value_Temp_FR.setText((disptemp))
                self.lineEdit_value_Temp_FR.setStyleSheet(temp_color1)

            if mylist[i][6] == '03':

                pres = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])

                pres_color, dispPsi = display.displayPresValidation(pres)
                pres_color1 = self.displayColorSet(pres_color)
                print "03 - Pressure", pres_color, dispPsi, pres_color1                
                
                temp_color, disptemp = display.displayTempValidation(temp)    
                temp_color1 = self.displayColorSet(temp_color)
                print "03 - Temp", temp_color, disptemp, temp_color1
                
                #position = "RLO"
                self.lineEdit_Value_Press_RLO.setText((dispPsi))
                self.lineEdit_Value_Press_RLO.setStyleSheet(pres_color1)

                self.lineEdit_Value_Temp_RLO.setText((disptemp))
                self.lineEdit_Value_Temp_RLO.setStyleSheet(temp_color1)

            if mylist[i][6] == '04':

                pres = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])

                pres_color, dispPsi = display.displayPresValidation(pres)
                pres_color1 = self.displayColorSet(pres_color)
                print "04 - Pressure", pres_color, dispPsi, pres_color1
                
                temp_color, disptemp = display.displayTempValidation(temp)    
                temp_color1 = self.displayColorSet(temp_color)
                print "04 - Temp", temp_color, disptemp, temp_color1
                
                #position = "RLI"
                self.lineEdit_Value_Press_RLI.setText((dispPsi))
                self.lineEdit_Value_Press_RLI.setStyleSheet(pres_color1)

                self.lineEdit_Value_Temp_RLI.setText((disptemp))
                self.lineEdit_Value_Temp_RLI.setStyleSheet(temp_color1)

            if mylist[i][6] == '05':

                pres = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])

                pres_color, dispPsi = display.displayPresValidation(pres)
                pres_color1 = self.displayColorSet(pres_color)
                print "05 - Pressure", pres_color, dispPsi, pres_color1
                
                temp_color, disptemp = display.displayTempValidation(temp)    
                temp_color1 = self.displayColorSet(temp_color)
                print "05 - Temp", temp_color, disptemp, temp_color1
                
                #position = "RRI"
                self.lineEdit_Value_Press_RRI.setText((dispPsi))
                self.lineEdit_Value_Press_RRI.setStyleSheet(pres_color1)

                self.lineEdit_Value_Temp_RRI.setText((disptemp))
                self.lineEdit_Value_Temp_RRI.setStyleSheet(temp_color1)

            if mylist[i][6] == '06':

                #print "RRO"
                pres = (mylist[i][10] + mylist[i][11])
                temp = (mylist[i][12])

                pres_color, dispPsi = display.displayPresValidation(pres)
                pres_color1 = self.displayColorSet(pres_color)
                print "06 - Pressure", pres_color, dispPsi, pres_color1
                
                temp_color, disptemp = display.displayTempValidation(temp)    
                temp_color1 = self.displayColorSet(temp_color)
                print "06 - Temp", temp_color, disptemp, temp_color1
                
                #position = "RRO"
                self.lineEdit_Value_Press_RRO.setText((dispPsi))
                self.lineEdit_Value_Press_RRO.setStyleSheet(pres_color1)

                self.lineEdit_Value_Temp_RRO.setText((disptemp))
                self.lineEdit_Value_Temp_RRO.setStyleSheet(temp_color1)
   
                

        print "end of display method"
        self.lineEdit_Value_BusNumber.setText(vehName)

        #Current date and time
        #t = datetime.utcnow()
        curdate_time = time.strftime('%H:%M:%S %d/%m/%Y')
        predate_time = curdate_time
        self.label_Value_Time_Date.setText(predate_time)


    '''
    def optionClick(self, optionID):
        print "optionClick", optionID
        
        statusAuto = self.radioButton.isChecked()
        statusMan  = self.radioButton_2.isChecked()
        print "self.radiobutton.isChecked()", statusAuto, statusMan
        
        if optionID == "Automatic":
            print "Automatic Mode Enabled"

            self.radioButton.setChecked(True)
            
            self.pushButton_Scan.setEnabled(False)
            #self.horizontalLayout.setEnabled(False)
            self.pushButton_Scan.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.062, y1:0.062, x2:1, y2:0.0113636, stop:0.506537 rgba(212, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "background-color: qlineargradient(spread:pad, x1:0.147227, y1:0.068, x2:1, y2:0.0113636, stop:0.506537 rgba(0, 10, 9, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 75 24pt \"MS Shell Dlg 2\";\n"
            "border-radius: 20px;")

            #Keypad Disable
            self.pushButton_1.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self.pushButton_9.setEnabled(False)
            self.pushButton_0.setEnabled(False)
            
            
            loopStatus = True
            RFID_UID = ""
            #self.callMethod2()
            print "Option Click Loopstatus",loopStatus 
            optionReturn = self.loopFun(loopStatus, RFID_UID)

            if statusMan == True:

                loopStatus = False
            

        if optionID == "Manual":
            
            print "Manual Mode Enabled"

            self.radioButton_2.setChecked(True)
            
            self.pushButton_Scan.setEnabled(True)
            self.pushButton_Scan.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.062, y1:0.062, x2:1, y2:0.0113636, stop:0.506537 rgba(212, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "background-color: qlineargradient(spread:pad, x1:0.147227, y1:0.068, x2:1, y2:0.0113636, stop:0.506537 rgba(0, 135, 9, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 75 24pt \"MS Shell Dlg 2\";\n"
            "border-radius: 20px;")

            loopStatus = False
            print "Option Click Loopstatus",loopStatus

    '''


    

    def optionClick(self, optionID):
        #print "optionClick", optionID
        
        #self.radioButton.setChecked(True)
        
        statusAuto = self.radioButton.isChecked()
        statusMan  = self.radioButton_2.isChecked()
        print "self.radiobutton.isChecked()", statusAuto, statusMan

        #self.radioButton.setChecked(True)

        QtCore.QCoreApplication.processEvents()
            
        if (optionID == "Automatic") and (statusAuto == True):
            print "Automatic Mode Enabled"

            #self.radioButton.setChecked(True)
            
            self.pushButton_Scan.setEnabled(False)
            #self.horizontalLayout.setEnabled(False)
            self.pushButton_Scan.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.062, y1:0.062, x2:1, y2:0.0113636, stop:0.506537 rgba(212, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "background-color: qlineargradient(spread:pad, x1:0.147227, y1:0.068, x2:1, y2:0.0113636, stop:0.506537 rgba(0, 10, 9, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 75 24pt \"MS Shell Dlg 2\";\n"
            "border-radius: 20px;")

            #Keypad Disable
            self.pushButton_1.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self.pushButton_9.setEnabled(False)
            self.pushButton_0.setEnabled(False)
            
            
            loopStatus = True
            RFID_UID = ""
            #self.callMethod2()
            print "Option Click Loopstatus",loopStatus 
            optionReturn = self.loopFun(loopStatus, RFID_UID)
            QtCore.QCoreApplication.processEvents()
            

        if (optionID == "Manual") and (statusMan == True):
            #self.radioButton.setChecked(False)
            #QtCore.QCoreApplication.processEvents()
            print "Manual Mode Enabled"
            
            #Keypad Disable
            self.pushButton_1.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            self.pushButton_9.setEnabled(True)
            self.pushButton_0.setEnabled(True)
            
            #self.radioButton_2.setChecked(True)
            
            self.pushButton_Scan.setEnabled(True)
            self.pushButton_Scan.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.062, y1:0.062, x2:1, y2:0.0113636, stop:0.506537 rgba(212, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "background-color: qlineargradient(spread:pad, x1:0.147227, y1:0.068, x2:1, y2:0.0113636, stop:0.506537 rgba(0, 135, 9, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "font: 75 24pt \"MS Shell Dlg 2\";\n"
            "border-radius: 20px;")
            
            loopStatus = False
            print "Option Click Loopstatus",loopStatus
            QtCore.QCoreApplication.processEvents()
    
    def loopFun(self, loopStatus, loopRFIDUID):
        #global loopStatus
        
        print "loopstatus: ", loopStatus 
        while (loopStatus != False):
            print ("looping ")
            
            loopStatusReturn = self.callMethod2(loopRFIDUID)
            #QtCore.QCoreApplication.processEvents()
            time.sleep(1.5)

            if loopStatusReturn == "Success":
                print "loopStatusReturn", loopStatusReturn

                return loopStatusReturn

            elif loopStatusReturn == "Failed":
                print "loopStatusReturn", loopStatusReturn
                
                loopStatus = False
                return loopStatusReturn

        print "Done clicked"

        

    def callMethod2(self, RFID_UID):

        #global RFID_UID
        #Call method 2 in work.py
        #Returns mylist
        print "method 2 RFID_UID ", RFID_UID

        if (RFID_UID != None) and (RFID_UID != ""):
            
            print "CallMethod2 (RFID_UID != None) or (RFID_UID != ):", RFID_UID
            mylistVar, vehName, status = work.fun_main(RFID_UID)

        elif (RFID_UID == None) or (RFID_UID == ""):
            
            print "CallMethod2 Else", RFID_UID
            mylistVar, vehName, status = work.fun_main(RFID_UID)

#        status = "Success"
#        print "Status", status

        if(status == "Success"):
            print "Call method 2 "
            #mylistVar from work.py
            
            mylistVar = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                          [0, 'a1', '41', '08', '63', '00', '05'], \
                          [0, 'a1', '41', '0f', '63', '00', '01', 'ba', '6b', '09', '01', '50', '78', '00'], \
                          [0, 'a1', '41', '0f', '63', '00', '02', 'ba', '6d', '6d', '01', '25', '58', '00'], \
                          [0, 'a1', '41', '0f', '63', '00', '03', '56', 'a8', 'cb', '01', '30', '70', '00'], \
                          [0, 'a1', '41', '0f', '63', '00', '04', '56', 'a6', 'be', '01', '45', '65', '00'], \
                          [0, 'a1', '41', '0f', '63', '00', '05', '56', 'a7', '81', '00', '00', '00', '00'], \
                          [0, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
            
#            vehName = "SND 9406"
            print "vehName", vehName
	    
            self.displayTPData(vehName, mylistVar)

        elif (status == "Failed"):
            return "Failed"

    def showdialog(message):
        print ("dialog ", message)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(message)
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def callMethod1(self):
        
        #Call method 1 in work.py to verify the vehicle exists or not
	# If exists return rfuid
        # If not exists display a message
        print "Call method 1" + self.lineEdit_bus_No.displayText()
        
        if(len(self.lineEdit_bus_No.displayText()) > 0):

            print "Call method 1" + self.lineEdit_bus_No.displayText()
            
            
            #RFID = work.fun_vehName(self.lineEdit_bus_No.displayText())
            RFID = work.fun_VehName(self.lineEdit_bus_No.displayText())

            print RFID
            return RFID
        
            # For testing
            # return "RFUID"
        else:
            return None

    		

    def endProcess(self):

        # Stop the loop
#        global loopStatus
        loopStatus = False
        # Clear all the text fields

        self.lineEdit_Value_BusNumber.setText("")
        self.lineEdit_Value_Press_FL.setText("")
        self.lineEdit_Value_Temp_FL.setText("")
        self.lineEdit_Value_Press_FR.setText("")
        self.lineEdit_value_Temp_FR.setText("")
        self.lineEdit_Value_Press_RLO.setText("")
        self.lineEdit_Value_Temp_RLO.setText("")
        self.lineEdit_Value_Press_RLI.setText("")
        self.lineEdit_Value_Temp_RLI.setText("")
        self.lineEdit_Value_Press_RRI.setText("")
        self.lineEdit_Value_Temp_RRI.setText("")
        self.lineEdit_Value_Press_RRO.setText("")
        self.lineEdit_Value_Temp_RRO.setText("")

        print ("Cleared all the text boxes")

    

    def btnClick(self, btnEvent):
        global sec
        #global loopStatus
        global RFID_UID
        
        RFID_UID = ""

        # Stoping the loop
        loopStatus = False

        

        if btnEvent == "Scan" :

            #By default closing the last thread
            self.endProcess()

            #Clicked Scan Button
            if len(self.lineEdit_bus_No.displayText()) > 0 and len(self.lineEdit_bus_No.displayText()) < 4:
                print ("Please enter 4 digits bus no", self.lineEdit_bus_No.displayText())

            else:
                print ("Call work.py -> function(): ", self.lineEdit_bus_No.displayText())

                if(len(self.lineEdit_bus_No.displayText()) > 0):
                    # Checking for RFID_UID
                    method1Resp = self.callMethod1()

                    if method1Resp != None:
                        loopStatus = True
                        RFID_UID = method1Resp

                        #self.callMethod2()
                        self.loopFun(loopStatus, RFID_UID)

                    else:
                        print("Method 1 error ", "Vehicle not found")

                else:
                    loopStatus = True
                    RFID_UID = ""
                    #self.callMethod2()
                    self.loopFun(loopStatus, RFID_UID)

        else:
            #Clicked Done Button
            print("inside else done")
            self.numberString = ""
            self.lineEdit_bus_No.setText("")
            self.endProcess()

    def keypadEvent(self, bid):
        print (bid, self.numberString)

        if bid != "clear" and bid != "back" and len(self.lineEdit_bus_No.displayText()) > 3:

            print "Maximum bus no is 4 digits"

        else:

            if bid == "b1":
                self.numberString = self.numberString + "1"
            if bid == "b2":
                self.numberString = self.numberString + "2"
            if bid == "b3":
                self.numberString = self.numberString + "3"
            if bid == "b4":
                self.numberString = self.numberString + "4"
            if bid == "b5":
                self.numberString = self.numberString + "5"
            if bid == "b6":
                self.numberString = self.numberString + "6"
            if bid == "b7":
                self.numberString = self.numberString + "7"
            if bid == "b8":
                self.numberString = self.numberString + "8"
            if bid == "b9":
                self.numberString = self.numberString + "9"
            if bid == "b0":
                self.numberString = self.numberString + "0"
            if bid == "back":
                self.numberString = self.numberString[:-1]
            if bid == "clear":
                self.numberString = ""

        print (self.numberString)
        self.lineEdit_bus_No.setText(self.numberString)

    
    
    #def MainWindow(QMainWindow):
        '''def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setGeometry(50, 50, 600, 750)
            self.setFixedSize(600, 750)
            self.startUIWindow()

            self.movie = QMovie("/home/pi/Documents/TZcL7Cc.gif")
            self.movie.frameChanged.connect(self.repaint)
            self.movie.start()

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("My Program")
        self.show()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    '''

    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1316, 815)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/window_Icon/Images/4898_-_Pressure_Check-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("")
        self.label_Image_Bus = QtWidgets.QLabel(Form)
        self.label_Image_Bus.setGeometry(QtCore.QRect(770, 120, 191, 561))
        self.label_Image_Bus.setStyleSheet("border-image: url(:/bus_Image/Images/bustyres - Copy.png);")
        self.label_Image_Bus.setText("")
        self.label_Image_Bus.setObjectName("label_Image_Bus")
        self.label_Text_TPMS = QtWidgets.QLabel(Form)
        self.label_Text_TPMS.setGeometry(QtCore.QRect(330, 10, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_Text_TPMS.setFont(font)
        self.label_Text_TPMS.setStyleSheet("color: rgb(0, 85, 0);")
        self.label_Text_TPMS.setObjectName("label_Text_TPMS")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 160, 361, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layoutWidget.sizePolicy().hasHeightForWidth())
        self.layoutWidget.setSizePolicy(sizePolicy)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_bus_No = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_bus_No.sizePolicy().hasHeightForWidth())
        self.lineEdit_bus_No.setSizePolicy(sizePolicy)
        self.lineEdit_bus_No.setStyleSheet("font: 75 18pt \"MS Shell Dlg 2\";")
        self.lineEdit_bus_No.setText("")
        self.lineEdit_bus_No.setObjectName("lineEdit_bus_No")
        self.horizontalLayout.addWidget(self.lineEdit_bus_No)
        self.pushButton_Scan = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Scan.sizePolicy().hasHeightForWidth())
        self.pushButton_Scan.setSizePolicy(sizePolicy)
        self.pushButton_Scan.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.062, y1:0.062, x2:1, y2:0.0113636, stop:0.506537 rgba(212, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"background-color: qlineargradient(spread:pad, x1:0.147227, y1:0.068, x2:1, y2:0.0113636, stop:0.506537 rgba(0, 135, 9, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(255, 255, 255);\n"
"font: 75 24pt \"MS Shell Dlg 2\";\n"
"border-radius: 20px;")
        self.pushButton_Scan.setObjectName("pushButton_Scan")
        self.horizontalLayout.addWidget(self.pushButton_Scan)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(70, 240, 361, 341))
        self.layoutWidget1.setStyleSheet("")
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_Done = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Done.sizePolicy().hasHeightForWidth())
        self.pushButton_Done.setSizePolicy(sizePolicy)
        self.pushButton_Done.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.062, y1:0.062, x2:1, y2:0.0113636, stop:0.506537 rgba(212, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(255, 255, 255);\n"
"font: 75 24pt \"MS Shell Dlg 2\";\n"
"border-radius: 20px;")
        self.pushButton_Done.setObjectName("pushButton_Done")
        self.gridLayout.addWidget(self.pushButton_Done, 4, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 2, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_1.sizePolicy().hasHeightForWidth())
        self.pushButton_1.setSizePolicy(sizePolicy)
        self.pushButton_1.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 0, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 2, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.pushButton_Clear = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Clear.sizePolicy().hasHeightForWidth())
        self.pushButton_Clear.setSizePolicy(sizePolicy)
        self.pushButton_Clear.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.gridLayout.addWidget(self.pushButton_Clear, 3, 2, 1, 1)
        self.pushButton_0 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_0.sizePolicy().hasHeightForWidth())
        self.pushButton_0.setSizePolicy(sizePolicy)
        self.pushButton_0.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_0.setObjectName("pushButton_0")
        self.gridLayout.addWidget(self.pushButton_0, 3, 1, 1, 1)
        self.pushButton_Back = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Back.sizePolicy().hasHeightForWidth())
        self.pushButton_Back.setSizePolicy(sizePolicy)
        self.pushButton_Back.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_Back.setObjectName("pushButton_Back")
        self.gridLayout.addWidget(self.pushButton_Back, 3, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 2, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.0284091 rgba(34, 34, 34, 255), stop:0.426136 rgba(86, 72, 65, 255), stop:0.971591 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(760, 50, 221, 41))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_Text_BusNumber = QtWidgets.QLabel(self.layoutWidget2)
        self.label_Text_BusNumber.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_BusNumber.setObjectName("label_Text_BusNumber")
        self.horizontalLayout_2.addWidget(self.label_Text_BusNumber)
        self.lineEdit_Value_BusNumber = QtWidgets.QLineEdit(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Value_BusNumber.sizePolicy().hasHeightForWidth())
        self.lineEdit_Value_BusNumber.setSizePolicy(sizePolicy)
        self.lineEdit_Value_BusNumber.setObjectName("lineEdit_Value_BusNumber")
        self.horizontalLayout_2.addWidget(self.lineEdit_Value_BusNumber)
        self.layoutWidget_2 = QtWidgets.QWidget(Form)
        self.layoutWidget_2.setGeometry(QtCore.QRect(530, 380, 211, 131))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_Image_Temp_RLO = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_Image_Temp_RLO.setStyleSheet("image: url(:/temp_Image/Images/temp.png);")
        self.label_Image_Temp_RLO.setText("")
        self.label_Image_Temp_RLO.setObjectName("label_Image_Temp_RLO")
        self.gridLayout_3.addWidget(self.label_Image_Temp_RLO, 1, 1, 1, 1)
        self.lineEdit_Value_Temp_RLO = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lineEdit_Value_Temp_RLO.setObjectName("lineEdit_Value_Temp_RLO")
        self.gridLayout_3.addWidget(self.lineEdit_Value_Temp_RLO, 2, 1, 1, 1)
        self.lineEdit_Value_Press_RLO = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lineEdit_Value_Press_RLO.setObjectName("lineEdit_Value_Press_RLO")
        self.gridLayout_3.addWidget(self.lineEdit_Value_Press_RLO, 2, 0, 1, 1)
        self.label_Image_Press_RLO = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_Image_Press_RLO.setStyleSheet("image: url(:/pressure_Image/Images/pressure1psi.png);")
        self.label_Image_Press_RLO.setText("")
        self.label_Image_Press_RLO.setObjectName("label_Image_Press_RLO")
        self.gridLayout_3.addWidget(self.label_Image_Press_RLO, 1, 0, 1, 1)
        self.label_Text_RLO = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_RLO.sizePolicy().hasHeightForWidth())
        self.label_Text_RLO.setSizePolicy(sizePolicy)
        self.label_Text_RLO.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_RLO.setObjectName("label_Text_RLO")
        self.gridLayout_3.addWidget(self.label_Text_RLO, 0, 0, 1, 2)
        self.layoutWidget_3 = QtWidgets.QWidget(Form)
        self.layoutWidget_3.setGeometry(QtCore.QRect(530, 540, 211, 131))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lineEdit_Value_Press_RLI = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_Value_Press_RLI.setObjectName("lineEdit_Value_Press_RLI")
        self.gridLayout_4.addWidget(self.lineEdit_Value_Press_RLI, 2, 0, 1, 1)
        self.lineEdit_Value_Temp_RLI = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_Value_Temp_RLI.setObjectName("lineEdit_Value_Temp_RLI")
        self.gridLayout_4.addWidget(self.lineEdit_Value_Temp_RLI, 2, 1, 1, 1)
        self.label_Image_Press_RLI = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_Image_Press_RLI.setStyleSheet("image: url(:/pressure_Image/Images/pressure1psi.png);")
        self.label_Image_Press_RLI.setText("")
        self.label_Image_Press_RLI.setObjectName("label_Image_Press_RLI")
        self.gridLayout_4.addWidget(self.label_Image_Press_RLI, 1, 0, 1, 1)
        self.label_Image_Temp_RLI = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_Image_Temp_RLI.setStyleSheet("image: url(:/temp_Image/Images/temp.png);")
        self.label_Image_Temp_RLI.setText("")
        self.label_Image_Temp_RLI.setObjectName("label_Image_Temp_RLI")
        self.gridLayout_4.addWidget(self.label_Image_Temp_RLI, 1, 1, 1, 1)
        self.label_Text_RLI = QtWidgets.QLabel(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_RLI.sizePolicy().hasHeightForWidth())
        self.label_Text_RLI.setSizePolicy(sizePolicy)
        self.label_Text_RLI.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_RLI.setObjectName("label_Text_RLI")
        self.gridLayout_4.addWidget(self.label_Text_RLI, 0, 0, 1, 2)
        self.layoutWidget_4 = QtWidgets.QWidget(Form)
        self.layoutWidget_4.setGeometry(QtCore.QRect(990, 140, 211, 131))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget_4)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_Text_FR = QtWidgets.QLabel(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_FR.sizePolicy().hasHeightForWidth())
        self.label_Text_FR.setSizePolicy(sizePolicy)
        self.label_Text_FR.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_FR.setObjectName("label_Text_FR")
        self.gridLayout_5.addWidget(self.label_Text_FR, 0, 0, 1, 1)
        self.lineEdit_Value_Press_FR = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.lineEdit_Value_Press_FR.setObjectName("lineEdit_Value_Press_FR")
        self.gridLayout_5.addWidget(self.lineEdit_Value_Press_FR, 2, 0, 1, 1)
        self.lineEdit_value_Temp_FR = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.lineEdit_value_Temp_FR.setObjectName("lineEdit_value_Temp_FR")
        self.gridLayout_5.addWidget(self.lineEdit_value_Temp_FR, 2, 1, 1, 1)
        self.label_Image_Press_FR = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_Image_Press_FR.setStyleSheet("image: url(:/pressure_Image/Images/pressure1psi.png);")
        self.label_Image_Press_FR.setText("")
        self.label_Image_Press_FR.setObjectName("label_Image_Press_FR")
        self.gridLayout_5.addWidget(self.label_Image_Press_FR, 1, 0, 1, 1)
        self.label_Image_Temp_FR = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_Image_Temp_FR.setStyleSheet("image: url(:/temp_Image/Images/temp.png);")
        self.label_Image_Temp_FR.setText("")
        self.label_Image_Temp_FR.setObjectName("label_Image_Temp_FR")
        self.gridLayout_5.addWidget(self.label_Image_Temp_FR, 1, 1, 1, 1)
        self.layoutWidget_5 = QtWidgets.QWidget(Form)
        self.layoutWidget_5.setGeometry(QtCore.QRect(990, 380, 211, 131))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget_5)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.lineEdit_Value_Press_RRO = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.lineEdit_Value_Press_RRO.setObjectName("lineEdit_Value_Press_RRO")
        self.gridLayout_6.addWidget(self.lineEdit_Value_Press_RRO, 2, 0, 1, 1)
        self.lineEdit_Value_Temp_RRO = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.lineEdit_Value_Temp_RRO.setObjectName("lineEdit_Value_Temp_RRO")
        self.gridLayout_6.addWidget(self.lineEdit_Value_Temp_RRO, 2, 1, 1, 1)
        self.label_Image_Press_RRO = QtWidgets.QLabel(self.layoutWidget_5)
        self.label_Image_Press_RRO.setStyleSheet("image: url(:/pressure_Image/Images/pressure1psi.png);")
        self.label_Image_Press_RRO.setText("")
        self.label_Image_Press_RRO.setObjectName("label_Image_Press_RRO")
        self.gridLayout_6.addWidget(self.label_Image_Press_RRO, 1, 0, 1, 1)
        self.label_Image_Temp_RRO = QtWidgets.QLabel(self.layoutWidget_5)
        self.label_Image_Temp_RRO.setStyleSheet("image: url(:/temp_Image/Images/temp.png);")
        self.label_Image_Temp_RRO.setText("")
        self.label_Image_Temp_RRO.setObjectName("label_Image_Temp_RRO")
        self.gridLayout_6.addWidget(self.label_Image_Temp_RRO, 1, 1, 1, 1)
        self.label_Text_RRO = QtWidgets.QLabel(self.layoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_RRO.sizePolicy().hasHeightForWidth())
        self.label_Text_RRO.setSizePolicy(sizePolicy)
        self.label_Text_RRO.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_RRO.setObjectName("label_Text_RRO")
        self.gridLayout_6.addWidget(self.label_Text_RRO, 0, 0, 1, 2)
        self.layoutWidget_6 = QtWidgets.QWidget(Form)
        self.layoutWidget_6.setGeometry(QtCore.QRect(990, 540, 211, 131))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.layoutWidget_6)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lineEdit_Value_Temp_RRI = QtWidgets.QLineEdit(self.layoutWidget_6)
        self.lineEdit_Value_Temp_RRI.setObjectName("lineEdit_Value_Temp_RRI")
        self.gridLayout_7.addWidget(self.lineEdit_Value_Temp_RRI, 2, 1, 1, 1)
        self.label_Image_Press_RRI = QtWidgets.QLabel(self.layoutWidget_6)
        self.label_Image_Press_RRI.setStyleSheet("image: url(:/pressure_Image/Images/pressure1psi.png);")
        self.label_Image_Press_RRI.setText("")
        self.label_Image_Press_RRI.setObjectName("label_Image_Press_RRI")
        self.gridLayout_7.addWidget(self.label_Image_Press_RRI, 1, 0, 1, 1)
        self.lineEdit_Value_Press_RRI = QtWidgets.QLineEdit(self.layoutWidget_6)
        self.lineEdit_Value_Press_RRI.setObjectName("lineEdit_Value_Press_RRI")
        self.gridLayout_7.addWidget(self.lineEdit_Value_Press_RRI, 2, 0, 1, 1)
        self.label_Image_Temp_RRI = QtWidgets.QLabel(self.layoutWidget_6)
        self.label_Image_Temp_RRI.setStyleSheet("image: url(:/temp_Image/Images/temp.png);")
        self.label_Image_Temp_RRI.setText("")
        self.label_Image_Temp_RRI.setObjectName("label_Image_Temp_RRI")
        self.gridLayout_7.addWidget(self.label_Image_Temp_RRI, 1, 1, 1, 1)
        self.label_Text_RRI = QtWidgets.QLabel(self.layoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_RRI.sizePolicy().hasHeightForWidth())
        self.label_Text_RRI.setSizePolicy(sizePolicy)
        self.label_Text_RRI.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_RRI.setObjectName("label_Text_RRI")
        self.gridLayout_7.addWidget(self.label_Text_RRI, 0, 0, 1, 2)
        self.layoutWidget3 = QtWidgets.QWidget(Form)
        self.layoutWidget3.setGeometry(QtCore.QRect(530, 140, 211, 131))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_Value_Press_FL = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_Value_Press_FL.setObjectName("lineEdit_Value_Press_FL")
        self.gridLayout_2.addWidget(self.lineEdit_Value_Press_FL, 2, 0, 1, 1)
        self.lineEdit_Value_Temp_FL = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_Value_Temp_FL.setObjectName("lineEdit_Value_Temp_FL")
        self.gridLayout_2.addWidget(self.lineEdit_Value_Temp_FL, 2, 1, 1, 1)
        self.label_Image_Press_FL = QtWidgets.QLabel(self.layoutWidget3)
        self.label_Image_Press_FL.setStyleSheet("image: url(:/pressure_Image/Images/pressure1psi.png);")
        self.label_Image_Press_FL.setText("")
        self.label_Image_Press_FL.setObjectName("label_Image_Press_FL")
        self.gridLayout_2.addWidget(self.label_Image_Press_FL, 1, 0, 1, 1)
        self.label_Image_Temp_FL = QtWidgets.QLabel(self.layoutWidget3)
        self.label_Image_Temp_FL.setStyleSheet("image: url(:/temp_Image/Images/temp.png);")
        self.label_Image_Temp_FL.setText("")
        self.label_Image_Temp_FL.setObjectName("label_Image_Temp_FL")
        self.gridLayout_2.addWidget(self.label_Image_Temp_FL, 1, 1, 1, 1)
        self.label_Text_FL = QtWidgets.QLabel(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_FL.sizePolicy().hasHeightForWidth())
        self.label_Text_FL.setSizePolicy(sizePolicy)
        self.label_Text_FL.setStyleSheet("color: rgb(0, 85, 0);\n"
"font: 75 14pt \"MS Shell Dlg 2\";")
        self.label_Text_FL.setObjectName("label_Text_FL")
        self.gridLayout_2.addWidget(self.label_Text_FL, 0, 0, 1, 2)

        #Radio Button
        self.layoutWidget4 = QtWidgets.QWidget(Form)
        self.layoutWidget4.setGeometry(QtCore.QRect(70, 70, 221, 41))
        self.layoutWidget4.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";")
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton.sizePolicy().hasHeightForWidth())
        self.radioButton.setSizePolicy(sizePolicy)
        self.radioButton.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";")
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_3.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_2.sizePolicy().hasHeightForWidth())
        self.radioButton_2.setSizePolicy(sizePolicy)
        self.radioButton_2.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";")
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_3.addWidget(self.radioButton_2)

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(1020, 50, 261, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_Text_Time_Date = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Text_Time_Date.sizePolicy().hasHeightForWidth())
        self.label_Text_Time_Date.setSizePolicy(sizePolicy)
        self.label_Text_Time_Date.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.label_Text_Time_Date.setObjectName("label_Text_Time_Date")
        self.horizontalLayout_4.addWidget(self.label_Text_Time_Date)
        self.label_Value_Time_Date = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Value_Time_Date.sizePolicy().hasHeightForWidth())
        self.label_Value_Time_Date.setSizePolicy(sizePolicy)
        self.label_Value_Time_Date.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.label_Value_Time_Date.setText("")
        self.label_Value_Time_Date.setObjectName("label_Value_Time_Date")
        self.horizontalLayout_4.addWidget(self.label_Value_Time_Date)

        '''
        self.currentFrame = self.movie.currentPixmap()
        self.frameRect = self.currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)
        '''
        
        
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.label_Image_Bus.raise_()
        self.layoutWidget.raise_()
        self.label_Text_TPMS.raise_()
        self.layoutWidget_2.raise_()
        self.layoutWidget_3.raise_()
        self.layoutWidget_4.raise_()
        self.layoutWidget_5.raise_()
        self.layoutWidget_6.raise_()

        self.label_Text_Time_Date.raise_()
        self.label_Value_Time_Date.raise_()

        self.retranslateUi(Form)

        #GIF
        #self.paintEvent(event)
        #self.movie.start()


        
        QtCore.QMetaObject.connectSlotsByName(Form)


    #GIF
    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        #Form.setWindowTitle(_translate("Form", "Form"))
        Form.setWindowTitle(_translate("Form", "TPMS"))
        self.label_Text_TPMS.setText(_translate("Form", "Tyre Pressure Management System"))
        self.pushButton_Scan.setText(_translate("Form", "Scan"))
        self.pushButton_Done.setText(_translate("Form", "Done"))
        self.pushButton_6.setText(_translate("Form", "6"))
        self.pushButton_5.setText(_translate("Form", "5"))
        self.pushButton_1.setText(_translate("Form", "1"))
        self.pushButton_7.setText(_translate("Form", "7"))
        self.pushButton_8.setText(_translate("Form", "8"))
        self.pushButton_4.setText(_translate("Form", "4"))
        self.pushButton_Clear.setText(_translate("Form", "C"))
        self.pushButton_0.setText(_translate("Form", "0"))
        self.pushButton_Back.setText(_translate("Form", "<-"))
        self.pushButton_9.setText(_translate("Form", "9"))
        self.pushButton_3.setText(_translate("Form", "3"))
        self.pushButton_2.setText(_translate("Form", "2"))
        self.label_Text_BusNumber.setText(_translate("Form", "Bus Number"))
        self.label_Text_RLO.setText(_translate("Form", "Rear Left Outer"))
        self.label_Text_RLI.setText(_translate("Form", "Rear Left Inner"))
        self.label_Text_FR.setText(_translate("Form", "Front Right"))
        self.label_Text_RRO.setText(_translate("Form", "Rear Right Outer"))
        self.label_Text_RRI.setText(_translate("Form", "Rear Right Inner"))
        self.label_Text_FL.setText(_translate("Form", "Front Left"))
        
        #Radio Button
        self.radioButton.setText(_translate("Form", "Automatic"))
        self.radioButton_2.setText(_translate("Form", "Manual"))

        self.label_Text_Time_Date.setText(_translate("Form", "Time/ Date :"))

        self.radioButton.clicked.connect(lambda: self.optionClick("Automatic"))
        self.radioButton_2.clicked.connect(lambda: self.optionClick("Manual"))

        self.pushButton_Scan.clicked.connect(lambda: self.btnClick("Scan"))
        self.pushButton_Done.clicked.connect(lambda: self.btnClick("Done"))

        # Keypad event
        self.pushButton_1.clicked.connect(lambda: self.keypadEvent("b1"))
        self.pushButton_2.clicked.connect(lambda: self.keypadEvent("b2"))
        self.pushButton_3.clicked.connect(lambda: self.keypadEvent("b3"))
        self.pushButton_4.clicked.connect(lambda: self.keypadEvent("b4"))
        self.pushButton_5.clicked.connect(lambda: self.keypadEvent("b5"))
        self.pushButton_6.clicked.connect(lambda: self.keypadEvent("b6"))
        self.pushButton_7.clicked.connect(lambda: self.keypadEvent("b7"))
        self.pushButton_8.clicked.connect(lambda: self.keypadEvent("b8"))
        self.pushButton_9.clicked.connect(lambda: self.keypadEvent("b9"))
        self.pushButton_0.clicked.connect(lambda: self.keypadEvent("b0"))
        self.pushButton_Clear.clicked.connect(lambda: self.keypadEvent("clear"))
        self.pushButton_Back.clicked.connect(lambda: self.keypadEvent("back"))


        #GIF
        #self.movie = QMovie("/home/pi/Documents/TZcL7Cc.gif")
        #self.movie.frameChanged.connect(lambda: self.repaint("event"))
        #self.movie.start()
        

if __name__ == "__main__":


    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()

    #app = QApplication(sys.argv)
    #w = MainWindow()
    
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    statusOption = "Automatic"
    ui.radioButton.setChecked(True)
    while True:
        

               
        ui.optionClick(statusOption)
        time.sleep(2)
    
        def myExitHandler():
            loopStatus = False
            ui.endProcess()
            print "On close of main window stopping the thread"

    app.aboutToQuit.connect(myExitHandler)
    sys.exit(app.exec_())

