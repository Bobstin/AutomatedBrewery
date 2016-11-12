import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.HeatControl import HeatController
import time
import threading
from multiprocessing import Pipe
import sys

def startHeatControl(heatConn,IGNORE):
    HeatCtrl = HeatController(pipeConn=heatConn)
    HeatCtrl.kettle = "BLK"

testSelection = input("Select test to run (Alternating or Long run): ")

if testSelection == "Alternating":
    try:
        heatConn,testConn = Pipe()
        IGNORE = None
        heatThread = threading.Thread(target = startHeatControl, args=(heatConn,IGNORE))
        heatThread.start()

        print("The kettles should switch every 5 seconds, starting with BLK")
        print("The SSRs should be off for the first cycle, then be on for progressively longer each time")

        firstPass=1
        heatSetting = 0

        while True:
            time.sleep(5)
            if not(firstPass):
                heatSetting += (100-heatSetting)/2
                testConn.send(["heatSetting",heatSetting])
            else: firstPass=0
            testConn.send(["kettle","HLT"])
            time.sleep(5)
            testConn.send(["kettle","BLK"])

    except KeyboardInterrupt:
        print("\nShutting off both kettles")
        testConn.send(["kettle","None"])
    
if testSelection == "Long run":
    try:
        kettleSelection = input("Select kettle (HLT or BLK): ")
        heatConn,testConn = Pipe()
        IGNORE = None
        heatThread = threading.Thread(target = startHeatControl, args=(heatConn,IGNORE))
        heatThread.start()

        print("Will turn on {} at NO HEAT for 30 seconds, then turn on the heat to 100%".format(kettleSelection))
        print("To end test, press ctrl-C")

        if kettleSelection != "HLT" and kettleSelection != "BLK":
            print("Error: invalid kettle selected. Ending test")
            testConn.send(["kettle","None"])
            sys.exit()
        else:
            testConn.send(["kettle",kettleSelection])
            time.sleep(30)
            print("Turning on heat")
            testConn.send(["heatSetting",100])

        #This loop is just here to handle interrupts
        while True:
            time.sleep(2)
                  
    except KeyboardInterrupt:
        print("\nShutting off both kettles")
        testConn.send(["kettle","None"])
            
        
