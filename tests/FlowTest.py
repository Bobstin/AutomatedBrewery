import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
import time
from automatedbrewery.FlowSensor import flowSensors
import threading

qtCreatorFile = "../UI/AutomatedBreweryUI/flowtestui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    graphSignal = QtCore.pyqtSignal(list,list)

    def __init__(self):
        #sets global pyqtgraph settings
        pyqtgraph.setConfigOption('background', 'w')
        pyqtgraph.setConfigOption('foreground', 'k')

        super(MyApp, self).__init__()

        self.graphSignal.connect(self.graphUpdate)

        self.setupUi(self)
        self.show()

        sensorThread = threading.Thread(target = self.startSensors)
        sensorThread.start()

    def graphUpdate(self, rates, totals):
        self.HLT_In.plot(rates[0][0],rates[0][1],clear=True)
        self.HLT_Out.plot(rates[1][0],rates[1][1],clear=True)
        self.MLT_In.plot(rates[2][0],rates[2][1],clear=True)
        self.MLT_Out.plot(rates[3][0],rates[3][1],clear=True)
        self.BLK_In.plot(rates[4][0],rates[4][1],clear=True)
        self.BLK_Out.plot(rates[5][0],rates[5][1],clear=True)

        self.HLT.plot(totals[0][0],totals[0][1],clear=True)
        self.MLT.plot(totals[1][0],totals[1][1],clear=True)
        self.BLK.plot(totals[2][0],totals[2][1],clear=True)

    def startSensors(self):
        flowSensor = flowSensors(self.graphSignal)
        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
