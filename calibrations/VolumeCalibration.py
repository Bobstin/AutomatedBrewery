import time
import Adafruit_ADS1x15
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import threading

#loads the UI
qtCreatorFile = "../UI/AutomatedBreweryUI/VolumeCalibrationDialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class volumeCalibration(QtWidgets.QMainWindow, Ui_MainWindow):
    volumeSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(volumeCalibration,self).__init__()

        self.volumeSignal.connect(self.volumeUpdate)
        
        self.setupUi(self)
        self.show()

        #Sets headers to auto-adjust
        self.ADC_Values.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.Calibration_Points.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        #Initially clears the tables
        self.clearADC()
        for i in range(0,self.Calibration_Points.rowCount()+1): self.Calibration_Points.removeRow(0)

        #Initializes the sensor to keep running, and the ADC with no points
        self.stop = False
        self.ADCValues = []

        #Starts the sensor thread
        self.sensorThread = threading.Thread(target = self.startSensor)
        self.sensorThread.start()

        self.Add_Point.clicked.connect(self.addPoint)
        self.Remove_Point.clicked.connect(self.removePoint)
        self.Complete_Calibration.clicked.connect(self.completeCalibration)
        self.Kettle.currentIndexChanged.connect(self.clearADC)

        #Imports the old calibration
        with open('../calibrations/VolumeCalibration.pk1','rb') as input:
            self.oldHLTVolumeCalibration = pickle.load(input)
            self.oldMLTVolumeCalibration = pickle.load(input)
            self.oldBLKVolumeCalibration = pickle.load(input)

        print("Old calibration:")
        print(self.oldHLTVolumeCalibration)
        print(self.oldMLTVolumeCalibration)
        print(self.oldBLKVolumeCalibration)
        print("")

    def startSensor(self,gain=1,HLTChannel=0,MLTChannel=1,BLKChannel=2):
        #Note: this code should match the VolumeSensor.py code, but pulls raw ADC
        #values instead of calibrated volumes

        #Creates the ADC object
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gain = gain

        #Sets the parameters
        self.HLTChannel=HLTChannel
        self.MLTChannel=MLTChannel
        self.BLKChannel=BLKChannel

        #Gets the values from the ADC
        while self.stop == False:
            if self.Kettle.currentText()== "HLT": adcValue = self.adc.read_adc(self.HLTChannel, gain=self.gain)
            if self.Kettle.currentText()== "MLT": adcValue = self.adc.read_adc(self.MLTChannel, gain=self.gain)
            if self.Kettle.currentText()== "BLK": adcValue = self.adc.read_adc(self.BLKChannel, gain=self.gain)

            #Sends the value to be graphed
            self.volumeSignal.emit(adcValue)

            time.sleep(2)

    def volumeUpdate(self,adcValue):
        self.ADC_Values.insertRow(0)
        self.ADC_Values.setItem(0,0,QtWidgets.QTableWidgetItem(str(adcValue)))
        self.ADCValues.append(adcValue)
        
        while self.ADC_Values.rowCount() > self.Num_Pts.value():
            self.ADC_Values.removeRow(self.ADC_Values.rowCount()-1)
            self.ADCValues.pop(0)

        self.averageADC = float(sum(self.ADCValues)/len(self.ADCValues))

        self.Average_ADC.setText("{:.2f}".format(self.averageADC))

        #print(self.ADCValues)
            

    def closeEvent(self, *args, **kwargs):
        self.stop = True     
        super(volumeCalibration, self).closeEvent

    def clearADC(self):
        for i in range(0,self.ADC_Values.rowCount()+1): self.ADC_Values.removeRow(0)
        self.ADCValues = []

    def addPoint(self):
        rowCount = self.Calibration_Points.rowCount()
        self.Calibration_Points.insertRow(rowCount)
        self.Calibration_Points.setItem(rowCount,0,QtWidgets.QTableWidgetItem(self.Kettle.currentText()))
        self.Calibration_Points.setItem(rowCount,1,QtWidgets.QTableWidgetItem(str(self.averageADC)))
        self.Calibration_Points.setItem(rowCount,2,QtWidgets.QTableWidgetItem(self.Volume.text()))

    def removePoint(self):
        rowToRemove = int(self.Pt_To_Remove.text())-1
        self.Calibration_Points.removeRow(rowToRemove)

    def completeCalibration(self):
        #Initializes the calibration results as empty
        self.calibrationResults = [[[],[]],[[],[]],[[],[]]]
        kettles = {"HLT":0,"MLT":1,"BLK":2}

        #Loops through the table to create the calibration results
        for i in range(0,self.Calibration_Points.rowCount()):
            kettle = self.Calibration_Points.item(i,0).text()
            ADCValue = float(self.Calibration_Points.item(i,1).text())
            volume = float(self.Calibration_Points.item(i,2).text())

            kettle = kettles[kettle]

            self.calibrationResults[kettle][0].append(ADCValue)
            self.calibrationResults[kettle][1].append(volume)

        print("New calibration points:")
        print(self.calibrationResults)
        print("")

        #Breaks the calibration into each kettle for use with the volume sensor    
        if len(self.calibrationResults[0][0])== 0:
            HLTVolumeCalibration = self.oldHLTVolumeCalibration
        else:
            HLTVolumeCalibration=self.calibrationResults[0]

        if len(self.calibrationResults[1][0])== 0:
            MLTVolumeCalibration = self.oldMLTVolumeCalibration
        else:
            MLTVolumeCalibration=self.calibrationResults[1]

        if len(self.calibrationResults[2][0])== 0:
            BLKVolumeCalibration = self.oldBLKVolumeCalibration
        else:
            BLKVolumeCalibration=self.calibrationResults[2]

        print("New calibration:")
        print(HLTVolumeCalibration)
        print(MLTVolumeCalibration)
        print(BLKVolumeCalibration)
        


        #Creates a pickle with the calibration results
        with open('VolumeCalibration.pk1','wb') as output:
            pickle.dump(HLTVolumeCalibration,output,protocol = pickle.HIGHEST_PROTOCOL)
            pickle.dump(MLTVolumeCalibration,output,protocol = pickle.HIGHEST_PROTOCOL)
            pickle.dump(BLKVolumeCalibration,output,protocol = pickle.HIGHEST_PROTOCOL)

        #closes window and stops sensor thread
        self.stop = True
        self.close()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = volumeCalibration()
	sys.exit(app.exec_())

