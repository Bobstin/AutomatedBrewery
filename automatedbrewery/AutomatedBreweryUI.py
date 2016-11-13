import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
from multiprocessing import Pipe
import threading
import time
import RTD
import PID
import HeatControl

qtCreatorFile = "./UI/AutomatedBreweryUI/DashboardLarge.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	tempGraphSignal = QtCore.pyqtSignal(float,float)
	heatGraphSignal = QtCore.pyqtSignal(float,float,str)
	heatConn, PIDConn = Pipe()

	def __init__(self):
		pyqtgraph.setConfigOption('background', 'w')
		pyqtgraph.setConfigOption('foreground', 'k')

		super(MyApp, self).__init__()

		self.tempx = []
		self.tempy = []
		self.heatx = []
		self.heaty = []

		self.tempGraphSignal.connect(self.tempGraph)
		self.heatGraphSignal.connect(self.heatGraph)

		self.setupUi(self)
		self.show()

		heatThread = threading.Thread(target = self.startHeatControl, args=(self.heatConn,self.heatGraphSignal))
		PIDThread = threading.Thread(target = self.startPID, args=(self.PIDConn,self.tempGraphSignal))

		heatThread.start()
		PIDThread.start()

	def startHeatControl(self,heatConn,heatGraphSignal):
		HeatCtrl = HeatControl.HeatController(pipeConn=heatConn, heatGraphSignal=heatGraphSignal)
		HeatCtrl.kettle = "MLT"    	

	def startPID(self,PIDConn,tempGraphSignal):
		#Sets up the RTD
		cs_pin = 8
		clock_pin = 11
		data_in_pin = 9
		data_out_pin = 10
		rtd = RTD.MAX31865(cs_pin, clock_pin, data_in_pin, data_out_pin, units='f')

		time.sleep(5)
		#Sets up the PID
		inputSource = rtd
		inputAttributeName = 'temp'
		pid = PID.PID(inputSource,inputAttributeName)
		pid.outputPipeConn = PIDConn
		pid.outputMin = 0
		pid.outputMax = 100
		pid.cycleTime = 2000
		pid.semiAutoValue = 10
		pid.outputAttributeName = 'heatSetting'
		pid.mode = 'SemiAuto'
		pid.tempGraphSignal = tempGraphSignal
		#pid.run()

		outputStartValue = 50
		outputChange = 50
		expectedNoiseAmplitude = 1
		steadyRequirementTime = 30*1000
		triggerDelta = 2
		lookBackTime = 10000
		requiredAccuracy=0.02
		pid.autoTune(outputStartValue,outputChange,expectedNoiseAmplitude, steadyRequirementTime, triggerDelta, lookBackTime, requiredAccuracy)
				

	def tempGraph(self, x, y):
		self.tempx.append(x)
		self.tempy.append(y)
		self.graph1.plot(self.tempx,self.tempy,clear=True)

	def heatGraph(self, x, y, kettle):
		self.heatx.append(x)
		self.heaty.append(y)
		self.graph2.plot(self.heatx,self.heaty,clear=True)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	sys.exit(app.exec_())

	heatProcess.join()
	PIDProcess.join()
