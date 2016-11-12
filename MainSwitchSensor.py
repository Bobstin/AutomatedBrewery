import time
import RPi.GPIO as GPIO

class mainSwitchSensors(object):
    def __init__(self, ThreeWayIn1Pins = [4,27,10,5], ThreeWayIn2Pins = [17,22,9,6], TwoWayInPins = [11,26]):
        #Sets the parameters
        self.ThreeWayIn1Pins = ThreeWayIn1Pins
        self.ThreeWayIn2Pins = ThreeWayIn2Pins
        self.TwoWayInPins = TwoWayInPins
        self.Switches = ["Heat Select","Water Pump","Wort Pump","Aeration","Master Heat","Alarm"]
        self.ThreeStateOptions=[["Auto","BLK","HLT","ERROR"],["Off","On","Auto"],["Off","On","Auto"],["Off","On","Auto"]]
        self.TwoStateOptions = [["Off","On"],["On","Off"]]
        self.ThreeStateSwitches = ["Heat Select","Water Pump","Wort Pump","Aeration"]
        self.TwoStateSwitches = ["Master Heat","Alarm"]

        #Sets the pins with pull down resistors    
        GPIO.setmode(GPIO.BCM)
        for i in range(0,4):
            GPIO.setup(self.ThreeWayIn1Pins[i],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.ThreeWayIn2Pins[i],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        for i in range(0,2): GPIO.setup(self.TwoWayInPins[i],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    def interruptSetUp(self,callbackFunction,bounceTime=50):
        for i in range(0,4):
            GPIO.add_event_detect(self.ThreeWayIn1Pins[i], GPIO.BOTH, callback=callbackFunction, bouncetime=bounceTime)
            GPIO.add_event_detect(self.ThreeWayIn2Pins[i], GPIO.BOTH, callback=callbackFunction, bouncetime=bounceTime)

        for i in range(0,2): GPIO.add_event_detect(self.TwoWayInPins[i], GPIO.BOTH, callback=callbackFunction, bouncetime=bounceTime)


    def allMainSwitchStates(self,bounceTime=0.5):
        #Unless it can gets a good state, assumes switch is in error
        state=["ERROR"]*6

        time.sleep(bounceTime)

        #gets the state of each of the switches
        for i in range(0,4):state[i]=self.ThreeStateOptions[i][GPIO.input(self.ThreeWayIn1Pins[i])+2*GPIO.input(self.ThreeWayIn2Pins[i])]
        for i in range(0,2):state[i+4]=self.TwoStateOptions[i][GPIO.input(self.TwoWayInPins[i])]

        return state

    def switchState(self, switch):
        #This is used for getting the value of a single switch
        allStates = self.allMainSwitchStates()
        switchIndex = self.Switches.index(switch)
        return allStates[switchIndex]

        
