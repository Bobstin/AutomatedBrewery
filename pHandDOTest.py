import sys
import time
from pHandDOSensor import pHandDOSensors

pHandDOSensor = pHandDOSensors()

Sensor = input(">>Enter sensor to test (pH or DO)")

try:
    if Sensor == "pH":
        print("Pulling device information")
        print(pHandDOSensor.pHSensor.query("I")+"\n")
        while True:
            print(pHandDOSensor.pH())
            time.sleep(2)
    elif Sensor == "DO":
        print("Pulling device information")
        print(pHandDOSensor.DOSensor.query("I")+"\n")
        while True:
            print(pHandDOSensor.DO())
            time.sleep(2)
    else:
        print("Error: sensor inputted was not valid")
        sys.exit()
except KeyboardInterrupt: print("\n Ending {} sensor test".format(Sensor))
