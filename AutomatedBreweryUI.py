import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph

qtCreatorFile = "./UI/AutomatedBreweryUI/DashboardLarge.ui"

pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(MyApp, self).__init__()
		self.setupUi(self)
		self.show()
		#self.initUI()

	def initUI(self):
		self.sld.setMinimum(10)
		self.sld.setMaximum(30)
		self.sld.valueChanged.connect(self.testfunc)

	def testfunc(self):
		self.HLT.setValue(self.sld.value())
		if self.sld.value()<20:
			self.water.setStyleSheet('QFrame {\n	background:rgb(255, 0, 0)\n}')
		else:
			self.water.setStyleSheet('QFrame {\n	background:rgb(0, 255, 0)\n}')

