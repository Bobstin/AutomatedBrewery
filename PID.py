import time

class Source:
	def __init__(self):
		self.value=1

class Output:
	def __init__(self):
		self.setting = None

# Input source must have a parameter called value
# Input source must be available when PIF is initialized to get the starting value
class PID(object):
	def __init__(self,inputSource, temperature=0):
		#creates placeholders for the PID values. These are allowed to be empty, but run() will
		#check if they are filled, and fail if they are not
		self.setPoint = None
		self.Kp = None
		self.Ki = None
		self.Kd = None
		self.outputDest = None
		self.outputMin = None
		self.outputMax = None
		self.output = None

		self.inputSource = inputSource
		self.lastRun = time.time()*1000
		self.lastInput = self.inputSource.value
		self.integralTerm = 0
		self.semiAutoValue = None
		self._mode = 'Auto'


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
				self.lastInput = self.inputSource.value
				if self._mode == 'SemiAuto': self.integralTerm = self.semiAutoValue
				else: self.integralTerm = 0

			self._mode = value
		else:
			print('Error: mode must be Auto, SemiAuto, or Manual. Not changing the mode.')




	def run(self):
		#Call this function to run the PID

		#Performs checks to see if all parameters are set properly
		if (self.Kp == None) | (self.Ki == None) | (self.Kd == None):
			print('Error: Kp, Ki, and Kd are not all set')
			return

		if self.outputMin >= self.outputMax:
			print('Error: outputMin is greater than or equal to outputMax')
			return

		if ((self.Kp <0) | (self.Ki <0) | (self.Kd <0)) & ((self.Kp >0) | (self.Ki >0) | (self.Kd >0)):
			print('Error: all K parameters must have the same sign')
			return

		#If mode is manual, don't do anything. If it is semiauto, then produce the set output
		if self._mode == 'Manual':
			return
		elif self._mode == 'SemiAuto':
			if self.semiAutoValue == None:
				print ('Error: mode is set to SemiAuto, but semiAutoValue is not set')
				return
			else:
				self.output = self.semiAutoValue
		elif self._mode == 'Auto':
			#gets the time change based on the last time it was run
			time.sleep(.1)
			now = time.time()*1000
			timeChange = now-self.lastRun

			#gets the input value from the input source
			latestInput = self.inputSource.value

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

			#preserves some values for the next run
			self.lastInput = latestInput
			self.lastRun = now





Source = Source()
PID = PID(Source)

PID.Kp=1
PID.Ki=-5
PID.Kd=1
PID.outputMin = 0
PID.outputMax = 100
PID.setPoint = 1.1

PID.run()


