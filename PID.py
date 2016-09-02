import time

class Source:
	def __init__(self):
		self.value=1

# Input source must have a parameter called value
# Input source must be available when PIF is initialized to get the starting value
class PID:
	def __init__(self,inputSource):
		#creates placeholders for the PID values. These are allowed to be empty, but run() will
		#check if they are filled, and fail if they are not
		self.setPoint = None
		self.CV = None
		self.Kp = None
		self.Ki = None
		self.Kd = None
		self.controllerDirection = None
		self.outputDest = None
		self.outputMin = None
		self.outputMax = None
		self.latestInput = None
		self.output = None

		self.inputSource = inputSource
		self.lastRun = time.time()*1000
		self.latestInput = self.inputSource.value
		self.integralTerm = 0
		self.mode = 'Auto'
		self.semiAutoValue = 0



	def run(self):
		#If mode is manual, don't do anything. If it is semiauto, then produce the set output
		if self.mode = 'Manual':
			return
		elif self.mode = 'SemiAuto':
			self.output = self.semiAutoValue
		elif self.mode = 'Auto':
			#gets the time change based on the last time it was run
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
			self.integralTerm=max(min(self.integralTerm,self.outputmax),self.outputmin)


			dInput = (latestInput - self.lastInput) / timeChange

			#calculates the result based on the parameters and error
			#output is limited to be no larger than outputmax and no smaller than outputmin
			self.output = self.Kp*error + self.integralTerm - self.Kd*dError
			self.output = max(min(output,self.outputmax),self.outputmin)

			#preserves some values for the next run
			self.lastInput = latestInput
			self.lastRun = now

			print(inputValue)



Source = Source()
PID = PID(Source)

PID.Kp=1
PID.Ki=2
PID.Kd=1
PID.setPoint = 1
PID.run()
Source.value=2
PID.run()

