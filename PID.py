import time
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

		self.inputSource = inputSource
		self.outputAttributeName = 'setting'
		self.inputAttributeName = inputAttributeName
		self.lastInput = getattr(self.inputSource,self.inputAttributeName)
		if self.lastInput == None: raise ValueError('Unable to get input value. Check inputSource and inputAttributeName')


		self.lastRun = time.time()*1000
		self.integralTerm = 0

		self._mode = 'Auto'
		self.stop = 0
		self.nextCycleStart =time.time()*1000
		


	@property
	def mode(self):
		return self._mode

	@mode.setter
	def mode(self, value):
		if (value == 'Auto') | (value == 'SemiAuto') | (value == 'Manual'):
			#If switching to Auto from another mode, reset the last input value
			#If switching from SemiAuto to Auto, set the integral term to SemiAuto so
			#the PID maintains that value
			#If switching from Manual to Auto, reset the integral term so it doesn't overshoot
			if value == 'Auto':
				self.lastInput = getattr(self.inputSource,self.inputAttributeName)
				if self._mode == 'SemiAuto': self.integralTerm = self.semiAutoValue
				else: self.integralTerm = 0

			self._mode = value
		else:
			print('Error: mode must be Auto, SemiAuto, or Manual. Not changing the mode.')

	def checkPipe(self):
		if self.inputPipeConn.poll():
			data = self.pipeConn.recv()
			setattr(self,data[0],data[1])

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
				self.outputPipeConn.send((self.outputAttributeName,self.output))

			#checks the input pipe to see if anything needs to change
			if self.inputPipeConn != None:
				self.checkPipe()
			
			#waits until the next cycle
			if self.cycleTime != None:
				if time.time()*1000 > self.nextCycleStart:
					print('Error: I was not able to calculate the next output prior to the next cycle. Please set a longer cycle time (note that cycle time is measured in ms). Stopping the PID.')
					self.stop = 1
				else:
					waittime = (self.nextCycleStart - time.time()*1000)/1000
					time.sleep(waittime)



	def calculateOutput(self):
		#Performs checks to see if all parameters are set properly
		
		if self.outputMin >= self.outputMax:
			print('Error: outputMin is greater than or equal to outputMax')
			self.stop = 1
			return
		
		#if cycleTime is not set, then the PID will just run once (this is so that you can run the PID externally
		#and not in its own loop). However, warn people that this is the case
		if self.cycleTime == None:
				print('Warning: Cycle time is not set. Running PID a single time')
				self.stop = 1

		#If mode is manual, don't do anything. If it is semiauto, then produce the set output
		if self._mode == 'Manual':
			return
		elif self._mode == 'SemiAuto':
			if self.semiAutoValue == None:
				print ('Error: mode is set to SemiAuto, but semiAutoValue is not set')
				self.stop = 1
				return
			else:
				self.output = self.semiAutoValue
		elif self._mode == 'Auto':
			#checks that all parameters are set properly
			if (self.Kp == None) | (self.Ki == None) | (self.Kd == None):
				print('Error: Kp, Ki, and Kd are not all set')
				self.stop = 1
				return

			if ((self.Kp <0) | (self.Ki <0) | (self.Kd <0)) & ((self.Kp >0) | (self.Ki >0) | (self.Kd >0)):
				print('Error: all K parameters must have the same sign')
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

			self.integralTerm += self.Ki*error*timeChange
			self.integralTerm=max(min(self.integralTerm,self.outputMax),self.outputMin)

			dInput = (latestInput - self.lastInput) / timeChange

			#calculates the result based on the parameters and error
			#output is limited to be no larger than outputMax and no smaller than outputMin
			self.output = self.Kp*error + self.integralTerm - self.Kd*dInput
			self.output = max(min(self.output,self.outputMax),self.outputMin)
			print(self.output)

			#preserves some values for the next run
			self.lastInput = latestInput
			self.lastRun = now

	def autoTune(self,outputStartValue,outputChange,expectedNoiseAmplitude,movingAverageTime):
		#Autotunes the PID
		#Starts by setting the output to a single value, and getting the system to a steady state
		#Then introduces a known perterbance, and measures the response
		#outputStartValue is the initial value to set the output at, and wait for steady state
		#outputChange is the magnitude of the perterbance (output will go from outputStartValue+outputChange
		#to outputStartValue-outputChange)
		#expected noise amplitude and lookBackTime are smoothing parameters

		#sets the output to the outputStartValue
		self.outputPipeConn.send((self.outputAttributeName,self.outputStartValue))

		#waits until the temperature has reached a steady state
		steady = False
		while steady = False:




