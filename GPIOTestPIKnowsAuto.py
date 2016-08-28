import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

onswitch = GPIO.input(4)
autoswitch = GPIO.input(17)

#below is just for testing; autostatus would come from program
autostatus = True

if autoswitch:
	GPIO.output(2, autostatus)
elif onswitch:
	GPIO.output(2, True)
else:
	GPIO.output(2, False)

time.sleep(2)

#below is just for testing; autostatus would come from program
autostatus = False

if autoswitch:
	GPIO.output(2, autostatus)
elif onswitch:
	GPIO.output(2, True)
else:
	GPIO.output(2, False)
#GPIO.cleanup()