/********************************************************************************
** Form generated from reading UI file 'flowtestui.ui'
**
** Created by: Qt User Interface Compiler version 5.7.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FLOWTESTUI_H
#define UI_FLOWTESTUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>
#include "pyqtgraph"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    PlotWidget *HLT_In;
    PlotWidget *MLT_In;
    PlotWidget *BLK_In;
    PlotWidget *HLT_Out;
    PlotWidget *MLT_Out;
    PlotWidget *BLK_Out;
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QLabel *label_8;
    QLabel *label_9;
    PlotWidget *HLT;
    PlotWidget *MLT;
    PlotWidget *BLK;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(800, 638);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        HLT_In = new PlotWidget(centralwidget);
        HLT_In->setObjectName(QStringLiteral("HLT_In"));
        HLT_In->setGeometry(QRect(30, 30, 301, 61));
        MLT_In = new PlotWidget(centralwidget);
        MLT_In->setObjectName(QStringLiteral("MLT_In"));
        MLT_In->setGeometry(QRect(30, 230, 301, 61));
        BLK_In = new PlotWidget(centralwidget);
        BLK_In->setObjectName(QStringLiteral("BLK_In"));
        BLK_In->setGeometry(QRect(30, 430, 301, 61));
        HLT_Out = new PlotWidget(centralwidget);
        HLT_Out->setObjectName(QStringLiteral("HLT_Out"));
        HLT_Out->setGeometry(QRect(460, 30, 301, 61));
        MLT_Out = new PlotWidget(centralwidget);
        MLT_Out->setObjectName(QStringLiteral("MLT_Out"));
        MLT_Out->setGeometry(QRect(460, 230, 301, 61));
        BLK_Out = new PlotWidget(centralwidget);
        BLK_Out->setObjectName(QStringLiteral("BLK_Out"));
        BLK_Out->setGeometry(QRect(460, 430, 301, 61));
        label = new QLabel(centralwidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(150, 100, 60, 13));
        label_2 = new QLabel(centralwidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(590, 100, 60, 13));
        label_3 = new QLabel(centralwidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(160, 300, 60, 13));
        label_4 = new QLabel(centralwidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(600, 300, 60, 13));
        label_5 = new QLabel(centralwidget);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(150, 500, 60, 13));
        label_6 = new QLabel(centralwidget);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(600, 500, 60, 13));
        label_7 = new QLabel(centralwidget);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(350, 570, 70, 13));
        label_8 = new QLabel(centralwidget);
        label_8->setObjectName(QStringLiteral("label_8"));
        label_8->setGeometry(QRect(350, 170, 70, 13));
        label_9 = new QLabel(centralwidget);
        label_9->setObjectName(QStringLiteral("label_9"));
        label_9->setGeometry(QRect(350, 370, 70, 13));
        HLT = new PlotWidget(centralwidget);
        HLT->setObjectName(QStringLiteral("HLT"));
        HLT->setGeometry(QRect(230, 100, 301, 61));
        MLT = new PlotWidget(centralwidget);
        MLT->setObjectName(QStringLiteral("MLT"));
        MLT->setGeometry(QRect(230, 300, 301, 61));
        BLK = new PlotWidget(centralwidget);
        BLK->setObjectName(QStringLiteral("BLK"));
        BLK->setGeometry(QRect(230, 500, 301, 61));
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 21));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0));
        label->setText(QApplication::translate("MainWindow", "HLT In", 0));
        label_2->setText(QApplication::translate("MainWindow", "HLT Out", 0));
        label_3->setText(QApplication::translate("MainWindow", "MLT In", 0));
        label_4->setText(QApplication::translate("MainWindow", "MLT Out", 0));
        label_5->setText(QApplication::translate("MainWindow", "BLK In", 0));
        label_6->setText(QApplication::translate("MainWindow", "BLK Out", 0));
        label_7->setText(QApplication::translate("MainWindow", "BLK Total", 0));
        label_8->setText(QApplication::translate("MainWindow", "HLT Total", 0));
        label_9->setText(QApplication::translate("MainWindow", "MLT Total", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FLOWTESTUI_H
