import binascii
import sys
import time
import string



def pressureToBarPsiConvertion(pres):

    presint_Bar = ((int(pres, 16)*0.025))
    presint_Psi = int (round(presint_Bar * 14.5038))
    dispPsi = str(presint_Psi).zfill(3)

    return presint_Psi


def temperatureToCelciousConvertion(temp):

    tempint_Celcious  = round(int(temp, 16) - 50)
    disptemp = str(int(tempint_Celcious)).zfill(3)


    return tempint_Celcious


def displayPresValidation(pres):
    print "utilities", pres

    try:

        #Check for the Valid Pres is not 0000
        if pres.strip() != "0000" :
                        
            
            presint_Psi = utlities.pressureToBarPsiConvertion(pres)
            dispPsi = str(presint_Psi).zfill(3)
                        
                        
            #Staturated PSI value between 121 to 125 Should be Green Color
            if (presint_Psi) < 125 and presint_Psi >= 120:

                pres_color = Green
                #print pres_color
                        
            #Staturated PSI value between 121 to 125 Should be Yellow Color
            elif presint_Psi < 120 and presint_Psi >= 115:

                pres_color = Yellow

            #Staturated PSI value between 114 to below Should be Red Color
            elif presint_Psi < 114 :
                pres_color = Red

            #Staturated PSI value is above 125 Should be White Color
            elif presint_Psi > 125 :
                pres_color = White

            else:
                pres_color = Red
 
                        
        #Check for the Valid Pres is 0000
        else:
            pres_color = Blue
            dispPsi = "---"

        return  pres_color, dispPsi

    except:
        e = sys.exc_info()[0]
        my_logger.error("Failed - Pressure Calculation:%s ",e)
        print ("Failed - Pressure Calculation: ",e)

        return None
