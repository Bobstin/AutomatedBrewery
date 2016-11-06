import HeatControl
import time
import threading
from multiprocessing import Pipe

def startHeatControl(heatConn,IGNORE):
    HeatCtrl = HeatControl.HeatController(pipeConn=heatConn)
    HeatCtrl.kettle = "BLK"

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
    
