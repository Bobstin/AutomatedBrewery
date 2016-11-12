import time
from MCP23017 import MCP23017
import RPi.GPIO as GPIO

class valveSwitchSensors(object):
    def __init__(self, mcp2Address = 0x22,mcp3Address = 0x21,In1Pins_2 = [8,10,12,14,7,5,3,1],In2Pins_2 = [9,11,13,15,6,4,2,0],In1Pins_3 = [6,5],In2Pins_3 = [7,4],interrupt2Pin = 13, interrupt3Pin = 19):
        #stores the inpins
        self.In1Pins_2 = In1Pins_2
        self.In2Pins_2 = In2Pins_2
        self.In1Pins_3 = In1Pins_3
        self.In2Pins_3 = In2Pins_3
        self.interrupt2Pin = interrupt2Pin
        self.interrupt3Pin = interrupt3Pin

        #sets up the MCP23017s, including turning on the mirrored interrupts
        self.mcp2 = MCP23017(address = mcp2Address, num_gpios = 16)
        self.mcp2.configSystemInterrupt(self.mcp2.INTMIRRORON, self.mcp2.INTPOLACTIVEHIGH)

        self.mcp3 = MCP23017(address = mcp3Address, num_gpios = 16)
        self.mcp3.configSystemInterrupt(self.mcp3.INTMIRRORON, self.mcp3.INTPOLACTIVEHIGH)

        #sets the pins to inputs, configures them to initiate an interrupt when changes, and pulls up the 2nd pins
        for i in range(0,15):
            self.mcp2.pinMode(i,self.mcp2.INPUT)
            self.mcp2.configPinInterrupt(i, self.mcp2.INTERRUPTON, self.mcp2.INTERRUPTCOMPAREPREVIOUS)
            #if i in self.In2Pins_2:
            self.mcp2.pullUp(i,1)

        #sets up the valves on mcp3
        for i in range(4,8):
            self.mcp3.pinMode(i,self.mcp3.INPUT)
            self.mcp3.configPinInterrupt(i, self.mcp3.INTERRUPTON, self.mcp3.INTERRUPTCOMPAREPREVIOUS)
            #if i in In2Pins_3:
            self.mcp3.pullUp(i,1)

    def interruptSetUp(self,callbackFunction,bounceTime=50):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.interrupt2Pin,GPIO.IN)
        GPIO.setup(self.interrupt3Pin,GPIO.IN)
        
        GPIO.add_event_detect(self.interrupt2Pin, GPIO.RISING, callback=callbackFunction, bouncetime=bounceTime)
        GPIO.add_event_detect(self.interrupt3Pin, GPIO.RISING, callback=callbackFunction, bouncetime=bounceTime)

    def allValveSwitchStates(self, bounceTime=0.05):
        #Unless it can get a good valve state, assumes that there is an error
        valvestate=["ERROR"]*10
        
        #Waits some time to handle debouncing (default is 50 ms)
        time.sleep(bounceTime)
 
        #Valve is off if both pins are high, auto if pin one is low and pin two is high, and on if pin one is high and pin two is low
        #Both pins should never be low, so if that is the state, then set the value to error
        
        #gets the valve state for the first 8 valves 
        for i in range(0,8):
            if self.mcp2.input(self.In1Pins_2[i]) and self.mcp2.input(self.In2Pins_2[i]): valvestate[i]="Off"
            if not(self.mcp2.input(self.In1Pins_2[i])) and self.mcp2.input(self.In2Pins_2[i]): valvestate[i]="Auto"
            if self.mcp2.input(self.In1Pins_2[i]) and not(self.mcp2.input(self.In2Pins_2[i])): valvestate[i]="On"
            if not(self.mcp2.input(self.In1Pins_2[i])) and not(self.mcp2.input(self.In2Pins_2[i])): valvestate[i]="ERROR"

        #gets the valve state for the remaining 2 valves
        for i in range(0,2):
            if self.mcp3.input(self.In1Pins_3[i]) and self.mcp3.input(self.In2Pins_3[i]):  valvestate[i+8]="Off"
            if not(self.mcp3.input(self.In1Pins_3[i])) and self.mcp3.input(self.In2Pins_3[i]):  valvestate[i+8]="Auto"
            if self.mcp3.input(self.In1Pins_3[i]) and not(self.mcp3.input(self.In2Pins_3[i])):  valvestate[i+8]="On"
            if not(self.mcp3.input(self.In1Pins_3[i])) and not(self.mcp3.input(self.In2Pins_3[i])):  valvestate[i+8]="ERROR"

        #clears the interrupts - assumes that whenever the interrupt happens, this is called in some form
        self.mcp2.clearInterrupts()
        self.mcp3.clearInterrupts()

        return valvestate

    def valveSwitchState(self, valveSwitch):
        #This is used if you only want the value of one of the valve switches
        allValveSwitches = self.allValveSwitchStates()
        return allValveSwitches[valveSwitch-1]

        
