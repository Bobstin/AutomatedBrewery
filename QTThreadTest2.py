import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph
import time
import threading

qtCreatorFile = "./UI/AutomatedBreweryUI/DashboardLarge.ui"

pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	updateTempGraph = QtCore.pyqtSignal(float,float)

	def __init__(self):
		super(MyApp, self).__init__()

		self.tempx = []
		self.tempy = []

		self.updateTempGraph.connect(self.tempGraph)
		self.setupUi(self)
		self.show()

		PIDThread = threading.Thread(target = self.PID, args=(self.updateTempGraph,))
		PIDThread.start()

	def PID(self,updateTempGraph):
		counter = 0
		while True:
			counter +=1
			updateTempGraph.emit(time.time(),counter)
			time.sleep(4)

	def tempGraph(self, x, y):
		print ("Updating Temp Graph")
		self.tempx.append(x)
		self.tempy.append(y)
		self.graph1.plot(self.tempx,self.tempy,clear=True)



if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	sys.exit(app.exec_())
