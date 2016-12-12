import sys
import os
sys.path.insert(0, os.path.abspath(".."))

import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
import threading
from multiprocessing import Pipe
import pickle

from automatedbrewery.HeatControl import HeatController
from automatedbrewery.RTDSensor import tempSensors
from automatedbrewery.PID import PID

qtCreatorFile = "../UI/AutomatedBreweryUI/PIDCalibrationDialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class PIDCalibration(QtWidgets.QMainWindow, Ui_MainWindow):
    tempSignal = QtCore.pyqtSignal(list)
    #heatControlSignal = QtCore.pyqtSignal(list)
    #HLTPIDSignal = QtCore.pyqtSignal(list)
    #BLKPIDSignal = QtCore.pyqtSignal(list)
    heatGraphSignal = QtCore.pyqtSignal(float,float,str)
    #setHeatSignal = QtCore.pyqtSignal(str,str,int)
    messageSignal = QtCore.pyqtSignal(str,str)

    heatToHLTPIDPipe, HLTPIDToHeatPipe = Pipe()
    UIToHLTPIDPipe, HLTPIDToUIPipe = Pipe()
    heatToBLKPIDPipe, BLKPIDToHeatPipe = Pipe()
    UIToBLKPIDPipe, BLKPIDToUIPipe = Pipe()
    UIToHeatPipe, heatToUIPipe = Pipe()

    errorBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    errorBrush.setColor(QtGui.QColor(203,34,91))

    successBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    successBrush.setColor(QtGui.QColor(7,155,132))

    

    def __init__(self):
        super(PIDCalibration, self).__init__()

        #Imports the old calibration, if there is a file available
        if os.path.isfile('../calibrations/PIDCalibration.pk1'):
            with open('../calibrations/PIDCalibration.pk1','rb') as input:
                self.HLTResults = pickle.load(input)
                self.BLKResults = pickle.load(input)
        else:
            self.HLTResults = []
            self.BLKResults = []

        #Sets global pyqtgraph settings
        pyqtgraph.setConfigOption('background', 'w')
        pyqtgraph.setConfigOption('foreground', 'k')

        #connects the signals to their respective functions
        self.tempSignal.connect(self.tempUpdate)
        #self.setHeatSignal.connect(self.setHeat)
        self.heatGraphSignal.connect(self.updateHeatGraph)
        self.messageSignal.connect(self.newMessage)        

        #Starts up the UI
        self.setupUi(self)
        self.Messages.clear()
        self.show()

        self.turnOffTempSensing = False
        self.currentlyCalibrating = False
        self.stopCalibration = False

        #Creates threads for each of the sensors and controllers
        self.HLTPIDThread = threading.Thread(name='HLTPIDThread',target = self.startHLTPID)
        self.BLKPIDThread = threading.Thread(name='BLKPIDThread',target = self.startBLKPID)
        self.heatThread = threading.Thread(name='heatThread',target = self.startHeatControl)
        self.tempThread = threading.Thread(name='tempThread',target = self.startTempSensing)
        self.resultListenerThread = threading.Thread(name='resultListenerThread',target = self.listenForCalibrationResults)

        #Connects the buttons
        self.Calibrate_HLT.clicked.connect(lambda: self.startCalibration("HLT"))
        self.Calibrate_BLK.clicked.connect(lambda: self.startCalibration("BLK"))
        self.Complete_Calibration.clicked.connect(self.completeCalibration)

        #Defaults the kettle setting to none
        self.kettleSetting = "None"

        #creates the initial graph series and pens
        self.tempx=[[],[],[]]
        self.tempy=[[],[],[]]

        self.heatx=[[],[]]
        self.heaty=[[],[]]

        self.HLTPen = pyqtgraph.mkPen(color = (157,224,234), width = 3)
        self.MLTPen = pyqtgraph.mkPen(color = (0,138,179), width = 3)
        self.BLKPen = pyqtgraph.mkPen(color = (0,44,119), width = 3)

        self.startTime = time.time()

        #Starts the above threads
        self.tempThread.start()
        self.heatThread.start()
        self.HLTPIDThread.start()
        self.BLKPIDThread.start()
        self.resultListenerThread.start()

    def startHLTPID(self):
        time.sleep(1)
        self.HLTPID = PID(self,"HLTTemp")
        self.HLTPID.outputPipeConn = self.HLTPIDToHeatPipe
        self.HLTPID.inputPipeConn = self.HLTPIDToUIPipe
        self.HLTPID.messageSignal = self.messageSignal
        self.HLTPID.outputMin = 0
        self.HLTPID.outputMax = 100
        self.HLTPID.cycleTime = 2000
        self.HLTPID.outputAttributeName = "heatSetting"
        #self.HLTPID.semiAutoValue = 0
        self.HLTPID.mode = "Off"
        #self.HLTPID.tempGraphSignal = self.tempSignal
        self.HLTPID.run()

    def startBLKPID(self):
        time.sleep(1)
        self.BLKPID = PID(self,"BLKTemp")
        self.BLKPID.outputPipeConn = self.BLKPIDToHeatPipe
        self.BLKPID.inputPipeConn = self.BLKPIDToUIPipe
        self.BLKPID.messageSignal = self.messageSignal
        self.BLKPID.outputMin = 0
        self.BLKPID.outputMax = 100
        self.BLKPID.cycleTime = 2000
        self.BLKPID.outputAttributeName = "heatSetting"
        #self.BLKPID.semiAutoValue = 0
        self.BLKPID.mode = "Off"
        #self.BLKPID.tempGraphSignal = self.tempSignal
        self.BLKPID.run()

    def startHeatControl(self):
        heatCtrl = HeatController(pipeConn = self.heatToHLTPIDPipe,pipeConn2 = self.heatToBLKPIDPipe,pipeConn3 = self.heatToUIPipe, heatGraphSignal = self.heatGraphSignal)
        heatCtrl.run()

    def startTempSensing(self):
        self.tempSensor = tempSensors()
        while self.turnOffTempSensing == False:
            temps = [self.tempSensor.HLTTemp(),self.tempSensor.MLTTemp(),self.tempSensor.BLKTemp()]
            self.tempSignal.emit(temps)
            time.sleep(.1)

    def tempUpdate(self, tempValues):
        #OldHLTText = self.HLT_Heat.text()
        #OldMLTText = self.MLT_Heat.text()
        #OldBLKText = self.BLK_Heat.text()

        self.HLTTemp = tempValues[0]
        self.MLTTemp = tempValues[1]
        self.BLKTemp = tempValues[2]

        if tempValues[0]>999:tempValues[0]=999
        if tempValues[1]>999:tempValues[1]=999
        if tempValues[2]>999:tempValues[2]=999

        if tempValues[0]<0:tempValues[0]=0
        if tempValues[1]<0:tempValues[1]=0
        if tempValues[2]<0:tempValues[2]=0

        #NewHLTText=OldHLTText[:14]+"{: >3d}".format(int(round(tempValues[0])))+OldHLTText[17:]
        #NewMLTText=OldMLTText[:14]+"{: >3d}".format(int(round(tempValues[1])))+OldMLTText[17:]
        #NewBLKText=OldBLKText[:14]+"{: >3d}".format(int(round(tempValues[2])))+OldBLKText[17:]

        #self.HLT_Heat.setText(NewHLTText)
        #self.MLT_Heat.setText(NewMLTText)
        #self.BLK_Heat.setText(NewBLKText)

        currTime = (time.time() - self.startTime)/60
        if tempValues[0] != 999 and tempValues[0] != 0:
            self.tempy[0].append(tempValues[0])
            self.tempx[0].append(currTime)            
        if tempValues[1] != 999 and tempValues[1] != 0:
            self.tempy[1].append(tempValues[1])
            self.tempx[1].append(currTime)            
        if tempValues[2] != 999 and tempValues[2] != 0:
            self.tempy[2].append(tempValues[2])
            self.tempx[2].append(currTime)            

        self.Temp_Graph.clear()
        self.Temp_Graph.plot(self.tempx[0],self.tempy[0], pen=self.HLTPen)
        self.Temp_Graph.plot(self.tempx[1],self.tempy[1], pen=self.MLTPen)
        self.Temp_Graph.plot(self.tempx[2],self.tempy[2], pen=self.BLKPen)


    def updateHeatGraph(self,time,heatSetting,kettle):
        currTime = (time/1000 - self.startTime)/60
        if kettle == "HLT":
            self.heaty[0].append(heatSetting)
            self.heatx[0].append(currTime)
            self.heaty[1].append(0)
            self.heatx[1].append(currTime)
        elif kettle == "BLK":
            self.heaty[1].append(heatSetting)
            self.heatx[1].append(currTime)
            self.heaty[0].append(0)
            self.heatx[0].append(currTime)
        else:
            self.heaty[0].append(0)
            self.heatx[0].append(currTime)
            self.heaty[1].append(0)
            self.heatx[1].append(currTime)
            

        self.Power_Graph.clear()
        self.Power_Graph.plot(self.heatx[0],self.heaty[0], pen=self.HLTPen)
        self.Power_Graph.plot(self.heatx[1],self.heaty[1], pen=self.BLKPen)

    def printAndSendMessage(self,message,messageType):
        print(message)
        self.newMessage(message,messageType)

    def newMessage(self,message,messageType):
        newmessage = QtWidgets.QListWidgetItem(self.Messages)
        newmessage.setText(message)

        if messageType == "Alarm": newmessage.setBackground(self.errorBrush)
        elif messageType == "Warning": newmessage.setForeground(self.errorBrush)
        elif messageType == "Success": newmessage.setForeground(self.successBrush)

        self.Messages.scrollToBottom()

    def startCalibration(self,kettle):
        #gets the parameters from the UI
        outputStartValue = float(self.Output_Start_Value.text())
        outputChange = float(self.Output_Change.text())
        expectedNoiseAmplitude = float(self.Expected_Noise_Amplitude.text())
        steadyRequirementTime = float(self.Steady_Requirement.text())*1000
        triggerDelta = float(self.Temp_Change_Requirement.text())
        lookBackTime = float(self.Lookback_Time.text())*1000
        requiredAccuracy = float(self.Accuracy_Requirement.text())

        #packs the parameters into a list to be sent
        autoTuneParameters = [outputStartValue,outputChange,expectedNoiseAmplitude,steadyRequirementTime,triggerDelta,lookBackTime,requiredAccuracy]

        #sends instructions to the kettle to calibrate, and waits for calibration results
        if kettle == "HLT":
            if self.currentlyCalibrating != True:
                self.currentlyCalibrating = True
                self.kettleSetting = "HLT"
                self.UIToBLKPIDPipe.send(("mode","Off"))
                self.UIToHLTPIDPipe.send(("autoTune",autoTuneParameters))
                self.UIToHeatPipe.send(("kettle","HLT"))
            else: self.printAndSendMessage("Error: Currently calibrating a PID","Alarm")
        if kettle == "BLK":
            if self.currentlyCalibrating != True:
                self.currentlyCalibrating = True
                self.kettleSetting = "BLK"
                self.UIToHLTPIDPipe.send(("mode","Off"))
                self.UIToBLKPIDPipe.send(("autoTune",autoTuneParameters))
                self.UIToHeatPipe.send(("kettle","BLK"))
            else: self.printAndSendMessage("Error: Currently calibrating a PID","Alarm")

    def listenForCalibrationResults(self):
        while self.stopCalibration == False:
            if self.UIToHLTPIDPipe.poll():
                self.HLTResults = self.UIToHLTPIDPipe.recv()
                self.currentlyCalibrating = False
                #self.printAndSendMessage(self.HLTResults,"Message")
            if self.UIToBLKPIDPipe.poll():
                self.BLKResults = self.UIToBLKPIDPipe.recv()
                self.currentlyCalibrating = False
                #self.printAndSendMessage(self.BLKResults,"Message")
            time.sleep(2)

    def completeCalibration(self):
        self.printAndSendMessage("New calibrations:","success")
        if self.HLTResults != []:
            self.printAndSendMessage("HLT: Kp={:.2f}, Ki={:.2f}, Kd={:.2f}".format(self.HLTResults[0],self.HLTResults[1],self.HLTResults[2]),"success")
        if self.BLKResults != []:
            self.printAndSendMessage("BLK: Kp={:.2f}, Ki={:.2f}, Kd={:.2f}".format(self.BLKResults[0],self.BLKResults[1],self.BLKResults[2]),"success")

        with open('PIDCalibration.pk1','wb') as output:
            pickle.dump(self.HLTResults,output,protocol = pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.BLKResults,output,protocol = pickle.HIGHEST_PROTOCOL)

        self.close()

    def closeEvent(self, *args, **kwargs):
        #turns off heat
        self.UIToHLTPIDPipe.send(("mode","Off"))
        self.UIToHLTPIDPipe.send(("stop",True))
        self.UIToBLKPIDPipe.send(("mode","Off"))
        self.UIToBLKPIDPipe.send(("stop",True))
        self.UIToHeatPipe.send(("kettle","None"))
        self.UIToHeatPipe.send(("heatSetting",0))
        self.UIToHeatPipe.send(("turnOff",True))

        self.turnOffTempSensing = True
        self.stopCalibration = True
       
        super(PIDCalibration, self).closeEvent         

    

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = PIDCalibration()
	sys.exit(app.exec_())	
        








        
        
    
    
