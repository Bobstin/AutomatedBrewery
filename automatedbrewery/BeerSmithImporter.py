import re

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QHeaderView)
from PyQt5.QtGui import QIcon

import sys

importQtCreatorFile = "../UI/AutomatedBreweryUI/ImportBeersmithDialog.ui"
Ui_ImportDialog, QtBaseClass = uic.loadUiType(importQtCreatorFile)

mashPopupQtCreatorFile = "../UI/AutomatedBreweryUI/MashPopup.ui"
Ui_MashPopup,MashPopupQtBaseClass = uic.loadUiType(mashPopupQtCreatorFile)

boilPopupQtCreatorFile = "../UI/AutomatedBreweryUI/BoilPopup.ui"
Ui_BoilPopup,BoilPopupQtBaseClass = uic.loadUiType(boilPopupQtCreatorFile)

class mashPopup(QtWidgets.QMainWindow, Ui_MashPopup):
    def __init__(self,addMashSignal):
        super(mashPopup, self).__init__()

        self.setupUi(self)
        self.show()
        
        self.addMashSignal = addMashSignal
        self.Add_Step.clicked.connect(self.addStep)
        self.Cancel.clicked.connect(self.cancel)

    def addStep(self):
        self.addMashSignal.emit(self.Step_Num.text(),self.Infusion_Temp.text(),self.Volume_Added.text(),self.Step_Temp.text(),self.Rise_Time.text(),self.Step_Time.text())
        self.close()

    def cancel(self): self.close()

class boilPopup(QtWidgets.QMainWindow, Ui_BoilPopup):
    def __init__(self,addBoilSignal):
        super(boilPopup, self).__init__()

        self.setupUi(self)
        self.show()
        
        self.addBoilSignal = addBoilSignal
        self.Add_Step.clicked.connect(self.addStep)
        self.Cancel.clicked.connect(self.cancel)

    def addStep(self):
        self.addBoilSignal.emit(self.Time.text(),self.Ingredient.text(),self.Amount.text())
        self.close()

    def cancel(self): self.close()

class importDialog(QtWidgets.QMainWindow, Ui_ImportDialog):
    addMashSignal = QtCore.pyqtSignal(str,str,str,str,str,str)
    addBoilSignal = QtCore.pyqtSignal(str,str,str)

    def __init__(self,importSignal):
        super(importDialog, self).__init__()
        self.setupUi(self)
        self.show()

        self.Mash_Steps.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Boil_Steps.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ImportButton.clicked.connect(self.importFromBeerSmith)
        self.ResetButton.clicked.connect(self.clearData)
        self.Add_Mash_Step.clicked.connect(self.openMashPopup)
        self.Add_Boil_Step.clicked.connect(self.openBoilPopup)
        self.ContinueButton.clicked.connect(self.sendToDashboard)

        self.addMashSignal.connect(self.addMashStep)
        self.addBoilSignal.connect(self.addBoilStep)        

        self.clearData()

        self.importSignal = importSignal

    def importFromBeerSmith(self):
        beerSmithFilePath = QFileDialog.getOpenFileName(self, 'Open file', '/home',"BeerSmith Files (*.bsmx)")
        if beerSmithFilePath[0]: 
            self.importResults = self.loadBeerSmithFileData(beerSmithFilePath[0])

            #clears the old data, just in case
            self.clearData()

            #Unpacks the importResults
            self.volumeValues = self.importResults[0]
            self.tempValues = self.importResults[1]
            self.boilSchedule = self.importResults[2]
            self.dryHopSchedule = self.importResults[3]
            self.mashSchedule = self.importResults[4]

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

        #Updates the volumes
        self.HLT_Fill_1_Target.setText("")
        self.Strike_Target.setText("")
        self.HLT_Fill_2_Target.setText("")
        self.Sparge_Target.setText("")
        self.Pre_Boil_Target.setText("")
        self.Post_Boil_Target.setText("")
        self.Fermenter_Target.setText("")

        #updates the temps
        self.Strike_Temp.setText("")
        self.HLT_Fill_2_Temp.setText("")
        self.Sparge_Temp.setText("")

    def openMashPopup(self):
        self.mashPopup = mashPopup(self.addMashSignal)

    def openBoilPopup(self):
        self.BoilPopup = boilPopup(self.addBoilSignal)

    def addMashStep(self,stepNum,infusionTemp,volumeAdded,stepTemp,riseTime,stepTime):
        #Handles steps without infusions
        if infusionTemp == "":infusionTemp = stepTemp
        if volumeAdded == "":volumeAdded = "0"

        rowPosition = int(stepNum) - 1
        self.Mash_Steps.insertRow(rowPosition)
        self.Mash_Steps.setItem(rowPosition,0,QtWidgets.QTableWidgetItem("{:.0f} F".format(float(infusionTemp))))
        self.Mash_Steps.setItem(rowPosition,1,QtWidgets.QTableWidgetItem("{:.2f} gal".format(float(volumeAdded))))
        self.Mash_Steps.setItem(rowPosition,2,QtWidgets.QTableWidgetItem("{:.0f} F".format(float(stepTemp))))
        self.Mash_Steps.setItem(rowPosition,3,QtWidgets.QTableWidgetItem("{:.0f} min".format(float(riseTime))))
        self.Mash_Steps.setItem(rowPosition,4,QtWidgets.QTableWidgetItem("{:.0f} min".format(float(stepTime))))

        if not(hasattr(self,"mashSchedule")):self.mashSchedule = []
        self.mashSchedule.insert(int(stepNum)-1,("User Added",float(volumeAdded),float(stepTime),float(infusionTemp),float(riseTime),float(stepTime)))
        print(self.mashSchedule)

    def addBoilStep(self,time,ingredient,amount):
        
        if not(hasattr(self,"boilSchedule")): self.boilSchedule = []

        #figures out which step to add the boil step as
        rowPosition = 0
        for i in range(0,len(self.boilSchedule)):
            if self.boilSchedule[i][1]<float(time):
                rowPosition += 1
                print(rowPosition)
                print(self.boilSchedule[i])


        self.Boil_Steps.insertRow(rowPosition)
        self.Boil_Steps.setItem(rowPosition,1,QtWidgets.QTableWidgetItem(ingredient))
        self.Boil_Steps.setItem(rowPosition,0,QtWidgets.QTableWidgetItem("{:.0f} min".format(float(time))))
        self.Boil_Steps.setItem(rowPosition,2,QtWidgets.QTableWidgetItem(amount))

        self.boilSchedule.insert(rowPosition,(ingredient,float(time),amount))
        print(self.boilSchedule)

    def sendToDashboard(self):
        self.importSignal.emit(volumeValues,tempValues,boilSchedule,dryHopSchedule,mashSchedule)


    def loadBeerSmithFileData(self,beerSmithFilePath):
        #Opens the BeerSmith file
        beerSmithFile = open(beerSmithFilePath,'r').read()

        #Volumes are in fl oz, temps are in F
        globalTags = ['F_R_NAME','F_MS_TUN_VOL','F_E_BOIL_VOL','F_E_BOIL_OFF','F_E_BATCH_VOL','F_MH_TUN_DEADSPACE','F_MH_SPARGE_TEMP','F_MS_GRAIN_WEIGHT','F_G_BOIL_TIME']
        #globalNames = ['Recipe name','Mash tun volume','Pre-boil volume','Boil off','Batch volume','Mash deadspace','Sparge temp','Grain Weight','Boil time']
        globalRegexs = [tag+">(.*?)<\/"+tag for tag in globalTags]
        globalResults = [re.search(regex,beerSmithFile).group(1) for regex in globalRegexs]
        #print(globalResults)

        hopsTags = ['F_H_NAME','F_H_BOIL_TIME','F_H_AMOUNT','F_H_DRY_HOP_TIME','F_H_USE']
        hopsRegexs = [tag+">(.*?)<\/"+tag for tag in hopsTags]
        miscTags = ['F_M_NAME','F_M_TIME','F_M_AMOUNT']
        miscRegexs = [tag+">(.*?)<\/"+tag for tag in miscTags]
        mashTags = ['F_MS_NAME','F_MS_INFUSION','F_MS_TUN_ADDITION','F_MS_STEP_TEMP','F_MS_START_TEMP','F_MS_INFUSION_TEMP','F_MS_STEP_TIME','F_MS_RISE_TIME']
        mashRegexs = [tag+">(.*?)<\/"+tag for tag in mashTags]
        grainTags = ['F_G_NAME','F_G_AMOUNT','F_G_RECOMMEND_MASH','F_G_BOIL_TIME']
        grainRegexs = [tag+">(.*?)<\/"+tag for tag in grainTags]

        hopsResults = [re.findall(regex,beerSmithFile) for regex in hopsRegexs]
        miscResults = [re.findall(regex,beerSmithFile) for regex in miscRegexs]
        mashResults = [re.findall(regex,beerSmithFile) for regex in mashRegexs]
        grainResults = [re.findall(regex,beerSmithFile) for regex in grainRegexs]


        #Calculates the volumes
        volumeNames = ['HLT first fill','Strike','HLT second fill','Sparge','Pre-boil','Post-boil','Fermenter']
        volumeValues = [None]*7 
        #Recommend filling the HLT to 85% of max initially
        volumeValues[0] = .85*float(globalResults[1])

        #Strike water is calculated based on the infusion + mash tun addition from the first Mash step
        volumeValues[1] = float(mashResults[1][0]) + float(mashResults[2][0])

        #For now, just filling the HLT back up with the strike volume
        volumeValues[2] = volumeValues[1]

        #Initially skips the sparge, since it is dependent on the pre-boil volume
        #Gets the pre-boil volume from the global results
        volumeValues[4] = float(globalResults[2])

        #Calculates the sparge volume as pre boil - total mash volume + mash tun deadspace + grain absorbtion
        mashVolumes  = [float(mashResults[1][i])+float(mashResults[2][i]) for i in range(0,len(mashResults[1]))]
        totalMashVolume = sum(mashVolumes)

        #Uses assumption of .96 fl oz absorbed per oz of grain
        grainAbsorbtion = .96*float(globalResults[7])

        volumeValues[3] = volumeValues[4] - totalMashVolume + float(globalResults[5]) + grainAbsorbtion

        #Post boil is based on the boil-off value
        volumeValues[5] = volumeValues[4] - float(globalResults[3])

        #Fermenter volume is based on batch size
        volumeValues[6] = float(globalResults[4])

        #Converts the volumeValues to gallons from fl oz
        volumeValues = [value/128 for value in volumeValues]



        #Calculates the temps
        tempNames = ['Strike','HLT second fill','Sparge']
        tempValues = [None]*3

        #The strike temp is the infusion temp of the first mash step
        tempValues[0] = float(mashResults[5][0])

        #The second fill temp is the step temp of the first mash step
        tempValues[1] = float(mashResults[3][0])

        #The sparge temp is captured in the global results
        tempValues[2] = float(globalResults[6])



        #Converts the misc and boil schedule to the prefered units (and as floats, not strings)
        boilTime = float(globalResults[8])

        #Combines the hops and misc schedules, and converts them to time added, instead of time in boil
        #First, converts all of the strings to floats
        hopsTimes = [float(hopsTimeStr) for hopsTimeStr in hopsResults[1]]
        hopsAmounts = ["{:.2f} oz".format(float(hopsAmtStr)) for hopsAmtStr in hopsResults[2]]
        hopsDryTimes = [float(hopsDryTimeStr) for hopsDryTimeStr in hopsResults[3]]
        hopsUses = [float(hopsUseStr) for hopsUseStr in hopsResults[4]]
        miscTimes = [float(miscTimeStr) for miscTimeStr in miscResults[1]]
        miscAmounts = [float(miscAmtStr) for miscAmtStr in miscResults[2]]
        grainTimes = [float(grainTimeStr) for grainTimeStr in grainResults[3]]
        grainAmounts = ["{:.2f} oz".format(float(grainAmtStr)) for grainAmtStr in grainResults[1]]
        grainUses = [float(grainUseStr) for grainUseStr in grainResults[2]]
        #print(miscAmounts)

        #Splits the dry hops into their own list to avoid sorting them with the flameout additions
        boilHopsTimes = [hopsTimes[i] for i in range(0,len(hopsTimes)) if hopsUses[i]==0]
        boilHopsAmounts = [hopsAmounts[i] for i in range(0,len(hopsTimes)) if hopsUses[i]==0]
        boilHopsNames = [hopsResults[0][i] for i in range(0,len(hopsTimes)) if hopsUses[i]==0]

        dryHopsTimes = [hopsDryTimes[i] for i in range(0,len(hopsTimes)) if hopsUses[i]==1]
        dryHopsAmounts = [hopsAmounts[i] for i in range(0,len(hopsTimes)) if hopsUses[i]==1]
        dryHopsNames = [hopsResults[0][i] for i in range(0,len(hopsTimes)) if hopsUses[i]==1]

        #we only care about grains that are added during the boil. Note that we start at 1, because
        #beersmith has an odd extra "base grain" entry before the ingredients
        boilGrainTimes = [grainTimes[i] for i in range(1,len(grainTimes)) if grainUses[i]==0]
        boilGrainAmounts = [grainAmounts[i] for i in range(1,len(grainAmounts)) if grainUses[i]==0]
        boilGrainNames = [grainResults[0][i] for i in range(1,len(grainTimes)) if grainUses[i]==0]

        #combines the boil hops, misc, and boil grains into a single list of boil aditions
        boilAdditionNames = boilHopsNames + miscResults[0] + boilGrainNames
        boilAdditionTimes = boilHopsTimes + miscTimes + boilGrainTimes
        boilAdditionAmounts = boilHopsAmounts + miscAmounts + boilGrainAmounts

        #Converts the times to times since boil started
        boilAdditionTimes = [boilTime - additionLength for additionLength in boilAdditionTimes]

        #Prints an warning if any of the boil addition times are negative (that is, you are supposed to boil and ingredient for longer than the whole boil)
        if min(boilAdditionTimes)<0: print("Warning: one or more of the ingredients has a boil time longer than the whole boil")

        #Sorts everything based on the boil addition times
        boilSchedule = zip(boilAdditionNames,boilAdditionTimes,boilAdditionAmounts)
        boilSchedule=sorted(boilSchedule,key=lambda x:x[1])

        dryHopSchedule = zip(dryHopsNames,dryHopsTimes,dryHopsAmounts)
        dryHopSchedule=sorted(dryHopSchedule,key=lambda x:x[1],reverse=True)

        #Generates the mash schedule
        #first, converts strings to floats with the proper units (gallons from fl oz)
        #Combines the infusion and addition amounts
        mashNames = mashResults[0]
        mashAmounts = [float(mashResults[1][i])/128 + float(mashResults[2][i])/128 for i in range(0,len(mashResults[1]))]
        mashStartTemp = [float(temp) for temp in mashResults[4]]
        mashStepTemp = [float(temp) for temp in mashResults[3]]
        mashInfusionTemp = [float(temp) for temp in mashResults[5]]
        mashRiseTime = [float(time) for time in mashResults[7]]
        mashStepTime = [float(time) for time in mashResults[6]]

        mashSchedule = list(zip(mashNames,mashAmounts,mashStepTemp,mashInfusionTemp,mashRiseTime,mashStepTime))

        importResults=[volumeValues,tempValues,boilSchedule,dryHopSchedule,mashSchedule]
        return importResults        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = importDialog()
    sys.exit(app.exec_())
    #importFromBeersmith()

