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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFrame, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(819, 600)
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
        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(260, 430, 75, 23))
        self.initial_marking_label = QLabel(self.centralwidget)
        self.initial_marking_label.setObjectName(u"initial_marking_label")
        self.initial_marking_label.setGeometry(QRect(20, 460, 121, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(400, 350, 111, 16))
        self.prevButton = QPushButton(self.centralwidget)
        self.prevButton.setObjectName(u"prevButton")
        self.prevButton.setGeometry(QRect(150, 430, 75, 23))
        self.marking = QLabel(self.centralwidget)
        self.marking.setObjectName(u"marking")
        self.marking.setGeometry(QRect(20, 480, 141, 16))
        self.photo = QLabel(self.centralwidget)
        self.photo.setObjectName(u"photo")
        self.photo.setGeometry(QRect(10, 10, 421, 331))
        self.photo.setFrameShape(QFrame.Box)
        self.photo.setScaledContents(False)
        self.photo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.photo.setWordWrap(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 510, 141, 16))
        self.actual_marking = QLabel(self.centralwidget)
        self.actual_marking.setObjectName(u"actual_marking")
        self.actual_marking.setGeometry(QRect(20, 530, 131, 16))
        self.steps = QListWidget(self.centralwidget)
        self.steps.setObjectName(u"steps")
        self.steps.setGeometry(QRect(400, 370, 391, 221))
        self.steps.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.steps.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.steps.setSelectionMode(QAbstractItemView.NoSelection)
        self.clearAll = QPushButton(self.centralwidget)
        self.clearAll.setObjectName(u"clearAll")
        self.clearAll.setGeometry(QRect(680, 110, 75, 23))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.loadFile.setText(QCoreApplication.translate("MainWindow", u"Open file", None))
        self.fileNameLabel.setText("")
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.initial_marking_label.setText(QCoreApplication.translate("MainWindow", u"Po\u010diato\u010dn\u00e9 ozna\u010denie", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Postupnos\u0165 krokov", None))
        self.prevButton.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.marking.setText("")
        self.photo.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Aktu\u00e1lne zna\u010denie", None))
        self.actual_marking.setText("")
        self.clearAll.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
    # retranslateUi

