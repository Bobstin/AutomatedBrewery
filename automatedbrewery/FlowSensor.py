import RPi.GPIO as GPIO
import time
import sys
import pickle

class flowSensors(object):
    def __init__(self,graphSignal,flowPins = [8,7,12,16,20,21],flowNames = ["HLT In","HLT Out","MLT In","MLT Out","BLK In","BLK Out"],sendSeries=True,inputPipe=None):
        #stores the parameters
        self.flowPins = flowPins
        self.flowNames = flowNames
        self.graphSignal = graphSignal
        self.sendSeries = sendSeries
        self.inputPipe = inputPipe
        
        #Sets up the pins as inputs with detection events
        GPIO.setmode(GPIO.BCM)        
        for i in range(0,6):
            GPIO.setup(flowPins[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)
            GPIO.add_event_detect(flowPins[i], GPIO.FALLING, callback=self.countPulse)

        #Sets up variables to store the counts in
        self.counts=[0]*6
        self.totalCounts = [0]*3

        #Sets up variable to store the graph information in (six x,y lists)
        self.rates=[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
        self.totals=[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]

        #defaults the sensor to keep sensing
        self.turnOffSensor = False

        #imports the calibration parameters
        with open('../calibrations/FlowCalibration.pk1','rb') as FlowCalibration:
            self.calibration = pickle.load(FlowCalibration)

        #starts counting
        self.startTime=time.time()
        self.run()

    def countPulse(self,pin):
        index = self.flowPins.index(pin)
        self.counts[index] += 1

        #counts against the total flow if it is out, and with if it is in
        if index in [0,2,4]: self.totalCounts[int(index/2)] += 1
        else: self.totalCounts[int((index-1)/2)] -= 1


    def run(self):
                while self.turnOffSensor == False:
                    self.lastRun = time.time()
                    time.sleep(1)

                    for i in range(0,6):
                        #For rates, append the counts divided by the time since the last run (multiplies by 60 since rate is in gal/min)
                        self.rates[i][1].append(self.counts[i]*self.calibration[i]/(time.time()-self.lastRun)*60)
                        
                        #Add the time that the data was collected
                        self.rates[i][0].append(time.time()-self.startTime)

                        if i<=2:
                            #For totals, just append the total counts
                            self.totals[i][1].append(self.totalCounts[i]*self.calibration[i])
                            self.totals[i][0].append(time.time()-self.startTime)

                    #resets the counts
                    self.counts=[0]*6

                    #send the data to the UI
                    self.graphSignal.emit(self.rates,self.totals)

                    #checks the pipe for an instruction (mostly used to turn the sensor off)
                    if self.inputPipe != None:
                        #print("checking pipe")
                        while self.inputPipe.poll():
                            data = self.inputPipe.recv()
                            #print(data)
                            setattr(self,data[0],data[1])

        

        

        
