# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'responsive.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1130, 789)
        MainWindow.setStyleSheet(u"background: #bdbdbd;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.photo = QLabel(self.centralwidget)
        self.photo.setObjectName(u"photo")
        self.photo.setEnabled(True)
        self.photo.setMinimumSize(QSize(400, 400))
        self.photo.setFrameShape(QFrame.Box)
        self.photo.setLineWidth(0)

        self.horizontalLayout.addWidget(self.photo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.fileNameLabel = QLabel(self.centralwidget)
        self.fileNameLabel.setObjectName(u"fileNameLabel")
        self.fileNameLabel.setMinimumSize(QSize(150, 25))
        self.fileNameLabel.setMaximumSize(QSize(150, 25))
        self.fileNameLabel.setStyleSheet(u"background: white;")

        self.horizontalLayout_4.addWidget(self.fileNameLabel)

        self.loadFile = QPushButton(self.centralwidget)
        self.loadFile.setObjectName(u"loadFile")
        self.loadFile.setMinimumSize(QSize(75, 25))
        self.loadFile.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_4.addWidget(self.loadFile)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QSize(150, 25))
        self.comboBox.setMaximumSize(QSize(150, 25))

        self.horizontalLayout_5.addWidget(self.comboBox)

        self.runButton = QPushButton(self.centralwidget)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setMinimumSize(QSize(75, 25))
        self.runButton.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_5.addWidget(self.runButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.clearAll = QPushButton(self.centralwidget)
        self.clearAll.setObjectName(u"clearAll")
        self.clearAll.setMinimumSize(QSize(75, 25))
        self.clearAll.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_6.addWidget(self.clearAll)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(3, 6)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 2)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.prevButton = QPushButton(self.centralwidget)
        self.prevButton.setObjectName(u"prevButton")
        self.prevButton.setMinimumSize(QSize(75, 25))
        self.prevButton.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_9.addWidget(self.prevButton)

        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setMinimumSize(QSize(75, 25))
        self.nextButton.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_9.addWidget(self.nextButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.initial_marking_label = QLabel(self.centralwidget)
        self.initial_marking_label.setObjectName(u"initial_marking_label")

        self.verticalLayout_5.addWidget(self.initial_marking_label)

        self.marking = QLabel(self.centralwidget)
        self.marking.setObjectName(u"marking")

        self.verticalLayout_5.addWidget(self.marking)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.actual_marking = QLabel(self.centralwidget)
        self.actual_marking.setObjectName(u"actual_marking")

        self.verticalLayout_5.addWidget(self.actual_marking)


        self.verticalLayout_3.addLayout(self.verticalLayout_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.steps = QListWidget(self.centralwidget)
        self.steps.setObjectName(u"steps")
        self.steps.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.steps.sizePolicy().hasHeightForWidth())
        self.steps.setSizePolicy(sizePolicy1)
        self.steps.setMinimumSize(QSize(500, 75))
        self.steps.setMaximumSize(QSize(500, 200))

        self.verticalLayout_4.addWidget(self.steps)


        self.horizontalLayout_7.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.photo.setText("")
        self.fileNameLabel.setText("")
        self.loadFile.setText(QCoreApplication.translate("MainWindow", u"Open file", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.clearAll.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
        self.prevButton.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.initial_marking_label.setText(QCoreApplication.translate("MainWindow", u"Po\u010diato\u010dn\u00e9 ozna\u010denie", None))
        self.marking.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Aktu\u00e1lne zna\u010denie", None))
        self.actual_marking.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Postupnos\u0165 krokov", None))
    # retranslateUi

