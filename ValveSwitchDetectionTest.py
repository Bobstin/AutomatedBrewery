import time
from MCP23017 import MCP23017

#Sets up the mcps to control the valves
mcp2 = MCP23017(address = 0x22, num_gpios = 16)
mcp3 = MCP23017(address = 0x21, num_gpios = 16)

#InxPins_y represents the xth set of input pins on mcp y
In1Pins_2 = [8,10,12,14,7,5,3,1]
In2Pins_2 = [9,11,13,15,6,4,2,0]
In1Pins_3 = [6,5]
In2Pins_3 = [7,4]

valvestate=[]

#sets up the valves on mcp2
for i in range(0,15):
    mcp2.pinMode(i,mcp2.INPUT)
    #if i in In2Pins_2:
    mcp2.pullUp(i,1)

#sets up the valves on mcp3
for i in range(4,8):
    mcp3.pinMode(i,mcp3.INPUT)
    if i in In2Pins_3:
        mcp3.pullUp(i,1)
while True:        
    #gets the valve state for the first 8 valves 
    for i in range(0,8):
        if mcp2.input(In1Pins_2[i]) and mcp2.input(In2Pins_2[i]): valvestate.append("Off")
        if not(mcp2.input(In1Pins_2[i])) and mcp2.input(In2Pins_2[i]): valvestate.append("Auto")
        if mcp2.input(In1Pins_2[i]) and not(mcp2.input(In2Pins_2[i])): valvestate.append("On")
        if not(mcp2.input(In1Pins_2[i])) and not(mcp2.input(In2Pins_2[i])): valvestate.append("ERROR")

    #gets the valve state for the remaining 2 valves
    for i in range(0,2):
        if mcp3.input(In1Pins_3[i]) and mcp3.input(In2Pins_3[i]): valvestate.append("Off")
        if not(mcp3.input(In1Pins_3[i])) and mcp3.input(In2Pins_3[i]): valvestate.append("Auto")
        if mcp3.input(In1Pins_3[i]) and not(mcp3.input(In2Pins_3[i])): valvestate.append("On")
        if not(mcp3.input(In1Pins_3[i])) and not(mcp3.input(In2Pins_3[i])): valvestate.append("ERROR")

    print(valvestate)
    valvestate=[]
    time.sleep(2)

    
