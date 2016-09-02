import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

qtCreatorFile = "./UI/AutomatedBreweryUI/Dashboard.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(MyApp, self).__init__()
		self.setupUi(self)
		self.show()
		self.initUI()

	def initUI(self):
		self.sld.setMinimum(10)
		self.sld.setMaximum(30)
		self.sld.valueChanged.connect(self.testfunc)

	def testfunc(self):
		self.lcd.display(self.sld.value())
		self.HLT.setValue(self.sld.value())



if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()

	sys.exit(app.exec_())
