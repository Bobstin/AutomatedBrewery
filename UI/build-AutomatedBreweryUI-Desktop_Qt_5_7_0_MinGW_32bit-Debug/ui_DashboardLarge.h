/********************************************************************************
** Form generated from reading UI file 'DashboardLarge.ui'
**
** Created by: Qt User Interface Compiler version 5.7.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DASHBOARDLARGE_H
#define UI_DASHBOARDLARGE_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>
#include "pyqtgraph"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QProgressBar *HLT;
    QProgressBar *MLT;
    QProgressBar *BLK;
    QFrame *frame;
    QFrame *water;
    QPushButton *valve2;
    QFrame *frame_2;
    QPushButton *valve1;
    QPushButton *valve3u;
    QPushButton *valve3d;
    QPushButton *waterPump;
    QFrame *valve3;
    QFrame *line;
    QFrame *frame_3;
    QFrame *frame_4;
    QFrame *frame_5;
    QFrame *frame_6;
    QFrame *frame_7;
    QFrame *frame_8;
    QFrame *frame_9;
    QFrame *frame_10;
    QPushButton *valve4;
    QFrame *frame_11;
    QFrame *frame_12;
    QPushButton *valve6;
    QFrame *frame_13;
    QPushButton *valve5;
    QFrame *frame_14;
    QFrame *frame_15;
    QFrame *frame_16;
    QFrame *frame_17;
    QFrame *frame_18;
    QFrame *frame_19;
    QFrame *frame_20;
    QPushButton *valve7u;
    QFrame *valve7;
    QPushButton *valve7d;
    QPushButton *valve8d;
    QFrame *valve8;
    QPushButton *valve8u;
    QFrame *frame_21;
    QFrame *frame_22;
    QPushButton *valve10;
    QFrame *frame_23;
    QFrame *frame_24;
    QFrame *frame_25;
    QFrame *frame_26;
    QFrame *frame_27;
    QFrame *frame_28;
    QFrame *frame_29;
    QPushButton *wortPump;
    QFrame *frame_30;
    QFrame *frame_31;
    QFrame *frame_32;
    QFrame *frame_33;
    QFrame *frame_34;
    QFrame *frame_35;
    QFrame *frame_36;
    QFrame *frame_37;
    QFrame *frame_38;
    QFrame *frame_39;
    QFrame *frame_40;
    QFrame *water_2;
    QFrame *frame_41;
    QFrame *frame_44;
    QFrame *frame_45;
    QFrame *frame_46;
    QFrame *frame_42;
    QFrame *water_4;
    PlotWidget *graph1;
    PlotWidget *graph2;
    QPushButton *HLT_Heat;
    QPushButton *BLK_Heat;
    QPushButton *phase1;
    QPushButton *phase2;
    QPushButton *phase3;
    QPushButton *phase4;
    QPushButton *phase5;
    QPushButton *phase9;
    QPushButton *phase6;
    QPushButton *phase10;
    QPushButton *phase7;
    QPushButton *phase8;
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QLabel *label_5;
    QLineEdit *Strike_Target;
    QLineEdit *Strike_Actual;
    QLineEdit *Sparg_Target;
    QLineEdit *Sparge_Actual;
    QLabel *label_6;
    QLabel *label_7;
    QLineEdit *Pre_Boil_Target;
    QLineEdit *Pre_Boil_Actual;
    QLineEdit *Post_Boil_Target;
    QLineEdit *Post_Boil_Actual;
    QLabel *label_8;
    QLineEdit *HLT_Fill_1_Actual;
    QLineEdit *HLT_Fill_1_Target;
    QLabel *label_9;
    QLabel *label_10;
    QLineEdit *HLT_Fill_2_Target;
    QLineEdit *HLT_Fill_2_Actual;
    QLabel *label_11;
    QLabel *label_12;
    QLineEdit *Strike_Temp;
    QLabel *label_13;
    QLabel *label_15;
    QLineEdit *Fermenter_Actual;
    QLineEdit *Fermenter_Target;
    QLabel *label_16;
    QLineEdit *HLT_Fill_2_Temp;
    QLabel *label_17;
    QLineEdit *Sparge_Temp;
    QLabel *label_18;
    QTableWidget *Mash_Steps;
    QLabel *label_14;
    QPushButton *Add_Mash_Step;
    QPushButton *Add_Boil_Step;
    QLabel *label_19;
    QTableWidget *Boil_Steps;
    QLabel *label_20;
    QLabel *Mash_Timer;
    QLabel *Boil_Timer;
    QLabel *label_23;
    QTextEdit *Notes;
    QLabel *label_24;
    QListWidget *Messages;
    QLabel *label_25;
    QPushButton *Turn_Off_Alarm;
    QLabel *label_26;
    QLabel *pH;
    QLabel *DO;
    QLabel *label_29;
    QLabel *label_30;
    QLabel *DO_target;
    QLabel *pH_target;
    QLabel *label_27;
    QPushButton *Pause;
    QPushButton *E_Stop;
    QLabel *label_39;
    QLabel *label_40;
    QPushButton *MLT_Heat;
    QLabel *alarm_Text;
    QLabel *label_21;
    QLabel *HLT_Vol;
    QLabel *label_41;
    QLabel *label_42;
    QLabel *MLT_Vol;
    QLabel *BLK_Vol;
    QLabel *label_43;
    QPushButton *master_Heat;
    QPushButton *aeration;
    QPushButton *valve9;
    QFrame *valve3_5;
    QLabel *label_44;
    QLabel *HLT_In_4;
    QLabel *BLK_Out;
    QLabel *label_45;
    QLabel *BLK_In;
    QLabel *label_37;
    QFrame *valve3_6;
    QLabel *label_46;
    QLabel *HLT_In_5;
    QLabel *HLT_Out;
    QLabel *label_47;
    QLabel *HLT_In;
    QLabel *label_48;
    QFrame *valve3_7;
    QLabel *label_51;
    QLabel *HLT_In_7;
    QLabel *MLT_Out;
    QLabel *label_52;
    QLabel *MLT_In;
    QLabel *label_53;
    QPushButton *Beersmith_Import;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(1920, 1080);
        MainWindow->setStyleSheet(QLatin1String("QMainWindow {\n"
"background: white;\n"
"}"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        HLT = new QProgressBar(centralWidget);
        HLT->setObjectName(QStringLiteral("HLT"));
        HLT->setGeometry(QRect(130, 40, 140, 140));
        HLT->setStyleSheet(QLatin1String("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"	border-top-color: white;\n"
"	text-align: top center;\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 138, 205);\n"
"    height: 1px;\n"
"}"));
        HLT->setMaximum(1000);
        HLT->setValue(1000);
        HLT->setTextVisible(false);
        HLT->setOrientation(Qt::Vertical);
        HLT->setInvertedAppearance(false);
        MLT = new QProgressBar(centralWidget);
        MLT->setObjectName(QStringLiteral("MLT"));
        MLT->setGeometry(QRect(380, 40, 140, 140));
        MLT->setStyleSheet(QLatin1String("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"	border-top-color: white;\n"
"	text-align: top center;\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 138, 205);\n"
"    height: 1px;\n"
"}"));
        MLT->setMaximum(1000);
        MLT->setValue(500);
        MLT->setTextVisible(false);
        MLT->setOrientation(Qt::Vertical);
        MLT->setInvertedAppearance(false);
        BLK = new QProgressBar(centralWidget);
        BLK->setObjectName(QStringLiteral("BLK"));
        BLK->setGeometry(QRect(630, 40, 140, 140));
        BLK->setStyleSheet(QLatin1String("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"	border-top-color: white;\n"
"	text-align: top center;\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 138, 205);\n"
"    height: 1px;\n"
"}"));
        BLK->setMaximum(1000);
        BLK->setValue(0);
        BLK->setTextVisible(false);
        BLK->setOrientation(Qt::Vertical);
        BLK->setInvertedAppearance(false);
        frame = new QFrame(centralWidget);
        frame->setObjectName(QStringLiteral("frame"));
        frame->setGeometry(QRect(80, 327, 33, 20));
        frame->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: red;\n"
"}"));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        water = new QFrame(centralWidget);
        water->setObjectName(QStringLiteral("water"));
        water->setGeometry(QRect(40, 310, 40, 40));
        water->setStyleSheet(QLatin1String("QFrame {\n"
"	background:rgb(0, 138, 205)\n"
"}"));
        water->setFrameShape(QFrame::StyledPanel);
        water->setFrameShadow(QFrame::Raised);
        valve2 = new QPushButton(centralWidget);
        valve2->setObjectName(QStringLiteral("valve2"));
        valve2->setGeometry(QRect(100, 370, 20, 20));
        QFont font;
        font.setPointSize(6);
        valve2->setFont(font);
        valve2->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        frame_2 = new QFrame(centralWidget);
        frame_2->setObjectName(QStringLiteral("frame_2"));
        frame_2->setGeometry(QRect(107, 290, 20, 40));
        frame_2->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_2->setFrameShape(QFrame::StyledPanel);
        frame_2->setFrameShadow(QFrame::Raised);
        valve1 = new QPushButton(centralWidget);
        valve1->setObjectName(QStringLiteral("valve1"));
        valve1->setGeometry(QRect(100, 270, 20, 20));
        valve1->setFont(font);
        valve1->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve3u = new QPushButton(centralWidget);
        valve3u->setObjectName(QStringLiteral("valve3u"));
        valve3u->setGeometry(QRect(190, 300, 20, 20));
        valve3u->setFont(font);
        valve3u->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve3d = new QPushButton(centralWidget);
        valve3d->setObjectName(QStringLiteral("valve3d"));
        valve3d->setGeometry(QRect(190, 340, 20, 20));
        valve3d->setFont(font);
        valve3d->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        waterPump = new QPushButton(centralWidget);
        waterPump->setObjectName(QStringLiteral("waterPump"));
        waterPump->setGeometry(QRect(280, 310, 40, 40));
        waterPump->setFont(font);
        waterPump->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 20px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}\n"
""));
        valve3 = new QFrame(centralWidget);
        valve3->setObjectName(QStringLiteral("valve3"));
        valve3->setGeometry(QRect(190, 320, 40, 20));
        valve3->setStyleSheet(QLatin1String("QFrame {\n"
"	background: rgb(7, 155, 132);\n"
"}"));
        valve3->setFrameShape(QFrame::StyledPanel);
        valve3->setFrameShadow(QFrame::Raised);
        line = new QFrame(centralWidget);
        line->setObjectName(QStringLiteral("line"));
        line->setGeometry(QRect(800, 50, 21, 961));
        line->setFrameShape(QFrame::VLine);
        line->setFrameShadow(QFrame::Sunken);
        frame_3 = new QFrame(centralWidget);
        frame_3->setObjectName(QStringLiteral("frame_3"));
        frame_3->setGeometry(QRect(107, 60, 20, 210));
        frame_3->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_3->setFrameShape(QFrame::StyledPanel);
        frame_3->setFrameShadow(QFrame::Raised);
        frame_4 = new QFrame(centralWidget);
        frame_4->setObjectName(QStringLiteral("frame_4"));
        frame_4->setGeometry(QRect(113, 240, 84, 20));
        frame_4->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_4->setFrameShape(QFrame::StyledPanel);
        frame_4->setFrameShadow(QFrame::Raised);
        frame_5 = new QFrame(centralWidget);
        frame_5->setObjectName(QStringLiteral("frame_5"));
        frame_5->setGeometry(QRect(197, 240, 20, 60));
        frame_5->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_5->setFrameShape(QFrame::StyledPanel);
        frame_5->setFrameShadow(QFrame::Raised);
        frame_6 = new QFrame(centralWidget);
        frame_6->setObjectName(QStringLiteral("frame_6"));
        frame_6->setGeometry(QRect(197, 360, 20, 20));
        frame_6->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_6->setFrameShape(QFrame::StyledPanel);
        frame_6->setFrameShadow(QFrame::Raised);
        frame_7 = new QFrame(centralWidget);
        frame_7->setObjectName(QStringLiteral("frame_7"));
        frame_7->setGeometry(QRect(230, 327, 50, 20));
        frame_7->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_7->setFrameShape(QFrame::StyledPanel);
        frame_7->setFrameShadow(QFrame::Raised);
        frame_8 = new QFrame(centralWidget);
        frame_8->setObjectName(QStringLiteral("frame_8"));
        frame_8->setGeometry(QRect(297, 220, 20, 90));
        frame_8->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_8->setFrameShape(QFrame::StyledPanel);
        frame_8->setFrameShadow(QFrame::Raised);
        frame_9 = new QFrame(centralWidget);
        frame_9->setObjectName(QStringLiteral("frame_9"));
        frame_9->setGeometry(QRect(113, 60, 17, 20));
        frame_9->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_9->setFrameShape(QFrame::StyledPanel);
        frame_9->setFrameShadow(QFrame::Raised);
        frame_10 = new QFrame(centralWidget);
        frame_10->setObjectName(QStringLiteral("frame_10"));
        frame_10->setGeometry(QRect(270, 160, 27, 20));
        frame_10->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_10->setFrameShape(QFrame::StyledPanel);
        frame_10->setFrameShadow(QFrame::Raised);
        valve4 = new QPushButton(centralWidget);
        valve4->setObjectName(QStringLiteral("valve4"));
        valve4->setGeometry(QRect(290, 200, 20, 20));
        valve4->setFont(font);
        valve4->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        frame_11 = new QFrame(centralWidget);
        frame_11->setObjectName(QStringLiteral("frame_11"));
        frame_11->setGeometry(QRect(297, 160, 20, 40));
        frame_11->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_11->setFrameShape(QFrame::StyledPanel);
        frame_11->setFrameShadow(QFrame::Raised);
        frame_12 = new QFrame(centralWidget);
        frame_12->setObjectName(QStringLiteral("frame_12"));
        frame_12->setGeometry(QRect(197, 377, 93, 20));
        frame_12->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_12->setFrameShape(QFrame::StyledPanel);
        frame_12->setFrameShadow(QFrame::Raised);
        valve6 = new QPushButton(centralWidget);
        valve6->setObjectName(QStringLiteral("valve6"));
        valve6->setGeometry(QRect(330, 420, 20, 20));
        valve6->setFont(font);
        valve6->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        frame_13 = new QFrame(centralWidget);
        frame_13->setObjectName(QStringLiteral("frame_13"));
        frame_13->setGeometry(QRect(337, 380, 20, 40));
        frame_13->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_13->setFrameShape(QFrame::StyledPanel);
        frame_13->setFrameShadow(QFrame::Raised);
        valve5 = new QPushButton(centralWidget);
        valve5->setObjectName(QStringLiteral("valve5"));
        valve5->setGeometry(QRect(290, 370, 20, 20));
        valve5->setFont(font);
        valve5->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        frame_14 = new QFrame(centralWidget);
        frame_14->setObjectName(QStringLiteral("frame_14"));
        frame_14->setGeometry(QRect(310, 377, 33, 20));
        frame_14->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_14->setFrameShape(QFrame::StyledPanel);
        frame_14->setFrameShadow(QFrame::Raised);
        frame_15 = new QFrame(centralWidget);
        frame_15->setObjectName(QStringLiteral("frame_15"));
        frame_15->setGeometry(QRect(337, 130, 20, 250));
        frame_15->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: red;\n"
"}"));
        frame_15->setFrameShape(QFrame::StyledPanel);
        frame_15->setFrameShadow(QFrame::Raised);
        frame_16 = new QFrame(centralWidget);
        frame_16->setObjectName(QStringLiteral("frame_16"));
        frame_16->setGeometry(QRect(250, 130, 87, 20));
        frame_16->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_16->setFrameShape(QFrame::StyledPanel);
        frame_16->setFrameShadow(QFrame::Raised);
        frame_17 = new QFrame(centralWidget);
        frame_17->setObjectName(QStringLiteral("frame_17"));
        frame_17->setGeometry(QRect(250, 60, 130, 20));
        frame_17->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_17->setFrameShape(QFrame::StyledPanel);
        frame_17->setFrameShadow(QFrame::Raised);
        frame_18 = new QFrame(centralWidget);
        frame_18->setObjectName(QStringLiteral("frame_18"));
        frame_18->setGeometry(QRect(337, 440, 20, 40));
        frame_18->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_18->setFrameShape(QFrame::StyledPanel);
        frame_18->setFrameShadow(QFrame::Raised);
        frame_19 = new QFrame(centralWidget);
        frame_19->setObjectName(QStringLiteral("frame_19"));
        frame_19->setGeometry(QRect(330, 470, 40, 40));
        frame_19->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: red;\n"
"	border-radius: 20px;\n"
"}"));
        frame_19->setFrameShape(QFrame::StyledPanel);
        frame_19->setFrameShadow(QFrame::Raised);
        frame_20 = new QFrame(centralWidget);
        frame_20->setObjectName(QStringLiteral("frame_20"));
        frame_20->setGeometry(QRect(337, 500, 20, 46));
        frame_20->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_20->setFrameShape(QFrame::StyledPanel);
        frame_20->setFrameShadow(QFrame::Raised);
        valve7u = new QPushButton(centralWidget);
        valve7u->setObjectName(QStringLiteral("valve7u"));
        valve7u->setGeometry(QRect(390, 400, 20, 20));
        valve7u->setFont(font);
        valve7u->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve7 = new QFrame(centralWidget);
        valve7->setObjectName(QStringLiteral("valve7"));
        valve7->setGeometry(QRect(390, 420, 40, 20));
        valve7->setStyleSheet(QLatin1String("QFrame {\n"
"	background: rgb(7, 155, 132);\n"
"}"));
        valve7->setFrameShape(QFrame::StyledPanel);
        valve7->setFrameShadow(QFrame::Raised);
        valve7d = new QPushButton(centralWidget);
        valve7d->setObjectName(QStringLiteral("valve7d"));
        valve7d->setGeometry(QRect(390, 440, 20, 20));
        valve7d->setFont(font);
        valve7d->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve8d = new QPushButton(centralWidget);
        valve8d->setObjectName(QStringLiteral("valve8d"));
        valve8d->setGeometry(QRect(450, 500, 20, 20));
        valve8d->setFont(font);
        valve8d->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve8 = new QFrame(centralWidget);
        valve8->setObjectName(QStringLiteral("valve8"));
        valve8->setGeometry(QRect(450, 480, 40, 20));
        valve8->setStyleSheet(QLatin1String("QFrame {\n"
"	background: rgb(7, 155, 132);\n"
"}"));
        valve8->setFrameShape(QFrame::StyledPanel);
        valve8->setFrameShadow(QFrame::Raised);
        valve8u = new QPushButton(centralWidget);
        valve8u->setObjectName(QStringLiteral("valve8u"));
        valve8u->setGeometry(QRect(450, 460, 20, 20));
        valve8u->setFont(font);
        valve8u->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        frame_21 = new QFrame(centralWidget);
        frame_21->setObjectName(QStringLiteral("frame_21"));
        frame_21->setGeometry(QRect(430, 427, 27, 20));
        frame_21->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_21->setFrameShape(QFrame::StyledPanel);
        frame_21->setFrameShadow(QFrame::Raised);
        frame_22 = new QFrame(centralWidget);
        frame_22->setObjectName(QStringLiteral("frame_22"));
        frame_22->setGeometry(QRect(457, 427, 20, 33));
        frame_22->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_22->setFrameShape(QFrame::StyledPanel);
        frame_22->setFrameShadow(QFrame::Raised);
        valve10 = new QPushButton(centralWidget);
        valve10->setObjectName(QStringLiteral("valve10"));
        valve10->setGeometry(QRect(590, 160, 20, 20));
        valve10->setFont(font);
        valve10->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        frame_23 = new QFrame(centralWidget);
        frame_23->setObjectName(QStringLiteral("frame_23"));
        frame_23->setGeometry(QRect(530, 150, 41, 40));
        frame_23->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: red;\n"
"	border-radius: 20px;\n"
"}"));
        frame_23->setFrameShape(QFrame::StyledPanel);
        frame_23->setFrameShadow(QFrame::Raised);
        frame_24 = new QFrame(centralWidget);
        frame_24->setObjectName(QStringLiteral("frame_24"));
        frame_24->setGeometry(QRect(520, 167, 30, 20));
        frame_24->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_24->setFrameShape(QFrame::StyledPanel);
        frame_24->setFrameShadow(QFrame::Raised);
        frame_25 = new QFrame(centralWidget);
        frame_25->setObjectName(QStringLiteral("frame_25"));
        frame_25->setGeometry(QRect(570, 167, 10, 20));
        frame_25->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_25->setFrameShape(QFrame::StyledPanel);
        frame_25->setFrameShadow(QFrame::Raised);
        frame_26 = new QFrame(centralWidget);
        frame_26->setObjectName(QStringLiteral("frame_26"));
        frame_26->setGeometry(QRect(610, 167, 20, 20));
        frame_26->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_26->setFrameShape(QFrame::StyledPanel);
        frame_26->setFrameShadow(QFrame::Raised);
        frame_27 = new QFrame(centralWidget);
        frame_27->setObjectName(QStringLiteral("frame_27"));
        frame_27->setGeometry(QRect(580, 167, 10, 20));
        frame_27->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: grey;\n"
"}"));
        frame_27->setFrameShape(QFrame::StyledPanel);
        frame_27->setFrameShadow(QFrame::Raised);
        frame_28 = new QFrame(centralWidget);
        frame_28->setObjectName(QStringLiteral("frame_28"));
        frame_28->setGeometry(QRect(577, 167, 20, 303));
        frame_28->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: red;\n"
"}"));
        frame_28->setFrameShape(QFrame::StyledPanel);
        frame_28->setFrameShadow(QFrame::Raised);
        frame_29 = new QFrame(centralWidget);
        frame_29->setObjectName(QStringLiteral("frame_29"));
        frame_29->setGeometry(QRect(107, 330, 20, 40));
        frame_29->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: blue;\n"
"}"));
        frame_29->setFrameShape(QFrame::StyledPanel);
        frame_29->setFrameShadow(QFrame::Raised);
        wortPump = new QPushButton(centralWidget);
        wortPump->setObjectName(QStringLiteral("wortPump"));
        wortPump->setGeometry(QRect(560, 470, 40, 40));
        wortPump->setFont(font);
        wortPump->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 20px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}\n"
""));
        frame_30 = new QFrame(centralWidget);
        frame_30->setObjectName(QStringLiteral("frame_30"));
        frame_30->setGeometry(QRect(490, 487, 70, 20));
        frame_30->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_30->setFrameShape(QFrame::StyledPanel);
        frame_30->setFrameShadow(QFrame::Raised);
        frame_31 = new QFrame(centralWidget);
        frame_31->setObjectName(QStringLiteral("frame_31"));
        frame_31->setGeometry(QRect(457, 520, 20, 20));
        frame_31->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_31->setFrameShape(QFrame::StyledPanel);
        frame_31->setFrameShadow(QFrame::Raised);
        frame_32 = new QFrame(centralWidget);
        frame_32->setObjectName(QStringLiteral("frame_32"));
        frame_32->setGeometry(QRect(343, 540, 120, 20));
        frame_32->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_32->setFrameShape(QFrame::StyledPanel);
        frame_32->setFrameShadow(QFrame::Raised);
        frame_33 = new QFrame(centralWidget);
        frame_33->setObjectName(QStringLiteral("frame_33"));
        frame_33->setGeometry(QRect(397, 460, 20, 27));
        frame_33->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_33->setFrameShape(QFrame::StyledPanel);
        frame_33->setFrameShadow(QFrame::Raised);
        frame_34 = new QFrame(centralWidget);
        frame_34->setObjectName(QStringLiteral("frame_34"));
        frame_34->setGeometry(QRect(107, 487, 296, 20));
        frame_34->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_34->setFrameShape(QFrame::StyledPanel);
        frame_34->setFrameShadow(QFrame::Raised);
        frame_35 = new QFrame(centralWidget);
        frame_35->setObjectName(QStringLiteral("frame_35"));
        frame_35->setGeometry(QRect(397, 327, 20, 73));
        frame_35->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_35->setFrameShape(QFrame::StyledPanel);
        frame_35->setFrameShadow(QFrame::Raised);
        frame_36 = new QFrame(centralWidget);
        frame_36->setObjectName(QStringLiteral("frame_36"));
        frame_36->setGeometry(QRect(403, 327, 140, 20));
        frame_36->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_36->setFrameShape(QFrame::StyledPanel);
        frame_36->setFrameShadow(QFrame::Raised);
        frame_37 = new QFrame(centralWidget);
        frame_37->setObjectName(QStringLiteral("frame_37"));
        frame_37->setGeometry(QRect(537, 183, 20, 144));
        frame_37->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_37->setFrameShape(QFrame::StyledPanel);
        frame_37->setFrameShadow(QFrame::Raised);
        frame_38 = new QFrame(centralWidget);
        frame_38->setObjectName(QStringLiteral("frame_38"));
        frame_38->setGeometry(QRect(537, 66, 20, 91));
        frame_38->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_38->setFrameShape(QFrame::StyledPanel);
        frame_38->setFrameShadow(QFrame::Raised);
        frame_39 = new QFrame(centralWidget);
        frame_39->setObjectName(QStringLiteral("frame_39"));
        frame_39->setGeometry(QRect(537, 60, 93, 20));
        frame_39->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_39->setFrameShape(QFrame::StyledPanel);
        frame_39->setFrameShadow(QFrame::Raised);
        frame_40 = new QFrame(centralWidget);
        frame_40->setObjectName(QStringLiteral("frame_40"));
        frame_40->setGeometry(QRect(250, 66, 20, 64));
        frame_40->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_40->setFrameShape(QFrame::StyledPanel);
        frame_40->setFrameShadow(QFrame::Raised);
        water_2 = new QFrame(centralWidget);
        water_2->setObjectName(QStringLiteral("water_2"));
        water_2->setGeometry(QRect(90, 430, 40, 80));
        water_2->setStyleSheet(QLatin1String("QFrame {\n"
"	border:6px solid grey\n"
"}"));
        water_2->setFrameShape(QFrame::StyledPanel);
        water_2->setFrameShadow(QFrame::Raised);
        frame_41 = new QFrame(centralWidget);
        frame_41->setObjectName(QStringLiteral("frame_41"));
        frame_41->setGeometry(QRect(107, 390, 20, 40));
        frame_41->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: blue;\n"
"}"));
        frame_41->setFrameShape(QFrame::StyledPanel);
        frame_41->setFrameShadow(QFrame::Raised);
        frame_44 = new QFrame(centralWidget);
        frame_44->setObjectName(QStringLiteral("frame_44"));
        frame_44->setGeometry(QRect(107, 510, 20, 10));
        frame_44->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: blue;\n"
"}"));
        frame_44->setFrameShape(QFrame::StyledPanel);
        frame_44->setFrameShadow(QFrame::Raised);
        frame_45 = new QFrame(centralWidget);
        frame_45->setObjectName(QStringLiteral("frame_45"));
        frame_45->setGeometry(QRect(107, 447, 20, 40));
        frame_45->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_45->setFrameShape(QFrame::StyledPanel);
        frame_45->setFrameShadow(QFrame::Raised);
        frame_46 = new QFrame(centralWidget);
        frame_46->setObjectName(QStringLiteral("frame_46"));
        frame_46->setGeometry(QRect(50, 453, 20, 67));
        frame_46->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: none none none solid;\n"
"	border-color: grey;\n"
"}"));
        frame_46->setFrameShape(QFrame::StyledPanel);
        frame_46->setFrameShadow(QFrame::Raised);
        frame_42 = new QFrame(centralWidget);
        frame_42->setObjectName(QStringLiteral("frame_42"));
        frame_42->setGeometry(QRect(50, 447, 57, 20));
        frame_42->setStyleSheet(QLatin1String("QFrame {\n"
"	border-width: 6px;\n"
"	border-style: solid none none none;\n"
"	border-color: blue;\n"
"}"));
        frame_42->setFrameShape(QFrame::StyledPanel);
        frame_42->setFrameShadow(QFrame::Raised);
        water_4 = new QFrame(centralWidget);
        water_4->setObjectName(QStringLiteral("water_4"));
        water_4->setGeometry(QRect(90, 520, 40, 40));
        water_4->setStyleSheet(QLatin1String("QFrame {\n"
"	background:rgb(0, 138, 205)\n"
"}"));
        water_4->setFrameShape(QFrame::StyledPanel);
        water_4->setFrameShadow(QFrame::Raised);
        graph1 = new PlotWidget(centralWidget);
        graph1->setObjectName(QStringLiteral("graph1"));
        graph1->setGeometry(QRect(40, 650, 731, 151));
        graph2 = new PlotWidget(centralWidget);
        graph2->setObjectName(QStringLiteral("graph2"));
        graph2->setGeometry(QRect(40, 860, 731, 151));
        HLT_Heat = new QPushButton(centralWidget);
        HLT_Heat->setObjectName(QStringLiteral("HLT_Heat"));
        HLT_Heat->setGeometry(QRect(130, 190, 140, 41));
        HLT_Heat->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(226, 152, 21);\n"
"	font: 12pt \"Arial\";\n"
"	color:white;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        BLK_Heat = new QPushButton(centralWidget);
        BLK_Heat->setObjectName(QStringLiteral("BLK_Heat"));
        BLK_Heat->setGeometry(QRect(630, 190, 140, 41));
        BLK_Heat->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color:white;\n"
"	font: 12pt \"Arial\";\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase1 = new QPushButton(centralWidget);
        phase1->setObjectName(QStringLiteral("phase1"));
        phase1->setGeometry(QRect(850, 50, 171, 61));
        phase1->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(191, 191, 191);\n"
"	color:grey;\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase1->setCheckable(false);
        phase2 = new QPushButton(centralWidget);
        phase2->setObjectName(QStringLiteral("phase2"));
        phase2->setGeometry(QRect(1070, 50, 171, 61));
        phase2->setStyleSheet(QLatin1String("QPushButton {\n"
"    color:white;\n"
"	border-radius: 0px;\n"
"    background-color: rgb(0, 138, 179);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase3 = new QPushButton(centralWidget);
        phase3->setObjectName(QStringLiteral("phase3"));
        phase3->setGeometry(QRect(1290, 50, 171, 61));
        phase3->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase4 = new QPushButton(centralWidget);
        phase4->setObjectName(QStringLiteral("phase4"));
        phase4->setGeometry(QRect(1510, 50, 171, 61));
        phase4->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase5 = new QPushButton(centralWidget);
        phase5->setObjectName(QStringLiteral("phase5"));
        phase5->setGeometry(QRect(1730, 50, 171, 61));
        phase5->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase9 = new QPushButton(centralWidget);
        phase9->setObjectName(QStringLiteral("phase9"));
        phase9->setGeometry(QRect(1510, 140, 171, 61));
        phase9->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase6 = new QPushButton(centralWidget);
        phase6->setObjectName(QStringLiteral("phase6"));
        phase6->setGeometry(QRect(850, 140, 171, 61));
        phase6->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase10 = new QPushButton(centralWidget);
        phase10->setObjectName(QStringLiteral("phase10"));
        phase10->setGeometry(QRect(1730, 140, 171, 61));
        phase10->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase7 = new QPushButton(centralWidget);
        phase7->setObjectName(QStringLiteral("phase7"));
        phase7->setGeometry(QRect(1070, 140, 171, 61));
        phase7->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        phase8 = new QPushButton(centralWidget);
        phase8->setObjectName(QStringLiteral("phase8"));
        phase8->setGeometry(QRect(1290, 140, 171, 61));
        phase8->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(196, 236, 244);\n"
"	font: 12pt \"Arial\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        label = new QLabel(centralWidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(1290, 240, 71, 21));
        QFont font1;
        font1.setFamily(QStringLiteral("Arial"));
        font1.setPointSize(12);
        font1.setBold(true);
        font1.setItalic(false);
        font1.setWeight(75);
        label->setFont(font1);
        label->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(1290, 270, 71, 21));
        label_2->setFont(font1);
        label_2->setStyleSheet(QStringLiteral(""));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(1400, 270, 71, 21));
        label_3->setFont(font1);
        label_3->setStyleSheet(QStringLiteral(""));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(1510, 270, 71, 21));
        label_4->setFont(font1);
        label_4->setStyleSheet(QStringLiteral(""));
        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(1290, 340, 71, 31));
        QFont font2;
        font2.setFamily(QStringLiteral("Arial"));
        font2.setPointSize(12);
        label_5->setFont(font2);
        label_5->setStyleSheet(QStringLiteral(""));
        Strike_Target = new QLineEdit(centralWidget);
        Strike_Target->setObjectName(QStringLiteral("Strike_Target"));
        Strike_Target->setGeometry(QRect(1390, 340, 71, 31));
        Strike_Target->setFont(font2);
        Strike_Actual = new QLineEdit(centralWidget);
        Strike_Actual->setObjectName(QStringLiteral("Strike_Actual"));
        Strike_Actual->setGeometry(QRect(1500, 340, 71, 31));
        Strike_Actual->setFont(font2);
        Strike_Actual->setReadOnly(true);
        Sparg_Target = new QLineEdit(centralWidget);
        Sparg_Target->setObjectName(QStringLiteral("Sparg_Target"));
        Sparg_Target->setGeometry(QRect(1390, 420, 71, 31));
        Sparg_Target->setFont(font2);
        Sparge_Actual = new QLineEdit(centralWidget);
        Sparge_Actual->setObjectName(QStringLiteral("Sparge_Actual"));
        Sparge_Actual->setGeometry(QRect(1500, 420, 71, 31));
        Sparge_Actual->setFont(font2);
        Sparge_Actual->setReadOnly(true);
        label_6 = new QLabel(centralWidget);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(1290, 420, 71, 31));
        label_6->setFont(font2);
        label_6->setStyleSheet(QStringLiteral(""));
        label_7 = new QLabel(centralWidget);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(1290, 460, 71, 31));
        label_7->setFont(font2);
        label_7->setStyleSheet(QStringLiteral(""));
        Pre_Boil_Target = new QLineEdit(centralWidget);
        Pre_Boil_Target->setObjectName(QStringLiteral("Pre_Boil_Target"));
        Pre_Boil_Target->setGeometry(QRect(1390, 460, 71, 31));
        Pre_Boil_Target->setFont(font2);
        Pre_Boil_Actual = new QLineEdit(centralWidget);
        Pre_Boil_Actual->setObjectName(QStringLiteral("Pre_Boil_Actual"));
        Pre_Boil_Actual->setGeometry(QRect(1500, 460, 71, 31));
        Pre_Boil_Actual->setFont(font2);
        Pre_Boil_Actual->setReadOnly(true);
        Post_Boil_Target = new QLineEdit(centralWidget);
        Post_Boil_Target->setObjectName(QStringLiteral("Post_Boil_Target"));
        Post_Boil_Target->setGeometry(QRect(1390, 500, 71, 31));
        Post_Boil_Target->setFont(font2);
        Post_Boil_Actual = new QLineEdit(centralWidget);
        Post_Boil_Actual->setObjectName(QStringLiteral("Post_Boil_Actual"));
        Post_Boil_Actual->setGeometry(QRect(1500, 500, 71, 31));
        Post_Boil_Actual->setFont(font2);
        Post_Boil_Actual->setReadOnly(true);
        label_8 = new QLabel(centralWidget);
        label_8->setObjectName(QStringLiteral("label_8"));
        label_8->setGeometry(QRect(1290, 500, 71, 31));
        label_8->setFont(font2);
        label_8->setStyleSheet(QStringLiteral(""));
        HLT_Fill_1_Actual = new QLineEdit(centralWidget);
        HLT_Fill_1_Actual->setObjectName(QStringLiteral("HLT_Fill_1_Actual"));
        HLT_Fill_1_Actual->setGeometry(QRect(1500, 300, 71, 31));
        HLT_Fill_1_Actual->setFont(font2);
        HLT_Fill_1_Actual->setReadOnly(true);
        HLT_Fill_1_Target = new QLineEdit(centralWidget);
        HLT_Fill_1_Target->setObjectName(QStringLiteral("HLT_Fill_1_Target"));
        HLT_Fill_1_Target->setGeometry(QRect(1390, 300, 71, 31));
        HLT_Fill_1_Target->setFont(font2);
        label_9 = new QLabel(centralWidget);
        label_9->setObjectName(QStringLiteral("label_9"));
        label_9->setGeometry(QRect(1290, 300, 81, 31));
        label_9->setFont(font2);
        label_9->setStyleSheet(QStringLiteral(""));
        label_10 = new QLabel(centralWidget);
        label_10->setObjectName(QStringLiteral("label_10"));
        label_10->setGeometry(QRect(1290, 380, 81, 31));
        label_10->setFont(font2);
        label_10->setStyleSheet(QStringLiteral(""));
        HLT_Fill_2_Target = new QLineEdit(centralWidget);
        HLT_Fill_2_Target->setObjectName(QStringLiteral("HLT_Fill_2_Target"));
        HLT_Fill_2_Target->setGeometry(QRect(1390, 380, 71, 31));
        HLT_Fill_2_Target->setFont(font2);
        HLT_Fill_2_Actual = new QLineEdit(centralWidget);
        HLT_Fill_2_Actual->setObjectName(QStringLiteral("HLT_Fill_2_Actual"));
        HLT_Fill_2_Actual->setGeometry(QRect(1500, 380, 71, 31));
        HLT_Fill_2_Actual->setFont(font2);
        HLT_Fill_2_Actual->setReadOnly(true);
        label_11 = new QLabel(centralWidget);
        label_11->setObjectName(QStringLiteral("label_11"));
        label_11->setGeometry(QRect(1610, 340, 81, 31));
        label_11->setFont(font2);
        label_11->setStyleSheet(QStringLiteral(""));
        label_12 = new QLabel(centralWidget);
        label_12->setObjectName(QStringLiteral("label_12"));
        label_12->setGeometry(QRect(1610, 270, 101, 21));
        label_12->setFont(font1);
        label_12->setStyleSheet(QStringLiteral(""));
        Strike_Temp = new QLineEdit(centralWidget);
        Strike_Temp->setObjectName(QStringLiteral("Strike_Temp"));
        Strike_Temp->setGeometry(QRect(1730, 340, 71, 31));
        Strike_Temp->setFont(font2);
        label_13 = new QLabel(centralWidget);
        label_13->setObjectName(QStringLiteral("label_13"));
        label_13->setGeometry(QRect(1610, 240, 111, 21));
        label_13->setFont(font1);
        label_13->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        label_15 = new QLabel(centralWidget);
        label_15->setObjectName(QStringLiteral("label_15"));
        label_15->setGeometry(QRect(1740, 270, 71, 21));
        label_15->setFont(font1);
        label_15->setStyleSheet(QStringLiteral(""));
        Fermenter_Actual = new QLineEdit(centralWidget);
        Fermenter_Actual->setObjectName(QStringLiteral("Fermenter_Actual"));
        Fermenter_Actual->setGeometry(QRect(1500, 540, 71, 31));
        Fermenter_Actual->setFont(font2);
        Fermenter_Actual->setReadOnly(true);
        Fermenter_Target = new QLineEdit(centralWidget);
        Fermenter_Target->setObjectName(QStringLiteral("Fermenter_Target"));
        Fermenter_Target->setGeometry(QRect(1390, 540, 71, 31));
        Fermenter_Target->setFont(font2);
        label_16 = new QLabel(centralWidget);
        label_16->setObjectName(QStringLiteral("label_16"));
        label_16->setGeometry(QRect(1290, 540, 81, 31));
        label_16->setFont(font2);
        label_16->setStyleSheet(QStringLiteral(""));
        HLT_Fill_2_Temp = new QLineEdit(centralWidget);
        HLT_Fill_2_Temp->setObjectName(QStringLiteral("HLT_Fill_2_Temp"));
        HLT_Fill_2_Temp->setGeometry(QRect(1730, 380, 71, 31));
        HLT_Fill_2_Temp->setFont(font2);
        label_17 = new QLabel(centralWidget);
        label_17->setObjectName(QStringLiteral("label_17"));
        label_17->setGeometry(QRect(1610, 380, 81, 31));
        label_17->setFont(font2);
        label_17->setStyleSheet(QStringLiteral(""));
        Sparge_Temp = new QLineEdit(centralWidget);
        Sparge_Temp->setObjectName(QStringLiteral("Sparge_Temp"));
        Sparge_Temp->setGeometry(QRect(1730, 420, 71, 31));
        Sparge_Temp->setFont(font2);
        label_18 = new QLabel(centralWidget);
        label_18->setObjectName(QStringLiteral("label_18"));
        label_18->setGeometry(QRect(1610, 420, 81, 31));
        label_18->setFont(font2);
        label_18->setStyleSheet(QStringLiteral(""));
        Mash_Steps = new QTableWidget(centralWidget);
        if (Mash_Steps->columnCount() < 4)
            Mash_Steps->setColumnCount(4);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        __qtablewidgetitem->setFont(font2);
        Mash_Steps->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        __qtablewidgetitem1->setFont(font2);
        Mash_Steps->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        __qtablewidgetitem2->setFont(font2);
        Mash_Steps->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        __qtablewidgetitem3->setFont(font2);
        Mash_Steps->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        if (Mash_Steps->rowCount() < 1)
            Mash_Steps->setRowCount(1);
        Mash_Steps->setObjectName(QStringLiteral("Mash_Steps"));
        Mash_Steps->setGeometry(QRect(840, 270, 421, 261));
        Mash_Steps->setFont(font2);
        Mash_Steps->setRowCount(1);
        Mash_Steps->setColumnCount(4);
        Mash_Steps->horizontalHeader()->setCascadingSectionResizes(false);
        label_14 = new QLabel(centralWidget);
        label_14->setObjectName(QStringLiteral("label_14"));
        label_14->setGeometry(QRect(1110, 240, 121, 21));
        label_14->setFont(font1);
        label_14->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        Add_Mash_Step = new QPushButton(centralWidget);
        Add_Mash_Step->setObjectName(QStringLiteral("Add_Mash_Step"));
        Add_Mash_Step->setGeometry(QRect(840, 542, 421, 31));
        Add_Mash_Step->setFont(font2);
        Add_Boil_Step = new QPushButton(centralWidget);
        Add_Boil_Step->setObjectName(QStringLiteral("Add_Boil_Step"));
        Add_Boil_Step->setGeometry(QRect(840, 980, 421, 31));
        Add_Boil_Step->setFont(font2);
        label_19 = new QLabel(centralWidget);
        label_19->setObjectName(QStringLiteral("label_19"));
        label_19->setGeometry(QRect(840, 620, 121, 21));
        label_19->setFont(font1);
        label_19->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        Boil_Steps = new QTableWidget(centralWidget);
        if (Boil_Steps->columnCount() < 4)
            Boil_Steps->setColumnCount(4);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        __qtablewidgetitem4->setFont(font2);
        Boil_Steps->setHorizontalHeaderItem(0, __qtablewidgetitem4);
        QTableWidgetItem *__qtablewidgetitem5 = new QTableWidgetItem();
        __qtablewidgetitem5->setFont(font2);
        Boil_Steps->setHorizontalHeaderItem(1, __qtablewidgetitem5);
        QTableWidgetItem *__qtablewidgetitem6 = new QTableWidgetItem();
        __qtablewidgetitem6->setFont(font2);
        Boil_Steps->setHorizontalHeaderItem(2, __qtablewidgetitem6);
        QTableWidgetItem *__qtablewidgetitem7 = new QTableWidgetItem();
        __qtablewidgetitem7->setFont(font2);
        Boil_Steps->setHorizontalHeaderItem(3, __qtablewidgetitem7);
        if (Boil_Steps->rowCount() < 1)
            Boil_Steps->setRowCount(1);
        Boil_Steps->setObjectName(QStringLiteral("Boil_Steps"));
        Boil_Steps->setGeometry(QRect(840, 650, 421, 321));
        Boil_Steps->setFont(font2);
        Boil_Steps->setRowCount(1);
        Boil_Steps->setColumnCount(4);
        Boil_Steps->horizontalHeader()->setCascadingSectionResizes(false);
        label_20 = new QLabel(centralWidget);
        label_20->setObjectName(QStringLiteral("label_20"));
        label_20->setGeometry(QRect(840, 240, 121, 21));
        label_20->setFont(font1);
        label_20->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        Mash_Timer = new QLabel(centralWidget);
        Mash_Timer->setObjectName(QStringLiteral("Mash_Timer"));
        Mash_Timer->setGeometry(QRect(1210, 240, 51, 21));
        Mash_Timer->setFont(font1);
        Mash_Timer->setStyleSheet(QStringLiteral(""));
        Boil_Timer = new QLabel(centralWidget);
        Boil_Timer->setObjectName(QStringLiteral("Boil_Timer"));
        Boil_Timer->setGeometry(QRect(1210, 620, 51, 21));
        Boil_Timer->setFont(font1);
        Boil_Timer->setStyleSheet(QStringLiteral(""));
        label_23 = new QLabel(centralWidget);
        label_23->setObjectName(QStringLiteral("label_23"));
        label_23->setGeometry(QRect(1110, 620, 121, 21));
        label_23->setFont(font1);
        label_23->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        Notes = new QTextEdit(centralWidget);
        Notes->setObjectName(QStringLiteral("Notes"));
        Notes->setGeometry(QRect(1290, 650, 291, 361));
        label_24 = new QLabel(centralWidget);
        label_24->setObjectName(QStringLiteral("label_24"));
        label_24->setGeometry(QRect(1290, 620, 71, 21));
        label_24->setFont(font1);
        label_24->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        Messages = new QListWidget(centralWidget);
        QBrush brush(QColor(255, 255, 255, 255));
        brush.setStyle(Qt::NoBrush);
        QBrush brush1(QColor(203, 34, 91, 255));
        brush1.setStyle(Qt::SolidPattern);
        QListWidgetItem *__qlistwidgetitem = new QListWidgetItem(Messages);
        __qlistwidgetitem->setBackground(brush1);
        __qlistwidgetitem->setForeground(brush);
        QBrush brush2(QColor(203, 34, 91, 255));
        brush2.setStyle(Qt::NoBrush);
        QListWidgetItem *__qlistwidgetitem1 = new QListWidgetItem(Messages);
        __qlistwidgetitem1->setForeground(brush2);
        new QListWidgetItem(Messages);
        QBrush brush3(QColor(7, 155, 132, 255));
        brush3.setStyle(Qt::NoBrush);
        QListWidgetItem *__qlistwidgetitem2 = new QListWidgetItem(Messages);
        __qlistwidgetitem2->setForeground(brush3);
        Messages->setObjectName(QStringLiteral("Messages"));
        Messages->setGeometry(QRect(1610, 651, 291, 321));
        label_25 = new QLabel(centralWidget);
        label_25->setObjectName(QStringLiteral("label_25"));
        label_25->setGeometry(QRect(1610, 620, 111, 21));
        label_25->setFont(font1);
        label_25->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        Turn_Off_Alarm = new QPushButton(centralWidget);
        Turn_Off_Alarm->setObjectName(QStringLiteral("Turn_Off_Alarm"));
        Turn_Off_Alarm->setGeometry(QRect(1610, 980, 291, 31));
        Turn_Off_Alarm->setFont(font2);
        label_26 = new QLabel(centralWidget);
        label_26->setObjectName(QStringLiteral("label_26"));
        label_26->setGeometry(QRect(400, 240, 71, 21));
        label_26->setFont(font1);
        label_26->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        pH = new QLabel(centralWidget);
        pH->setObjectName(QStringLiteral("pH"));
        pH->setGeometry(QRect(470, 240, 51, 21));
        pH->setFont(font1);
        pH->setStyleSheet(QStringLiteral(""));
        DO = new QLabel(centralWidget);
        DO->setObjectName(QStringLiteral("DO"));
        DO->setGeometry(QRect(200, 520, 51, 20));
        DO->setFont(font1);
        DO->setStyleSheet(QStringLiteral(""));
        label_29 = new QLabel(centralWidget);
        label_29->setObjectName(QStringLiteral("label_29"));
        label_29->setGeometry(QRect(140, 520, 31, 20));
        label_29->setFont(font1);
        label_29->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        label_30 = new QLabel(centralWidget);
        label_30->setObjectName(QStringLiteral("label_30"));
        label_30->setGeometry(QRect(140, 540, 61, 20));
        label_30->setFont(font1);
        label_30->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        DO_target = new QLabel(centralWidget);
        DO_target->setObjectName(QStringLiteral("DO_target"));
        DO_target->setGeometry(QRect(200, 540, 51, 20));
        DO_target->setFont(font1);
        DO_target->setStyleSheet(QStringLiteral(""));
        pH_target = new QLabel(centralWidget);
        pH_target->setObjectName(QStringLiteral("pH_target"));
        pH_target->setGeometry(QRect(470, 260, 51, 21));
        pH_target->setFont(font1);
        pH_target->setStyleSheet(QStringLiteral(""));
        label_27 = new QLabel(centralWidget);
        label_27->setObjectName(QStringLiteral("label_27"));
        label_27->setGeometry(QRect(400, 260, 71, 21));
        label_27->setFont(font1);
        label_27->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        Pause = new QPushButton(centralWidget);
        Pause->setObjectName(QStringLiteral("Pause"));
        Pause->setGeometry(QRect(630, 330, 141, 61));
        Pause->setFont(font2);
        E_Stop = new QPushButton(centralWidget);
        E_Stop->setObjectName(QStringLiteral("E_Stop"));
        E_Stop->setGeometry(QRect(630, 410, 141, 61));
        QPalette palette;
        QBrush brush4(QColor(255, 255, 255, 255));
        brush4.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::WindowText, brush4);
        QLinearGradient gradient(0, 0, 0, 1);
        gradient.setSpread(QGradient::PadSpread);
        gradient.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient.setColorAt(0, QColor(255, 42, 117, 255));
        gradient.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush5(gradient);
        palette.setBrush(QPalette::Active, QPalette::Button, brush5);
        palette.setBrush(QPalette::Active, QPalette::Text, brush4);
        palette.setBrush(QPalette::Active, QPalette::ButtonText, brush4);
        QLinearGradient gradient1(0, 0, 0, 1);
        gradient1.setSpread(QGradient::PadSpread);
        gradient1.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient1.setColorAt(0, QColor(255, 42, 117, 255));
        gradient1.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush6(gradient1);
        palette.setBrush(QPalette::Active, QPalette::Base, brush6);
        QLinearGradient gradient2(0, 0, 0, 1);
        gradient2.setSpread(QGradient::PadSpread);
        gradient2.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient2.setColorAt(0, QColor(255, 42, 117, 255));
        gradient2.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush7(gradient2);
        palette.setBrush(QPalette::Active, QPalette::Window, brush7);
        palette.setBrush(QPalette::Inactive, QPalette::WindowText, brush4);
        QLinearGradient gradient3(0, 0, 0, 1);
        gradient3.setSpread(QGradient::PadSpread);
        gradient3.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient3.setColorAt(0, QColor(255, 42, 117, 255));
        gradient3.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush8(gradient3);
        palette.setBrush(QPalette::Inactive, QPalette::Button, brush8);
        palette.setBrush(QPalette::Inactive, QPalette::Text, brush4);
        palette.setBrush(QPalette::Inactive, QPalette::ButtonText, brush4);
        QLinearGradient gradient4(0, 0, 0, 1);
        gradient4.setSpread(QGradient::PadSpread);
        gradient4.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient4.setColorAt(0, QColor(255, 42, 117, 255));
        gradient4.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush9(gradient4);
        palette.setBrush(QPalette::Inactive, QPalette::Base, brush9);
        QLinearGradient gradient5(0, 0, 0, 1);
        gradient5.setSpread(QGradient::PadSpread);
        gradient5.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient5.setColorAt(0, QColor(255, 42, 117, 255));
        gradient5.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush10(gradient5);
        palette.setBrush(QPalette::Inactive, QPalette::Window, brush10);
        palette.setBrush(QPalette::Disabled, QPalette::WindowText, brush4);
        QLinearGradient gradient6(0, 0, 0, 1);
        gradient6.setSpread(QGradient::PadSpread);
        gradient6.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient6.setColorAt(0, QColor(255, 42, 117, 255));
        gradient6.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush11(gradient6);
        palette.setBrush(QPalette::Disabled, QPalette::Button, brush11);
        palette.setBrush(QPalette::Disabled, QPalette::Text, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::ButtonText, brush4);
        QLinearGradient gradient7(0, 0, 0, 1);
        gradient7.setSpread(QGradient::PadSpread);
        gradient7.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient7.setColorAt(0, QColor(255, 42, 117, 255));
        gradient7.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush12(gradient7);
        palette.setBrush(QPalette::Disabled, QPalette::Base, brush12);
        QLinearGradient gradient8(0, 0, 0, 1);
        gradient8.setSpread(QGradient::PadSpread);
        gradient8.setCoordinateMode(QGradient::ObjectBoundingMode);
        gradient8.setColorAt(0, QColor(255, 42, 117, 255));
        gradient8.setColorAt(1, QColor(203, 34, 91, 255));
        QBrush brush13(gradient8);
        palette.setBrush(QPalette::Disabled, QPalette::Window, brush13);
        E_Stop->setPalette(palette);
        E_Stop->setFont(font2);
        E_Stop->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ff2a75, stop: 1 #cb225b);\n"
"	font: 12pt \"Arial\";\n"
"	color:white;\n"
"	border: 2px solid black;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        label_39 = new QLabel(centralWidget);
        label_39->setObjectName(QStringLiteral("label_39"));
        label_39->setGeometry(QRect(40, 620, 111, 21));
        label_39->setFont(font1);
        label_39->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        label_40 = new QLabel(centralWidget);
        label_40->setObjectName(QStringLiteral("label_40"));
        label_40->setGeometry(QRect(40, 830, 111, 21));
        label_40->setFont(font1);
        label_40->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        MLT_Heat = new QPushButton(centralWidget);
        MLT_Heat->setObjectName(QStringLiteral("MLT_Heat"));
        MLT_Heat->setGeometry(QRect(380, 190, 140, 41));
        MLT_Heat->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color:white;\n"
"	font: 12pt \"Arial\";\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        alarm_Text = new QLabel(centralWidget);
        alarm_Text->setObjectName(QStringLiteral("alarm_Text"));
        alarm_Text->setGeometry(QRect(1870, 620, 51, 21));
        alarm_Text->setFont(font1);
        alarm_Text->setStyleSheet(QStringLiteral("color:rgb(203, 34, 91)"));
        label_21 = new QLabel(centralWidget);
        label_21->setObjectName(QStringLiteral("label_21"));
        label_21->setGeometry(QRect(1760, 620, 121, 21));
        label_21->setFont(font1);
        label_21->setStyleSheet(QStringLiteral("color: rgb(0, 138, 179)"));
        HLT_Vol = new QLabel(centralWidget);
        HLT_Vol->setObjectName(QStringLiteral("HLT_Vol"));
        HLT_Vol->setGeometry(QRect(200, 20, 71, 20));
        HLT_Vol->setFont(font1);
        HLT_Vol->setStyleSheet(QStringLiteral(""));
        label_41 = new QLabel(centralWidget);
        label_41->setObjectName(QStringLiteral("label_41"));
        label_41->setGeometry(QRect(130, 20, 71, 21));
        label_41->setFont(font1);
        label_41->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        label_42 = new QLabel(centralWidget);
        label_42->setObjectName(QStringLiteral("label_42"));
        label_42->setGeometry(QRect(380, 20, 71, 21));
        label_42->setFont(font1);
        label_42->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        MLT_Vol = new QLabel(centralWidget);
        MLT_Vol->setObjectName(QStringLiteral("MLT_Vol"));
        MLT_Vol->setGeometry(QRect(450, 20, 71, 20));
        MLT_Vol->setFont(font1);
        MLT_Vol->setStyleSheet(QStringLiteral(""));
        BLK_Vol = new QLabel(centralWidget);
        BLK_Vol->setObjectName(QStringLiteral("BLK_Vol"));
        BLK_Vol->setGeometry(QRect(700, 20, 71, 20));
        BLK_Vol->setFont(font1);
        BLK_Vol->setStyleSheet(QStringLiteral(""));
        label_43 = new QLabel(centralWidget);
        label_43->setObjectName(QStringLiteral("label_43"));
        label_43->setGeometry(QRect(630, 20, 71, 21));
        label_43->setFont(font1);
        label_43->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        master_Heat = new QPushButton(centralWidget);
        master_Heat->setObjectName(QStringLiteral("master_Heat"));
        master_Heat->setGeometry(QRect(10, 190, 71, 41));
        master_Heat->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(226, 152, 21);\n"
"	font: 12pt \"Arial\";\n"
"	color:white;\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        aeration = new QPushButton(centralWidget);
        aeration->setObjectName(QStringLiteral("aeration"));
        aeration->setGeometry(QRect(20, 520, 60, 40));
        aeration->setFont(font);
        aeration->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve9 = new QPushButton(centralWidget);
        valve9->setObjectName(QStringLiteral("valve9"));
        valve9->setGeometry(QRect(550, 160, 20, 20));
        valve9->setFont(font);
        valve9->setStyleSheet(QLatin1String("QPushButton {\n"
"    border-radius: 0px;\n"
"    background-color: rgb(203, 34, 91);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: grey;\n"
"}"));
        valve3_5 = new QFrame(centralWidget);
        valve3_5->setObjectName(QStringLiteral("valve3_5"));
        valve3_5->setGeometry(QRect(640, 80, 121, 61));
        valve3_5->setStyleSheet(QLatin1String("QFrame {\n"
"	background: white;\n"
"	border-radius: 10px;\n"
"}"));
        valve3_5->setFrameShape(QFrame::StyledPanel);
        valve3_5->setFrameShadow(QFrame::Raised);
        label_44 = new QLabel(valve3_5);
        label_44->setObjectName(QStringLiteral("label_44"));
        label_44->setGeometry(QRect(10, 40, 31, 21));
        label_44->setFont(font1);
        label_44->setStyleSheet(QStringLiteral("color: rgb(0, 138, 205)"));
        HLT_In_4 = new QLabel(valve3_5);
        HLT_In_4->setObjectName(QStringLiteral("HLT_In_4"));
        HLT_In_4->setGeometry(QRect(60, 20, 51, 20));
        HLT_In_4->setFont(font1);
        HLT_In_4->setStyleSheet(QStringLiteral(""));
        BLK_Out = new QLabel(valve3_5);
        BLK_Out->setObjectName(QStringLiteral("BLK_Out"));
        BLK_Out->setGeometry(QRect(50, 40, 71, 20));
        BLK_Out->setFont(font1);
        BLK_Out->setStyleSheet(QStringLiteral(""));
        label_45 = new QLabel(valve3_5);
        label_45->setObjectName(QStringLiteral("label_45"));
        label_45->setGeometry(QRect(10, 20, 21, 21));
        label_45->setFont(font1);
        label_45->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        BLK_In = new QLabel(valve3_5);
        BLK_In->setObjectName(QStringLiteral("BLK_In"));
        BLK_In->setGeometry(QRect(50, 20, 71, 20));
        BLK_In->setFont(font1);
        BLK_In->setStyleSheet(QStringLiteral(""));
        label_37 = new QLabel(valve3_5);
        label_37->setObjectName(QStringLiteral("label_37"));
        label_37->setGeometry(QRect(40, 0, 71, 21));
        label_37->setFont(font1);
        label_37->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        valve3_6 = new QFrame(centralWidget);
        valve3_6->setObjectName(QStringLiteral("valve3_6"));
        valve3_6->setGeometry(QRect(140, 80, 121, 61));
        valve3_6->setStyleSheet(QLatin1String("QFrame {\n"
"	background: white;\n"
"	border-radius: 10px;\n"
"}"));
        valve3_6->setFrameShape(QFrame::StyledPanel);
        valve3_6->setFrameShadow(QFrame::Raised);
        label_46 = new QLabel(valve3_6);
        label_46->setObjectName(QStringLiteral("label_46"));
        label_46->setGeometry(QRect(10, 40, 31, 21));
        label_46->setFont(font1);
        label_46->setStyleSheet(QStringLiteral("color: rgb(0, 138, 205)"));
        HLT_In_5 = new QLabel(valve3_6);
        HLT_In_5->setObjectName(QStringLiteral("HLT_In_5"));
        HLT_In_5->setGeometry(QRect(60, 20, 51, 20));
        HLT_In_5->setFont(font1);
        HLT_In_5->setStyleSheet(QStringLiteral(""));
        HLT_Out = new QLabel(valve3_6);
        HLT_Out->setObjectName(QStringLiteral("HLT_Out"));
        HLT_Out->setGeometry(QRect(50, 40, 71, 20));
        HLT_Out->setFont(font1);
        HLT_Out->setStyleSheet(QStringLiteral(""));
        label_47 = new QLabel(valve3_6);
        label_47->setObjectName(QStringLiteral("label_47"));
        label_47->setGeometry(QRect(10, 20, 21, 21));
        label_47->setFont(font1);
        label_47->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        HLT_In = new QLabel(valve3_6);
        HLT_In->setObjectName(QStringLiteral("HLT_In"));
        HLT_In->setGeometry(QRect(50, 20, 71, 20));
        HLT_In->setFont(font1);
        HLT_In->setStyleSheet(QStringLiteral(""));
        label_48 = new QLabel(valve3_6);
        label_48->setObjectName(QStringLiteral("label_48"));
        label_48->setGeometry(QRect(40, 0, 71, 21));
        label_48->setFont(font1);
        label_48->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        valve3_7 = new QFrame(centralWidget);
        valve3_7->setObjectName(QStringLiteral("valve3_7"));
        valve3_7->setGeometry(QRect(390, 80, 121, 61));
        valve3_7->setStyleSheet(QLatin1String("QFrame {\n"
"	background: white;\n"
"	border-radius: 10px;\n"
"}"));
        valve3_7->setFrameShape(QFrame::StyledPanel);
        valve3_7->setFrameShadow(QFrame::Raised);
        label_51 = new QLabel(valve3_7);
        label_51->setObjectName(QStringLiteral("label_51"));
        label_51->setGeometry(QRect(10, 40, 31, 21));
        label_51->setFont(font1);
        label_51->setStyleSheet(QStringLiteral("color: rgb(0, 138, 205)"));
        HLT_In_7 = new QLabel(valve3_7);
        HLT_In_7->setObjectName(QStringLiteral("HLT_In_7"));
        HLT_In_7->setGeometry(QRect(60, 20, 51, 20));
        HLT_In_7->setFont(font1);
        HLT_In_7->setStyleSheet(QStringLiteral(""));
        MLT_Out = new QLabel(valve3_7);
        MLT_Out->setObjectName(QStringLiteral("MLT_Out"));
        MLT_Out->setGeometry(QRect(50, 40, 71, 20));
        MLT_Out->setFont(font1);
        MLT_Out->setStyleSheet(QStringLiteral(""));
        label_52 = new QLabel(valve3_7);
        label_52->setObjectName(QStringLiteral("label_52"));
        label_52->setGeometry(QRect(10, 20, 21, 21));
        label_52->setFont(font1);
        label_52->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        MLT_In = new QLabel(valve3_7);
        MLT_In->setObjectName(QStringLiteral("MLT_In"));
        MLT_In->setGeometry(QRect(50, 20, 71, 20));
        MLT_In->setFont(font1);
        MLT_In->setStyleSheet(QStringLiteral(""));
        label_53 = new QLabel(valve3_7);
        label_53->setObjectName(QStringLiteral("label_53"));
        label_53->setGeometry(QRect(40, 0, 71, 21));
        label_53->setFont(font1);
        label_53->setStyleSheet(QStringLiteral("color:  rgb(0, 138, 205)"));
        Beersmith_Import = new QPushButton(centralWidget);
        Beersmith_Import->setObjectName(QStringLiteral("Beersmith_Import"));
        Beersmith_Import->setGeometry(QRect(630, 250, 141, 61));
        Beersmith_Import->setFont(font2);
        MainWindow->setCentralWidget(centralWidget);
        HLT->raise();
        BLK->raise();
        MLT->raise();
        frame_38->raise();
        frame_24->raise();
        frame_34->raise();
        valve3->raise();
        water->raise();
        frame_2->raise();
        valve2->raise();
        valve1->raise();
        valve3u->raise();
        valve3d->raise();
        waterPump->raise();
        line->raise();
        frame_3->raise();
        frame_4->raise();
        frame_5->raise();
        frame_6->raise();
        frame_7->raise();
        frame_8->raise();
        frame_9->raise();
        frame_10->raise();
        valve4->raise();
        frame_11->raise();
        frame_12->raise();
        valve6->raise();
        frame_13->raise();
        valve5->raise();
        frame_15->raise();
        frame_14->raise();
        frame_17->raise();
        frame_18->raise();
        frame_20->raise();
        frame_19->raise();
        valve7u->raise();
        valve7->raise();
        valve7d->raise();
        valve8d->raise();
        valve8->raise();
        valve8u->raise();
        frame_21->raise();
        frame_22->raise();
        valve10->raise();
        frame_25->raise();
        frame_26->raise();
        frame_27->raise();
        frame_28->raise();
        frame_29->raise();
        frame->raise();
        wortPump->raise();
        frame_30->raise();
        frame_31->raise();
        frame_32->raise();
        frame_33->raise();
        frame_35->raise();
        frame_36->raise();
        frame_37->raise();
        frame_23->raise();
        frame_39->raise();
        water_2->raise();
        frame_41->raise();
        frame_44->raise();
        frame_45->raise();
        frame_46->raise();
        frame_42->raise();
        water_4->raise();
        graph1->raise();
        graph2->raise();
        HLT_Heat->raise();
        BLK_Heat->raise();
        phase1->raise();
        phase2->raise();
        phase3->raise();
        phase4->raise();
        phase5->raise();
        phase9->raise();
        phase6->raise();
        phase10->raise();
        phase7->raise();
        phase8->raise();
        label->raise();
        label_2->raise();
        label_3->raise();
        label_4->raise();
        label_5->raise();
        Strike_Target->raise();
        Strike_Actual->raise();
        Sparg_Target->raise();
        Sparge_Actual->raise();
        label_6->raise();
        label_7->raise();
        Pre_Boil_Target->raise();
        Pre_Boil_Actual->raise();
        Post_Boil_Target->raise();
        Post_Boil_Actual->raise();
        label_8->raise();
        HLT_Fill_1_Actual->raise();
        HLT_Fill_1_Target->raise();
        label_9->raise();
        label_10->raise();
        HLT_Fill_2_Target->raise();
        HLT_Fill_2_Actual->raise();
        label_11->raise();
        label_12->raise();
        Strike_Temp->raise();
        label_13->raise();
        label_15->raise();
        Fermenter_Actual->raise();
        Fermenter_Target->raise();
        label_16->raise();
        HLT_Fill_2_Temp->raise();
        label_17->raise();
        Sparge_Temp->raise();
        label_18->raise();
        Mash_Steps->raise();
        label_14->raise();
        Add_Mash_Step->raise();
        Add_Boil_Step->raise();
        label_19->raise();
        Boil_Steps->raise();
        label_20->raise();
        Mash_Timer->raise();
        Boil_Timer->raise();
        label_23->raise();
        Notes->raise();
        label_24->raise();
        Messages->raise();
        label_25->raise();
        Turn_Off_Alarm->raise();
        label_26->raise();
        pH->raise();
        DO->raise();
        label_29->raise();
        label_30->raise();
        DO_target->raise();
        pH_target->raise();
        label_27->raise();
        Pause->raise();
        E_Stop->raise();
        label_39->raise();
        label_40->raise();
        MLT_Heat->raise();
        alarm_Text->raise();
        label_21->raise();
        HLT_Vol->raise();
        label_41->raise();
        label_42->raise();
        MLT_Vol->raise();
        BLK_Vol->raise();
        label_43->raise();
        master_Heat->raise();
        aeration->raise();
        valve9->raise();
        valve3_5->raise();
        valve3_6->raise();
        valve3_7->raise();
        frame_40->raise();
        frame_16->raise();
        Beersmith_Import->raise();
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1920, 21));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Automated Brewery Dashboard", 0));
        HLT->setFormat(QApplication::translate("MainWindow", "%v gal", 0));
        MLT->setFormat(QApplication::translate("MainWindow", "%v gal", 0));
        BLK->setFormat(QApplication::translate("MainWindow", "%v gal", 0));
        valve2->setText(QApplication::translate("MainWindow", "2", 0));
        valve1->setText(QApplication::translate("MainWindow", "1", 0));
        valve3u->setText(QApplication::translate("MainWindow", "3u", 0));
        valve3d->setText(QApplication::translate("MainWindow", "3d", 0));
        waterPump->setText(QApplication::translate("MainWindow", "Water", 0));
        valve4->setText(QApplication::translate("MainWindow", "4", 0));
        valve6->setText(QApplication::translate("MainWindow", "6", 0));
        valve5->setText(QApplication::translate("MainWindow", "5", 0));
        valve7u->setText(QApplication::translate("MainWindow", "7u", 0));
        valve7d->setText(QApplication::translate("MainWindow", "7d", 0));
        valve8d->setText(QApplication::translate("MainWindow", "8d", 0));
        valve8u->setText(QApplication::translate("MainWindow", "8u", 0));
        valve10->setText(QApplication::translate("MainWindow", "10", 0));
        wortPump->setText(QApplication::translate("MainWindow", "Wort", 0));
        HLT_Heat->setText(QApplication::translate("MainWindow", "Current temp: XXX \n"
"Target temp: XXX", 0));
        BLK_Heat->setText(QApplication::translate("MainWindow", "Current temp: XXX", 0));
        phase1->setText(QApplication::translate("MainWindow", "Phase 1: filling HLT \n"
"with cold water", 0));
        phase2->setText(QApplication::translate("MainWindow", "Phase 2: heating and \n"
"recirculating HLT", 0));
        phase3->setText(QApplication::translate("MainWindow", "Phase 3: filling MLT \n"
"with heated water", 0));
        phase4->setText(QApplication::translate("MainWindow", "Phase 4: refilling HLT\n"
"with water as needed", 0));
        phase5->setText(QApplication::translate("MainWindow", "Phase 5: heating and \n"
"recirculating HLT/MLT", 0));
        phase9->setText(QApplication::translate("MainWindow", "Phase 9: cooling wort \n"
"and filling fermenter", 0));
        phase6->setText(QApplication::translate("MainWindow", "Phase 6: mashing", 0));
        phase10->setText(QApplication::translate("MainWindow", "Phase 10: cleaning", 0));
        phase7->setText(QApplication::translate("MainWindow", "Phase 7: sparging", 0));
        phase8->setText(QApplication::translate("MainWindow", "Phase 8: boiling", 0));
        label->setText(QApplication::translate("MainWindow", "Volumes", 0));
        label_2->setText(QApplication::translate("MainWindow", "Volume", 0));
        label_3->setText(QApplication::translate("MainWindow", "Target", 0));
        label_4->setText(QApplication::translate("MainWindow", "Actual", 0));
        label_5->setText(QApplication::translate("MainWindow", "Strike", 0));
        Strike_Actual->setText(QString());
        Sparge_Actual->setText(QString());
        label_6->setText(QApplication::translate("MainWindow", "Sparge", 0));
        label_7->setText(QApplication::translate("MainWindow", "Pre-boil", 0));
        Pre_Boil_Actual->setText(QString());
        Post_Boil_Actual->setText(QString());
        label_8->setText(QApplication::translate("MainWindow", "Post-boil", 0));
        HLT_Fill_1_Actual->setText(QString());
        label_9->setText(QApplication::translate("MainWindow", "HLT 1st  fill", 0));
        label_10->setText(QApplication::translate("MainWindow", "HLT 2nd fill", 0));
        HLT_Fill_2_Actual->setText(QString());
        label_11->setText(QApplication::translate("MainWindow", "Strike", 0));
        label_12->setText(QApplication::translate("MainWindow", "Temperature", 0));
        label_13->setText(QApplication::translate("MainWindow", "Temperatures", 0));
        label_15->setText(QApplication::translate("MainWindow", "Target", 0));
        Fermenter_Actual->setText(QString());
        label_16->setText(QApplication::translate("MainWindow", "Fermenter", 0));
        label_17->setText(QApplication::translate("MainWindow", "HLT 2nd fill", 0));
        label_18->setText(QApplication::translate("MainWindow", "Sparge", 0));
        QTableWidgetItem *___qtablewidgetitem = Mash_Steps->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QApplication::translate("MainWindow", "#", 0));
        QTableWidgetItem *___qtablewidgetitem1 = Mash_Steps->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QApplication::translate("MainWindow", "Vol added", 0));
        QTableWidgetItem *___qtablewidgetitem2 = Mash_Steps->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QApplication::translate("MainWindow", "Tempurature", 0));
        QTableWidgetItem *___qtablewidgetitem3 = Mash_Steps->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QApplication::translate("MainWindow", "Length", 0));
        label_14->setText(QApplication::translate("MainWindow", "Mash timer:", 0));
        Add_Mash_Step->setText(QApplication::translate("MainWindow", "Add mash step", 0));
        Add_Boil_Step->setText(QApplication::translate("MainWindow", "Add boil step", 0));
        label_19->setText(QApplication::translate("MainWindow", "Boil schedule", 0));
        QTableWidgetItem *___qtablewidgetitem4 = Boil_Steps->horizontalHeaderItem(0);
        ___qtablewidgetitem4->setText(QApplication::translate("MainWindow", "#", 0));
        QTableWidgetItem *___qtablewidgetitem5 = Boil_Steps->horizontalHeaderItem(1);
        ___qtablewidgetitem5->setText(QApplication::translate("MainWindow", "Time", 0));
        QTableWidgetItem *___qtablewidgetitem6 = Boil_Steps->horizontalHeaderItem(2);
        ___qtablewidgetitem6->setText(QApplication::translate("MainWindow", "Ingredient", 0));
        QTableWidgetItem *___qtablewidgetitem7 = Boil_Steps->horizontalHeaderItem(3);
        ___qtablewidgetitem7->setText(QApplication::translate("MainWindow", "Amount", 0));
        label_20->setText(QApplication::translate("MainWindow", "Mash schedule", 0));
        Mash_Timer->setText(QApplication::translate("MainWindow", "99:99", 0));
        Boil_Timer->setText(QApplication::translate("MainWindow", "99:99", 0));
        label_23->setText(QApplication::translate("MainWindow", "Boil timer:", 0));
        label_24->setText(QApplication::translate("MainWindow", "Notes", 0));

        const bool __sortingEnabled = Messages->isSortingEnabled();
        Messages->setSortingEnabled(false);
        QListWidgetItem *___qlistwidgetitem = Messages->item(0);
        ___qlistwidgetitem->setText(QApplication::translate("MainWindow", "Alarm", 0));
        QListWidgetItem *___qlistwidgetitem1 = Messages->item(1);
        ___qlistwidgetitem1->setText(QApplication::translate("MainWindow", "Warning", 0));
        QListWidgetItem *___qlistwidgetitem2 = Messages->item(2);
        ___qlistwidgetitem2->setText(QApplication::translate("MainWindow", "Message", 0));
        QListWidgetItem *___qlistwidgetitem3 = Messages->item(3);
        ___qlistwidgetitem3->setText(QApplication::translate("MainWindow", "Sucess", 0));
        Messages->setSortingEnabled(__sortingEnabled);

        label_25->setText(QApplication::translate("MainWindow", "Messages", 0));
        Turn_Off_Alarm->setText(QApplication::translate("MainWindow", "Turn off alarm", 0));
        label_26->setText(QApplication::translate("MainWindow", "MLT pH:", 0));
        pH->setText(QApplication::translate("MainWindow", "7.00", 0));
        DO->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_29->setText(QApplication::translate("MainWindow", "<html><head/><body><p>DO:</p></body></html>", 0));
        label_30->setText(QApplication::translate("MainWindow", "<html><head/><body><p>Target:</p></body></html>", 0));
        DO_target->setText(QApplication::translate("MainWindow", "7.00", 0));
        pH_target->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_27->setText(QApplication::translate("MainWindow", "Target:", 0));
        Pause->setText(QApplication::translate("MainWindow", "Pause", 0));
        E_Stop->setText(QApplication::translate("MainWindow", "Emergency Stop", 0));
        label_39->setText(QApplication::translate("MainWindow", "Temperature", 0));
        label_40->setText(QApplication::translate("MainWindow", "Power", 0));
        MLT_Heat->setText(QApplication::translate("MainWindow", "Current temp: XXX", 0));
        alarm_Text->setText(QApplication::translate("MainWindow", "Off", 0));
        label_21->setText(QApplication::translate("MainWindow", "Alarm switch:", 0));
        HLT_Vol->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_41->setText(QApplication::translate("MainWindow", "HLT Vol:", 0));
        label_42->setText(QApplication::translate("MainWindow", "MLT Vol:", 0));
        MLT_Vol->setText(QApplication::translate("MainWindow", "7.00", 0));
        BLK_Vol->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_43->setText(QApplication::translate("MainWindow", "BLK Vol:", 0));
        master_Heat->setText(QApplication::translate("MainWindow", "Master\n"
"heat", 0));
        aeration->setText(QApplication::translate("MainWindow", "Aeration", 0));
        valve9->setText(QApplication::translate("MainWindow", "9", 0));
        label_44->setText(QApplication::translate("MainWindow", "Out:", 0));
        HLT_In_4->setText(QApplication::translate("MainWindow", "7.00", 0));
        BLK_Out->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_45->setText(QApplication::translate("MainWindow", "In:", 0));
        BLK_In->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_37->setText(QApplication::translate("MainWindow", "Flow", 0));
        label_46->setText(QApplication::translate("MainWindow", "Out:", 0));
        HLT_In_5->setText(QApplication::translate("MainWindow", "7.00", 0));
        HLT_Out->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_47->setText(QApplication::translate("MainWindow", "In:", 0));
        HLT_In->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_48->setText(QApplication::translate("MainWindow", "Flow", 0));
        label_51->setText(QApplication::translate("MainWindow", "Out:", 0));
        HLT_In_7->setText(QApplication::translate("MainWindow", "7.00", 0));
        MLT_Out->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_52->setText(QApplication::translate("MainWindow", "In:", 0));
        MLT_In->setText(QApplication::translate("MainWindow", "7.00", 0));
        label_53->setText(QApplication::translate("MainWindow", "Flow", 0));
        Beersmith_Import->setText(QApplication::translate("MainWindow", "Import\n"
"BeerSmith File", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DASHBOARDLARGE_H
