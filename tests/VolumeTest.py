import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.VolumeSensor import volumeSensors
import time

sensor = input(">>Enter temp sensor to test (HLT,MLT,BLK, or All): ")
volumeSensor = volumeSensors()

try:
    while True:
            if sensor == "HLT" or sensor == "All": print("HLT Volume: {}".format(volumeSensor.HLTVolume()))
            if sensor == "MLT" or sensor == "All": print("MLT Volume: {}".format(volumeSensor.MLTVolume()))
            if sensor == "BLK" or sensor == "All": print("BLK Volume: {}".format(volumeSensor.BLKVolume()))
            if sensor == "All": print("")
            if not(sensor == "HLT") and not(sensor=="MLT") and not(sensor=="BLK") and not(sensor=="All"):
                    print("Error: Volume sensor was not valid")
                    sys.exit()
            time.sleep(2)
except KeyboardInterrupt: print("\nEnding volume sensor test")
