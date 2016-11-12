from RTDSensor import tempSensors
import time
import sys

sensor = input(">>Enter temp sensor to test (HLT,MLT,BLK, or All): ")
tempSensor = tempSensors()

try:
    while True:
            if sensor == "HLT" or sensor == "All": print("HLT Temp: {}".format(tempSensor.HLTTemp()))
            if sensor == "MLT" or sensor == "All": print("MLT Temp: {}".format(tempSensor.MLTTemp()))
            if sensor == "BLK" or sensor == "All": print("BLK Temp: {}".format(tempSensor.BLKTemp()))
            if sensor == "All": print("")
            if not(sensor == "HLT") and not(sensor=="MLT") and not(sensor=="BLK") and not(sensor=="All"):
                    print("Error: temp sensor was not valid")
                    sys.exit()
            time.sleep(2)
except KeyboardInterrupt: print("\nEnding temperature sensor test")
    
