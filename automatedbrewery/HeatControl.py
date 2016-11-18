import RPi.GPIO as GPIO
#from EmulatorGUI import GPIO
import time
import sys

class HeatController(object):
    @property
    def relay1(self):
        return self._relay1

    #whenever you set a relay to a value, then set the appropriate pin in the GPIO
    @relay1.setter
    def relay1(self,value):
        if (value == 1)|(value == 0):
            self._relay1 = value
            if value == 1:
                GPIO.output(self.relay1Pin,self.relayOn)
            elif value == 0:
                GPIO.output(self.relay1Pin,self.relayOff)
        else:
            print("Error: relay must be set to either 1 (on) or 0 (off). Not changing relay setting")


    @property
    def relay2(self):
        return self._relay2

    #whenever you set a relay to a value, then set the appropriate pin in the GPIO
    @relay2.setter
    def relay2(self,value):
        if (value == 1)|(value == 0):
            self._relay2 = value
            if value == 1:
                GPIO.output(self.relay2Pin,self.relayOn)
            elif value == 0:
                GPIO.output(self.relay2Pin,self.relayOff)
        else:
            print("Error: relay must be set to either 1 (on) or 0 (off). Not changing relay setting")


    @property
    def SSR1(self):
        return self._SSR1

    #whenever you set a relay to a value, then set the appropriate pin in the GPIO
    @SSR1.setter
    def SSR1(self,value):
        if (value == 1)|(value == 0):
            self._SSR1 = value
            if value == 1:
                GPIO.output(self.SSR1Pin,self.SSROn)
            elif value == 0:
                GPIO.output(self.SSR1Pin,self.SSROff)
        else:
            print("Error: relay must be set to either 1 (on) or 0 (off). Not changing relay setting")


    @property
    def SSR2(self):
        return self._SSR2

    #whenever you set a relay to a value, then set the appropriate pin in the GPIO
    @SSR2.setter
    def SSR2(self,value):
        if (value == 1)|(value == 0):
            self._SSR2 = value
            if value == 1:
                GPIO.output(self.SSR2Pin,self.SSROn)
            elif value == 0:
                GPIO.output(self.SSR2Pin,self.SSROff)
        else:
            print("Error: relay must be set to either 1 (on) or 0 (off). Not changing relay setting")

    #when you set a kettle, set the relays appropriately, and start the heating loop
    @property
    def kettle(self):
        return self._kettle

    @kettle.setter
    def kettle(self,value):
        if value == "None":
            self._kettle = value
            self.relay1 = 0
            self.relay2 = 0
            self.SSR1 = 0
            self.SSR2 = 0
        elif value == "HLT":
            #note that this turns off the other relay before opening the correct relay. It should be impossible
            #to heat both kettles simultaniously (relays are in series), but this is precautionary
            #(as is turning off the other SSR)
            #Note that this also turns off the SSR for the kettle, but it will be turned on in the run loop
            self._kettle = value
            self.relay2 = 0
            self.SSR2 = 0
            self.SSR1 = 0
            self.relay1 = 1
            self.run()
        elif value == "BLK":
            self._kettle = value
            self.relay1 = 0
            self.SSR1 = 0
            self.SSR2 = 0
            self.relay2 = 1
            self.run()
        else:
            self.relay1 = 0
            self.relay2 = 0
            self.SSR1 = 0
            self.SSR2 = 0
            print("Error: kettle must be set to either HLT or BLK. Turning off the heat")

    @property
    def heatSetting(self):
        return self._heatSetting

    @heatSetting.setter
    def heatSetting(self,value):
        #when you set the heatSetting, check that it is in range, and calculate the onTime and offTime (to reduce
        #calculations when it is running)
        if (value<self.minSetting)|(value>self.maxSetting):
            print("Error: setting is outside of range (check minSetting and maxSetting). Not changing setting")
        else:
            self._heatSetting = value
            self.calcOnOffTime()

    @property
    def cycleTime(self):
        return self._cycleTime

    @cycleTime.setter
    def cycleTime(self,value):
        if value<=0:
            print("Error: cycleTime is outside of range (must be >0). Not changing cycleTime")
        else:
            self._cycleTime = value
            self.calcOnOffTime()

    def __init__(self, relay1Pin = 14, relay2Pin = 15, SSR1Pin = 18, SSR2Pin=23, heatSetting=0, cycleTime=2000, maxSetting=100, minSetting=0, pipeConn=None, pipeConn2=None,pipeConn3=None, heatGraphSignal=None):
        #Note that for the relays, 0 is on, but for the SSR, 1 is on, however this is handled on the backend
        #just set the relay/ssr to the right status
        self.relayOn = 0
        self.relayOff = 1
        self.SSROn = 1
        self.SSROff = 0

        self.relay1Pin = relay1Pin
        self.relay2Pin = relay2Pin
        self.SSR1Pin = SSR1Pin
        self.SSR2Pin = SSR2Pin

        #If you want to access the control from a different process, you can pass a pipe connection that it will
        #check during run() to adjust parameters
        #Allows for two connections; one from the HLT and one from the BLK PID
        self.pipeConn = pipeConn
        self.pipeConn2= pipeConn2
        self.pipeConn3= pipeConn3

        #If you want to update an external graph, you can pass a signal
        self.heatGraphSignal = heatGraphSignal

        #Setup the GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.relay1Pin, GPIO.OUT)
        GPIO.setup(self.relay2Pin, GPIO.OUT)
        GPIO.setup(self.SSR1Pin, GPIO.OUT)
        GPIO.setup(self.SSR2Pin, GPIO.OUT)     

        self.maxSetting = maxSetting
        self.minSetting = minSetting
        self._cycleTime = cycleTime
        self.heatSetting = heatSetting
        self.cycleTime = cycleTime
        self.kettle = "None"


        #Set everything to off intially
        self.relay1 = 0
        self.relay2 = 0
        self.SSR1 = 0
        self.SSR2 = 0

        #Set onTime and offTime
        self.calcOnOffTime()

    def calcOnOffTime(self):
        self.onTime = (self.heatSetting/100)*self.cycleTime
        self.offTime = (1-self.heatSetting/100)*self.cycleTime

    def checkPipe(self):
        #print("Checking pipe")
        if self.pipeConn != None:
            while self.pipeConn.poll():
                data = self.pipeConn.recv()
                #print("Pipe 1:")
                #print(data)
                setattr(self,data[0],data[1])
        if self.pipeConn2 != None:
            while self.pipeConn2.poll():
                data = self.pipeConn2.recv()
                #print("Pipe 2:")
                #print(data)
                setattr(self,data[0],data[1])
        if self.pipeConn3 != None:
            while self.pipeConn3.poll():
                data = self.pipeConn3.recv()
                #print("Pipe 3:")
                #print(data)
                setattr(self,data[0],data[1])

    def sendGraphPoint(self):
        self.heatGraphSignal.emit(time.time()*1000, self.heatSetting, self.kettle)
        

    def run(self):
        #if onTime or offTime = 0, then does not switch the relay. This reduces the number of
        #switches, as well as any delay due to code execution
        
        while True:
            if self.kettle == "HLT":
                if self.onTime!=0:
                    self.SSR1 = 1
                    time.sleep(self.onTime/1000)
                if self.offTime !=0:
                    self.SSR1 = 0
                    time.sleep(self.offTime/1000)
                self.checkPipe()
                if self.heatGraphSignal != None: self.sendGraphPoint()
            elif self.kettle == "BLK":
                if self.onTime!=0:
                    self.SSR2 = 1
                    time.sleep(self.onTime/1000)
                if self.offTime !=0:
                    self.SSR2 = 0
                    time.sleep(self.offTime/1000)
                self.checkPipe()
                if self.heatGraphSignal != None: self.sendGraphPoint()
            elif self.kettle == "None":
                self.checkPipe()
                time.sleep(2)
        






    
    


        
