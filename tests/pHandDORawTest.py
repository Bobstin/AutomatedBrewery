import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from automatedbrewery.pHandDOSensor import AtlasI2C
Sensor = input(">>Enter sensor to test (pH or DO)")

if Sensor == "pH":Address = 99
elif Sensor == "DO":Address = 97
else:
    print("Error: sensor inputted was not valid")
    sys.exit()



device = AtlasI2C(address = Address) 	# creates the I2C port object, specify the address or bus if necessary

print("Pulling device information")
print(device.query("I")+"\n")
device.continuouspolling(2)


