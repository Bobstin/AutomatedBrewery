import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.AlarmControl import AlarmController
import time
import RPi.GPIO as GPIO

print("Turning the alarm off and on every 5 seconds")

Alarm = AlarmController()
time.sleep(5)

try:
    while True:
        Alarm.alarm = 1
        time.sleep(5)
        Alarm.alarm = 0
        time.sleep(5)

except KeyboardInterrupt:
    Alarm.alarm = 0
    GPIO.cleanup()
    print("\nEnding alarm test")
    
