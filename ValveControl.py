import time
from MCP23017 import MCP23017

class ValveController(object):
    @property
    def valveStates(self):
        return self._valveStates

    #whenever you set a valve state, then set the appropriate pins on the MCP23017
    #Note that the pins are set to low for open, so it is the opposite value
    @valveStates.setter
    def valveStates(self,states):
        if len(states)==10:
            for i in range(0,10):
                if self.partiallyOpen[i]:print("Warning: Valve {} is partially open; to change it to open or closed, use fullyOpenClose".format(i+1))
                if states[i]==1 or states[i]==0:
                    self._valveStates[i]=states[i]
                    if states[i] == 1: self.mcp.output(self.valvePositivePins[i],0)
                    elif states[i] == 0: self.mcp.output(self.valvePositivePins[i],1)
                else:
                    print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(i+1))
        else: print("Error: valveStates is not 10 elements; not updating valve states")

    @property
    def valve1(self):
        return self.valveStates[0]

    @valve1.setter
    def valve1(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[0] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(1))

    @property
    def valve2(self):
        return self.valveStates[1]

    @valve2.setter
    def valve2(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[1] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(2))

    @property
    def valve3(self):
        return self.valveStates[2]

    @valve3.setter
    def valve3(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[2] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(3))

    @property
    def valve4(self):
        return self.valveStates[3]

    @valve4.setter
    def valve4(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[3] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(4))

    @property
    def valve5(self):
        return self.valveStates[4]

    @valve5.setter
    def valve5(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[4] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(5))

    @property
    def valve6(self):
        return self.valveStates[5]

    @valve6.setter
    def valve6(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[5] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(6))

    @property
    def valve7(self):
        return self.valveStates[6]

    @valve7.setter
    def valve7(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[6] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(7))

    @property
    def valve8(self):
        return self.valveStates[7]

    @valve8.setter
    def valve8(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[7] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(8))

    @property
    def valve9(self):
        return self.valveStates[8]

    @valve9.setter
    def valve9(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[8] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(9))

    @property
    def valve10(self):
        return self.valveStates[9]

    @valve10.setter
    def valve10(self,value):
        if value==1 or value==0:
            newStates = self.valveStates
            newStates[9] = value
            self.valveStates = newStates
        else: print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(10))

    def partialOpenClose(self,valve,amount):
        if self.valveNeutralPins[valve-1] != None:
            if amount>=0:
                #It takes less than valveOpenTime seconds to fully open the valve, so limits the amount to the valveOpenTime (default 5 secs)
                if amount>self.valveOpenTime:
                    amount = self.valveOpenTime
                    print("It takes less than {1} seconds to fully open the valve, so setting amount to {1}".format(self.valveOpenTime))

                #Begins opening the valve
                self.mcp.output(self.valvePositivePins[valve-1],0)
                self.mcp.output(self.valveNeutralPins[valve-1],1)
                
                #waits amount seconds before turning off the neutral
                time.sleep(amount)

                #turns off the neutral pin
                self.mcp.output(self.valveNeutralPins[valve-1],0)


                #Stores the fact that the valve is partially open
                self.partiallyOpen[valve-1] = 1

            else:
                #It takes less than valveOpenTime seconds to fully open the valve, so limits the amount to the valveOpenTime (default 5 secs)
                #Since amount is negative, partially closes the valve
                if amount<-self.valveOpenTime:
                    amount = self.valveOpenTime
                    print("It takes less than {1} seconds to fully open the valve, so setting amount to {1}".format(self.valveOpenTime))
                else: amount = -amount

                #Begins closing the valve
                self.mcp.output(self.valvePositivePins[valve-1],1)
                self.mcp.output(self.valveNeutralPins[valve-1],1)

                #waits amount seconds before turning off the neutral
                time.sleep(amount)

                #turns off the neutral pin
                self.mcp.output(self.valveNeutralPins[valve-1],0)

                #Stores the fact that the valve is partially open
                self.partiallyOpen[valve-1] = 1
        else: print("Error: Valve {} does not have neutral control, so it cannot be partially opened/closed".format(valve))

    def fullyOpenClose(self,valve,state):
        if self.valveNeutralPins[valve-1] != None:
            if state==1 or state==0:
                self.mcp.output(self.valveNeutralPins[valve-1],1)
                self.partiallyOpen[valve-1] = 0
                newStates = self.valveStates
                newStates[valve-1] = state
                self.valveStates = newStates
                
            else:print("Error: Valve {} must be set to either  1 (open) or 0 (closed)".format(valve))
            
        else: print("Error: Valve {} does not have neutral control, so it cannot be partially opened/closed".format(valve))
            
            

    def __init__(self,valvePositivePins = [8,9,10,11,12,13,14,15,7,6],valveNeutralPins = [None,None,None,None,5,None,None,None,4,None],address = 0x20,valveOpenTime=5):
        #Stores the parameters
        self.valvePositivePins = valvePositivePins
        self.valveNeutralPins = valveNeutralPins
        self.address = address
        self.valveOpenTime = valveOpenTime        

        #Creates the MCP23017 object
        self.mcp = MCP23017(address = address, num_gpios = 16)

        #Initializes the pins, with all the valves closed and neutral connected (note that neutral is normally closed)
        for i in range(0,10):
            self.mcp.pinMode(self.valvePositivePins[i],self.mcp.OUTPUT)
            self.mcp.output(self.valvePositivePins[i],1)
            if self.valveNeutralPins[i] != None:
                self.mcp.pinMode(self.valveNeutralPins[i],self.mcp.OUTPUT)
                self.mcp.output(self.valveNeutralPins[i],1)

        self._valveStates =[0]*10
        self.partiallyOpen = [0]*10
