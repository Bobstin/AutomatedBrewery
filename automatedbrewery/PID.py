import time
import numpy
#Based heavily on the Arduino PID library by Brett Beauregard

# By default, looks for an attribute called value for the input, and setting for the output
# If you want to change that, then you can change the input/outputAttributeName
# Input source must be available when PID is initialized to get the starting value
# assumes that the output device is regularly checking a pipe to get the next value to go to
class PID(object):
        def __init__(self,inputSource,inputAttributeName='value'):
                #creates placeholders for the PID values. These are allowed to be empty, but run() will
                #check if they are filled, and fail if they are not
                self.setPoint = None
                self.Kp = None
                self.Ki = None
                self.Kd = None
                self.outputPipeConn = None
                self.outputMin = None
                self.outputMax = None
                self.output = None
                self.cycleTime = None
                self.semiAutoValue = None
                self.inputPipeConn = None
                self.tempGraphSignal = None
                self.messageSignal = None

                self.inputSource = inputSource
                self.outputAttributeName = 'setting'
                self.inputAttributeName = inputAttributeName
                self.lastInput = getattr(self.inputSource,self.inputAttributeName)
                if self.lastInput == None: raise ValueError('Unable to get input value. Check inputSource and inputAttributeName')


                self.lastRun = time.time()*1000
                self.integralWindupBlocker = False
                self.integralTerm = 0

                self._mode = 'Auto'
                self.stop = 0
                self.nextCycleStart =time.time()*1000

                self.sentOffSignal = False
                


        @property
        def mode(self):
                return self._mode

        @mode.setter
        def mode(self, value):
                if (value == 'Auto') | (value == 'SemiAuto') | (value == 'Off'):
                        #If switching to Auto from another mode, reset the last input value
                        #If switching from SemiAuto to Auto, set the integral term to SemiAuto so
                        #the PID maintains that value
                        #If switching from Off to Auto, reset the integral term so it doesn't overshoot
                        if value == 'Auto':
                                self.lastInput = getattr(self.inputSource,self.inputAttributeName)
                                if self._mode == 'SemiAuto': self.integralTerm = self.semiAutoValue
                                else:
                                        self.integralTerm = 0
                                        self.inControllableRegion = False

                        self._mode = value
                else:
                        self.printAndSendMessage('Error: mode must be Auto, SemiAuto, or Off. Not changing the mode.',"Alarm")

        def checkPipe(self):
                if self.inputPipeConn.poll():
                        data = self.inputPipeConn.recv()
                        if data[0] == "autoTune":
                                self.autoTune(data[1][0],data[1][1],data[1][2],data[1][3],data[1][4],data[1][5],data[1][6])
                        else:
                                setattr(self,data[0],data[1])

        def printAndSendMessage(self,message,messageType):
                print(message)
                if self.messageSignal != None: self.messageSignal.emit(message,messageType)

        def run(self):
                #since you just started the run, resets stop to 0
                self.stop = 0

                #main PID loop
                while self.stop == 0:
                        #If it is going to cycle, then calculate the time the next cycle should start. This reduces
                        #drift in time due to the time it takes to execute the code
                        if self.cycleTime != None:
                                self.nextCycleStart = time.time()*1000 + self.cycleTime

                        #prints the temperature
                        latestInput = getattr(self.inputSource,self.inputAttributeName)
                        if self.tempGraphSignal != None:
                                self.tempGraphSignal.emit(time.time()*1000,latestInput)
                                

                        #calculates the new setting
                        self.calculateOutput()

                        #sends the output to the output pipe connection
                        if self.outputPipeConn == None:
                                print('Error: outputPipeConn is not set')
                                self.stop = 1
                        else:                           
                                #print(self.output)
                                if self._mode != "Off": self.outputPipeConn.send((self.outputAttributeName,self.output))
                                else:
                                        if not(self.sentOffSignal):
                                                self.outputPipeConn.send((self.outputAttributeName,0))
                                                #print("Sending off signal")
                                                self.sentOffSignal = True


                        #checks the input pipe to see if anything needs to change
                        if self.inputPipeConn != None:
                                #print("Checking pipe")
                                self.checkPipe()
                        
                        #waits until the next cycle
                        if self.cycleTime != None:
                                if time.time()*1000 > self.nextCycleStart:
                                        self.printAndSendMessage('Error: I was not able to calculate the next output prior to the next cycle. Please set a longer cycle time (note that cycle time is measured in ms). Stopping the PID.',"Alarm")
                                        self.stop = 1
                                else:
                                        waittime = (self.nextCycleStart - time.time()*1000)/1000
                                        time.sleep(waittime)



        def calculateOutput(self):
                #Performs checks to see if all parameters are set properly
 
                if self.outputMin >= self.outputMax:
                        self.printAndSendMessage('Error: outputMin is greater than or equal to outputMax',"Alarm")
                        self.stop = 1
                        return
                
                #if cycleTime is not set, then the PID will just run once (this is so that you can run the PID externally
                #and not in its own loop). However, warn people that this is the case
                if self.cycleTime == None:
                                self.printAndSendMessage('Warning: Cycle time is not set. Running PID a single time',"Warning")
                                self.stop = 1

                #If mode is Off, don't do anything. If it is semiauto, then produce the set output
                if self._mode == 'Off':
                        return
                elif self._mode == 'SemiAuto':
                        self.sentOffSignal = False
                        if self.semiAutoValue == None:
                                self.printAndSendMessage ('Error: mode is set to SemiAuto, but semiAutoValue is not set',"Alarm")
                                self.stop = 1
                                return
                        else:
                                self.output = self.semiAutoValue
                elif self._mode == 'Auto':
                        self.sentOffSignal = False
                        #checks that all parameters are set properly
                        if (self.Kp == None) | (self.Ki == None) | (self.Kd == None):
                                self.printAndSendMessage('Error: Kp, Ki, and Kd are not all set',"Alarm")
                                self.stop = 1
                                return

                        if ((self.Kp <0) | (self.Ki <0) | (self.Kd <0)) & ((self.Kp >0) | (self.Ki >0) | (self.Kd >0)):
                                self.printAndSendMessage('Error: all K parameters must have the same sign',"Alarm")
                                self.stop = 1
                                return
                
                        #gets the time change based on the last time it was run
                        time.sleep(.1)
                        now = time.time()*1000
                        timeChange = now-self.lastRun

                        #gets the input value from the input source
                        latestInput = getattr(self.inputSource,self.inputAttributeName)

                        #calculates the error, the sum (integral) of the error, and the derivative of the input
                        
                        #we can use the derivative of the input, becasue the dError = dSetpoint - dInput, and
                        #either setpoint is constant, and that term would be zero, or the setpoint has changed
                        #and we intentionally ignore it to prevent a spike

                        #the multiplication by Ki here (instead of later) allows for the Ki to change during the 
                        #run without dramatically shifting the integral term

                        #The integral term is limited to be no larger than the output, so that when the output is
                        #maxed out, the integral term does not continue growing in a futile attempt to increase
                        #the output

                        error = self.setPoint - latestInput

                        #For the integral windup blocker, only adds to the integral factor if we are in the
                        #controllable regioun
                        if self.integralWindupBlocker == False or self.inControllableRegion == True:
                                self.integralTerm += self.Ki*error*timeChange
                                self.integralTerm=max(min(self.integralTerm,self.outputMax),self.outputMin)
                        #print(self.integralTerm)

                        dInput = (latestInput - self.lastInput) / timeChange

                        #calculates the result based on the parameters and error
                        #output is limited to be no larger than outputMax and no smaller than outputMin

                        #print("P: {:.2f}".format(self.Kp*error))
                        #print("I: {:.2f}".format(self.integralTerm))
                        #print("D: {:.2f}".format(self.Kd*dInput))
                        #print("")
                        output = self.Kp*error + self.integralTerm - self.Kd*dInput
                        #print(output)
                        self.output = max(min(output,self.outputMax),self.outputMin)

                        if self.output < self.outputMax and self.output > self.outputMin:
                                self.inControllableRegion = True
                        else:
                                #If just exited the controllable region, remove the addition to the integral term
                                if self.inControllableRegion == True and self.integralWindupBlocker == True: self.integralTerm -= self.Ki*error*timeChange
                                self.inControllableRegion = False
                        
                        #print(self.output)
                        #self.printAndSendMessage(self.output,"Message")

                        #preserves some values for the next run
                        self.lastInput = latestInput
                        self.lastRun = now

        def autoTune(self,outputStartValue,outputChange,expectedNoiseAmplitude, steadyRequirementTime, triggerDelta, lookBackTime, requiredAccuracy):
                #Autotunes the PID
                #Starts by setting the output to a single value, and getting the system to a steady state
                #Then introduces a known perterbance, and measures the response
                #outputStartValue is the initial value to set the output at, and wait for steady state
                #outputChange is the magnitude of the perterbance (output will go from outputStartValue+outputChange
                #to outputStartValue-outputChange)
                #expected noise amplitude and lookBackTime are smoothing parameters

                self.printAndSendMessage("Starting autoTune","Message")
                self.stop = 0

                #checks that the output ranges are allowed
                if ((outputStartValue - outputChange)< self.outputMin)|((outputStartValue + outputChange)> self.outputMax):
                        self.printAndSendMessage ("Error: outputs will exceed allowed values given outputStartValue and outputChange","Alarm")

                #sets the output to the outputStartValue
                self.outputPipeConn.send((self.outputAttributeName,outputStartValue))

                #waits until the temperature has reached a steady state
                steady = False
                times = []
                temp = []
                firstCycleTime = time.time()*1000
                
                while steady == False:
                        #gets the next cycle time
                        self.nextCycleStart = time.time()*1000 + self.cycleTime

                        # gets and prints the temperature
                        latestInput = getattr(self.inputSource,self.inputAttributeName)
                        #self.printAndSendMessage(latestInput,"Message")
                        if self.tempGraphSignal != None:
                                self.tempGraphSignal.emit(time.time()*1000,latestInput)

                        # adds the point to the new chart
                        newTime = time.time()*1000
                        times.append(newTime)
                        temp.append(latestInput)

                        #filters to the latest time period
                        oldestAllowed = newTime - steadyRequirementTime
                        temp = [y for (x,y) in zip(times,temp) if x>=oldestAllowed]
                        times = [x for x in times if x>=oldestAllowed]
                        

                        #calculates the max and the min
                        maxTemp = max(temp)
                        minTemp = min(temp)

                        #checks if temp has settled enough
                        if ((maxTemp - minTemp) < expectedNoiseAmplitude)&(oldestAllowed > firstCycleTime):
                                steady = True
                                self.printAndSendMessage("Steady state achieved","Success")

                        #checks the input pipe to see if anything needs to change
                        if self.inputPipeConn != None:
                                self.checkPipe()

                        #if stop signal has been sent, then stops
                                if self.stop == 1:return

                        #waits until the next cycle
                        if time.time()*1000 > self.nextCycleStart:
                                self.printAndSendMessage('Error: I was not able to calculate the next output prior to the next cycle. Please set a longer cycle time (note that cycle time is measured in ms). Stopping the PID.',"Alarm")
                                return
                        else:
                                waittime = (self.nextCycleStart - time.time()*1000)/1000
                                time.sleep(waittime)

                #Starts the calibration
                #trigger level is set by taking a delta from the stable value
                triggerLow = sum(temp)/float(len(temp)) - triggerDelta - expectedNoiseAmplitude/2
                triggerHigh = sum(temp)/float(len(temp)) + triggerDelta + expectedNoiseAmplitude/2
                self.printAndSendMessage("Low temperature trigger is {:2f}\nHigh temperature trigger is {:2f}".format(triggerLow,triggerHigh),"Message")


                #decreases the input by the outputChange
                self.outputPipeConn.send((self.outputAttributeName,(outputStartValue - outputChange)))
                direction = -1

                #resets the time and temp measurements
                times=[]
                temp=[]
                priorMinOrMax = 0
                possibleMins=[]
                possibleMinTimes=[]
                possibleMaxs=[]
                possibleMaxTimes=[]
                actualMins=[]
                actualMinTimes=[]
                actualMaxs=[]
                actualMaxTimes=[]
                cycles = 0

                calibrating=True
                
                while calibrating == True:
                        

                        #gets the next cycle time
                        self.nextCycleStart = time.time()*1000 + self.cycleTime
                        
                         # gets and prints the temperature
                        latestInput = getattr(self.inputSource,self.inputAttributeName)
                        if self.tempGraphSignal != None:
                                self.tempGraphSignal.emit(time.time()*1000,latestInput)

                        # adds the point to the new chart
                        newTime = time.time()*1000
                        times.append(newTime)
                        temp.append(latestInput)

                        #waits 10 cycles before doing the check:
                        cycles += 1

                        if cycles >10:
                                #checks to see if this is the largest or smallest in the last lookBackTime (this
                                #is designed to reduce impact from noise), then check if it is a true local min or max
                                pastComparisonLimit = newTime - lookBackTime
                                comparisonTime = [x for x in times if x >= pastComparisonLimit]
                                comparisonTemp = [y for (x,y) in zip(times,temp) if x>=pastComparisonLimit]

                                if comparisonTemp[-1]==min(comparisonTemp):
                                        possibleMins.append(comparisonTemp[-1])
                                        possibleMinTimes.append(comparisonTime[-1])
                                        if priorMinOrMax == 1:
                                                actualMaxs.append(possibleMaxs[-1])
                                                actualMaxTimes.append(possibleMaxTimes[-1])
                                                self.printAndSendMessage("Adding actual Max: {:.2f}".format(possibleMaxs[-1]),"Message")
                                                #for max, checks to see if the last three maxs are close enough. If so,
                                                #calibration is complete!
                                                if len(actualMaxs) >= 3:
                                                        lastThree = actualMaxs[-3:]
                                                        self.printAndSendMessage ("Last Three Maximums:{:.2f}, {:.2f}, {:.2f}".format(lastThree[0],lastThree[1],lastThree[2]),"Message")
                                                        
                                                        maxDelta = (max(lastThree)-min(lastThree))
                                                        if maxDelta < requiredAccuracy:
                                                                averageMax = sum(actualMaxs[-3:])/float(3)
                                                                averageMin = sum(actualMins[-3:])/float(3)
                                                                lastThreeTimes = actualMaxTimes[-3:]
                                                                Pu = (actualMaxTimes[-1]-actualMaxTimes[-3])/float(2)
                                                                Ku = (4*outputChange)/float((averageMax-averageMin)*3.14159)
                                                                Kp = 0.6*Ku
                                                                Ki = 1.2*Ku/float(Pu)
                                                                Kd = 0.075*Ku*Pu
                                                                self.printAndSendMessage("Calibration Successful! Kp={:.4f}, Ki={:.4f}, Kd={:.4f}".format(Kp,Ki,Kd),"Success")
                                                                calibrating == False
                                                                self.inputPipeConn.send([Kp,Ki,Kd])
                                                                return
                                        priorMinOrMax = -1
                                elif comparisonTemp[-1]==max(comparisonTemp):
                                        possibleMaxs.append(comparisonTemp[-1])
                                        possibleMaxTimes.append(comparisonTime[-1])
                                        if priorMinOrMax == -1:
                                                actualMins.append(possibleMins[-1])
                                                actualMinTimes.append(possibleMinTimes[-1])
                                                self.printAndSendMessage("Adding actual Min: {:.2f}".format(possibleMins[-1]),"Message")
                                        priorMinOrMax = 1

                        #sets the heat based on if it is above or below the appropriate trigger value
                        if temp[-1] > triggerHigh:
                                self.outputPipeConn.send((self.outputAttributeName,(outputStartValue - outputChange)))
                        elif temp[-1] < triggerLow:
                                self.outputPipeConn.send((self.outputAttributeName,(outputStartValue + outputChange)))
                        
                        #checks the input pipe to see if anything needs to change
                        if self.inputPipeConn != None:
                                self.checkPipe()

                        #if stop signal has been sent, then stops
                        if self.stop == 1:return

                        #waits until the next cycle
                        if time.time()*1000 > self.nextCycleStart:
                                self.printAndSendMessage('Error: I was not able to calculate the next output prior to the next cycle. Please set a longer cycle time (note that cycle time is measured in ms). Stopping the PID.',"Error")
                                return
                        else:
                                waittime = (self.nextCycleStart - time.time()*1000)/1000
                                time.sleep(waittime)
                        
                        

                

                        
                        




