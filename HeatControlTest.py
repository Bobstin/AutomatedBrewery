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

    while True:
        time.sleep(5)
        testConn.send(["kettle","MLT"])
        time.sleep(5)
        testConn.send(["kettle","BLK"])

except KeyboardInterrupt:
    print("\nShutting off both kettles")
    testConn.send(["kettle","None"])
    
