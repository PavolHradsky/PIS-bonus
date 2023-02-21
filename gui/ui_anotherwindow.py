# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'anotherwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.enter = QPushButton(self.centralwidget)
        self.enter.setObjectName(u"enter")
        self.enter.setGeometry(QRect(690, 550, 93, 28))
        self.places = QLabel(self.centralwidget)
        self.places.setObjectName(u"places")
        self.places.setGeometry(QRect(60, 30, 101, 21))
        self.transitions = QLabel(self.centralwidget)
        self.transitions.setObjectName(u"transitions")
        self.transitions.setGeometry(QRect(510, 40, 131, 21))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.enter.setText(QCoreApplication.translate("MainWindow", u"SAVE", None))
        self.places.setText("")
        self.transitions.setText("")
    # retranslateUi

