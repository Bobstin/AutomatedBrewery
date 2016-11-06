import time
from PumpAerationValveControl import PumpAerationValveController

print("Testing the valves. Should start with all valve closed for 5 seconds,")
print("then all valves open for 5 seconds, then all closed again for 5 seconds")
print("This is followed by the opening of each valve in order, one second apart")
print("Then all valves are turned off\n")
PAVControl = PumpAerationValveController()
'''time.sleep(5)

PAVControl.valveStates = [1]*10
time.sleep(5)
PAVControl.valveStates = [0]*10
time.sleep(5)

PAVControl.valve1 = 1
time.sleep(1)
PAVControl.valve2 = 1
time.sleep(1)
PAVControl.valve3 = 1
time.sleep(1)
PAVControl.valve4 = 1
time.sleep(1)
PAVControl.valve5 = 1
time.sleep(1)
PAVControl.valve6 = 1
time.sleep(1)
PAVControl.valve7 = 1
time.sleep(1)
PAVControl.valve8 = 1
time.sleep(1)
PAVControl.valve9 = 1
time.sleep(1)
PAVControl.valve10 = 1
time.sleep(5)

PAVControl.valveStates = [0]*10
time.sleep(5)

print("Testing the ability to partially open valves 5 and 9.")
print("Both valves will be closed for 5 seconds, then valve 5 will be partially")
print("opened, then fully opened, followed by the same pattern for valve 9.")
print("Then they will be partially closed, followed by fully closed\n")

PAVControl.partialOpenClose(5,1.5)
time.sleep(2)
PAVControl.fullyOpenClose(5,1)
time.sleep(5)

PAVControl.partialOpenClose(9,1.5)
time.sleep(2)
PAVControl.fullyOpenClose(9,1)
time.sleep(5)

PAVControl.partialOpenClose(5,-1.5)
time.sleep(2)
PAVControl.fullyOpenClose(5,0)
time.sleep(5)

PAVControl.partialOpenClose(9,-1.5)
time.sleep(2)
PAVControl.fullyOpenClose(9,0)
time.sleep(5)

print("Testing the ability to repeatedly partially open")
print("Both valves will be opened in steps, then closed in steps")

for i in range(0,6):
    PAVControl.partialOpenClose(5,.5)
    PAVControl.partialOpenClose(9,.5)
    time.sleep(2)

for i in range(0,6):
    PAVControl.partialOpenClose(5,-.5)
    PAVControl.partialOpenClose(9,-.5)
    time.sleep(2)

PAVControl.fullyOpenClose(5,0)
PAVControl.fullyOpenClose(9,0)
time.sleep(5)'''

PAVControl.wortPump = 1
time.sleep(2)
PAVControl.wortPump = 0
time.sleep(2)
PAVControl.wortPump = 1
time.sleep(2)
PAVControl.wortPump = 0


