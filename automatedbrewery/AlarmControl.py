import time
import sys
import RPi.GPIO as GPIO

class AlarmController(object):
    @property
    def alarm(self):
        return self._alarm

    @alarm.setter
    def alarm(self,value):
        if (value == 1) or (value == 0):
            #Since this goes through a relay, low turns the alarm on
            self._alarm = value
            GPIO.output(self.alarmPin,not(value))
        else: print("Error: alarm must be set to either 1 (on) or 0 (off). Not changing alarm setting")


    def __init__(self,alarmPin = 25):
        self.alarmPin = alarmPin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.alarmPin,GPIO.OUT)
        GPIO.output(self.alarmPin,1)
