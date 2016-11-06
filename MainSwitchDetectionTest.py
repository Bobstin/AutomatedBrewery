import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#These are the GPIO pins with inputs (except for the alarm and master heat pins, which only have one input)
ThreeWayIn1Pins = [4,27,10,5]
ThreeWayIn2Pins = [17,22,9,6]
TwoWayInPins = [11,26]
Switches = ["Heat Select","Wort Pump","Water Pump","Aeration","Master Heat","Alarm"]

ThreeStateOptions=[["Auto","BLK","HLT","ERROR"],["Off","On","Auto"],["Off","On","Auto"],["Off","On","Auto"]]
TwoStateOptions = [["Off","On"],["On","Off"]]

global j
j=0

def getstate(IGNORE):
    print(IGNORE)
    global j
    j=j+1
    print(j)
    state=["ERROR"]*7

    time.sleep(0.5)

    for i in range(0,4):
        state[i]=ThreeStateOptions[i][GPIO.input(ThreeWayIn1Pins[i])+2*GPIO.input(ThreeWayIn2Pins[i])]
        print(Switches[i]+":"+str(GPIO.input(ThreeWayIn1Pins[i]))+","+str(GPIO.input(ThreeWayIn2Pins[i]))+" ("+state[i]+")")

    for i in range(0,2):
        state[i+4]=TwoStateOptions[i][GPIO.input(TwoWayInPins[i])]
        print(Switches[i+4]+":"+str(GPIO.input(TwoWayInPins[i]))+" ("+state[i+4]+")")

    print("")

for i in range(0,4):
    GPIO.setup(ThreeWayIn1Pins[i],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(ThreeWayIn1Pins[i], GPIO.BOTH, callback=getstate, bouncetime=1000)
    GPIO.setup(ThreeWayIn2Pins[i],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(ThreeWayIn2Pins[i], GPIO.BOTH, callback=getstate, bouncetime=1000)

for i in range(0,2):
    GPIO.setup(TwoWayInPins[i],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(TwoWayInPins[i], GPIO.BOTH, callback=getstate, bouncetime=1000)


while True:
    time.sleep(2)
GPIO.cleanup()
