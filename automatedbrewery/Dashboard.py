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

    importSignal = QtCore.pyqtSignal(list,list,list,list,list,list,float)

    heatGraphSignal = QtCore.pyqtSignal(float,float,str)

    messageSignal = QtCore.pyqtSignal(str,str)

    lockFieldSignal = QtCore.pyqtSignal(str,bool)
    actualValueSignal = QtCore.pyqtSignal(str,str)
    phaseButtonStylesSignal = QtCore.pyqtSignal(int)

    mashTimerSignal = QtCore.pyqtSignal(str)
    mashTimerUpdateSignal = QtCore.pyqtSignal(float)
    highlightMashStepSignal = QtCore.pyqtSignal(int)
    mashTimerTextSignal = QtCore.pyqtSignal(float)

    boilTimerSignal = QtCore.pyqtSignal(str)
    boilTimerUpdateSignal = QtCore.pyqtSignal(float)
    highlightBoilStepsSignal = QtCore.pyqtSignal(list)
    boilTimerTextSignal = QtCore.pyqtSignal(float)

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
        color:rgb(143,143,143);
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
        color:rgb(143,143,143) ;
    }'''

    futurePhaseStyle = '''
    QPushButton {
        border-radius: 0px;
        background-color: rgb(196,236,244);
        font: 12pt "Arial";
    }

    QPushButton::pressed {
        background-color: rgb(191,191,191);
        color: rgb(143,143,143);
    }'''

    lockedInputStyle = '''
    QLineEdit {
        background-color: rgb(229,229,229);
        font: 12pt "Arial";
    }'''

    unlockedInputStyle = '''
    QLineEdit {
        background-color: rgb(255,255,255);
        font: 12pt "Arial";
    }'''

    kettleWaterStyle = '''
    QProgressBar {
        border: 2px solid rgb(143,143,143);
        border-radius: 5px;
        border-top-color: white;
        text-align: top center;
        font: 12pt "Arial";
    }

    QProgressBar::chunk {
        background-color: rgb(0,138,205);
        height: 1px;
    }'''

    kettleWortStyle = '''
    QProgressBar {
        border: 2px solid rgb(143,143,143);
        border-radius: 5px;
        border-top-color: white;
        text-align: top center;
        font: 12pt "Arial";
    }

    QProgressBar::chunk {
        background-color: rgb(226,152,21);
        height: 1px;
    }'''

    redBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    redBrush.setColor(QtGui.QColor(203,34,91))

    greenBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    greenBrush.setColor(QtGui.QColor(7,155,132))

    whiteBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    whiteBrush.setColor(QtGui.QColor(255,255,255))

    blueBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    blueBrush.setColor(QtGui.QColor(196,236,244))

    lightGreyBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    lightGreyBrush.setColor(QtGui.QColor(191,191,191))

    darkGreyBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    darkGreyBrush.setColor(QtGui.QColor(143,143,143))

    blackBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
    blackBrush.setColor(QtGui.QColor(0,0,0))



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
                     (1,8):[[1,2,23,25],[]],
                     (1,3,7):[[1,2,23,25],[]],
                     (3,4,7):[[2,3,4,5,6],[]],
                     (3,4):[[2,3,4,5,6],[]],
                     (4,5,7,8):[[3,4,5,7,21,22],[]],
                     (4,5,7):[[3,4,5,7,21,22],[]],
                     (4,5):[[3,4,5,7,21,22],[]],
                     (4,5,8):[[3,4,5,7,21,22],[]],
                     (3,4,6,7,9):[[2,3,4,5,6,7,8,9,10,11,12,20],[]],
                     (3,4,6,9):[[2,3,4,5,6,7,8,9,10,11,12,20],[]],
                     (3,7,8,9):[[],[8,9,10,13,14,20]],
                     (7,8,9):[[],[8,9,10,13,14,20]],
                     (4,5,7,8):[[3,4,5,7,21,22],[8,9,10,13,14,20]],
                     (2,8,10):[[1,19,24],[10,13,15,16,17,18,20]],
                     (8,10):[[],[10,13,15,16,17,18,20]],
                     (1,4,5,8):[[1,2,3,4,5,7,21,22,23,25],[]],
                     (1,4,5):[[1,2,3,4,5,7,21,22,23,25],[]],
                     (6,9):[[7,8,9,10,11,12,20],[]],
                     (8,9):[[8,9,10,13,17,18,20],[]]
    }

    #Defines the list of targets and actuals
    targets = ["HLT_Fill_1_Target","Strike_Target","HLT_Fill_2_Target","Sparge_Target","Pre_Boil_Target","Post_Boil_Target","Fermenter_Target","Strike_Temp","HLT_Fill_2_Temp","Sparge_Temp"]
    actuals = ["HLT_Fill_1_Actual","Strike_Actual","HLT_Fill_2_Actual","Sparge_Actual","Pre_Boil_Actual","Post_Boil_Actual","Fermenter_Actual"]
                                    

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
        self.lockFieldSignal.connect(self.lockField)
        self.actualValueSignal.connect(self.setActualValue)
        self.phaseButtonStylesSignal.connect(self.setPhaseButtonStyles)
        self.mashTimerSignal.connect(self.startMashTimer)
        self.mashTimerUpdateSignal.connect(self.updateMashTimerText)
        self.highlightMashStepSignal.connect(self.highlightCurrentMashStep)
        self.mashTimerTextSignal.connect(self.updateMashTimerText)
        self.boilTimerSignal.connect(self.startBoilTimer)
        self.boilTimerUpdateSignal.connect(self.updateBoilTimerText)
        self.highlightBoilStepsSignal.connect(self.highlightCurrentBoilStep)
        self.boilTimerTextSignal.connect(self.updateBoilTimerText)

        #Starts up the UI and sets some default states
        self.setupUi(self)
        self.Messages.clear()
        self.Messages.setWordWrap(True)

        #Sets default phase button styles
        for i in range(1,11):
            getattr(self,"phase"+str(i)).setStyleSheet(self.futurePhaseStyle)

        #Sets default input styles
        for target in self.targets:
            getattr(self,target).setStyleSheet(self.unlockedInputStyle)
            getattr(self,target).setReadOnly(False)

        for actual in self.actuals:
            getattr(self,actual).setStyleSheet(self.lockedInputStyle)
            getattr(self,actual).setReadOnly(True)

        #Sets default kettle styles
        self.HLT.setStyleSheet(self.kettleWaterStyle)
        self.MLT.setStyleSheet(self.kettleWaterStyle)
        self.BLK.setStyleSheet(self.kettleWortStyle)        
           
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

        #Defaults the mash schedule to be empty, and the mash start time to empty
        self.mashSchedule = None
        self.mashStartTime = None
        self.stopMashTimer = False
        self.mashPauseTime = 0
        self.latestMashTime = 0

        #Defaults the boil schedule to be empty, and the mash start time to empty
        self.boilSchedule = None
        self.boilStartTime = None
        self.stopBoilTimer = False
        self.boilPauseTime = 0
        self.latestBoilTime = 0

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
        self.HLTFlowIn = flowRateValues[0][1][-1]
        self.HLTFlowOut = flowRateValues[1][1][-1]
        self.MLTFlowIn = flowRateValues[2][1][-1]
        self.MLTFlowOut = flowRateValues[3][1][-1]
        self.BLKFlowIn = flowRateValues[4][1][-1]
        self.BLKFlowOut = flowRateValues[5][1][-1]
        
        self.HLT_In.setText("{:.2f} g/m".format(flowRateValues[0][1][-1]))
        self.HLT_Out.setText("{:.2f} g/m".format(flowRateValues[1][1][-1]))
        self.MLT_In.setText("{:.2f} g/m".format(flowRateValues[2][1][-1]))
        self.MLT_Out.setText("{:.2f} g/m".format(flowRateValues[3][1][-1]))
        self.BLK_In.setText("{:.2f} g/m".format(flowRateValues[4][1][-1]))
        self.BLK_Out.setText("{:.2f} g/m".format(flowRateValues[5][1][-1]))

    def volumeUpdate(self, volumeValues):
        #stores the numerical values for easier reading
        self.HLTVolume = volumeValues[0]
        self.MLTVolume = volumeValues[1]
        self.BLKVolume = volumeValues[2]

        #Sets the text labels on the UI
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
        self.pHValue = pH
        self.DOValue = DO

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
        #print(self.grainAdded)

        #if the valves are a known configuration, then assigns the relevant paths
        #Has a few overrides for paths that are different if grains have or have not been added
        if onValves in self.valvesToPaths:
            if (onValves==(3,4,6,7,9) or onValves==(3,4,6,9)) and self.grainAdded == True:
                newPaths = [[2,3,4,5,6],[7,8,9,10,11,12,20]]
            elif onValves==(7,8,9) and self.grainAdded == False:
                newPaths = [[8,9,10,13,14,20],[]]
            elif onValves==(8,10)  and self.grainAdded == False:
                newPaths = [[10,13,15,16,17,18,20],[]]
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

        #updates the MLT kettle style if grains have been added
        if self.grainAdded == True:
            self.MLT.setStyleSheet(self.kettleWortStyle)
            self.BLK.setStyleSheet(self.kettleWortStyle)
                

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

    def getVolumeInput(self,inputToCheck):
        if getattr(self,inputToCheck).text()[-4:]!=" gal":
            self.messageSignal.emit("Error: {} does not end in ' gal'. Press the phase {} button once resolved to try again".format(inputToCheck,self.phaseRunning),"Alarm")
            self.phaseRunning = None
            return None
        try:
            result = float(getattr(self,inputToCheck).text()[:-4])
            return result
        except:
            self.messageSignal.emit("Error: {} appears to be invalid. Press the phase{} button once resolved to try again".format(inputToCheck,self.phaseRunning),"Alarm")
            self.phaseRunning = None
            return None

    def getTempInput(self,inputToCheck):
        if getattr(self,inputToCheck).text()[-2:]!=" F":
            self.messageSignal.emit("Error: {} does not end in ' F'. Press the phase {} button once resolved to try again".format(inputToCheck,self.phaseRunning),"Alarm")
            self.phaseRunning = None
            return None
        try:
            result = float(getattr(self,inputToCheck).text()[:-2])
            return result
        except:
            self.messageSignal.emit("Error: {} appears to be invalid. Press the phase{} button once resolved to try again".format(inputToCheck,self.phaseRunning),"Alarm")
            self.phaseRunning = None
            return None

    def lockField(self,targetField,lock):
        if lock==True:
            getattr(self,targetField).setStyleSheet(self.lockedInputStyle)
            getattr(self,targetField).setReadOnly(True)
        elif lock==False:
            getattr(self,targetField).setStyleSheet(self.unlockedInputStyle)
            getattr(self,targetField).setReadOnly(False)

    def setActualValue(self,field,value):
        getattr(self,field).setText(value)

    def setPhaseButtonStyles(self,phase):
            for i in range(1,phase): getattr(self,"phase"+str(i)).setStyleSheet(self.pastPhaseStyle)
            getattr(self,"phase"+str(phase)).setStyleSheet(self.currentPhaseStyle)
            for i in range(phase+1,11): getattr(self,"phase"+str(i)).setStyleSheet(self.futurePhaseStyle)

    def startPhase(self,phase):
        #If currently staging a new phase, throws a warning
        if self.currentlyStagingPhase == True:
            self.messageSignal.emit("Warning: currently starting a new phase. Please wait a few seconds and try again. NOT starting phase {}".format(phase),"Warning")
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
            self.phaseButtonStylesSignal.emit(phase)

        #marks the staging as complete
        self.currentlyStagingPhase = False

        #creates and starts a thread for the new phase
        self.stopPhase = False
        self.phaseRunning = phase
        threading.Thread(name='phase'+str(phase)+'Thread',target = getattr(self,'startPhase'+str(phase))).start()
            
    def standardPhase(self,phase,phaseType,targetField,startValveStates,endValveStates,pumpAerationStates,kettle,endOfPhaseFlag):
        #Gets the input needed for the phase
        #If you give it a number (either int or float), then uses that target field
        if type(targetField) == float or type(targetField) == int : target = float(targetField)
        else:
            if phaseType == "Fill":
                startAmount = getattr(self,kettle+"Volume")
                fillAmount = self.getVolumeInput(targetField)
                if fillAmount != None:
                    target = startAmount + fillAmount
                else: target = None
            #For drain, you always give it a numerical target (usually 0), so if you passed a string, generates an error
            elif phaseType == "Drain": target = None
            elif phaseType == "Heat": target = self.getTempInput(targetField)
       
        #If failed to get the needed input, returns
        if target == None: return

        #Locks the inputs used
        if phaseType == "Fill" or phaseType == "Heat":
            if type(targetField) != float and type(targetField) != int:
                self.lockFieldSignal.emit(targetField,True)
        
        #For heat targets, checks that the temperature is not an error
        if phaseType == "Heat":
            if float(getattr(self,kettle+"_Heat").text()[14:17]) == 999 or float(getattr(self,kettle+"_Heat").text()[14:17]) == 0:
                self.messageSignal.emit("Error: {} temperature seems to be invalid. Press the phase {} button once resolved to try again".format(kettle,phase),"Alarm")
                self.phaseRunning = None
                return
            #If you are heating the MLT, then the HLT temperature also needs to be valid, since the HLT is the kettle being heated
            if kettle == "MLT":
                if float(self.HLT_Heat.text()[14:17]) == 999 or float(self.HLT_Heat.text()[14:17]) == 0:
                    self.messageSignal.emit("Error: HLT temperature seems to be invalid. Press the phase 6 button once resolved to try again","Alarm")
                    self.phaseRunning = None
                    return

        #If requirements not met, skips the remainder of the phase
        if self.phaseRunning != None:
            self.messageSignal.emit("Starting Phase {}".format(phase),"Message")

            #opens the valves to the correct state     
            self.PAVControl.valveStates = startValveStates

            #waits 5 seconds for the valves to change positions
            time.sleep(5)

            #starts the pumps
            self.PAVControl.waterPump = pumpAerationStates[0]
            self.PAVControl.wortPump = pumpAerationStates[1]
            self.PAVControl.aeration = pumpAerationStates[2]

            #For heat targets, turns on the heat. Note that if the MLT is being heated, we actually apply heat to the HLT (the MLT is heated though HERMS)
            if phaseType == "Heat":
                if kettle == "MLT":
                    self.setHeatSignal.emit("HLT","Auto",target)
                else:
                    self.setHeatSignal.emit(kettle,"Auto",target)

            #For drains, waits 5 seconds before starting the check to give it a chance to have a flow
            if phaseType == "Drain": time.sleep(5)

            #Waits until target is hit
            if phaseType == "Fill":  
                while getattr(self,kettle+"Volume")<target and self.stopPhase == False:
                    time.sleep(.5)
            elif phaseType == "Drain":
                while getattr(self,kettle+"FlowOut")>target and self.stopPhase == False:
                    time.sleep(.5)
            elif phaseType == "Heat":
                while getattr(self,kettle+"Temp")<target and self.stopPhase == False:
                    time.sleep(.5)

            #For drains, if the volume is still over two gallons, sends an alarm, since it is likely stuck.
            if phaseType == "Drain":
                if getattr(self,kettle+"Volume") >= 2: self.messageSignal.emit("Error: No more outflow from the {}, but {} volume is {:.2f}. Check if drain is stuck.".format(kettle,kettle,getattr(self,kettle+"Volume")),"Alarm")
       
            #For fills, stores the volume that was hit, and prints a message. For heat, just prints a message
            if phaseType == "Fill":
                if type(targetField) != float and type(targetField) != int: self.actualValueSignal.emit(targetField[:-6]+"Actual","{:.2f} gal".format(getattr(self,kettle+"Volume")-startAmount))
                self.messageSignal.emit("{} filled to {:.2f} gal".format(kettle,getattr(self,kettle+"Volume")),"Message")
            elif phaseType == "Heat":
                self.messageSignal.emit("{} heated to {:.0f} F".format(kettle,getattr(self,kettle+"Temp")),"Message")
            elif phaseType == "Drain":
                self.messageSignal.emit("No more outflow from {}. Current detected volume is {:.2f} gal.".format(kettle,getattr(self,kettle+"Volume")),"Message")
                

            #turns off the heat and pumps/aeration
            if kettle == "MLT":
                self.setHeatSignal.emit("HLT","Off",0)
            else:
                self.setHeatSignal.emit(kettle,"Off",0)
            self.PAVControl.waterPump = 0
            self.PAVControl.wortPump = 0
            self.PAVControl.aeration = 0

            #for safety, closes the valves to the endValveStates
            self.PAVControl.valveStates = endValveStates

            #Notes that this phase is complete (otherwise other phases won't start)
            self.phaseRunning = None

            #If it stopped naturally and flagged as end of phase, then starts next phase, otherwise sends an alarm
            if self.stopPhase == False and endOfPhaseFlag == True:
                self.messageSignal.emit("Phase {} complete! Beginning phase {}.\n".format(phase,phase+1),"Success")
                self.startPhase(phase+1)
            else: self.messageSignal.emit("Manually stopping phase {}".format(phase),"Alarm")

    def startPhase1(self):
        self.standardPhase(1,"Fill","HLT_Fill_1_Target",[1,0,1,0,0,0,1,0,0,0],[0,0,1,0,0,0,1,0,0,0],[0,0,0],"HLT",True)

    def startPhase2(self):
        self.standardPhase(2,"Heat","Strike_Temp",[0,0,1,1,0,0,1,0,0,0],[0,0,1,1,0,0,1,0,0,0],[1,0,0],"HLT",True)

    def startPhase3(self):
        self.standardPhase(3,"Fill","Strike_Target",[0,0,0,1,1,0,1,0,0,0],[0,0,1,1,1,0,1,0,0,0],[1,0,0],"MLT",True)

    def startPhase4(self):
        self.standardPhase(4,"Fill","HLT_Fill_2_Target",[1,0,1,0,0,0,1,0,0,0],[0,0,1,0,0,0,1,0,0,0],[0,0,0],"HLT",True)

    def startPhase5(self):
        self.standardPhase(5,"Heat","HLT_Fill_2_Temp",[0,0,1,1,0,1,1,0,1,0],[0,0,1,1,0,1,1,0,1,0],[1,1,0],"MLT",False)
        self.messageSignal.emit("Add grains and adjust pH as needed. Once ready to continue, press the phase 6 button","Warning")
        self.alarmControl.alarm = 1

    def startPhase6(self):
        #Checks if a mash schedule has been defined
        if self.mashSchedule == None:
            self.messageSignal.emit("Error: No mash schedule has been imported. Press the phase 6 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        #Checks that the temperature in the HLT and the MLT is not an error
        if float(self.HLT_Heat.text()[14:17]) == 999 or float(self.HLT_Heat.text()[14:17]) == 0:
            self.messageSignal.emit("Error: HLT temperature seems to be invalid. Press the phase 6 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        if float(self.MLT_Heat.text()[14:17]) == 999 or float(self.MLT_Heat.text()[14:17]) == 0:
            self.messageSignal.emit("Error: MLT temperature seems to be invalid. Press the phase 6 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        #If requirements not met, skips the remainder of the phase
        if self.phaseRunning != None:
            self.messageSignal.emit("Starting Phase 6","Message")

            #Notes that grains have been added (all this does is change the color of the liquid flow on the dashboard)
            self.grainAdded = True

            #opens the valves to the correct state     
            self.PAVControl.valveStates = [0,0,1,1,0,1,1,0,1,0]

            #waits 5 seconds for the valves to change positions
            time.sleep(5)

            #starts the pumps
            self.PAVControl.waterPump = 1
            self.PAVControl.wortPump = 1
            self.PAVControl.aeration = 0

            #starts the mash timer
            self.mashTimerSignal.emit("Start")
            
            #goes through the mash schedule, adding water and heating as needed
            for step in range(0,len(self.mashSchedule)):
                #highlights the current mash step
                self.highlightMashStepSignal.emit(step)
                
                #sets the heat to the correct temperature for the step
                self.setHeatSignal.emit("HLT","Auto",self.mashSchedule[step][2])
                
                #for each step, starts by adding the correct amount of water, if needed (except for the first step, where this was completed in advance)
                if step != 0 and self.mashSchedule[step][1] != 0:
                    #sets the new volume target based on the current volume, and the mashSchedule
                    volumeTarget = self.MLTVolume + self.mashSchedule[step][1]

                    #turns off the pumps
                    self.PAVControl.waterPump = 0
                    self.PAVControl.wortPump = 0
                    self.PAVControl.aeration = 0

                    #changes the valves to a fill configuration
                    self.PAVControl.valveStates = [0,0,0,1,1,0,1,0,0,0]

                    #waits for the valves to change positions
                    time.sleep(5)

                    #turns on the water pump
                    self.PAVControl.waterPump = 1

                    #waits until the volume target is reached
                    while self.MLTVolume<volumeTarget and self.stopPhase == False:
                        time.sleep(.5)

                #waits until the target temp is reached
                while self.MLTTemp<self.mashSchedule[step][2] and self.stopPhase == False:
                    time.sleep(.5)

                self.messageSignal.emit("Reached temp for {} (step {}). Holding for {:.0f} min.".format(self.mashSchedule[step][0],step+1,self.mashSchedule[step][5]),"Message")

                #once temp has been reached, waits the length of the mash step
                endOfStep = self.latestMashTime + 60*self.mashSchedule[step][5]
                while self.latestMashTime<endOfStep and self.stopPhase == False:
                    time.sleep(.5)

                #once the step is complete, sends a message
                self.messageSignal.emit("{} complete (step {}). Beginning next mash step.".format(self.mashSchedule[step][0],step+1),"Success")

            self.highlightMashStepSignal.emit(len(self.mashSchedule))
            
            #Stops the mash timer (uses pause to preserve the time)
            self.mashTimerSignal.emit("Pause")

            #turns off the heat and pumps/aeration
            self.setHeatSignal.emit("HLT","Off",0)
            self.PAVControl.waterPump = 0
            self.PAVControl.wortPump = 0
            self.PAVControl.aeration = 0

            #Notes that this phase is complete (otherwise other phases won't start)
            self.phaseRunning = None

            #If it stopped naturally, then starts next phase, otherwise sends an alarm
            if self.stopPhase == False:
                self.messageSignal.emit("Phase 6 complete! Beginning phase 7.\n","Success")
                self.startPhase(7)
            else: self.messageSignal.emit("Manually stopping phase 6","Alarm")

    def startPhase7(self):
        #Gets the input needed for the phase
        spargeAmount = self.getVolumeInput("Sparge_Target")
        BLKStartAmount = self.BLKVolume
        HLTStartAmount = self.HLTVolume
        if spargeAmount != None:
            targetVolume = BLKStartAmount + spargeAmount
        else:
            targetVolume = None
            self.phaseRunning = None
            return

        spargeTemp = self.getTempInput("Sparge_Temp")

        #If failed to get the needed inputs, returns
        if targetVolume == None or spargeTemp == None: return

        #Locks the inputs used
        self.lockFieldSignal.emit("Sparge_Target",True)
        self.lockFieldSignal.emit("Sparge_Temp",True)

        #Checks that the HLT and MLT temperatures are not errors
        if float(self.HLT_Heat.text()[14:17]) == 999 or float(self.HLT_Heat.text()[14:17]) == 0:
            self.messageSignal.emit("Error: HLT temperature seems to be invalid. Press the phase 7 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        if float(self.MLT_Heat.text()[14:17]) == 999 or float(self.MLT_Heat.text()[14:17]) == 0:
            self.messageSignal.emit("Error: MLT temperature seems to be invalid. Press the phase 7 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        #If requirements not met, skips the remainder of the phase
        if self.phaseRunning != None:
            self.messageSignal.emit("Starting Phase 7","Message")

            #opens the valves to start the mash-out    
            self.PAVControl.valveStates = [0,0,1,1,0,1,1,0,1,0]

            #waits 5 seconds for the valves to change positions
            time.sleep(5)

            #starts the pumps
            self.PAVControl.waterPump = 1
            self.PAVControl.wortPump = 1
            self.PAVControl.aeration = 0

            #Turn on the heat
            self.setHeatSignal.emit("HLT","Auto",spargeTemp)

            #Waits until target is hit
            while self.MLTTemp<spargeTemp and self.stopPhase == False:
                time.sleep(.5)

            #Sends a message that the mash-out temperature has been reached
            self.messageSignal.emit("Achieved mash-out temp of {}. Beginning sparge.".format(spargeTemp),"Success")

            #Turns off the pumps
            self.PAVControl.waterPump = 0
            self.PAVControl.wortPump = 0

            #Changes the valves to the intial sparge positions to let the tubing fill
            self.PAVControl.valveStates = [0,0,0,1,1,0,1,1,1,0]
            time.sleep(10)

            #Closes valves 5 and 9 (these will be the ones that are used to control sparge rate)
            self.PAVControl.valveStates = [0,0,0,1,0,0,1,1,0,0]
            time.sleep(5)

            #Partially opens valves 5 and 9 (two seconds, or approximately halfway)
            self.PAVControl.partialOpenClose(5,2)
            self.PAVControl.partialOpenClose(9,2)

            #Turns on the pumps
            self.PAVControl.waterPump = 1
            self.PAVControl.wortPump = 1

            #Begins sparge
            counter=0
            lastFiveMLTFlowOut=[]
            lastFiveBLKFlowIn=[]
            targetFlowRate = .2
            valveChangeMultiplier = 10
            while self.BLKVolume<targetVolume and self.stopPhase == False:
                time.sleep(1)
                if counter!=5:
                    #Records the last flow rate
                    lastFiveMLTFlowOut.append(self.MLTFlowOut)
                    lastFiveBLKFlowIn.append(self.BLKFlowIn)
                    counter += 1
                else:
                    #Every five seconds, compares the flow rate average to the target, and adjusts the valves
                    #Uses a 10:1 calculation to adjust flow rate - if the rate is off by .1 gal/min, opens the
                    #Valve for 1 second
                    MLTFlow = sum(lastFiveMLTFlowOut)/len(lastFiveMLTFlowOut)
                    MLTFlowError = targetFlowRate - MLTFlow
                    MLTCorrection = MLTFlowError*valveChangeMultiplier
                    #Doesn't change the value if change is less than .25 sec, to reduce impact on relays
                    if abs(MLTCorrection)>.25:
                        self.PAVControl.partialOpenClose(5,MLTCorrection)

                    BLKFlow = sum(lastFiveBLKFlowIn)/len(lastFiveBLKFlowIn)
                    BLKFlowError = targetFlowRate - BLKFlow
                    BLKCorrection = BLKFlowError*valveChangeMultiplier
                    if abs(BLKCorrection)>.25:
                        self.PAVControl.partialOpenClose(9,BLKCorrection)

                    #Resets the flow values and counter
                    lastFiveMLTFlowOut=[]
                    lastFiveBLKFlowIn=[]
                    counter=0

            #Since sparge is complete, fully closes valves 5 and 9, and turns off the pumps
            self.PAVControl.waterPump = 0
            self.PAVControl.wortPump = 0
            self.PAVControl.fullyOpenClose(5,0)
            self.PAVControl.fullyOpenClose(9,0)

            #Notes that this phase is complete (otherwise other phases won't start)
            self.phaseRunning = None

            #If it stopped naturally, then starts next phase, otherwise sends an alarm
            if self.stopPhase == False:
                #stores the sparge and pre-boil volume and prints a message
                self.actualValueSignal.emit("Sparge_Actual","{:.2f} gal".format(HLTStartAmount-self.HLTVolume))
                self.actualValueSignal.emit("Pre_Boil_Actual","{:.2f} gal".format(self.BLKVolume))
                self.messageSignal.emit("BLK filled to {:.2f} gal using {:.2f} gal of sparge water ".format(self.BLKVolume,HLTStartAmount-self.HLTVolume),"Message")
                self.messageSignal.emit("Phase 7 complete! Beginning phase 8.\n","Success")
                self.startPhase(8)
            else: self.messageSignal.emit("Manually stopping phase 7","Alarm")

    def startPhase8(self):
        BLKStartVolume = self.BLKVolume

        if self.boilSchedule == None:
            self.messageSignal.emit("Error: No boil schedule has been imported. Press the phase 8 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return

        if self.Boil_Time.text()[-4:]!=" min":
            self.messageSignal.emit("Error: Boil time does not end in ' min'. Press the phase 8 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return
        try:
            boilTime = float(self.Boil_Time.text()[:-4])
        except:
            self.messageSignal.emit("Error: Boil time appears to be invalid. Press the phase 8 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return
        
        #For heat targets, checks that the BLK temperature is not an error
        if float(self.BLK_Heat.text()[14:17]) == 999 or float(self.BLK_Heat.text()[14:17]) == 0:
            self.messageSignal.emit("Error: BLK temperature seems to be invalid. Press the phase 8 button once resolved to try again","Alarm")
            self.phaseRunning = None
            return            

        #If requirements not met, skips the remainder of the phase
        if self.phaseRunning != None:
            self.messageSignal.emit("Starting Phase 8","Message")

            #opens the valves to the correct state     
            self.PAVControl.valveStates = [0,0,0,0,0,0,1,1,0,0]

            #waits 5 seconds for the valves to change positions
            time.sleep(5)

            #makes sure the pumps are off
            self.PAVControl.waterPump = 0
            self.PAVControl.wortPump = 0
            self.PAVControl.aeration = 0

            #To get to boiling as quickly as possible, turns on the heat to 100%.
            self.setHeatSignal.emit("BLK","SemiAuto",100)

            #Waits until we hit near a boil (208 F), when it will alarm
            while self.BLKTemp<208 and self.stopPhase == False:
                time.sleep(.5)

            self.messageSignal.emit("Approaching boil. Add fermcap if you haven't yet, or watch for boil overs","Warning")
            self.alarmControl.alarm = 1

            #Waits for boil (212 F), when it will start the timer and reduce heat to 80% 
            while self.BLKTemp<212 and self.stopPhase == False:
                time.sleep(.5)

            self.messageSignal.emit("Reached boil - reducing heat to 85%. Add additions if needed.","Warning")
            self.alarmControl.alarm = 1
            self.setHeatSignal.emit("BLK","SemiAuto",85)
            self.boilTimerSignal.emit("Start")

            #Alarms whenever an addition is needed in 2 minutes, and turns off heat at the end of the boil
            alarmedSteps = 0
            additionNum = 1
            while self.latestBoilTime<60*boilTime and self.stopPhase == False:
                #If the next step is in next than 2 minutes, send an alarm
                #Stores the time in a variable, to prevent the unlikely situation where a step is missed due to code execution time
                currentBoilTime = self.latestBoilTime/60
                #Stops checking for two minute warnings once you have reached the last step
                if alarmedSteps < len(self.boilSchedule):
                    if (self.boilSchedule[alarmedSteps][1]-2) < currentBoilTime:
                        if self.boilSchedule[alarmedSteps][1] != 0:
                            self.messageSignal.emit("2 minute warning for addition #{} at {:.0f} mins".format(additionNum,self.boilSchedule[alarmedSteps][1]),"Warning")
                            self.alarmControl.alarm = 1
                        else:
                            self.messageSignal.emit("Add 0 minute additions","Warning")
                            self.alarmControl.alarm = 1
                        #Count the number of rows that will be added in this addition, and add them to the number of alarmed steps
                        if alarmedSteps < len(self.boilSchedule):
                            while (self.boilSchedule[alarmedSteps][1]-2) < currentBoilTime:
                                alarmedSteps += 1
                                if alarmedSteps == len(self.boilSchedule):
                                    break

                        #adds one to the addition number
                        additionNum += 1

                #Sends a signal to highlight the correct rows
                highlightData = []
                #print(self.latestBoilTime)
                for i in range(0,len(self.boilSchedule)):
                    if 60*self.boilSchedule[i][1] <= self.latestBoilTime: highlightData.append("Grey")
                    elif 60*self.boilSchedule[i][1] - 120 <= self.latestBoilTime: highlightData.append("Blue")
                    else: highlightData.append("White")
                self.highlightBoilStepsSignal.emit(highlightData)
                time.sleep(1)

            #Sends a signal to grey out all of the additions
            highlightData = ["Grey"]*len(self.boilSchedule)
            self.highlightBoilStepsSignal.emit(highlightData)

                        
            #Sends the post-boil volume to the UI, and sends a message
            self.actualValueSignal.emit("Post_Boil_Actual","{:.2f} gal".format(self.BLKVolume))
            self.messageSignal.emit("Boil complete. Post boil volume is {:.2f} gal".format(self.BLKVolume),"Message")

            #Stops the mash timer (uses pause to preserve the time)
            self.boilTimerSignal.emit("Pause")

            #turns off the heat and pumps/aeration, just in case
            self.setHeatSignal.emit("BLK","Off",0)
            self.PAVControl.waterPump = 0
            self.PAVControl.wortPump = 0
            self.PAVControl.aeration = 0

            #Notes that this phase is complete (otherwise other phases won't start)
            self.phaseRunning = None

            #If it stopped naturally, then starts next phase, otherwise sends an alarm
            if self.stopPhase == False:
                self.messageSignal.emit("Phase 8 complete! Beginning phase 9.\n","Success")
                self.startPhase(9)
            else: self.messageSignal.emit("Manually stopping phase 8","Alarm")

    def startPhase9(self):
        #Checks that the DO target is valid
        try:
            DOTarget = float(self.DO_target.text())
        except:
            self.stopPhase = True
            self.messageSignal.emit("Error: Dissolved Oxygen (DO) target appears to be invalid. Press the phase 9 button once resolved to try again","Alarm")

        #Drains the BLK
        self.standardPhase(9,"Drain",0,[0,1,0,0,0,0,0,1,0,1],[0,1,0,0,0,0,0,1,0,0],[0,1,0],"BLK",False)
        
        #Starts the aeration
        self.messageSignal.emit("Drain complete! Beginning aeration of wort in fermenter","Success")

        self.PAVControl.aeration = 1

        #Waits for aeration to hit target
        while self.DOValue<DOTarget and self.stopPhase == False:
            time.sleep(.5)

        #After this, the  brew day is complete! Sends a message, and an alarm
        #Note that it does not start the cleaning phase, since you need to move 
        #the outlet hose to the drain (also remove the grain from the MLT)
        self.messageSignal.emit("BREWING COMPLETE! Once MLT grain has been removed, and wort chiller out hose is connected to the sink (was connected to fermenter), press phase 10 to start cleaning cycle.","Success")
        self.alarmControl.alarm = 1

    def startPhase10(self):
        #Since it is a cleaning cycle, no grain should be added (only impacts color of liquid paths)
        self.grainAdded = False
        self.BLK.setStyleSheet(self.kettleWaterStyle)
        
        #Warns the brewer that they should switch the tap to hot water
        self.messageSignal.emit("Warning: for cleaning, switch tap to hot water","Warning")
        
        #Repeats the cleaning cycle until stopPhase is triggered
        while self.stopPhase == False:
            #First fills the HLT
            self.standardPhase("10a","Fill",max(8-self.HLTVolume,0),[1,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0,0],[0,0,0],"HLT",False)
            self.messageSignal.emit("Done filling the HLT. Now filling the MLT.","Message")
            
            #Then fills the MLT
            self.standardPhase("10b","Fill",max(8-self.MLTVolume,0),[0,0,0,1,1,0,0,1,0,0],[0,0,0,1,1,0,0,1,0,0],[1,0,0],"MLT",False)
            self.messageSignal.emit("Done filling the MLT. Now cycling the water in the MLT for 5 minutes","Message")

            #Cycles the water in the MLT for 5 minutes
            self.messageSignal.emit("Starting phase 10c","Message")
            self.PAVControl.valveStates = [0,0,0,0,0,1,0,0,1,0]
            time.sleep(5)
            self.PAVControl.wortPump = 1
            totalSleepTime = 0
            while totalSleepTime < 300 and self.stopPhase == False:
                time.sleep(1)
                totalSleepTime += 1

            #Drains the MLT
            self.standardPhase("10d","Drain",0,[0,0,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,1,1,0],[0,1,0],"MLT",False)

            #Fills the HLT again
            self.standardPhase("10e","Fill",max(8-self.HLTVolume,0),[1,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0,0],[0,0,0],"HLT",False)
            self.messageSignal.emit("Done filling the HLT. Now filling the MLT.","Message")

            #Then fills the MLT again
            self.standardPhase("10f","Fill",max(8-self.MLTVolume,0),[0,0,0,1,1,0,0,1,0,0],[0,0,0,1,1,0,0,1,0,0],[1,0,0],"MLT",False)
            self.messageSignal.emit("Done filling the MLT. Now filling the BLK.","Message")

            #Then fills the BLK
            self.standardPhase("10g","Fill",max(8-self.BLKVolume,0),[0,0,0,0,0,0,1,1,1,0],[0,0,0,0,0,0,1,1,1,0],[0,1,0],"BLK",False)
            self.messageSignal.emit("Done filling the BLK. Now draining the BLK","Message")

            #Then drains the BLK
            self.standardPhase("10h","Drain",0,[0,0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,1,0,1],[0,1,0],"BLK",False)
            self.messageSignal.emit("Done with a cleaning cycle. This will continue until you hit pause. Waiting 1 minute before next cycle","Warning")
            self.alarmControl.alarm = 1

            totalSleepTime = 0
            while totalSleepTime < 60 and self.stopPhase == False:
                time.sleep(1)
                totalSleepTime += 1
                        
                   

        
    def startMashTimer(self,command):
        if command == "Start":
            self.mashStartTime = time.time()
            threading.Thread(name='mashTimerThread',target = self.mashTimer).start()
        elif command == "Reset":
            self.mashStartTime = time.time()
            self.mashPauseTime = 0
        elif command == "Pause":
            self.stopMashTimer = True
            self.mashPauseTime = self.latestMashTime

    def mashTimer(self):
        while self.stopMashTimer == False:
            self.latestMashTime = self.mashPauseTime + time.time() - self.mashStartTime
            self.mashTimerTextSignal.emit(self.latestMashTime)
            time.sleep(1)

    def updateMashTimerText(self,latestMashTime):
        hours = int(latestMashTime/3600)
        minutes = int((latestMashTime%3600)/60)
        seconds = int(latestMashTime%60)
        self.Mash_Timer.setText("{} hrs {} mins {} secs".format(hours,minutes,seconds))

    def startBoilTimer(self,command):
        if command == "Start":
            self.boilStartTime = time.time()
            threading.Thread(name='boilTimerThread',target = self.boilTimer).start()
        elif command == "Reset":
            self.boilStartTime = time.time()
            self.boilPauseTime = 0
        elif command == "Pause":
            self.stopBoilTimer = True
            self.boilPauseTime = self.latestBoilTime

    def boilTimer(self):
        while self.stopBoilTimer == False:
            self.latestBoilTime = self.boilPauseTime + time.time() - self.boilStartTime
            self.boilTimerTextSignal.emit(self.latestBoilTime)
            time.sleep(1)

    def updateBoilTimerText(self,latestBoilTime):
        hours = int(latestBoilTime/3600)
        minutes = int((latestBoilTime%3600)/60)
        seconds = int(latestBoilTime%60)
        self.Boil_Timer.setText("{} hrs {} mins {} secs".format(hours,minutes,seconds))

    def highlightCurrentMashStep(self,stepNum):
        if stepNum < len(self.mashSchedule):
            #changes the prior steps to dark grey on light grey 
            for step in range(0,stepNum):
                for i in range(0,5):
                    self.Mash_Steps.item(step,i).setForeground(self.darkGreyBrush)
                    self.Mash_Steps.item(step,i).setBackground(self.lightGreyBrush)

            #changes the current step to black on blue       
            for i in range(0,5):
                self.Mash_Steps.item(stepNum,i).setForeground(self.blackBrush)
                self.Mash_Steps.item(stepNum,i).setBackground(self.blueBrush)

            #changes the future steps to black on white    
            for step in range(stepNum+1,len(self.mashSchedule)):
                for i in range(0,5):
                    self.Mash_Steps.item(step,i).setForeground(self.blackBrush)
                    self.Mash_Steps.item(step,i).setBackground(self.whiteBrush)
        elif stepNum == len(self.mashSchedule):
            #changes all steps to dark grey on light grey 
            for step in range(0,stepNum):
                for i in range(0,5):
                    self.Mash_Steps.item(step,i).setForeground(self.darkGreyBrush)
                    self.Mash_Steps.item(step,i).setBackground(self.lightGreyBrush)
        else:
            #If you send something larger than the length of the mash schedule, then resets everything
            for step in range(0,stepNum):
                for i in range(0,5):
                    self.Mash_Steps.item(step,i).setForeground(self.blackBrush)
                    self.Mash_Steps.item(step,i).setBackground(self.whiteBrush)

    def highlightCurrentBoilStep(self,highlightData):
        for i in range(0,len(self.boilSchedule)):
            if highlightData[i] == "Grey":
                for j in range(0,3):
                    self.Boil_Steps.item(i,j).setForeground(self.darkGreyBrush)
                    self.Boil_Steps.item(i,j).setBackground(self.lightGreyBrush)
            if highlightData[i] == "Blue":
                for j in range(0,3):
                    self.Boil_Steps.item(i,j).setForeground(self.blackBrush)
                    self.Boil_Steps.item(i,j).setBackground(self.blueBrush)
            if highlightData[i] == "White":
                for j in range(0,3):
                    self.Boil_Steps.item(i,j).setForeground(self.blackBrush)
                    self.Boil_Steps.item(i,j).setBackground(self.whiteBrush)   
           
    def closeEvent(self, *args, **kwargs):
        print("Beginning system shutdown")
        #Ends the current phase
        self.stopPhase = True
        
        #Closes all valves:
        self.PAVControl.fullyOpenClose(5,0)
        self.PAVControl.fullyOpenClose(9,0)
        self.PAVControl.valveStates = [0,0,0,0,0,0,0,0,0,0]

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

        #Stops the mash and boil timers
        self.stopMashTimer = True
        self.stopBoilTimer = True

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

    def beerSmithImport(self,volumeValues,tempValues,boilSchedule,dryHopSchedule,mashSchedule,pHValues,boilTime):
        self.clearData()
        
        self.volumeValues = volumeValues
        self.tempValues = tempValues
        self.boilSchedule = boilSchedule
        self.dryHopSchedule = dryHopSchedule
        self.mashSchedule = mashSchedule
        self.pHValues = pHValues
        self.boilTime = boilTime

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

        #Updates the boil time
        self.Boil_Time.setText("{:.0f} min".format(self.boilTime))                  

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
        #print(self.mashSchedule)
        
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

        #Updates the pH and boil time
        self.pH_target.setText("")
        self.Boil_Time.setText("")

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
	
	
