import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import time
from automatedbrewery.PumpAerationValveControl import PumpAerationValveController

def valveTest():
    print("Testing the valves. Should start with all valve closed for 5 seconds,")
    print("then all valves open for 5 seconds, then all closed again for 5 seconds")
    print("This is followed by the opening of each valve in order, one second apart")
    print("Then all valves are turned off\n")

    time.sleep(5)

    PAVControl.valveStates = [1]*10
    time.sleep(5)
    PAVControl.valveStates = [0]*10
    time.sleep(5)

    PAVControl.valve1 = 1
    time.sleep(1)
    PAVControl.valve2 = 1
    time.sleep(1)
    PAVControl.valve3 = 1
    time.sleep(1)
    PAVControl.valve4 = 1
    time.sleep(1)
    PAVControl.valve5 = 1
    time.sleep(1)
    PAVControl.valve6 = 1
    time.sleep(1)
    PAVControl.valve7 = 1
    time.sleep(1)
    PAVControl.valve8 = 1
    time.sleep(1)
    PAVControl.valve9 = 1
    time.sleep(1)
    PAVControl.valve10 = 1
    time.sleep(5)

    PAVControl.valveStates = [0]*10
    time.sleep(5)

    
def partialValveTest():
    print("Testing the ability to partially open valves 5 and 9.")
    print("Both valves will be closed for 5 seconds, then valve 5 will be partially")
    print("opened, then fully opened, followed by the same pattern for valve 9.")
    print("Then they will be partially closed, followed by fully closed\n")

    PAVControl.partialOpenClose(5,1.5)
    time.sleep(2)
    PAVControl.fullyOpenClose(5,1)
    time.sleep(5)

    PAVControl.partialOpenClose(9,1.5)
    time.sleep(2)
    PAVControl.fullyOpenClose(9,1)
    time.sleep(5)

    PAVControl.partialOpenClose(5,-1.5)
    time.sleep(2)
    PAVControl.fullyOpenClose(5,0)
    time.sleep(5)

    PAVControl.partialOpenClose(9,-1.5)
    time.sleep(2)
    PAVControl.fullyOpenClose(9,0)
    time.sleep(5)

    print("Testing the ability to repeatedly partially open")
    print("Both valves will be opened in steps, then closed in steps")

    for i in range(0,6):
        PAVControl.partialOpenClose(5,.5)
        PAVControl.partialOpenClose(9,.5)
        time.sleep(2)

    for i in range(0,6):
        PAVControl.partialOpenClose(5,-.5)
        PAVControl.partialOpenClose(9,-.5)
        time.sleep(2)

    PAVControl.fullyOpenClose(5,0)
    PAVControl.fullyOpenClose(9,0)
    time.sleep(5)

def pumpAerationTest():
    print("Testing the pumps and aeration. Should start with all off for 2 seconds,")
    print("then all on for 2 seconds, then all off again for 2 seconds")
    print("This is followed by the turning on of the Wort Pump, then the")
    print("Water pump, then Aeration, two seconds apart")
    print("Then all are turned off\n")
    time.sleep(2)

    PAVControl.wortPump = 1
    PAVControl.waterPump = 1
    PAVControl.aeration = 1
    time.sleep(2)

    PAVControl.wortPump = 0
    PAVControl.waterPump = 0
    PAVControl.aeration = 0
    time.sleep(2)

    PAVControl.wortPump = 1
    time.sleep(2)
    PAVControl.waterPump = 1
    time.sleep(2)
    PAVControl.aeration = 1
    time.sleep(2)

    PAVControl.wortPump = 0
    PAVControl.waterPump = 0
    PAVControl.aeration = 0
    time.sleep(2)

PAVControl = PumpAerationValveController()
test = input(">>Please select which test to run, either Valve, Partially Open Valve, Pump and Aeration, or All:")
print("")
if test == "Valve": valveTest()
elif test == "Partially Open Valve":partialValveTest()
elif test == "Pump and Aeration":pumpAerationTest()
elif test == "All":
    valveTest()
    partialValveTest()
    pumpAerationTest()
else: print("Error: selected test was not valid")

PAVControl.cleanup()


