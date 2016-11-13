import time
import Adafruit_ADS1x15
import pickle

class volumeSensors(object):
    def __init__(self,gain=1,HLTChannel=0,MLTChannel=1,BLKChannel=2):
        #Creates the ADC object
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gain = gain

        #Sets the parameters
        self.HLTChannel=HLTChannel
        self.MLTChannel=MLTChannel
        self.BLKChannel=BLKChannel

        #loads the calibration files
        with open('../calibrations/VolumeCalibration.pk1','rb') as input:
            self.HLTVolumeCalibration = pickle.load(input)
            self.MLTVolumeCalibration = pickle.load(input)
            self.BLKVolumeCalibration = pickle.load(input)

    def approximateVolume(self,kettle):
        #Pulls the value from the ADC
        if kettle=="HLT":    
            adcValue = self.adc.read_adc(self.HLTChannel, gain=self.gain)
            values = list(self.HLTVolumeCalibration[0])
            volumes = list(self.HLTVolumeCalibration[1])
        elif kettle=="MLT":
            adcValue = self.adc.read_adc(self.MLTChannel, gain=self.gain)
            values = list(self.MLTVolumeCalibration[0])
            volumes = list(self.MLTVolumeCalibration[1])
        elif kettle=="BLK":
            adcValue = self.adc.read_adc(self.BLKChannel, gain=self.gain)
            values = list(self.BLKVolumeCalibration[0])
            volumes = list(self.BLKVolumeCalibration[1])

        #Determines the volume based on the value
        #First, gets the closest value
        closestValue=min(values, key=lambda x:abs(x-adcValue))
        closestIndex = values.index(closestValue)
        closestVolume=volumes[closestIndex]

        #removes the closest value from the lists
        reducedValues = values
        reducedVolumes = volumes
        del reducedValues[closestIndex]
        del reducedVolumes[closestIndex]

        #Pulls the second closest value
        secondClosestValue=min(reducedValues, key=lambda x:abs(x-adcValue))
        secondClosestIndex = reducedValues.index(secondClosestValue)
        secondClosestVolume=reducedVolumes[secondClosestIndex]

        #takes a linear approximation between the two closest values
        alpha = (adcValue-closestValue)/(secondClosestValue-closestValue)
        volume = closestVolume+alpha*(secondClosestVolume-closestVolume)
       
        return volume

    def HLTVolume(self): return self.approximateVolume("HLT")
    def MLTVolume(self): return self.approximateVolume("MLT")
    def BLKVolume(self): return self.approximateVolume("BLK")

