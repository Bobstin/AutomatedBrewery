import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Pipe, Event
import RTD
import PID
import AutomatedBreweryUI
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph

class HeatControl(object):
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
        elif value == "MLT":
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
            print("Error: kettle must be set to either MLT or BLK. Turning off the heat")

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

    def __init__(self, relay1Pin = 2, relay2Pin = 14, SSR1Pin = 3, SSR2Pin=15, heatSetting=0, cycleTime=2000, maxSetting=100, minSetting=0, pipeConn=None, heatGraphInConn=None, updateGraph=None):
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
        self.pipeConn = pipeConn

        #If you want to update an external graph, you can pass a connection, as well as an event to trigger the update
        self.heatGraphInConn = heatGraphInConn
        self.updateGraph = updateGraph

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
        if self.pipeConn.poll():
            data = self.pipeConn.recv()
            setattr(self,data[0],data[1])

    def sendGraphPoint(self):
        self.heatGraphInConn.send((self.heatSetting, time.time()*1000))
        if self.updateGraph != None:
            self.updateGraph.set()
        

    def run(self):
        while (self.kettle != "None"):
            if self.kettle == "MLT":
                self.SSR1 = 1
                time.sleep(self.onTime/1000)
                self.SSR1 = 0
                time.sleep(self.offTime/1000)
                if self.pipeConn != None: self.checkPipe()
                if self.heatGraphInConn != None: self.sendGraphPoint()
            elif self.kettle == "BLK":
                self.SSR2 = 1
                time.sleep(self.onTime/1000)
                self.SSR2 = 0
                time.sleep(self.offTime/1000)
                if self.pipeConn != None: self.checkPipe()
                if self.heatGraphInConn != None: self.sendGraphPoint()
        
def startHeatControl(heatConn,heatGraphInConn,updateGraph):
    HeatCtrl = HeatControl(pipeConn=heatConn, heatGraphInConn=heatGraphInConn, updateGraph=updateGraph)
    time.sleep(2)
    HeatCtrl.heatSetting = 50
    HeatCtrl.kettle = "MLT"

def startPID(PIDConn,tempGraphInConn,updateGraph):
    #Sets up the RTD
    cs_pin = 8
    clock_pin = 11
    data_in_pin = 9
    data_out_pin = 10
    rtd = RTD.MAX31865(cs_pin, clock_pin, data_in_pin, data_out_pin, units='f')

    time.sleep(5)
    #Sets up the PID
    inputSource = rtd
    inputAttributeName = 'temp'
    pid = PID.PID(inputSource,inputAttributeName)
    pid.outputPipeConn = PIDConn
    pid.outputMin = 0
    pid.outputMax = 100
    pid.cycleTime = 2000
    pid.semiAutoValue = 10
    pid.outputAttributeName = 'heatSetting'
    pid.mode = 'SemiAuto'
    pid.tempGraphInConn = tempGraphInConn
    pid.updateGraph = updateGraph
    pid.run()

def startUI(tempGraphOutConn,heatGraphOutConn,updateGraph):
    #creates the UI
    app = QtWidgets.QApplication(sys.argv)
    window = AutomatedBreweryUI.MyApp()
    

    #graphs start empty
    tempx = []
    tempy = []
    heatx = []
    heaty = []
    #now = time.time()
    #updateGraph.wait()
    #updateGraph.clear()

    #while True:
        #print(time.time()-now)
       # now = time.time()
        #updateGraph.wait()
        #updateGraph.clear()

    #print("Got Here!")
    #window.graph1.plot(tempx,tempy,clear=True)
    
    #while True:
        #wait until something says to update the graphs
        #updateGraph.wait()

        #check if there are new data points, and if there are, append them
        #if tempGraphOutConn.poll():
           # newTempPoint = tempGraphOutConn.recv()
            #tempx = [tempx,newTempPoint[0]]
            #tempy = [tempy,newTempPoint[1]]
                     
       # if heatGraphOutConn.poll():
            #newHeatPoint = heatGraphOutConn.recv()
            #heatx = [heatx,newHeatPoint[0]]
            #heaty = [heaty,newHeatPoint[1]]

        #update the graphs
        #print(tempx)
       # print(tempy)
        #print(heatx)
        #print(heaty)
        #window.graph1.plot(tempx,tempy,clear=True)
        #window.graph2.plot(heatx,heaty,clear=True)

        #reset the flag
        #updateGraph.clear()
    sys.exit(app.exec_())

    
    

    

if __name__ == '__main__':
    GPIO.setwarnings(False)
    heatConn, PIDConn = Pipe()
    tempGraphInConn, tempGraphOutConn = Pipe()
    heatGraphInConn, heatGraphOutConn = Pipe()

    updateGraph = Event()
    
    heatProcess = Process(target = startHeatControl, args=(heatConn,heatGraphInConn,updateGraph))
    PIDProcess = Process(target = startPID, args=(PIDConn,tempGraphInConn,updateGraph))
    UIProcess = Process(target = startUI, args=(tempGraphOutConn,heatGraphOutConn,updateGraph))
    heatProcess.start()
    PIDProcess.start()
    UIProcess.start()


    
    heatProcess.join()
    PIDProcess.join()


        
