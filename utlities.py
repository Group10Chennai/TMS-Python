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

