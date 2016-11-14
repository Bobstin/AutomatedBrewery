import time
import Adafruit_ADS1x15
import pickle

adcValues = [1600,10000,20000,30000]
volumeValues1 = [0,3,6,9]
volumeValues2 = [0,3,6,9]
volumeValues3 = [0,3,6,9]

HLTVolumeCalibration=[adcValues,volumeValues1]
MLTVolumeCalibration=[adcValues,volumeValues2]
BLKVolumeCalibration=[adcValues,volumeValues3]

with open('VolumeCalibration.pk1','wb') as output:
    pickle.dump(HLTVolumeCalibration,output,protocol = pickle.HIGHEST_PROTOCOL)
    pickle.dump(MLTVolumeCalibration,output,protocol = pickle.HIGHEST_PROTOCOL)
    pickle.dump(BLKVolumeCalibration,output,protocol = pickle.HIGHEST_PROTOCOL)

