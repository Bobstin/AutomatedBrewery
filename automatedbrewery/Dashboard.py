from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
import time
import threading
from multiprocessing import Pipe
import sys

#imports sensor modules
from FlowSensor import flowSensors
from MainSwitchSensor import mainSwitchSensors
from pHandDOSensor import pHandDOSensors
from RTDSensor import tempSensors
from ValveSwitchSensor import valveSwitchSensors
from VolumeSensor import volumeSensors

#imports control modules
from AlarmControl import AlarmController
from HeatControl import HeatController
from PumpAerationValveControl import PumpAerationValveController
from PID import PID

#Loads the qtCreator file
qtCreatorFile = "../UI/AutomatedBreweryUI/DashboardLarge.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class dashboard(QtWidgets.QMainWindow, Ui_MainWindow):
    #Creates the signals used to pull data from sensors and controllers
    flowSignal = QtCore.pyqtSignal(list,list)
    volumeSignal = QtCore.pyqtSignal(list)
    tempSignal = QtCore.pyqtSignal(list)
    pHandDOSignal = QtCore.pyqtSignal(list)
    mainSwitchSignal = QtCore.pyqtSignal(list)
    valveSwitchSignal = QtCore.pyqtSignal(list)

    alarmControlSignal = QtCore.pyqtSignal(list)
    heatControlSignal = QtCore.pyqtSignal(list)
    PAVControlSignal = QtCore.pyqtSignal(list)
    HLTPIDSignal = QtCore.pyqtSignal(list)
    BLKPIDSignal = QtCore.pyqtSignal(list)

    #Creates the pipes used to talk to the control modules
    heatToHLTPIDPipe, HLTPIDToHeatPipe = Pipe()
    UIToHLTPIDPipe, HLTPIDToUIPipe = Pipe()
    heatToBLKPIDPipe, BLKPIDToHeatPipe = Pipe()
    UIToBLKPIDPipe, BLKPIDToUIPipe = Pipe()
    UIToAlarmPipe, AlarmToUIPipe = Pipe()
    UIToPAVPipe, PAVToUIPipe = Pipe()

    def __init__(self):
        super(dashboard, self).__init__()
        
        #Sets global pyqtgraph settings
        pyqtgraph.setConfigOption('background', 'w')
        pyqtgraph.setConfigOption('foreground', 'k')

        #connects the signals to their respective functions
        self.flowSignal.connect(self.flowUpdate)
        self.volumeSignal.connect(self.volumeUpdate)
        self.tempSignal.connect(self.tempUpdate)
        self.pHandDOSignal.connect(self.pHandDOUpdate)
        self.mainSwitchSignal.connect(self.mainSwitchUpdate)
        self.valveSwitchSignal.connect(self.valveSwitchUpdate)

        #Starts up the UI
        self.setupUi(self)
        self.show()

        #Creates threads for each of the sensors and controllers
        HLTPIDThread = threading.Thread(target = self.startHLTPID)
        BLKPIDThread = threading.Thread(target = self.startBLKPID)
        heatThread = threading.Thread(target = self.startHeatControl)
        alarmThread = threading.Thread(target = self.startAlarmControl)
        PAVThread = threading.Thread(target = self.startPAVControl)

        flowThread = threading.Thread(target = self.startFlowSensing)
        volumeThread  = threading.Thread(target = self.startVolumeSensing)
        tempThread = threading.Thread(target = self.startTempSensing)
        pHandDOThread = threading.Thread(target = self.startpHandDOSensing)
        mainSwitchThread = threading.Thread(target = self.startMainSwitchSensing)
        valveSwitchThread = threading.Thread(target = self.startValveSwitchSensing)

        #Starts the above threads
        HLTPIDThread.start()
        BLKPIDThread.start()
        heatThread.start()
        alarmThread.start()
        PAVThread.start()

        flowThread.start()
        volumeThread.start()
        tempThread.start()
        pHandDOThread.start()
        mainSwitchThread.start()
        valveSwitchThread.start()

    def startHLTPID(self):
        TEMP=1

    def startBLKPID(self):
        TEMP=1

    def startHeatControl(self):
        TEMP=1

    def startAlarmControl(self):
        TEMP=1

    def startPAVControl(self):
        TEMP=1

    def startFlowSensing(self):
        flowSensor = flowSensors(self.flowSignal)

    def startVolumeSensing(self):
        volumeSensor = volumeSensors()
        while True:
            volumes = [volumeSensor.HLTVolume(),volumeSensor.MLTVolume(),volumeSensor.BLKVolume()]
            self.volumeSignal.emit(volumes)
            time.sleep(5)

    def startTempSensing(self):
        TEMP=1

    def startpHandDOSensing(self):
        TEMP=1

    def startMainSwitchSensing(self):
        TEMP=1

    def startValveSwitchSensing(self):
        TEMP=1

    def flowUpdate(self, flowRateValues, flowTotalValues):
        self.HLT_In.setText("{:.2f} g/m".format(flowRateValues[0][1][-1]))
        self.HLT_Out.setText("{:.2f} g/m".format(flowRateValues[1][1][-1]))
        self.MLT_In.setText("{:.2f} g/m".format(flowRateValues[2][1][-1]))
        self.MLT_Out.setText("{:.2f} g/m".format(flowRateValues[3][1][-1]))
        self.BLK_In.setText("{:.2f} g/m".format(flowRateValues[4][1][-1]))
        self.BLK_Out.setText("{:.2f} g/m".format(flowRateValues[5][1][-1]))

    def volumeUpdate(self, volumeValues):
        print(volumeValues)
        
    def tempUpdate(self, tempValues):
        TEMP=1

    def pHandDOUpdate(self, pHandDOValues):
        TEMP=1

    def mainSwitchUpdate(self, mainSwitchValues):
        TEMP=1

    def valveSwitchUpdate(self, valveSwitchValues):
        TEMP=1
		
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = dashboard()
	sys.exit(app.exec_())	
	
	
