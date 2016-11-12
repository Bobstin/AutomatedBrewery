import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import time
import RPi.GPIO as GPIO
from automatedbrewery.MCP23017 import MCP23017

address = 0x20
valvePositivePins = [8,9,10,11,12,13,14,15,7,6]
valveNeutralPins = [None,None,None,None,5,None,None,None,4,None]
pumpAerationPins = [3,2,1]
pumpAerationLabels = ["Wort Pump","Water Pump","Aeration"]

#Sets up the MCP and the pins
mcp = MCP23017(address = address, num_gpios = 16)
for i in range(0,10):
    mcp.pinMode(valvePositivePins[i],mcp.OUTPUT)
    mcp.output(valvePositivePins[i],1)
    if valveNeutralPins[i] != None:
        mcp.pinMode(valveNeutralPins[i],mcp.OUTPUT)
        mcp.output(valveNeutralPins[i],1)

for i in range(0,3):
    mcp.pinMode(pumpAerationPins[i],mcp.OUTPUT)
    mcp.output(pumpAerationPins[i],1)


print("Testing the valves. Should start with all valve closed for 5 seconds,")
print("then all valves open for 5 seconds, then all closed again for 5 seconds")
print("This is followed by the opening of each valve in order, two seconds apart")
print("Then all valves are turned off\n")

#Note that low on the pin is valve open
for i in range(0,10): mcp.output(valvePositivePins[i],1)
time.sleep(5)
for i in range(0,10): mcp.output(valvePositivePins[i],0)
time.sleep(5)
for i in range(0,10): mcp.output(valvePositivePins[i],1)
time.sleep(5)
for i in range(0,10):
    mcp.output(valvePositivePins[i],0)
    time.sleep(2)
for i in range(0,10): mcp.output(valvePositivePins[i],1)

time.sleep(2)
print("Testing the ability to partially open valves 5 and 9.")
print("Both valves will be closed for 5 seconds, then valve 5 will be partially")
print("opened, then fully opened, followed by the same pattern for valve 9.")
print("Then they will be partially closed, followed by fully closed\n")

#Note that python indexes from 0, so the indices are one lower
for i in [4,8]:mcp.output(valvePositivePins[i],1)
time.sleep(5)

#Partial then full open of 5
mcp.output(valvePositivePins[4],0)
time.sleep(2)
mcp.output(valveNeutralPins[4],0)
time.sleep(2)
mcp.output(valveNeutralPins[4],1)
time.sleep(2)

#Partial then full open of 9
mcp.output(valvePositivePins[8],0)
time.sleep(2)
mcp.output(valveNeutralPins[8],0)
time.sleep(2)
mcp.output(valveNeutralPins[8],1)
time.sleep(2)

#Partial then full close of 5
mcp.output(valvePositivePins[4],1)
time.sleep(2)
mcp.output(valveNeutralPins[4],0)
time.sleep(2)
mcp.output(valveNeutralPins[4],1)
time.sleep(2)

#Partial then full close of 9
mcp.output(valvePositivePins[8],1)
time.sleep(2)
mcp.output(valveNeutralPins[8],0)
time.sleep(2)
mcp.output(valveNeutralPins[8],1)
time.sleep(2)


print("Testing the pumps and aeration. Should start with all off for 5 seconds,")
print("then all on for 5 seconds, then all off again for 5 seconds")
print("This is followed by the turning on of the Wort Pump, then the")
print("Water pump, then Aeration, two seconds apart")
print("Then all are turned off\n")
#Note that low on the pin is on
for i in range(0,3): mcp.output(pumpAerationPins[i],1)
time.sleep(5)
for i in range(0,3): mcp.output(pumpAerationPins[i],0)
time.sleep(5)
for i in range(0,3): mcp.output(pumpAerationPins[i],1)
time.sleep(5)
for i in range(0,3):
    mcp.output(pumpAerationPins[i],0)
    time.sleep(2)

print("Test complete!")

mcp.cleanup()
