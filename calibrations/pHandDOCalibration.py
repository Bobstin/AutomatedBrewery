import sys
import os
sys.path.insert(0, os.path.abspath(".."))

import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import threading
from automatedbrewery.pHandDOSensor import AtlasI2C

#loads the UI
qtCreatorFile = "../UI/AutomatedBreweryUI/pHandDOCalibrationDialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class pHandDOCalibration(QtWidgets.QMainWindow, Ui_MainWindow):
    DOSignal = QtCore.pyqtSignal(str)
    def __init__(self,pHAddress=99, DOAddress=97):
        super(pHandDOCalibration,self).__init__()       
        self.setupUi(self)
        self.show()

        #Creates two raw AtlasI2C sensors
        self.pHSensor = AtlasI2C(address=pHAddress)
        self.DOSensor = AtlasI2C(address=DOAddress)

        #Connects the buttons to their repersentative functions
        self.Calibrate_Midpoint.clicked.connect(self.calibrateMidpoint)
        self.Calibrate_Lowpoint.clicked.connect(self.calibrateLowpoint)
        self.Calibrate_Highpoint.clicked.connect(self.calibrateHighpoint)

        self.Calibrate_Air.clicked.connect(self.calibrateAir)
        self.Calibrate_Zero_DO.clicked.connect(self.calibrateZeroDO)
        
        #Since there is no calibration file (the Atlas I2C devices store thier own
        #calibration information, clicking "Complete calibration" just closes the window
        self.Complete_Calibration.clicked.connect(self.close)

        #A thread and signal are needed to keep checking the DO sensor after the first calibration point
        self.DOThread = threading.Thread(target = self.startDO)
        self.DOSignal.connect(self.updateDO)
        self.stop = False

    def calibrateMidpoint(self):
        self.pHSensor.query("Cal,mid,{:.2f}".format(float(self.Midpoint_pH.text())))

    def calibrateLowpoint(self):
        self.pHSensor.query("Cal,low,{:.2f}".format(float(self.Lowpoint_pH.text())))

    def calibrateHighpoint(self):
        self.pHSensor.query("Cal,high,{:.2f}".format(float(self.Highpoint_pH.text())))

    def calibrateAir(self):
        self.DOSensor.query("Cal")
        #Once the air calibration is done, then shows the current measurement for the
        #Zero DO calibration
        self.DOThread.start()

    def calibrateZeroDO(self):
        self.DOSensor.query("Cal,0")

    def startDO(self):
        while self.stop == False:
            result = self.DOSensor.query("R")
            result = result[18:].rstrip('\0')
            self.DOSignal.emit(result)
            time.sleep(2)

    def updateDO(self,result):
        self.Current_Reading.setText(result)

    def closeEvent(self, *args, **kwargs):
        self.stop = True     
        super(pHandDOCalibration, self).closeEvent
        
        

        


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = pHandDOCalibration()
	sys.exit(app.exec_())

