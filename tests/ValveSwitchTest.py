import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.ValveSwitchSensor import valveSwitchSensors
import time

valveSwitchSensor = valveSwitchSensors()

def printStatus(IGNORE):
    print(valveSwitchSensor.allValveSwitchStates())

for i in range(1,11):
    print("Valve {} started in the in the {} position".format(i,valveSwitchSensor.valveSwitchState(i)))
valveSwitchSensor.interruptSetUp(printStatus)

print("\nTesting detection of valve switches.")
print("Should display new positions any time a switch is flipped")

try:
    while True: time.sleep(2)

except KeyboardInterrupt: print("\nEnding valve switch detection test")
