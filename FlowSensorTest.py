import RPi.GPIO as GPIO
import time, sys

FLOW_SENSOR = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0

def countPulse(channel):
   global count
   count = count+1
   print(count)

GPIO.add_event_detect(8, GPIO.FALLING, callback=countPulse)
GPIO.add_event_detect(7, GPIO.FALLING, callback=countPulse)
GPIO.add_event_detect(12, GPIO.FALLING, callback=countPulse)
GPIO.add_event_detect(16, GPIO.FALLING, callback=countPulse)
GPIO.add_event_detect(20, GPIO.FALLING, callback=countPulse)
GPIO.add_event_detect(21, GPIO.FALLING, callback=countPulse)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print('\ncaught keyboard interrupt!, bye')
        GPIO.cleanup()
        sys.exit()
