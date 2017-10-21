from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
import time
import threading
from multiprocessing import Pipe
import sys
import pickle

#imports sensor modules
from MainSwitchSensor import mainSwitchSensors
from RTDSensor import tempSensors

#imports control modules
from AlarmControl import AlarmController
from HeatControl import HeatController
from PID import PID

#Loads the qtCreator file
qtCreatorFile = "../UI/AutomatedBreweryUI/StillDashboard.ui"
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
        self.setHeatSignal.emit(self.kettle,self.HeatMode.currentText(),heatSetting,self.kettle)
        self.close()

    def cancel(self): self.close()

class dashboard(QtWidgets.QMainWindow, Ui_MainWindow):
    #Creates the signals used to pull data from sensors and controllers
    tempSignal = QtCore.pyqtSignal(list)
    mainSwitchSignal = QtCore.pyqtSignal(list)
    setHeatSignal = QtCore.pyqtSignal(str,str,int,str)
    heatGraphSignal = QtCore.pyqtSignal(float,float,str)
    messageSignal = QtCore.pyqtSignal(str,str)

    
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

    
    #Creates the pipes used to talk to the control modules
    heatToHLTPIDPipe, HLTPIDToHeatPipe = Pipe()
    UIToHLTPIDPipe, HLTPIDToUIPipe = Pipe()
    UIToHeatPipe, heatToUIPipe = Pipe()

    def __init__(self):
        super(dashboard, self).__init__()
        
        #Sets global pyqtgraph settings
        pyqtgraph.setConfigOption('background', 'w')
        pyqtgraph.setConfigOption('foreground', 'k')

        #connects the signals to their respective functions
        self.tempSignal.connect(self.tempUpdate)
        self.mainSwitchSignal.connect(self.mainSwitchUpdate)
        self.setHeatSignal.connect(self.setHeat)
        self.heatGraphSignal.connect(self.updateHeatGraph)
        self.messageSignal.connect(self.printAndSendMessage)

        #Starts up the UI and sets some default states
        self.setupUi(self)
        self.Messages.clear()
        self.Messages.setWordWrap(True)      
           
        self.show()

        #Sets all of the sensor threads to keep sensing
        self.turnOffTempSensing = False
        self.turnOffMainSwitchSensing = False


        #Creates threads for each of the sensors and controllers
        self.HLTPIDThread = threading.Thread(name='HLTPIDThread',target = self.startHLTPID)
        self.heatThread = threading.Thread(name='heatThread',target = self.startHeatControl)        
        self.tempThread = threading.Thread(name='tempThread',target = self.startTempSensing)
        self.mainSwitchThread = threading.Thread(name='mainSwitchThread',target = self.startMainSwitchSensing)

        #Connects the heat buttons
        self.Heat_Other.clicked.connect(lambda: self.setHeatPopup("HLT"))
        self.Heat_100.clicked.connect(lambda:self.presetHeat(100))
        self.Heat_50.clicked.connect(lambda:self.presetHeat(50))
        self.Heat_off.clicked.connect(lambda:self.presetHeat(0))

        #Connects the alarm off button
        self.Turn_Off_Alarm.clicked.connect(self.turnOffAlarm)

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

        #Sets the system parameters
        self.boilWarningTemp = 208
        self.boilTemp = 212
        self.boilHeatLevel = 50
     
        #Starts the above threads
        self.tempThread.start()
        self.mainSwitchThread.start()
        self.heatThread.start()

        self.startAlarmControl()
        self.HLTPIDThread.start()

    def printAndSendMessage(self,message,messageType):
        print(message)
        self.newMessage(message,messageType)

    def newMessage(self,message,messageType):
        newmessage = QtWidgets.QListWidgetItem(self.Messages)
        newmessage.setText(message)

        if "Alarm" in messageType:
            newmessage.setBackground(self.redBrush)
            newmessage.setForeground(self.whiteBrush)
            self.alarmControl.alarm = 1
        elif messageType == "Warning": newmessage.setForeground(self.redBrush)
        elif messageType == "Success": newmessage.setForeground(self.greenBrush)

        if messageType == "HLT Heat Alarm": self.setHeatSignal.emit("HLT","Off",0,"HLT")
        if messageType == "BLK Heat Alarm": self.setHeatSignal.emit("BLK","Off",0,"HLT")

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
        self.HLTPID.integralWindupBlocker=True
        #self.HLTPID.semiAutoValue = 0
        self.HLTPID.mode = "Off"
        #self.HLTPID.tempGraphSignal = self.tempSignal
        self.HLTPID.run()
        
    def startHeatControl(self):
        heatCtrl = HeatController(pipeConn = self.heatToHLTPIDPipe,pipeConn2 = None,pipeConn3 = self.heatToUIPipe, heatGraphSignal = self.heatGraphSignal, dashboard = self, messageSignal = self.messageSignal,HLTSafeVolume = 0, BLKSafeVolume = 0)
        heatCtrl.run()

    def startAlarmControl(self):
        self.alarmControl = AlarmController()

    def startTempSensing(self):
        self.tempSensor = tempSensors()
        while self.turnOffTempSensing == False:
            temps = [self.tempSensor.HLTTemp(),self.tempSensor.MLTTemp(),self.tempSensor.BLKTemp()]
            self.tempSignal.emit(temps)
            time.sleep(1)

    def startMainSwitchSensing(self):
        self.mainSwitchSensor = mainSwitchSensors()
        self.mainSwitchSensor.interruptSetUp(self.interruptedMainSwitch)
        while self.turnOffMainSwitchSensing == False:
            mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
            self.mainSwitchSignal.emit(mainSwitchStates)
            time.sleep(1)

    def turnOffAlarm(self):
        self.alarmControl.alarm = 0

        
    def tempUpdate(self, tempValues):
        #Stores the temp values so that they can be polled by the PID
        self.BoilerTemp = tempValues[0]
        self.MidColTemp = tempValues[1]
        self.TopColTemp = tempValues[2]

        OldBoilerText = self.Boiler_Temp.text()
        OldMidColText = self.MidCol_Temp.text()
        OldTopColText = self.TopCol_Temp.text()

        if tempValues[0]>999:tempValues[0]=999
        if tempValues[1]>999:tempValues[1]=999
        if tempValues[2]>999:tempValues[2]=999

        if tempValues[0]<0:tempValues[0]=0
        if tempValues[1]<0:tempValues[1]=0
        if tempValues[2]<0:tempValues[2]=0

        NewBoilerText=OldBoilerText[:14]+"{: >6.2f}".format(int(round(tempValues[0])))+OldBoilerText[17:]
        NewMidColText=OldMidColText[:14]+"{: >6.2f}".format(int(round(tempValues[1])))+OldMidColText[17:]
        NewTopColText=OldTopColText[:14]+"{: >6.2f}".format(int(round(tempValues[2])))+OldTopColText[17:]

        self.Boiler_Temp.setText(NewBoilerText)
        self.MidCol_Temp.setText(NewMidColText)
        self.TopCol_Temp.setText(NewTopColText)

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

    def mainSwitchUpdate(self, mainSwitchValues):
        #Updates the heat select
        if mainSwitchValues[0]=="Auto":
            if self.kettleSetting == "HLT":
                self.Boiler_Heat.setStyleSheet(self.heatAutoOnStyle)
            if self.kettleSetting == "BLK":
                self.Boiler_Heat.setStyleSheet(self.heatAutoOffStyle)
            if self.kettleSetting == "None":
                self.Boiler_Heat.setStyleSheet(self.heatAutoOffStyle)
                
        if mainSwitchValues[0]=="BLK":
            self.Boiler_Heat.setStyleSheet(self.heatOffStyle)
        if mainSwitchValues[0]=="HLT":
            self.Boiler_Heat.setStyleSheet(self.heatOnStyle)

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
             
    def interruptedMainSwitch(self,pin):
        mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
        self.mainSwitchSignal.emit(mainSwitchStates)

    def interruptedValveSwitch(self,pin):
        valveSwitchStates = self.valveSwitchSensor.allValveSwitchStates()
        self.valveSwitchSignal.emit(valveSwitchStates)

    def setHeatPopup(self,kettle):
        self.tempPopup = tempPopup(self.setHeatSignal,kettle)

    def setHeat(self, kettle, mode, setting, inputKettle):
        #Adds a message
        if mode == "Off":
            self.printAndSendMessage("Turning off heat to the {}".format(kettle),"message")
        else:
            if self.mainSwitchSensor.switchState('Master Heat') == "On":
                if kettle == "HLT":
                    newKettle = "Boiler"
                else:
                    newKettle = kettle
                if mode == "SemiAuto":self.printAndSendMessage("Setting the {} to {:.0f}%".format(newKettle,setting),"Message")
                if mode == "Auto":self.printAndSendMessage("Heating the {} to get the {} to {:.0f} deg F".format(newKettle,inputKettle,setting),"Message")
            else:
                self.printAndSendMessage("Error: Master heat is switched to off, but heat is turned on. Please turn on the master heat","Alarm")
                return
        
        #print(setting)
        if kettle == "HLT": 
            if mode == "Auto":
                self.kettleSetting = "HLT"
                #Turns off the BLK, and turns on the HLT
                self.UIToHLTPIDPipe.send(("setPoint",setting))
                self.UIToHLTPIDPipe.send(("mode","Auto"))
                self.UIToHeatPipe.send(("kettle","HLT"))
                self.UIToHLTPIDPipe.send(("inputAttributeName",inputKettle+"Temp"))

                
            if mode == "SemiAuto":
                self.kettleSetting = "HLT"
                #Turns off the BLK, and turns on the HLT
                self.UIToHLTPIDPipe.send(("semiAutoValue",setting))
                self.UIToHLTPIDPipe.send(("mode","SemiAuto"))
                self.UIToHeatPipe.send(("kettle","HLT"))

                OldBoilerText = self.Boiler_Temp.text()
                NewBoilerText=OldBoilerText[:17]+"\nSetting: {:.0f}%".format(setting)
                self.Boiler_Temp.setText(NewBoilerText)
              
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
            self.printAndSendMessage("Error: Heat should only be applied to the HLT","Alarm")

        if mode == "Auto":
            OldBoilerText = self.Boiler_Temp.text()

            NewBoilerText=OldBoilerText[:17]
             
            if inputKettle == "HLT":
                NewBoilerText=NewBoilerText+"\nTarget temp: {:.0f}".format(setting)

            self.Boiler_Temp.setText(NewBoilerText)

            #Updates the main switch states to reflect the new Auto statuses
            mainSwitchStates = self.mainSwitchSensor.allMainSwitchStates()
            self.mainSwitchSignal.emit(mainSwitchStates)

    def emergencyStop(self):
        #sends a shutdown message:
        self.messageSignal.emit("Emergency stop signal recieved. Shutting off heat.","Alarm")


        #turns off heat
        self.setHeatSignal.emit("HLT","Off",0,"HLT")
        self.setHeatSignal.emit("BLK","Off",0,"BLK")
        self.UIToHLTPIDPipe.send(("mode","Off"))
        self.UIToHLTPIDPipe.send(("stop",True))
        self.UIToHeatPipe.send(("kettle","None"))
        self.UIToHeatPipe.send(("heatSetting",0))
        self.UIToHeatPipe.send(("turnOff",True))
                 
    def closeEvent(self, *args, **kwargs):
        print("Beginning system shutdown")
        #Ends the current phase
        self.stopPhase = True
        
        #turns off heat
        self.UIToHLTPIDPipe.send(("mode","Off"))
        self.UIToHLTPIDPipe.send(("stop",True))
        self.UIToHeatPipe.send(("kettle","None"))
        self.UIToHeatPipe.send(("heatSetting",0))
        self.UIToHeatPipe.send(("turnOff",True))

        #Turns off the sensors
        self.turnOffTempSensing = True
        self.turnOffMainSwitchSensing = True

        super(dashboard, self).closeEvent

    def updateHeatGraph(self,time,heatSetting,kettle):
        currTime = (time/1000 - self.startTime)/60
            self.heaty[0].append(heatSetting)
            self.heatx[0].append(currTime)
            self.heaty[1].append(0)
            self.heatx[1].append(currTime)
          
        self.graph2.clear()
        self.graph2.plot(self.heatx[0],self.heaty[0], pen=self.HLTPen)      
             
        
    
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = dashboard()
	sys.exit(app.exec_())	