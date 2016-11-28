import time
import RPi.GPIO as GPIO
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

#loads the UI
qtCreatorFile = "../UI/AutomatedBreweryUI/FlowCalibrationDialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class flowCalibration(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,flowPins = [8,7,12,16,20,21],flowNames = ["HLT In","HLT Out","MLT In","MLT Out","BLK In","BLK Out"]):
        super(flowCalibration,self).__init__()       
        self.setupUi(self)
        self.show()

        #Sets headers to auto-adjust
        self.Calibration_Points.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        #Initially clears the tables
        self.clearPulses()
        for i in range(0,self.Calibration_Points.rowCount()+1): self.Calibration_Points.removeRow(0)

        #Sets up the pins
        #Note: this code should match the FlowSensor.py code, but pulls raw pulse counts
        #values instead of calibrated flows

        #stores the parameters
        self.flowPins = flowPins
        self.flowNames = flowNames

        #Sets the pins and related events
        GPIO.setmode(GPIO.BCM)
        for i in range(0,6):
            GPIO.setup(flowPins[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)
            GPIO.add_event_detect(flowPins[i], GPIO.FALLING, callback=self.countPulse)

        self.Add_Point.clicked.connect(self.addPoint)
        self.Remove_Point.clicked.connect(self.removePoint)
        self.Complete_Calibration.clicked.connect(self.completeCalibration)
        self.Sensor_To_Calibrate.currentIndexChanged.connect(self.clearPulses)
        self.Reset_Pulse_Count.clicked.connect(self.clearPulses)

        #Imports the old calibration
        with open('../calibrations/FlowCalibration.pk1','rb') as input:
            self.oldCalibration = pickle.load(input)
            print("Old calibration:")
            print(self.oldCalibration)
            print("")


    def countPulse(self,pin):
        if pin == self.flowPins[self.flowNames.index(self.Sensor_To_Calibrate.currentText())]:
            numPulses = int(self.Num_Pulses.text())
            numPulses += 1
            self.Num_Pulses.setText(str(numPulses))

    def clearPulses(self):
        self.Num_Pulses.setText("0")

    def addPoint(self):
        rowCount = self.Calibration_Points.rowCount()
        self.Calibration_Points.insertRow(rowCount)
        self.Calibration_Points.setItem(rowCount,0,QtWidgets.QTableWidgetItem(self.Sensor_To_Calibrate.currentText()))
        self.Calibration_Points.setItem(rowCount,1,QtWidgets.QTableWidgetItem(self.Num_Pulses.text()))
        self.Calibration_Points.setItem(rowCount,2,QtWidgets.QTableWidgetItem(self.Flow_Volume.text()))
        numPulses = float(self.Num_Pulses.text())
        volume = float(self.Flow_Volume.text())
        volumePerPulse = volume/numPulses
        self.Calibration_Points.setItem(rowCount,3,QtWidgets.QTableWidgetItem("{:.16f}".format(volumePerPulse)))

        self.clearPulses()

    def removePoint(self):
        rowToRemove = int(self.Pt_To_Remove.text())-1
        self.Calibration_Points.removeRow(rowToRemove)

    def completeCalibration(self):
        #Initializes the calibration results as empty
        self.allCalibrationResults = [[],[],[],[],[],[]]
        self.calibrationResults=[]

        #Loops through the table to create the calibration results
        for i in range(0,self.Calibration_Points.rowCount()):
            sensor=self.flowNames.index(self.Calibration_Points.item(i,0).text())
            volumePerPulse = float(self.Calibration_Points.item(i,3).text())
            self.allCalibrationResults[sensor].append(volumePerPulse)

        print("All calibration points:")
        print(self.allCalibrationResults)
        print("")
        #Averages the calibrations for each of the sensors to produce one value
        #If there are no values, then uses the old calibration value
        for i in range(0,6):
            allSensorResults = self.allCalibrationResults[i]
            if len(allSensorResults) == 0: self.calibrationResults.append(self.oldCalibration[i])
            else:
                sensorResult = float(sum(allSensorResults))/float(len(allSensorResults))
                self.calibrationResults.append(sensorResult)           
            
        print("New calibration:")
        print(self.calibrationResults)

        #Creates a pickle with the calibration results
        with open('FlowCalibration.pk1','wb') as output:
            pickle.dump(self.calibrationResults,output,protocol = pickle.HIGHEST_PROTOCOL)
            
        #closes window and stops sensor thread
        #self.stop = True
        self.close()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = flowCalibration()
	sys.exit(app.exec_())

