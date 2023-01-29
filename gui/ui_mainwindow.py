# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: #bdbdbd;")
        self.runButton = QPushButton(self.centralwidget)
        self.runButton.setObjectName(u"runButton")
        self.runButton.setGeometry(QRect(680, 70, 75, 24))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(500, 70, 171, 22))
        self.loadFile = QPushButton(self.centralwidget)
        self.loadFile.setObjectName(u"loadFile")
        self.loadFile.setGeometry(QRect(680, 30, 75, 23))
        self.fileNameLabel = QLabel(self.centralwidget)
        self.fileNameLabel.setObjectName(u"fileNameLabel")
        self.fileNameLabel.setGeometry(QRect(500, 30, 171, 21))
        self.fileNameLabel.setStyleSheet(u"background: white;")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(220, 530, 75, 23))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(510, 260, 121, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(510, 320, 111, 16))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(120, 530, 75, 23))
        self.marking = QLabel(self.centralwidget)
        self.marking.setObjectName(u"marking")
        self.marking.setGeometry(QRect(510, 290, 141, 16))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.loadFile.setText(QCoreApplication.translate("MainWindow", u"Open file", None))
        self.fileNameLabel.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Po\u010diato\u010dn\u00e9 ozna\u010denie", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Postupnos\u0165 krokov", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.marking.setText("")
    # retranslateUi

