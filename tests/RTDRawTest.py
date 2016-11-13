import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import time
from automatedbrewery.RTDSensor import max31865
from automatedbrewery.MCP23017 import MCP23017

sensor = input(">>Enter temp sensor to test (HLT,MLT, or BLK): ")

if sensor == "HLT":
        csPin = 6
        misoPin = 7
        mosiPin = 4
        clkPin = 5
elif sensor == "MLT":
        csPin = 12
        misoPin = 11
        mosiPin = 8
        clkPin = 9
elif sensor == "BLK":
        csPin = 10
        misoPin = 11
        mosiPin = 8
        clkPin = 9
else:
        print("Error: temp sensor was not valid")
        sys.exit()
        
mcp = MCP23017(address = 0x23, num_gpios = 16)
tempSensor = max31865(mcp,csPin,misoPin,mosiPin,clkPin)
try:
        while True:
                temp = tempSensor.readTemp()
                print(temp)
                time.sleep(2)
except KeyboardInterrupt:
        print("\nEnding temperature sensor test")
