import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

status = not GPIO.input(2)
autoswitch=GPIO.input(4)
onswitch=GPIO.input(17)
GPIO.output(2, status)

if status:
	print('Auto status = Off')
else:
	print('Auto status = On')


if autoswitch:
	print('Auto LED = Off')
else:
	print('Auto LED = Blue')


if not onswitch:
	print ('Status LED = Green')
elif autoswitch:
	if status:
		print ('Status LED = Red')
	else:
		print ('Status LED = Green')
else:
	print ('Status LED = Red')




#GPIO.cleanup()
