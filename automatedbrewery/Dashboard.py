from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
import time
import threading
from multiprocessing import Pipe
import sys
import pickle

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

    messageSignal = QtCore.pyqtSignal(str,str)

    redSwitchStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(203,34,91);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    greenSwitchStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''
    
    autoGreenSwitchStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    autoRedSwitchStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(203,34,91);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    pumpOnStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 20px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    pumpOffStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 20px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    pumpAutoOnStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 20px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    pumpAutoOffStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 20px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    aerationOnStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    aerationOffStyle = '''
    QPushButton {
        border: 4px solid black;
        border-radius: 0px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    aerationAutoOnStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: rgb(7,155,132);
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    aerationAutoOffStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: white;
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    heatOffStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: white;
        font: 12pt "Arial";
        border: 2px solid black;
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
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
        background-color: rgb(191,191,191);
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
        background-color: rgb(191,191,191);
    }'''

    heatAutoOffStyle = '''
    QPushButton {
        border: 4px solid rgb(0,138,205);
        border-radius: 0px;
        background-color: white;
        font: 12pt "Arial";
    }

    QPushButton:pressed {
        background-color: rgb(191,191,191);
    }'''

    alarmSwitchOffStyle = "color:rgb(203,34,91)"

    alarmSwitchOnStyle = "color:rgb(7,155,132)"

    topWaterStyle = '''
    QFrame {
        border-width: 6px;
        border-style: solid none none none;
        border-color: rgb(0,138,205);
    }'''

    leftWaterStyle = '''
    QFrame {
        border-width: 6px;
        border-style: none none none solid;
        border-color: rgb(0,138,205);
    }'''

    leftRoundWaterStyle = '''
    QFrame {
        border-width: 6px;
        border-style: none none none solid;
        border-color: rgb(0,138,205);
        border-radius: 20px;
    }'''

    chillerWaterStyle = '''
    QFrame {
        border-width: 6px;
        border-style: solid;
        border-color: rgb(0,138,205);
    }'''



    topWortStyle = '''
    QFrame {
        border-width: 6px;
        border-style: solid none none none;
        border-color: rgb(226,152,21);
    }'''

    leftWortStyle = '''
    QFrame {
        border-width: 6px;
        border-style: none none none solid;
        border-color: rgb(226,152,21);
    }'''

    leftRoundWortStyle = '''
    QFrame {
        border-width: 6px;
        border-style: none none none solid;
        border-color: rgb(226,152,21);
        border-radius: 20px;
    }'''


    topOffStyle = '''
    QFrame {
        border-width: 6px;
        border-style: solid none none none;
        border-color: rgb(191,191,191);
    }'''

    leftOffStyle = '''
    QFrame {
        border-width: 6px;
        border-style: none none none solid;
        border-color: rgb(191,191,191);
    }'''

    leftRoundOffStyle = '''
    QFrame {
        border-width: 6px;
        border-style: none none none solid;
        border-color: rgb(191,191,191);
        border-radius: 20px;
    }'''

    chillerOffStyle = '''
    QFrame {
        border-width: 6px;
        border-style: solid;
        border-color: rgb(191,191,191);
    }'''

    pastPhaseStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(191,191,191);
        color:grey;
        font: 12pt "Arial";
    }

    QPushButton::pressed {
        background-color: rgb(191,191,191);
        color: rgb(191,191,191);
    }'''

    currentPhaseStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(0,138,179);
        color:white;
        font: 12pt "Arial";
    }

    QPushButton::pressed {
        background-color: rgb(191,191,191);
        color: grey;
    }'''

    futurePhaseStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(196,236,244);
        font: 12pt "Arial";
    }

    QPushButton::pressed {
        background-color: rgb(191,191,191);
        color: grey;
    }'''

    redBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    redBrush.setColor(QtGui.QColor(203,34,91))

    greenBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    greenBrush.setColor(QtGui.QColor(7,155,132))

    whiteBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    whiteBrush.setColor(QtGui.QColor(255,255,255))



    #Defines the mapping between liquid paths and frames
    pathsToFrames = {1:[1],
                     2:[3,9],
                     3:[10,11],
                     4:[8],
                     5:[7],
                     6:[5,4],
                     7:[15,16,40,17],
                     8:[24],
                     9:[25],
                     10:[30],
                     11:[31,32,20,19,18],
                     12:[13],
                     13:[22,21],
                     14:[35,36,37,23,38,39],
                     15:[26],
                     16:[27],
                     17:[33,34,45],
                     18:[42,46],
                     19:[41,44],
                     20:[28],
                     21:[6,12],
                     22:[14],
                     23:[2],
                     24:[29],
                     25:[49]
    }

    #Defines the frame types (top, left, or left round)
    frameTypes = {1:"top",
                  2:"left",
                  3:"left",
                  4:"top",
                  5:"left",
                  6:"left",
                  7:"top",
                  8:"left",
                  9:"top",
                  10:"top",
                  11:"left",
                  12:"top",
                  13:"left",
                  14:"top",
                  15:"left",
                  16:"top",
                  17:"top",
                  18:"left",
                  19:"left round",
                  20:"left",
                  21:"top",
                  22:"left",
                  23:"left round",
                  24:"top",
                  25:"top",
                  26:"top",
                  27:"top",
                  28:"left",
                  29:"left",
                  30:"top",
                  31:"left",
                  32:"top",
                  33:"left",
                  34:"top",
                  35:"left",
                  36:"top",
                  37:"left",
                  38:"left",
                  39:"top",
                  40:"left",
                  41:"left",
                  42:"top",
                  43:"none",
                  44:"left",
                  45:"left",
                  46:"left",
                  47:"none",
                  48:"none",
                  49:"left"                  
    }

    #Defines the mapping between valves and liquidpaths
    valvesToPaths = {():[[],[]],
                     (1,):[[1,2,23,25],[]],
                     (1,3,7):[[1,2,23,25],[]],
                     (3,4,7):[[2,3,4,5,6],[]],
                     (3,4):[[2,3,4,5,6],[]],
                     (4,5,7,8):[[3,4,5,7,21,22],[]],
                     (4,5,7):[[3,4,5,7,21,22],[]],
                     (4,5):[[3,4,5,7,21,22],[]],
                     (3,4,6,7,9):[[2,3,4,5,6,7,8,9,10,11,12,20],[]],
                     (3,4,6,9):[[2,3,4,5,6,7,8,9,10,11,12,20],[]],
                     (3,7,8,9):[[],[8,9,10,13,14,20]],
                     (7,8,9):[[],[8,9,10,13,14,20]],
                     (4,5,7,8):[[3,4,5,7,21,22],[8,9,10,13,14,20]],
                     (2,8,10):[[1,19,24],[10,13,15,16,17,18,20]],
                     (1,4,5,8):[[1,2,3,4,5,7,21,22,23,25],[]],
                     (1,4,5):[[1,2,3,4,5,7,21,22,23,25],[]],
                     (6,9):[[7,8,9,10,11,12,20],[]],
                     (7,8,9):[[],[8,9,10,13,14,20]],
                     (8,9):[[8,9,10,13,17,18,20],[]]
    }
                 
                     

    #Creates the pipes used to talk to the control modules
    heatToHLTPIDPipe, HLTPIDToHeatPipe = Pipe()
    UIToHLTPIDPipe, HLTPIDToUIPipe = Pipe()
    heatToBLKPIDPipe, BLKPIDToHeatPipe = Pipe()
    UIToBLKPIDPipe, BLKPIDToUIPipe = Pipe()
    UIToHeatPipe, heatToUIPipe = Pipe()
    UIToAlarmPipe, AlarmToUIPipe = Pipe()
    UIToPAVPipe, PAVToUIPipe = Pipe()

    #Also creates a pipe used to shut off the flow sensors
    UIToFlowPipe, FlowToUIPipe = Pipe()

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
        self.messageSignal.connect(self.printAndSendMessage)

        #Starts up the UI and sets some default states
        self.setupUi(self)
        self.Messages.clear()
        for i in range(1,11):
            getattr(self,"phase"+str(i)).setStyleSheet(self.futurePhaseStyle)
            
        self.show()

        self.Mash_Steps.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.Boil_Steps.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        #Sets all of the sensor threads to keep sensing
        self.turnOffVolumeSensing = False
        self.turnOffTempSensing = False
        self.turnOffpHandDOSensing = False
        self.turnOffMainSwitchSensing = False
        self.turnOffValveSwitchSensing = False

        #Defaults the grain added parameter to False
        self.grainAdded = False

        #Sets default state for the phase threads
        self.currentlyStagingPhase = False
        self.stopPhase = False
        self.phaseRunning = None

        #Creates threads for each of the sensors and controllers
        self.HLTPIDThread = threading.Thread(name='HLTPIDThread',target = self.startHLTPID)
        self.BLKPIDThread = threading.Thread(name='BLKPIDThread',target = self.startBLKPID)
        self.heatThread = threading.Thread(name='heatThread',target = self.startHeatControl)
        
        self.flowThread = threading.Thread(name='flowThread',target = self.startFlowSensing)
        self.volumeThread  = threading.Thread(name='volumeThread',target = self.startVolumeSensing)
        self.tempThread = threading.Thread(name='tempThread',target = self.startTempSensing)
        self.pHandDOThread = threading.Thread(name='pHandDOThread',target = self.startpHandDOSensing)
        self.mainSwitchThread = threading.Thread(name='mainSwitchThread',target = self.startMainSwitchSensing)
        self.valveSwitchThread = threading.Thread(name='valveSwitchThread',target = self.startValveSwitchSensing)

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

        #Connects the alarm off button
        self.Turn_Off_Alarm.clicked.connect(self.turnOffAlarm)

        #Connects the phase control buttons
        self.phase1.clicked.connect(lambda: self.startPhase(1))
        self.phase2.clicked.connect(lambda: self.startPhase(2))
        self.phase3.clicked.connect(lambda: self.startPhase(3))
        self.phase4.clicked.connect(lambda: self.startPhase(4))
        self.phase5.clicked.connect(lambda: self.startPhase(5))
        self.phase6.clicked.connect(lambda: self.startPhase(6))
        self.phase7.clicked.connect(lambda: self.startPhase(7))
        self.phase8.clicked.connect(lambda: self.startPhase(8))
        self.phase9.clicked.connect(lambda: self.startPhase(9))
        self.phase10.clicked.connect(lambda: self.startPhase(10))

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

        with open('../calibrations/PIDCalibration.pk1','rb') as PIDCalibration:
            self.HLTPIDCalibration = pickle.load(PIDCalibration)
            self.BLKPIDCalibration = pickle.load(PIDCalibration)
     
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

    def printAndSendMessage(self,message,messageType):
        print(message)
        self.newMessage(message,messageType)

    def newMessage(self,message,messageType):
        newmessage = QtWidgets.QListWidgetItem(self.Messages)
        newmessage.setText(message)

        if messageType == "Alarm":
            newmessage.setBackground(self.redBrush)
            newmessage.setForeground(self.whiteBrush)
            self.alarmControl.alarm = 1
        elif messageType == "Warning": newmessage.setForeground(self.redBrush)
        elif messageType == "Success": newmessage.setForeground(self.greenBrush)

        self.Messages.scrollToBottom()

    def startHLTPID(self):
        #Note that the PIDs get the temp from the dashboard; this prevents them from also
        #Polling the RTDs, which causes errors
        time.sleep(2)
        self.HLTPID = PID(self,"HLTTemp")
        self.HLTPID.outputPipeConn = self.HLTPIDToHeatPipe
        self.HLTPID.inputPipeConn = self.HLTPIDToUIPipe
        self.HLTPID.outputMin = 0
        self.HLTPID.outputMax = 100
        self.HLTPID.cycleTime = 2000
        self.HLTPID.outputAttributeName = "heatSetting"
        self.HLTPID.Kp = self.HLTPIDCalibration[0]
        self.HLTPID.Ki = self.HLTPIDCalibration[1]
        self.HLTPID.Kd = self.HLTPIDCalibration[2]
        #self.HLTPID.semiAutoValue = 0
        self.HLTPID.mode = "Off"
        #self.HLTPID.tempGraphSignal = self.tempSignal
        self.HLTPID.run()
        

    def startBLKPID(self):
        #Note that the PIDs get the temp from the dashboard; this prevents them from also
        #Polling the RTDs, which causes errors
        time.sleep(2)
        self.BLKPID = PID(self,"BLKTemp")
        self.BLKPID.outputPipeConn = self.BLKPIDToHeatPipe
        self.BLKPID.inputPipeConn = self.BLKPIDToUIPipe
        self.BLKPID.outputMin = 0
        self.BLKPID.outputMax = 100
        self.BLKPID.cycleTime = 2000
        self.BLKPID.outputAttributeName = "heatSetting"
        self.BLKPID.Kp = self.BLKPIDCalibration[0]
        self.BLKPID.Ki = self.BLKPIDCalibration[1]
        self.BLKPID.Kd = self.BLKPIDCalibration[2]
        #self.BLKPID.semiAutoValue = 0
        self.BLKPID.mode = "Off"
        #self.BLKPID.tempGraphSignal = self.tempSignal
        self.BLKPID.run()

    def startHeatControl(self):
        heatCtrl = HeatController(pipeConn = self.heatToHLTPIDPipe,pipeConn2 = self.heatToBLKPIDPipe,pipeConn3 = self.heatToUIPipe, heatGraphSignal = self.heatGraphSignal)
        heatCtrl.run()

    def startAlarmControl(self):
        self.alarmControl = AlarmController()

    def startPAVControl(self):
        self.PAVControl = PumpAerationValveController()

    def startFlowSensing(self):
        flowSensor = flowSensors(self.flowSignal, inputPipe=self.FlowToUIPipe)

    def startVolumeSensing(self):
        volumeSensor = volumeSensors()
        while self.turnOffVolumeSensing == False:
            volumes = [volumeSensor.HLTVolume(),volumeSensor.MLTVolume(),volumeSensor.BLKVolume()]
            self.volumeSignal.emit(volumes)
            time.sleep(1)
            #print(threading.enumerate())

    def startTempSensing(self):
        self.tempSensor = tempSensors()
        while self.turnOffTempSensing == False:
            temps = [self.tempSensor.HLTTemp(),self.tempSensor.MLTTemp(),self.tempSensor.BLKTemp()]
            self.tempSignal.emit(temps)
            time.sleep(1)

    def startpHandDOSensing(self):
        pHandDOSensor = pHandDOSensors()
        while self.turnOffpHandDOSensing == False:
            pH = pHandDOSensor.pH()
            DO = pHandDOSensor.DO()
            self.pHandDOSignal.emit(pH,DO)
            time.sleep(2)

    def startMainSwitchSensing(self):
        self.mainSwitchSensor = mainSwitchSensors()
        self.mainSwitchSensor.interruptSetUp(self.interruptedMainSwitch)
        while self.turnOffMainSwitchSensing == False:
            mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
            self.mainSwitchSignal.emit(mainSwitchStates)
            time.sleep(1)

    def startValveSwitchSensing(self):
        self.valveSwitchSensor = valveSwitchSensors()
        self.valveSwitchSensor.interruptSetUp(self.interruptedValveSwitch)
        while self.turnOffValveSwitchSensing == False:
            valveSwitchStates = self.valveSwitchSensor.allValveSwitchStates()
            self.valveSwitchSignal.emit(valveSwitchStates)
            time.sleep(1)

    def turnOffAlarm(self):
        self.alarmControl.alarm = 0

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
        #Stores the temp values so that they can be polled by the PID
        self.HLTTemp = tempValues[0]
        self.MLTTemp = tempValues[1]
        self.BLKTemp = tempValues[2]

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
        #print(autoValveStates)
        #print(valveSwitchStates)
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

        #Creates a list of the on valves based on the autoValveStates and ValveSwitchStates
        onValves = []
        #print(autoValveStates)
        for i in range(0,10):
            if valveSwitchStates[i] == "Auto":
                if autoValveStates[i] == 1: onValves.append(i+1)
            elif valveSwitchStates[i] == "On": onValves.append(i+1)

        onValves = tuple(onValves)
        #print(onValves)

        #if the valves are a known configuration, then assigns the relevant paths
        if onValves in self.valvesToPaths:
            if (onValves==(4,3,6,7,9) or onValves==(4,3,6,9)) and self.grainAdded == True:
                newPaths = [[2,3,4,5,6],[7,8,9,10,11,12,20]]
            else:
                newPaths = self.valvesToPaths[onValves]
        else: newPaths = [[],[]]

        #print(newPaths)

        #updates the stylesheets based on the new paths
        for i in range(0,25):
            if i+1 in newPaths[0]:
                for frame in self.pathsToFrames[i+1]:
                    #print(frame)
                    if self.frameTypes[frame] == "top":getattr(self,"frame_"+str(frame)).setStyleSheet(self.topWaterStyle)
                    elif self.frameTypes[frame] == "left": getattr(self,"frame_"+str(frame)).setStyleSheet(self.leftWaterStyle)
                    elif self.frameTypes[frame] == "left round": getattr(self,"frame_"+str(frame)).setStyleSheet(self.leftRoundWaterStyle)

                #for path 19, also change the chiller color (only needed for water and off, since no wort goes through the chiller's water coil)
                if i+1 == 19: self.chiller.setStyleSheet(self.chillerWaterStyle)
            elif i+1 in newPaths[1]:
                for frame in self.pathsToFrames[i+1]:
                    if self.frameTypes[frame] == "top": getattr(self,"frame_"+str(frame)).setStyleSheet(self.topWortStyle)
                    elif self.frameTypes[frame] == "left": getattr(self,"frame_"+str(frame)).setStyleSheet(self.leftWortStyle)
                    elif self.frameTypes[frame] == "left round": getattr(self,"frame_"+str(frame)).setStyleSheet(self.leftRoundWortStyle)
            else:
                for frame in self.pathsToFrames[i+1]:
                    if self.frameTypes[frame] == "top": getattr(self,"frame_"+str(frame)).setStyleSheet(self.topOffStyle)
                    elif self.frameTypes[frame] == "left": getattr(self,"frame_"+str(frame)).setStyleSheet(self.leftOffStyle)
                    elif self.frameTypes[frame] == "left round": getattr(self,"frame_"+str(frame)).setStyleSheet(self.leftRoundOffStyle)

                #for path 19, also change the chiller color (only needed for water and off, since no wort goes through the chiller's water coil)
                if i+1 == 19: self.chiller.setStyleSheet(self.chillerOffStyle)
                

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
        #Adds a message
        if mode == "Off":
            self.printAndSendMessage("Turning off heat to the {}".format(kettle),"message")
        else:
            if self.mainSwitchSensor.switchState('Master Heat') == "On":
                if mode == "SemiAuto":self.printAndSendMessage("Setting the {} to {:.0f}%".format(kettle,setting),"Message")
                if mode == "Auto":self.printAndSendMessage("Setting the {} to {:.0f} deg F".format(kettle,setting),"Message")
            else:
                self.printAndSendMessage("Error: Master heat is switched to off, but heat is turned on. Please turn on the master heat","Alarm")
                return
        
        #print(setting)
        if kettle == "HLT": 
            if mode == "Auto":
                self.kettleSetting = "HLT"
                #Turns off the BLK, and turns on the HLT
                self.UIToBLKPIDPipe.send(("mode","Off"))
                self.UIToHLTPIDPipe.send(("setPoint",setting))
                self.UIToHLTPIDPipe.send(("mode","Auto"))
                self.UIToHeatPipe.send(("kettle","HLT"))

                OldHLTText = self.HLT_Heat.text()
                NewHLTText=OldHLTText[:17]+"\nTarget temp: {:.0f}".format(setting)
                self.HLT_Heat.setText(NewHLTText)

                OldBLKText = self.BLK_Heat.text()
                NewBLKText=OldBLKText[:17]
                self.BLK_Heat.setText(NewBLKText)
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
            if mode == "Auto":
                self.kettleSetting = "BLK"
                #Turns off the BLK, and turns on the HLT
                self.UIToHLTPIDPipe.send(("mode","Off"))
                self.UIToBLKPIDPipe.send(("setPoint",setting))
                self.UIToBLKPIDPipe.send(("mode","Auto"))
                self.UIToHeatPipe.send(("kettle","BLK"))

                OldBLKText = self.BLK_Heat.text()
                NewBLKText=OldBLKText[:17]+"\nTarget temp: {:.0f}".format(setting)
                self.BLK_Heat.setText(NewBLKText)

                OldHLTText = self.HLT_Heat.text()
                NewHLTText=OldHLTText[:17]
                self.HLT_Heat.setText(NewHLTText)
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

    def startPhase(self,phase):
        #If currently staging a new phase, throws a warning
        if self.currentlyStagingPhase == True:
            self.printAndSendMessage("Warning: currently starting a new phase. Please wait a few seconds and try again. NOT starting phase {}".format(phase),"Warning")
            return
        #Creates and starts a staging thread with the proper phase
        threading.Thread(name='phaseStagingThread',target = self.phaseStaging,args=(phase,)).start()
    

    def phaseStaging(self,phase):
        #Stores the fact that staging is going on, and instructs the currently running phase to stop (if any)
        self.currentlyStagingPhase=True
        self.stopPhase = True

        #waits until no phase is running to start the new phase
        while self.phaseRunning != None:
            time.sleep(.1)

        #Updates the phase button colors
        if phase != None:
            for i in range(1,phase): getattr(self,"phase"+str(i)).setStyleSheet(self.pastPhaseStyle)
            getattr(self,"phase"+str(phase)).setStyleSheet(self.currentPhaseStyle)
            for i in range(phase+1,11): getattr(self,"phase"+str(i)).setStyleSheet(self.futurePhaseStyle)

        #creates and starts a thread for the new phase
        self.stopPhase = False
        self.phaseRunning = phase
        threading.Thread(name='phase'+str(phase)+'Thread',target = getattr(self,'startPhase'+str(phase))).start()

        #marks the staging as complete
        self.currentlyStagingPhase = False            
            
    def startPhase1(self):
        #checks that all needed parameters are set
        if self.HLT_Fill_1_Target.text()[-4:]!=" gal":
            self.messageSignal.emit("Error: HLT Fill 1 does not end in ' gal'. Press the phase 1 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return
       
        try:
            HLTFill1Target = float(self.HLT_Fill_1_Target.text()[:-4])
        except:
            self.messageSignal.emit("Error: HLT fill 1 appears to be invalid. Press the phase 1 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return


        #opens the valves to the correct state     
        self.PAVControl.valveStates = [1,0,1,0,0,0,1,0,0,0]

        #waits until the HLT is filled  
        while float(self.HLT_Vol.text()[:-4])<HLTFill1Target and self.stopPhase == False:
            time.sleep(.5)

        #for safety, closes valve 1 once filling is complete
        self.PAVControl.valveStates = [0,0,1,0,0,0,1,0,0,0]

        #Notes that this phase is complete (otherwise other phases won't start)
        self.phaseRunning = None

        #If it stopped naturally, then starts phase 2, otherwise sends an alarm
        if self.stopPhase == False:
            self.messageSignal.emit("Phase 1 complete! Beginning phase 2.","Success")
            self.startPhase(2)
        else: self.messageSignal.emit("Manually stopping phase 1","Alarm")

    def startPhase2(self):
        if self.Strike_Temp.text()[-2:]!=" F":
            print(self.Strike_Temp.text()[-2:])
            self.messageSignal.emit("Error: Strike Temp does not end in ' F'. Press the phase 2 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        try:
            strikeTempTarget = float(self.Strike_Temp.text()[:-2])
        except:
            self.messageSignal.emit("Strike Temp appears to be invalid. Press the phase 2 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        #checks that the current HLT tempurature is not an error
        if float(self.HLT_Heat.text()[14:17]) == 999 or float(self.HLT_Heat.text()[14:17]) == 0:
            self.messageSignal.emit("Error: HLT temperature seems to be invalid. Press the phase 2 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        #opens the valves to the correct state     
        self.PAVControl.valveStates = [0,0,1,1,0,0,1,0,0,0]

        #starts the water pump
        self.PAVControl.waterPump = 1

        #waits until the tempurature of the HLT reaches the strike temp
        while float(self.HLT_Heat.text()[14:17]) < strikeTempTarget and self.stopPhase == False:
            time.sleep(.5)

        #Notes that this phase is complete (otherwise other phases won't start)
        self.phaseRunning = None

        #If it stopped naturally, then starts phase 2, otherwise sends an alarm
        if self.stopPhase == False:
            self.messageSignal.emit("Phase 2 complete! Beginning phase 3.","Success")
            self.startPhase(3)
        else: self.messageSignal.emit("Manually stopping phase 1","Alarm")

        
            
        
            

    def closeEvent(self, *args, **kwargs):
        print("Beginning system shutdown")
        #Ends the current phase
        self.stopPhase = True
        
        #Closes all valves:
        for i in [1,11]: setattr(self.PAVControl,"valve"+str(i),0)

        #turns off pumps and aeration
        self.PAVControl.wortPump = 0
        self.PAVControl.waterPump = 0
        self.PAVControl.aeration = 0

        #turns off heat
        self.UIToHLTPIDPipe.send(("mode","Off"))
        self.UIToHLTPIDPipe.send(("stop",True))
        self.UIToBLKPIDPipe.send(("mode","Off"))
        self.UIToBLKPIDPipe.send(("stop",True))
        self.UIToHeatPipe.send(("kettle","None"))
        self.UIToHeatPipe.send(("heatSetting",0))
        self.UIToHeatPipe.send(("turnOff",True))

        #Turns off the sensors
        self.turnOffVolumeSensing = True
        self.turnOffTempSensing = True
        self.turnOffpHandDOSensing = True
        self.turnOffMainSwitchSensing = True
        self.turnOffValveSwitchSensing = True
        self.UIToFlowPipe.send(("turnOffSensor",True))

        #self.flowThread.exit()
        #self.volumeThread.exit()
        #self.tempThread.exit()
        #self.pHandDOThread.exit()
        #self.mainSwitchThread.exit()
        #self.valveSwitchThread.exit()
        #self.heatThread.exit()
        #self.HLTPIDThread.exit()
        #self.BLKPIDThread.exit()

        #time.sleep(10)
        #print(threading.enumerate())

        super(dashboard, self).closeEvent

        #hile len(threading.enumerate()) > 1:
            #time.sleep(1)

        #print("System exited successfully!")

    def beerSmithImportDialog(self):
        self.beerSmithImportDialog = importDialog(self.importSignal)
        self.printAndSendMessage("BeerSmith file imported successfully!","Success")

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
	
	
