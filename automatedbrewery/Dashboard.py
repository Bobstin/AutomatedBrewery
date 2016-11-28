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

#Imports other dialogs
from BeerSmithImporter import importDialog

#Loads the qtCreator file
qtCreatorFile = "../UI/AutomatedBreweryUI/DashboardLarge.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

tempPopupQtCreatorFile = "../UI/AutomatedBreweryUI/TempPopup.ui"
Ui_TempPopup,TempPopupQtBaseClass = uic.loadUiType(tempPopupQtCreatorFile)


class tempPopup(QtWidgets.QMainWindow, Ui_TempPopup):
    def __init__(self,setHeatSignal,kettle):
        super(tempPopup, self).__init__()

        self.setupUi(self)
        self.show()
        
        self.setHeatSignal = setHeatSignal
        self.kettle = kettle
        self.HeatLabel.setText("Please enter mode and setting to turn on "+kettle)
        self.StartHeat.clicked.connect(self.setHeat)
        self.Cancel.clicked.connect(self.cancel)

    def setHeat(self):
        if self.HeatMode.currentText() == "Off":heatSetting = 0
        else: heatSetting = int(round(float(self.Heat_Setting.text())))
        self.setHeatSignal.emit(self.kettle,self.HeatMode.currentText(),heatSetting)
        self.close()

    def cancel(self): self.close()
    

class dashboard(QtWidgets.QMainWindow, Ui_MainWindow):
    #Creates the signals used to pull data from sensors and controllers
    flowSignal = QtCore.pyqtSignal(list,list)
    volumeSignal = QtCore.pyqtSignal(list)
    tempSignal = QtCore.pyqtSignal(list)
    pHandDOSignal = QtCore.pyqtSignal(float,float)
    mainSwitchSignal = QtCore.pyqtSignal(list)
    valveSwitchSignal = QtCore.pyqtSignal(list)

    alarmControlSignal = QtCore.pyqtSignal(list)
    heatControlSignal = QtCore.pyqtSignal(list)
    PAVControlSignal = QtCore.pyqtSignal(list)
    HLTPIDSignal = QtCore.pyqtSignal(list)
    BLKPIDSignal = QtCore.pyqtSignal(list)
    setHeatSignal = QtCore.pyqtSignal(str,str,int)

    importSignal = QtCore.pyqtSignal(list,list,list,list,list,list)

    heatGraphSignal = QtCore.pyqtSignal(float,float,str)

    redSwitchStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(203,34,91);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    greenSwitchStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''
    
    autoGreenSwitchStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    autoRedSwitchStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(203,34,91);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    pumpOnStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 20px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    pumpOffStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 20px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    pumpAutoOnStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 20px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    pumpAutoOffStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 20px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    aerationOnStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    aerationOffStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 0px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    aerationAutoOnStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    aerationAutoOffStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    heatOffStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: white;
        font: 12pt "Arial";
        border: 2px solid black;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    heatOnStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(226,152,21);
        font: 12pt "Arial";
        color:white;
        border: 2px solid black;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    heatAutoOnStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(226,152,21);
        font: 12pt "Arial";
        color:white;
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    heatAutoOffStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: white;
        font: 12pt "Arial";
    }

    QPushButton:pressed {
        background-color: grey;
    }'''

    alarmSwitchOffStyle = "color:rgb(203,34,91)"

    alarmSwitchOnStyle = "color:rgb(7,155,132)"

    #Creates the pipes used to talk to the control modules
    heatToHLTPIDPipe, HLTPIDToHeatPipe = Pipe()
    UIToHLTPIDPipe, HLTPIDToUIPipe = Pipe()
    heatToBLKPIDPipe, BLKPIDToHeatPipe = Pipe()
    UIToBLKPIDPipe, BLKPIDToUIPipe = Pipe()
    UIToHeatPipe, heatToUIPipe = Pipe()
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
        self.setHeatSignal.connect(self.setHeat)
        self.importSignal.connect(self.beerSmithImport)
        self.heatGraphSignal.connect(self.updateHeatGraph)        

        #Starts up the UI
        self.setupUi(self)
        self.show()

        self.Mash_Steps.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.Boil_Steps.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        #Creates threads for each of the sensors and controllers
        self.HLTPIDThread = threading.Thread(target = self.startHLTPID)
        self.BLKPIDThread = threading.Thread(target = self.startBLKPID)
        self.heatThread = threading.Thread(target = self.startHeatControl)
        
        self.flowThread = threading.Thread(target = self.startFlowSensing)
        self.volumeThread  = threading.Thread(target = self.startVolumeSensing)
        self.tempThread = threading.Thread(target = self.startTempSensing)
        self.pHandDOThread = threading.Thread(target = self.startpHandDOSensing)
        self.mainSwitchThread = threading.Thread(target = self.startMainSwitchSensing)
        self.valveSwitchThread = threading.Thread(target = self.startValveSwitchSensing)

        #Connects the valve buttons to the valve control
        self.valve1.clicked.connect(lambda: self.changeValve(1))
        self.valve2.clicked.connect(lambda: self.changeValve(2))
        self.valve4.clicked.connect(lambda: self.changeValve(4))
        self.valve5.clicked.connect(lambda: self.changeValve(5))
        self.valve6.clicked.connect(lambda: self.changeValve(6))
        self.valve9.clicked.connect(lambda: self.changeValve(9))
        self.valve10.clicked.connect(lambda: self.changeValve(10))

        self.valve3u.clicked.connect(lambda: self.changeValve(3))
        self.valve3d.clicked.connect(lambda: self.changeValve(3))
        self.valve7u.clicked.connect(lambda: self.changeValve(7))
        self.valve7d.clicked.connect(lambda: self.changeValve(7))
        self.valve8u.clicked.connect(lambda: self.changeValve(8))
        self.valve8d.clicked.connect(lambda: self.changeValve(8))

        #Connects the pump and Aeration buttons
        self.waterPump.clicked.connect(lambda: self.changePumpAeration("waterPump"))
        self.wortPump.clicked.connect(lambda: self.changePumpAeration("wortPump"))
        self.aeration.clicked.connect(lambda: self.changePumpAeration("aeration"))

        #Connects the heat buttons
        self.HLT_Heat.clicked.connect(lambda: self.setHeatPopup("HLT"))
        self.BLK_Heat.clicked.connect(lambda: self.setHeatPopup("BLK"))

        #Connects the import button
        self.Beersmith_Import.clicked.connect(self.beerSmithImportDialog)

        #defaults the kettle setting to none
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
        self.flowThread.start()
        self.volumeThread.start()
        self.tempThread.start()
        self.pHandDOThread.start()
        self.mainSwitchThread.start()
        self.valveSwitchThread.start()
        self.heatThread.start()

        self.startAlarmControl()
        self.startPAVControl()

        self.HLTPIDThread.start()
        self.BLKPIDThread.start()

    def startHLTPID(self):
        self.HLTPID = PID(self.tempSensor,"HLTTemp")
        self.HLTPID.outputPipeConn = self.HLTPIDToHeatPipe
        self.HLTPID.inputPipeConn = self.HLTPIDToUIPipe
        self.HLTPID.outputMin = 0
        self.HLTPID.outputMax = 100
        self.HLTPID.cycleTime = 2000
        self.HLTPID.outputAttributeName = "heatSetting"
        #self.HLTPID.semiAutoValue = 0
        self.HLTPID.mode = "Off"
        #self.HLTPID.tempGraphSignal = self.tempSignal
        self.HLTPID.run()
        

    def startBLKPID(self):
        self.BLKPID = PID(self.tempSensor,"BLKTemp")
        self.BLKPID.outputPipeConn = self.BLKPIDToHeatPipe
        self.BLKPID.inputPipeConn = self.BLKPIDToUIPipe
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

    def startAlarmControl(self):
        TEMP=1

    def startPAVControl(self):
        self.PAVControl = PumpAerationValveController()

    def startFlowSensing(self):
        flowSensor = flowSensors(self.flowSignal)

    def startVolumeSensing(self):
        volumeSensor = volumeSensors()
        while True:
            volumes = [volumeSensor.HLTVolume(),volumeSensor.MLTVolume(),volumeSensor.BLKVolume()]
            self.volumeSignal.emit(volumes)
            time.sleep(2)

    def startTempSensing(self):
        self.tempSensor = tempSensors()
        while True:
            temps = [self.tempSensor.HLTTemp(),self.tempSensor.MLTTemp(),self.tempSensor.BLKTemp()]
            self.tempSignal.emit(temps)
            time.sleep(2)

    def startpHandDOSensing(self):
        pHandDOSensor = pHandDOSensors()
        while True:
            pH = pHandDOSensor.pH()
            DO = pHandDOSensor.DO()
            self.pHandDOSignal.emit(pH,DO)
            time.sleep(2)

    def startMainSwitchSensing(self):
        self.mainSwitchSensor = mainSwitchSensors()
        self.mainSwitchSensor.interruptSetUp(self.interruptedMainSwitch)
        while True:
            mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
            self.mainSwitchSignal.emit(mainSwitchStates)
            time.sleep(10)

    def startValveSwitchSensing(self):
        self.valveSwitchSensor = valveSwitchSensors()
        self.valveSwitchSensor.interruptSetUp(self.interruptedValveSwitch)
        while True:
            valveSwitchStates = self.valveSwitchSensor.allValveSwitchStates()
            self.valveSwitchSignal.emit(valveSwitchStates)
            time.sleep(10)

    def flowUpdate(self, flowRateValues, flowTotalValues):
        self.HLT_In.setText("{:.2f} g/m".format(flowRateValues[0][1][-1]))
        self.HLT_Out.setText("{:.2f} g/m".format(flowRateValues[1][1][-1]))
        self.MLT_In.setText("{:.2f} g/m".format(flowRateValues[2][1][-1]))
        self.MLT_Out.setText("{:.2f} g/m".format(flowRateValues[3][1][-1]))
        self.BLK_In.setText("{:.2f} g/m".format(flowRateValues[4][1][-1]))
        self.BLK_Out.setText("{:.2f} g/m".format(flowRateValues[5][1][-1]))

    def volumeUpdate(self, volumeValues):
        self.HLT_Vol.setText("{:.2f} gal".format(volumeValues[0]))
        self.MLT_Vol.setText("{:.2f} gal".format(volumeValues[1]))
        self.BLK_Vol.setText("{:.2f} gal".format(volumeValues[2]))

        #Floors the volume to 10 for the display of how full the kettle is
        if volumeValues[0]>10:volumeValues[0]=10
        if volumeValues[1]>10:volumeValues[1]=10
        if volumeValues[2]>10:volumeValues[2]=10

        #Multiplies the value by 100, since the kettle is up to 10 gallons, but
        #the object bar requires integer values, so it goes up to 1000
        self.HLT.setValue(int(round(volumeValues[0]*100)))
        self.MLT.setValue(int(round(volumeValues[1]*100)))
        self.BLK.setValue(int(round(volumeValues[2]*100)))
        
    def tempUpdate(self, tempValues):
        OldHLTText = self.HLT_Heat.text()
        OldMLTText = self.MLT_Heat.text()
        OldBLKText = self.BLK_Heat.text()

        if tempValues[0]>999:tempValues[0]=999
        if tempValues[1]>999:tempValues[1]=999
        if tempValues[2]>999:tempValues[2]=999

        if tempValues[0]<0:tempValues[0]=0
        if tempValues[1]<0:tempValues[1]=0
        if tempValues[2]<0:tempValues[2]=0

        NewHLTText=OldHLTText[:14]+"{: >3d}".format(int(round(tempValues[0])))+OldHLTText[17:]
        NewMLTText=OldMLTText[:14]+"{: >3d}".format(int(round(tempValues[1])))+OldMLTText[17:]
        NewBLKText=OldBLKText[:14]+"{: >3d}".format(int(round(tempValues[2])))+OldBLKText[17:]

        self.HLT_Heat.setText(NewHLTText)
        self.MLT_Heat.setText(NewMLTText)
        self.BLK_Heat.setText(NewBLKText)

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

        self.graph1.clear()
        self.graph1.plot(self.tempx[0],self.tempy[0], pen=self.HLTPen)
        self.graph1.plot(self.tempx[1],self.tempy[1], pen=self.MLTPen)
        self.graph1.plot(self.tempx[2],self.tempy[2], pen=self.BLKPen)

    def pHandDOUpdate(self, pH, DO):
        self.pH.setText("{:.2f}".format(pH))
        self.DO.setText("{:.2f}".format(DO))

    def mainSwitchUpdate(self, mainSwitchValues):
        #Updates the heat select
        if mainSwitchValues[0]=="Auto":
            if self.kettleSetting == "HLT":
                self.BLK_Heat.setStyleSheet(self.heatAutoOffStyle)
                self.HLT_Heat.setStyleSheet(self.heatAutoOnStyle)
            if self.kettleSetting == "BLK":
                self.BLK_Heat.setStyleSheet(self.heatAutoOnStyle)
                self.HLT_Heat.setStyleSheet(self.heatAutoOffStyle)
            if self.kettleSetting == "None":
                self.BLK_Heat.setStyleSheet(self.heatAutoOffStyle)
                self.HLT_Heat.setStyleSheet(self.heatAutoOffStyle)
                
        if mainSwitchValues[0]=="BLK":
            self.BLK_Heat.setStyleSheet(self.heatOnStyle)
            self.HLT_Heat.setStyleSheet(self.heatOffStyle)
        if mainSwitchValues[0]=="HLT":
            self.BLK_Heat.setStyleSheet(self.heatOffStyle)
            self.HLT_Heat.setStyleSheet(self.heatOnStyle)

        #Updates the pumps and aeration
        if mainSwitchValues[1]=="Off":self.waterPump.setStyleSheet(self.pumpOffStyle)
        if mainSwitchValues[1]=="On":self.waterPump.setStyleSheet(self.pumpOnStyle)
        if mainSwitchValues[1]=="Auto":
            if self.PAVControl.waterPump == 1:self.waterPump.setStyleSheet(self.pumpAutoOnStyle)
            if self.PAVControl.waterPump == 0:self.waterPump.setStyleSheet(self.pumpAutoOffStyle)

        if mainSwitchValues[2]=="Off":self.wortPump.setStyleSheet(self.pumpOffStyle)
        if mainSwitchValues[2]=="On":self.wortPump.setStyleSheet(self.pumpOnStyle)
        if mainSwitchValues[2]=="Auto":
            if self.PAVControl.wortPump == 1:self.wortPump.setStyleSheet(self.pumpAutoOnStyle)
            if self.PAVControl.wortPump == 0:self.wortPump.setStyleSheet(self.pumpAutoOffStyle)

        if mainSwitchValues[3]=="Off":self.aeration.setStyleSheet(self.aerationOffStyle)
        if mainSwitchValues[3]=="On":self.aeration.setStyleSheet(self.aerationOnStyle)
        if mainSwitchValues[3]=="Auto":
            if self.PAVControl.aeration == 1:self.aeration.setStyleSheet(self.aerationAutoOnStyle)
            if self.PAVControl.aeration == 0:self.aeration.setStyleSheet(self.aerationAutoOffStyle)

        #Updates the master heat switch
        if mainSwitchValues[4] == "Off":self.master_Heat.setStyleSheet(self.heatOffStyle)
        if mainSwitchValues[4] == "On":self.master_Heat.setStyleSheet(self.heatOnStyle)

        #Updates the alarm switch
        if mainSwitchValues[5] == "Off":
            self.alarm_Text.setStyleSheet(self.alarmSwitchOffStyle)
            self.alarm_Text.setText("Off")
        if mainSwitchValues[5] == "On":
            self.alarm_Text.setStyleSheet(self.alarmSwitchOnStyle)
            self.alarm_Text.setText("On")

    def valveSwitchUpdate(self, valveSwitchStates):
        autoValveStates = self.PAVControl.valveStates
        for i in range(1,11):
            if i in [1,2,4,5,6,9,10]:
                if valveSwitchStates[i-1]=="On": getattr(self,"valve"+str(i)).setStyleSheet(self.greenSwitchStyle)
                if valveSwitchStates[i-1]=="Off": getattr(self,"valve"+str(i)).setStyleSheet(self.redSwitchStyle)
                if valveSwitchStates[i-1]=="Auto":
                    if autoValveStates[i-1] == 0: getattr(self,"valve"+str(i)).setStyleSheet(self.autoRedSwitchStyle)
                    if autoValveStates[i-1] == 1: getattr(self,"valve"+str(i)).setStyleSheet(self.autoGreenSwitchStyle)
            else:
                if valveSwitchStates[i-1]=="On":                
                    getattr(self,"valve"+str(i)+"u").setStyleSheet(self.greenSwitchStyle)
                    getattr(self,"valve"+str(i)+"d").setStyleSheet(self.redSwitchStyle)
                if valveSwitchStates[i-1]=="Off":
                    getattr(self,"valve"+str(i)+"u").setStyleSheet(self.redSwitchStyle)
                    getattr(self,"valve"+str(i)+"d").setStyleSheet(self.greenSwitchStyle)
                if valveSwitchStates[i-1]=="Auto":
                    if autoValveStates[i-1] == 0:
                        getattr(self,"valve"+str(i)+"u").setStyleSheet(self.autoRedSwitchStyle)
                        getattr(self,"valve"+str(i)+"d").setStyleSheet(self.autoGreenSwitchStyle)
                    if autoValveStates[i-1] == 1:
                        getattr(self,"valve"+str(i)+"u").setStyleSheet(self.autoGreenSwitchStyle)
                        getattr(self,"valve"+str(i)+"d").setStyleSheet(self.autoRedSwitchStyle)

    def interruptedMainSwitch(self,pin):
        mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
        self.mainSwitchSignal.emit(mainSwitchStates)

    def interruptedValveSwitch(self,pin):
        valveSwitchStates = self.valveSwitchSensor.allValveSwitchStates()
        self.valveSwitchSignal.emit(valveSwitchStates)

    def changeValve(self,valve):
        #Pulls the current state of the valve
        currentState = self.PAVControl.valveStates[valve-1]
        if currentState == 0: newState = 1
        if currentState == 1: newState = 0

        #Sets the valve to the new state
        setattr(self.PAVControl,"valve"+str(valve),newState)

        #Updates the dashboard
        self.valveSwitchUpdate(self.valveSwitchSensor.allValveSwitchStates())

    def changePumpAeration(self,item):
        #Pulls the current state of the item
        currentState = getattr(self.PAVControl,item)
        #print(currentState)
        if currentState == 0: newState = 1
        if currentState == 1: newState = 0
        #print(newState)

        #Sets the item to the new state
        setattr(self.PAVControl,item,newState)

        #Updates the dashboard
        self.mainSwitchUpdate(self.mainSwitchSensor.allMainSwitchStates())

    def setHeatPopup(self,kettle):
        self.tempPopup = tempPopup(self.setHeatSignal,kettle)

    def setHeat(self, kettle, mode, setting):
        #print(setting)
        if kettle == "HLT": 
            if mode == "SemiAuto":
                self.kettleSetting = "HLT"
                #Turns off the BLK, and turns on the HLT
                self.UIToBLKPIDPipe.send(("mode","Off"))
                self.UIToHLTPIDPipe.send(("semiAutoValue",setting))
                self.UIToHLTPIDPipe.send(("mode","SemiAuto"))
                self.UIToHeatPipe.send(("kettle","HLT"))

                OldHLTText = self.HLT_Heat.text()
                NewHLTText=OldHLTText[:17]+"\nSetting: {:.0f}%".format(setting)
                self.HLT_Heat.setText(NewHLTText)

                OldBLKText = self.BLK_Heat.text()
                NewBLKText=OldBLKText[:17]
                self.BLK_Heat.setText(NewBLKText)
                
            if mode == "Off":
                self.UIToHLTPIDPipe.send(("mode","Off"))

                OldHLTText = self.HLT_Heat.text()
                NewHLTText=OldHLTText[:17]
                self.HLT_Heat.setText(NewHLTText)
                
                #If the current kettle is the one being turned off, then set the kettles to None for safety
                if self.kettleSetting == "HLT":
                    self.kettleSetting = "None"
                    self.UIToHeatPipe.send(("kettle","None"))
            
        if kettle == "BLK": 
            if mode == "SemiAuto":
                self.kettleSetting = "BLK"
                #Turns off the HLT, and turns on the BLK
                self.UIToHLTPIDPipe.send(("mode","Off"))
                self.UIToBLKPIDPipe.send(("semiAutoValue",setting))
                self.UIToBLKPIDPipe.send(("mode","SemiAuto"))
                self.UIToHeatPipe.send(("kettle","BLK"))

                OldBLKText = self.BLK_Heat.text()
                NewBLKText=OldBLKText[:17]+"\nSetting: {:.0f}%".format(setting)
                self.BLK_Heat.setText(NewBLKText)

                OldHLTText = self.HLT_Heat.text()
                NewHLTText=OldHLTText[:17]
                self.HLT_Heat.setText(NewHLTText)
            if mode == "Off":
                self.UIToBLKPIDPipe.send(("mode","Off"))

                OldBLKText = self.BLK_Heat.text()
                NewBLKText=OldBLKText[:17]
                self.BLK_Heat.setText(NewBLKText)
                
                #If the current kettle is the one being turned off, then set the kettles to None for safety
                if self.kettleSetting == "BLK":
                    self.kettleSetting = "None"
                    self.UIToHeatPipe.send(("kettle","None"))

            #Updates the main switch states to reflect the new Auto statuses
            mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
            self.mainSwitchSignal.emit(mainSwitchStates)
            

    def closeEvent(self, *args, **kwargs):
        #Closes all valves:
        for i in [1,11]: setattr(self.PAVControl,"valve"+str(i),0)

        #turns off pumps and aeration
        self.PAVControl.wortPump = 0
        self.PAVControl.waterPump = 0
        self.PAVControl.aeration = 0

        #turns off heat
        self.UIToHLTPIDPipe.send(("mode","Off"))
        self.UIToBLKPIDPipe.send(("mode","Off"))
        self.UIToHeatPipe.send(("kettle","None"))
        self.UIToHeatPipe.send(("heatSetting",0))

        #self.flowThread.exit()
        #self.volumeThread.exit()
        #self.tempThread.exit()
        #self.pHandDOThread.exit()
        #self.mainSwitchThread.exit()
        #self.valveSwitchThread.exit()
        #self.heatThread.exit()
        #self.HLTPIDThread.exit()
        #self.BLKPIDThread.exit()
        
        super(dashboard, self).closeEvent

        print("System exited successfully!")

    def beerSmithImportDialog(self):
        self.beerSmithImportDialog = importDialog(self.importSignal)

    def beerSmithImport(self,volumeValues,tempValues,boilSchedule,dryHopSchedule,mashSchedule,pHValues):
        self.clearData()
        
        self.volumeValues = volumeValues
        self.tempValues = tempValues
        self.boilSchedule = boilSchedule
        self.dryHopSchedule = dryHopSchedule
        self.mashSchedule = mashSchedule
        self.pHValues = pHValues

        #Updates the volumes
        self.HLT_Fill_1_Target.setText("{:.2f} gal".format(self.volumeValues[0]))
        self.Strike_Target.setText("{:.2f} gal".format(self.volumeValues[1]))
        self.HLT_Fill_2_Target.setText("{:.2f} gal".format(self.volumeValues[2]))
        self.Sparge_Target.setText("{:.2f} gal".format(self.volumeValues[3]))
        self.Pre_Boil_Target.setText("{:.2f} gal".format(self.volumeValues[4]))
        self.Post_Boil_Target.setText("{:.2f} gal".format(self.volumeValues[5]))
        self.Fermenter_Target.setText("{:.2f} gal".format(self.volumeValues[6]))

        #updates the temps
        self.Strike_Temp.setText("{:.0f} F".format(self.tempValues[0]))
        self.HLT_Fill_2_Temp.setText("{:.0f} F".format(self.tempValues[1]))
        self.Sparge_Temp.setText("{:.0f} F".format(self.tempValues[2]))

        #updates the pH
        self.pH_target.setText("{:.2f}".format(self.pHValues[0]))
                  

        #adds the boil schedule
        #print(boilSchedule)
        for i in range(0,len(self.boilSchedule)):
            rowPosition = self.Boil_Steps.rowCount()
            #print(rowPosition)
            
            #Adds a row and the required information
            self.Boil_Steps.insertRow(rowPosition)
            self.Boil_Steps.setItem(rowPosition,1,QtWidgets.QTableWidgetItem(str(self.boilSchedule[i][0])))
            self.Boil_Steps.setItem(rowPosition,0,QtWidgets.QTableWidgetItem("{:.0f} min".format(self.boilSchedule[i][1])))
            self.Boil_Steps.setItem(rowPosition,2,QtWidgets.QTableWidgetItem(str(self.boilSchedule[i][2])))


        #adds mash schedule
        for i in range(0,len(self.mashSchedule)):
            rowPosition = self.Mash_Steps.rowCount()
            self.Mash_Steps.insertRow(rowPosition)
            self.Mash_Steps.setItem(rowPosition,0,QtWidgets.QTableWidgetItem("{:.0f} F".format(self.mashSchedule[i][3])))
            self.Mash_Steps.setItem(rowPosition,1,QtWidgets.QTableWidgetItem("{:.2f} gal".format(self.mashSchedule[i][1])))
            self.Mash_Steps.setItem(rowPosition,2,QtWidgets.QTableWidgetItem("{:.0f} F".format(self.mashSchedule[i][2])))
            self.Mash_Steps.setItem(rowPosition,3,QtWidgets.QTableWidgetItem("{:.0f} min".format(self.mashSchedule[i][4])))
            self.Mash_Steps.setItem(rowPosition,4,QtWidgets.QTableWidgetItem("{:.0f} min".format(self.mashSchedule[i][5])))

    def clearData(self):
        for i in range(0,self.Boil_Steps.rowCount()+1): self.Boil_Steps.removeRow(0)
        for i in range(0,self.Mash_Steps.rowCount()+1): self.Mash_Steps.removeRow(0)

        #clears the volumes
        self.HLT_Fill_1_Target.setText("")
        self.Strike_Target.setText("")
        self.HLT_Fill_2_Target.setText("")
        self.Sparge_Target.setText("")
        self.Pre_Boil_Target.setText("")
        self.Post_Boil_Target.setText("")
        self.Fermenter_Target.setText("")

        #clears the temps
        self.Strike_Temp.setText("")
        self.HLT_Fill_2_Temp.setText("")
        self.Sparge_Temp.setText("")

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
            

        self.graph2.clear()
        self.graph2.plot(self.heatx[0],self.heaty[0], pen=self.HLTPen)
        self.graph2.plot(self.heatx[1],self.heaty[1], pen=self.BLKPen)
       
             
        
    
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = dashboard()
	sys.exit(app.exec_())	
	
	
