import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.MainSwitchSensor import mainSwitchSensors
import time

mainSwitchSensor = mainSwitchSensors()

def printStatus(interruptedPin):
    statuses = mainSwitchSensor.allMainSwitchStates()
    if interruptedPin in mainSwitchSensor.ThreeWayIn1Pins:
        pinIndex = mainSwitchSensor.ThreeWayIn1Pins.index(interruptedPin)
        print("{} switch was detected as changing".format(mainSwitchSensor.ThreeStateSwitches[pinIndex]))
    elif interruptedPin in mainSwitchSensor.ThreeWayIn2Pins:
        pinIndex = mainSwitchSensor.ThreeWayIn2Pins.index(interruptedPin)
        print("{} switch was detected as changing".format(mainSwitchSensor.ThreeStateSwitches[pinIndex]))
    elif interruptedPin in mainSwitchSensor.TwoWayInPins:
        pinIndex = mainSwitchSensor.TwoWayInPins.index(interruptedPin)
        print("{} switch was detected as changing".format(mainSwitchSensor.TwoStateSwitches[pinIndex]))
    for i in range(0,6): print(mainSwitchSensor.Switches[i]+": "+statuses[i])
    print("")

for i in range(0,6): print("The {} switch started in the {} position".format(mainSwitchSensor.Switches[i],mainSwitchSensor.switchState(mainSwitchSensor.Switches[i])))

print("\nTesting detection of main switches")
print("Should display new positions any time a switch is flipped")
mainSwitchSensor.interruptSetUp(printStatus)

try:
    while True: time.sleep(2)

except KeyboardInterrupt: print("\nEnding main switch detection test")

    
