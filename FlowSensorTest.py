import RPi.GPIO as GPIO
import time, sys

Sensor = input(">> Enter flow sensor to test (i.e. HLT IN): ")

if Sensor.lower() == "hlt in":FLOW_SENSOR = 8
elif Sensor.lower() == "hlt out":FLOW_SENSOR = 7
elif Sensor.lower() == "mlt in":FLOW_SENSOR = 12
elif Sensor.lower() == "mlt out":FLOW_SENSOR = 16
elif Sensor.lower() == "blk in":FLOW_SENSOR = 20
elif Sensor.lower() == "blk out":FLOW_SENSOR = 21
else:
   print("Error: flow sensor inputted was not valid")
   sys.exit()

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0

def countPulse(channel):
   global count
   count = count+1
   print(count)

GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print('\nEnding flow sensor test')
        GPIO.cleanup()
        sys.exit()
