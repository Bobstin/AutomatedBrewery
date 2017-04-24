import sys
import os
sys.path.insert(0, os.path.abspath(".."))
import pickle

if os.path.isfile('../calibrations/RTDCalibration.pk1'):
    with open('../calibrations/RTDCalibration.pk1','rb') as pickleInput:
        HLTOffset = pickle.load(pickleInput)
        MLTOffset = pickle.load(pickleInput)
        BLKOffset = pickle.load(pickleInput)
else:
    HLTOffset = 0
    MLTOffset = 0
    BLKOffset = 0

print("HLT offset = {:.2f}".format(HLTOffset))
print("MLT offset = {:.2f}".format(MLTOffset))
print("BLK offset = {:.2f}".format(BLKOffset))

print("\nPlease enter new offsets")
HLTOffset=float(input(">>Enter HLT Offset: "))
MLTOffset=float(input(">>Enter MLT Offset: "))
BLKOffset=float(input(">>Enter BLK Offset: "))

confirm=input(">> Save new calibrations? (Y/N): ")
if confirm=="Y":
    with open('RTDCalibration.pk1','wb') as output:
        pickle.dump(HLTOffset,output,protocol = pickle.HIGHEST_PROTOCOL)
        pickle.dump(MLTOffset,output,protocol = pickle.HIGHEST_PROTOCOL)
        pickle.dump(BLKOffset,output,protocol = pickle.HIGHEST_PROTOCOL)
        print("Calibrations saved")
else: print ("Calibrations not saved")








        
        
    
    
