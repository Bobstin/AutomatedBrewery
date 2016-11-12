import time
from MCP23017 import MCP23017
import RPi.GPIO as GPIO

def getvalvestate(IGNORE):        
    valvestate=["ERROR"]*10

    time.sleep(0.05)
    
    #gets the valve state for the first 8 valves 
    for i in range(0,8):
        if mcp2.input(In1Pins_2[i]) and mcp2.input(In2Pins_2[i]): valvestate[i]="Off"
        if not(mcp2.input(In1Pins_2[i])) and mcp2.input(In2Pins_2[i]): valvestate[i]="Auto"
        if mcp2.input(In1Pins_2[i]) and not(mcp2.input(In2Pins_2[i])): valvestate[i]="On"
        if not(mcp2.input(In1Pins_2[i])) and not(mcp2.input(In2Pins_2[i])): valvestate[i]="ERROR"

    #gets the valve state for the remaining 2 valves
    for i in range(0,2):
        if mcp3.input(In1Pins_3[i]) and mcp3.input(In2Pins_3[i]):  valvestate[i+8]="Off"
        if not(mcp3.input(In1Pins_3[i])) and mcp3.input(In2Pins_3[i]):  valvestate[i+8]="Auto"
        if mcp3.input(In1Pins_3[i]) and not(mcp3.input(In2Pins_3[i])):  valvestate[i+8]="On"
        if not(mcp3.input(In1Pins_3[i])) and not(mcp3.input(In2Pins_3[i])):  valvestate[i+8]="ERROR"

    mcp2.clearInterrupts()
    mcp3.clearInterrupts()
    print(valvestate)
    return valvestate

try:
    print("Testing detection of valve switches. Should display current switch positions,")
    print("then display new positions any time a switch is flipped")

    #Sets up the GPIO for the interrupts
    GPIO.setmode(GPIO.BCM)

    #Sets up the mcps to control the valves
    mcp2 = MCP23017(address = 0x22, num_gpios = 16)
    mcp2.configSystemInterrupt(mcp2.INTMIRRORON, mcp2.INTPOLACTIVEHIGH)

    mcp3 = MCP23017(address = 0x21, num_gpios = 16)
    mcp3.configSystemInterrupt(mcp3.INTMIRRORON, mcp3.INTPOLACTIVEHIGH)

    #InxPins_y represents the xth set of input pins on mcp y
    In1Pins_2 = [8,10,12,14,7,5,3,1]
    In2Pins_2 = [9,11,13,15,6,4,2,0]
    In1Pins_3 = [6,5]
    In2Pins_3 = [7,4]


    #sets up the valves on mcp2
    for i in range(0,15):
        mcp2.pinMode(i,mcp2.INPUT)
        mcp2.configPinInterrupt(i, mcp2.INTERRUPTON, mcp2.INTERRUPTCOMPAREPREVIOUS)
        if i in In2Pins_2:
            mcp2.pullUp(i,1)

    #sets up the valves on mcp3
    for i in range(4,8):
        mcp3.pinMode(i,mcp3.INPUT)
        mcp3.configPinInterrupt(i, mcp3.INTERRUPTON, mcp3.INTERRUPTCOMPAREPREVIOUS)
        if i in In2Pins_3:
            mcp3.pullUp(i,1)


    #GPIO.add_interrupt_callback(13, interrupted, edge='rising', pull_up_down=GPIO.PUD_DOWN, threaded_callback=Fasle, debounce_timeout_ms=5)
    GPIO.setup(13,GPIO.IN)
    GPIO.setup(19,GPIO.IN)
    GPIO.add_event_detect(13, GPIO.RISING, callback=getvalvestate, bouncetime=50)
    GPIO.add_event_detect(19, GPIO.RISING, callback=getvalvestate, bouncetime=50)

    getvalvestate(0)

    while True:
        time.sleep(2)
        #print(getvalvestate())
except KeyboardInterrupt: print("\nEnding valve switch detection test")
    
