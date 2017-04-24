import sys
import os
sys.path.insert(0, os.path.abspath(".."))
import pickle

if os.path.isfile('../calibrations/RTDCalibration.pk1'):
    with open('../calibrations/RTDCalibration.pk1','rb') as pickleInput:
        HLTOffset = pickle.load(pickleInput)
        MLTOffset = pickle.load(pickleInput)
        BLKOffset = pickle.load(pickleInput)

        print("HLT offset = {:.2f}".format(HLTOffset))
        print("MLT offset = {:.2f}".format(MLTOffset))
        print("BLK offset = {:.2f}".format(BLKOffset))
else:
    HLTResults = [0,0,0]
    BLKResults = [0,0,0]

kettle = input(">>Please select which PID calibration to override, either HLT or BLK: ")
if kettle=="HLT" or kettle=="BLK":
    Kp=float(input(">>Enter Kp: "))
    Ki=float(input(">>Enter Ki: "))
    Kd=float(input(">>Enter Kd: "))

    if kettle=="HLT": HLTResults=[Kp,Ki,Kd]
    if kettle=="BLK": BLKResults=[Kp,Ki,Kd]

    print("Proposed new calibrations (other kettle was pulled from pickle, or defaulted to all zeroes):")
    if HLTResults != []:
        print("HLT: Kp={:.2f}, Ki={:.12f}, Kd={:.2f}".format(HLTResults[0],HLTResults[1],HLTResults[2]))
    if BLKResults != []:
        print("BLK: Kp={:.2f}, Ki={:.12f}, Kd={:.2f}".format(BLKResults[0],BLKResults[1],BLKResults[2]))

    confirm=input(">> Save new calibrations? (Y/N): ")
    if confirm=="Y":
        with open('PIDCalibration.pk1','wb') as output:
            pickle.dump(HLTResults,output,protocol = pickle.HIGHEST_PROTOCOL)
            pickle.dump(BLKResults,output,protocol = pickle.HIGHEST_PROTOCOL)
            print("Calibrations saved")
    else: print ("Calibrations not saved")
else:
    print("Error: Kettle not valid")








        
        
    
    
