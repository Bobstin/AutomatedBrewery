import AlarmControl
import time
import RPi.GPIO as GPIO

print("Turning the alarm off and on every 5 seconds")

Alarm = AlarmControl.AlarmController()
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
    
