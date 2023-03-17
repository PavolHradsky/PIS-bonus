from math import sin, cos, pi, atan2, sqrt
import bcrypt
import cv2
from database import connect
import numpy as np
import xml.etree.ElementTree as ET
import re
import sys
from PetriNet import PetriNet
from Place import Place
from Transition import Transition
from functions import read_xml, list_is_greater
from Rpn import Rpn
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QMessageBox
from PySide6.QtCore import QFile, QTimer, QTime
import os
import glob
from PySide6.QtGui import QPixmap, QImage


def loading_data(name_file, fuzzy_flag, weights_flag, threshold_flag, flag):
    places, transitions, arcs, role = read_xml(
        name_file, fuzzy_flag, weights_flag, threshold_flag, flag)
    net: PetriNet = PetriNet(places, transitions, arcs, role)
    if flag:
        if weights_flag:
            net.weights = [float(t.getWeight()) for t in transitions]
        if threshold_flag:
            net.tresholds = [float(t.getTreshold()) for t in transitions]
        if weights_flag and threshold_flag:
            net.weights = [float(t.getWeight()) for t in transitions]
            net.tresholds = [float(t.getTreshold()) for t in transitions]
    return net


def reachability(net):
    M = []
    H = []
    M.append(Rpn(net.M0))
    for m in M:
        if not m.visited:
            for t in net.T:
                if net.step(t, m.state) is not None:
                    new_m = net.step(t, m.state)
                    if new_m not in [a.state for a in M]:
                        M.append(Rpn(new_m))
                    H.append((m.state, t, new_m))
            m.visited = True
            for old_m in [a.state for a in M]:
                if list_is_greater([a.state for a in M][-1], old_m):
                    print("Siet je neohranicena")
                    return None
    return M


class MainAplication(QMainWindow):
    loader = QUiLoader()
    file_path = None
    file_name = None
    anotherWindow = None

    def __init__(self):
        super().__init__()
        self.main_layout = QWidget()
        self.ui = QFile(".\\gui\\responsive.ui")
        self.ui.open(QFile.ReadOnly)
        self.main_layout = self.loader.load(self.ui)
        self.ui.close()
        self.setCentralWidget(self.main_layout)
        self.setWindowIcon(QtGui.QIcon(
            'C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            "QMainWindow::titleBar { background-color: black; }")
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Chronické zlyhávanie srdca")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.image_number = 1
        self.main_layout.loadFile.clicked.connect(self.open_dialog)
        self.main_layout.comboBox.addItems(["Logická Petriho sieť",
                                            "Fuzzy Petriho sieť",
                                            "Fuzzy Petriho sieť s váhami pravidiel",
                                            "Fuzzy Petriho sieť s váhami a prahmi pravidiel"])
        self.main_layout.comboBox.currentIndexChanged.connect(
            self.combo_changed)
        self.main_layout.runButton.clicked.connect(self.run)
        self.main_layout.prevButton.clicked.connect(self.prev)
        self.main_layout.nextButton.clicked.connect(self.next)
        self.main_layout.clearAll.clicked.connect(self.clear)
        self.main_layout.clearAll.setEnabled(False)
        self.main_layout.steps.setStyleSheet(
            "background-color: black; color: green;")
        self.main_layout.table.setStyleSheet("background-color: black;")
        self.image_dict = {}
        self.step_dict = {}
        self.actual_marking_dict = {}
        self.TR = []
        self.k = 0
        self.tree = None
        self.ui = QFile(".\\gui\\anotherWindowFinal.ui")
        self.ui.open(QFile.ReadOnly)
        self.anotherWindow = self.loader.load(self.ui)
        self.anotherWindow.setWindowIcon(QtGui.QIcon(
            'C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
        self.anotherWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.anotherWindow.setStyleSheet(
            "QMainWindow::titleBar { background-color: black; }")
        self.anotherWindow.setGeometry(200, 200, 800, 600)
        self.anotherWindow.setWindowTitle("Nastavenie váh a prahov pravidiel")
        self.anotherWindow.table.setStyleSheet("background-color: black;")
        self.ui.close()
        self.net = None
        self.root = None
        self.tresholds_flag = 0
        self.weights_flag = 0
        self.fuzzy_flag = 0
        self.logical_flag = 0
        self.dict_weights = {}
        self.dict_tresholds = {}
        self.dict_marks = {}
        self.dict_places = {}
        self.dict_transitions = {}
        self.database_output_table1 = ()
        self.database_output_table2 = ()
        self.image_index = 1
        self.dict_final = {}
        self.transitions_to_change = []
        self.fuzzyfication = 0
        self.list_edit_widgets = []
        self.fuzzyficated_M0 = [1, 0, 1, 0, 0, 0, 0, 0]
        self.anotherWindow.fuzzyficate_run.clicked.connect(self.fuzzyficate)
        if self.image_number == 1:
            self.main_layout.prevButton.setEnabled(False)
            self.main_layout.prevButton.setStyleSheet("""
                QPushButton:disabled {
                    color: green;
                }
                QPushButton:disabled:!checked {
                    background-color: rgba(255,0,0,0.5);
                }
            """)
        if len(self.dict_final) == 0:
            self.main_layout.nextButton.setEnabled(False)
            self.main_layout.nextButton.setStyleSheet("""
                QPushButton:disabled {
                    color: green;
                }
                QPushButton:disabled:!checked {
                    background-color: rgba(255,0,0,0.5);
                }
            """)

    def update_time(self):
        # Get the current system time
        current_time = QTime.currentTime()
        # Format the time as HH:mm:ss
        formatted_time = current_time.toString('HH:mm:ss')
        # Update the time label
        self.main_layout.time_actual.setText(formatted_time)

    def resizeEvent(self, event):
        if len(self.image_dict) > 0:
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(
            ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
        event.accept()

    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'c:\\', "XML files (*.xml)")
        if fname[0]:
            self.file_name = re.search(r'[^/\\&\?]+\.\w+$', fname[0]).group(0)
            self.main_layout.fileNameLabel.setText(self.file_name)
            self.file_path = fname[0]
        else:
            self.main_layout.fileNameLabel.setText("No file selected")
            self.file_path = None
            self.file_name = None
        self.main_layout.clearAll.setEnabled(True)

    def combo_changed(self):
        print(self.main_layout.comboBox.currentText())

    def run(self):
        self.anotherWindow.table.setColumnCount(5)
        self.anotherWindow.table.setHorizontalHeaderLabels(
            ["Pacient ID", "Pulz", "Okysličenie krvi", "Systolický KT", "Diastolický KT"])
        header = self.anotherWindow.table.horizontalHeader()
        header.setStyleSheet("background-color: black; color: black;")
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.anotherWindow.table.setRowCount(1)
        item_0 = QtWidgets.QTableWidgetItem(
            str(self.database_output_table2[1]))
        item_0.setForeground(QtGui.QColor("white"))
        self.anotherWindow.table.setItem(0, 0, item_0)

        item_1 = QtWidgets.QTableWidgetItem(
            str(self.database_output_table2[2]))
        item_1.setForeground(QtGui.QColor("white"))
        self.anotherWindow.table.setItem(0, 1, item_1)

        item_2 = QtWidgets.QTableWidgetItem(
            str(self.database_output_table2[3]))
        item_2.setForeground(QtGui.QColor("white"))
        self.anotherWindow.table.setItem(0, 2, item_2)

        item_3 = QtWidgets.QTableWidgetItem(
            str(self.database_output_table2[4]))
        item_3.setForeground(QtGui.QColor("white"))
        self.anotherWindow.table.setItem(0, 3, item_3)

        item_4 = QtWidgets.QTableWidgetItem(
            str(self.database_output_table2[5]))
        item_4.setForeground(QtGui.QColor("white"))
        self.anotherWindow.table.setItem(0, 4, item_4)

        if self.file_path:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            if "fuzzy" in self.file_name:
                self.fuzzy_flag = 1
            else:
                self.fuzzy_flag = 0
            self.net = loading_data(
                self.file_name, self.fuzzy_flag, self.weights_flag, self.tresholds_flag, 0)
            if self.main_layout.comboBox.currentText() == "Logická Petriho sieť":
                self.logical_flag = 1
                self.fuzzy_flag = 0
                self.anotherWindow.show()
                self.set_marking_initial()
                self.anotherWindow.enter.clicked.connect(self.run_final)
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť":
                self.fuzzy_flag = 1
                self.logical_flag = 0
                self.anotherWindow.show()
                self.set_marking_initial()
                self.anotherWindow.enter.clicked.connect(self.run_final)
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť s váhami pravidiel":
                self.weights_flag = 1
                self.tresholds_flag = 0
                self.fuzzy_flag = 1
                self.logical_flag = 0
                self.anotherWindow.show()
                self.set_marking_initial()
                self.anotherWindow.enter.clicked.connect(self.run_final)
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť s váhami a prahmi pravidiel":
                self.tresholds_flag = 1
                self.weights_flag = 1
                self.fuzzy_flag = 1
                self.logical_flag = 0
                self.anotherWindow.show()
                self.set_marking_initial()
                self.anotherWindow.enter.clicked.connect(self.run_final)
        else:
            self.tree = None
            dialog = QMessageBox(text="Nevybrali ste žiadny súbor")
            dialog.setWindowTitle("Message Dialog")
            dialog.setWindowIcon(QtGui.QIcon(
                'C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
            dialog.exec()   # Stores the return value for the button pressed

    def write_to_file_transitions(self):
        for i, rank in enumerate(self.root.iter('transition')):
            new_tag = ET.SubElement(rank, 'treshold')
            new_tag.text = str(self.net.tresholds[i])
            new_tag = ET.SubElement(rank, 'weight')
            new_tag.text = str(self.net.weights[i])

    def run_final(self):
        l = 0
        self.anotherWindow.close()
        for rank in self.root.iter('place'):
            for value in rank:
                if value.tag == 'tokens':
                    if self.fuzzy_flag:
                        value.text = str(float(self.net.M0[l]))
                    else:
                        value.text = str(int(self.net.M0[l]))
                    l += 1
        if self.fuzzy_flag:
            if self.tresholds_flag and self.weights_flag:
                if len(self.net.tresholds) == 0 or len(self.net.weights) == 0:
                    if len(self.net.tresholds) == 0:
                        self.net.tresholds = [
                            0 for _ in range(len(self.dict_transitions))]
                    if len(self.net.weights) == 0:
                        self.net.weights = [
                            0 for _ in range(len(self.dict_weights))]
                    # create new tag to xml to each transition
                    self.write_to_file_transitions()
                else:
                    if len(self.net.tresholds) != 0 and len(self.net.weights) == 0:
                        if len(self.net.weights) == 0:
                            self.net.weights = [
                                0 for _ in range(len(self.dict_weights))]
                        self.write_to_file_transitions()

                    if len(self.net.tresholds) == 0 and len(self.net.weights) != 0:
                        if len(self.net.tresholds) == 0:
                            self.net.tresholds = [
                                0 for _ in range(len(self.dict_transitions))]
                        self.write_to_file_transitions()

                    if len(self.net.tresholds) != 0 and len(self.net.weights) != 0:
                        self.write_to_file_transitions()

            if self.weights_flag and not self.tresholds_flag:
                if len(self.net.weights) == 0:
                    self.net.weights = [
                        0 for _ in range(len(self.dict_weights))]
                    for i, rank in enumerate(self.root.iter('transition')):
                        new_tag = ET.SubElement(rank, 'weight')
                        new_tag.text = str(self.net.weights[i])
                else:
                    for i, rank in enumerate(self.root.iter('transition')):
                        new_tag = ET.SubElement(rank, 'weight')
                        new_tag.text = str(self.net.weights[i])

        dir_path = os.path.dirname(self.file_path)

        self.tree.write(os.path.join(dir_path, self.file_name.split('.')[0] + "_initial" + "_marking.xml"),
                        encoding="UTF-8", xml_declaration=True)
        print("Počiatočné označkovanie: ", self.net.M0)

        if self.logical_flag and not self.fuzzy_flag and not self.weights_flag and not self.tresholds_flag:
            self.net = loading_data(self.file_name.split(
                '.')[0] + "_initial_marking.xml", 0, 0, 0, 1)
            self.run_logical()
        elif self.fuzzy_flag and not self.weights_flag and not self.tresholds_flag and not self.logical_flag:
            self.net = loading_data(self.file_name.split(
                '.')[0] + "_initial_marking.xml", 1, 0, 0, 1)
            self.run_fuzzy()
        elif self.weights_flag and not self.tresholds_flag and self.fuzzy_flag and not self.logical_flag:
            self.net = loading_data(self.file_name.split(
                '.')[0] + "_initial_marking.xml", 1, 1, 0, 1)
            self.run_fuzzy_with_weights()
        elif self.weights_flag and self.tresholds_flag and self.fuzzy_flag and not self.logical_flag:
            self.net = loading_data(self.file_name.split(
                '.')[0] + "_initial_marking.xml", 1, 1, 1, 1)
            self.run_fuzzy_with_weights_and_thresholds()

    def fuzzyficate(self):
        # TODO to the future there will be a function that will fuzzyficate the input data from database and results will be stored in self.fuzzyficated_M0
        # self.database_output_table1
        # self.database_output_table2
        self.net.M0 = self.fuzzyficated_M0
        placesLayout = self.anotherWindow.placesWidget.layout()
        self.anotherWindow.placesWidget.setStyleSheet(
            "background-color: black;")
        counter = 0
        for i, key in enumerate(self.dict_places):
            placeLabel = QtWidgets.QLabel(key)
            placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            placeLabelM0 = QtWidgets.QLabel(str(self.fuzzyficated_M0[i]))
            placeLabelM0.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            placeLabel.setStyleSheet("color: green;")
            placeLabelM0.setStyleSheet("color: green;")
            for j in range(2):
                edit = self.list_edit_widgets[i+j+counter]
                placeLayout = QtWidgets.QVBoxLayout()
                # remove edit widget from layout
                placeLayout.removeWidget(edit)
                edit.setParent(None)
                placeLayout.addWidget(placeLabel)
                placeLayout.addWidget(placeLabelM0)
                placeLayout.addStretch()
                placesLayout.addLayout(placeLayout)
            counter += 1
        self.anotherWindow.OK1.setEnabled(False)
        self.anotherWindow.fuzzyficate_run.setEnabled(False)

    def set_marking_initial(self):
        print(self.logical_flag, self.fuzzy_flag,
              self.weights_flag, self.tresholds_flag)
        self.dict_marks = {}
        self.dict_weights = {}
        self.dict_tresholds = {}
        self.list_edit_widgets = []
        for place in self.net.getPlaces():
            self.dict_places[place.label] = place.tokens
        for transition in self.net.getTransitions():
            self.dict_transitions[transition.getId()] = transition.label
        placesLayout = QtWidgets.QVBoxLayout()
        self.anotherWindow.placesWidget.setLayout(placesLayout)
        self.anotherWindow.placesWidget.setStyleSheet(
            "background-color: black;")
        for i, key in enumerate(self.dict_places):
            placeLabel = QtWidgets.QLabel(key)
            placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            placeLabel.setStyleSheet("color: green;")
            entry = QtWidgets.QLineEdit()
            entry.setMaximumWidth(50)
            entry.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(0|1)$"))) if self.logical_flag else entry.setValidator(
                QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(0(\.\d+)?|1)$")))
            entry.setStyleSheet("color: white;")
            self.list_edit_widgets.append(entry)
            self.list_edit_widgets.append(placeLabel)
            self.dict_marks[key] = entry
            placeLayout = QtWidgets.QVBoxLayout()
            placeLayout.addWidget(placeLabel)
            placeLayout.addWidget(entry)
            placeLayout.addStretch()
            placesLayout.addLayout(placeLayout)

        self.anotherWindow.placesScrollArea.setWidget(
            self.anotherWindow.placesWidget)
        self.anotherWindow.OK1.clicked.connect(
            lambda: [self.set_marking(self.dict_marks), self.delete_text(self.dict_marks)])
        self.anotherWindow.tresholdsWidget.setStyleSheet(
            "background-color: black;")
        self.anotherWindow.weightsWidget.setStyleSheet(
            "background-color: black;")

        if self.fuzzy_flag or self.logical_flag and not self.weights_flag and not self.tresholds_flag:
            self.anotherWindow.OK3.setDisabled(True)
            weightsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.weightsWidget.setLayout(weightsLayout)
            self.anotherWindow.weight.setText("Prechody")
            self.anotherWindow.weightsWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_transitions):
                transitionLabel0 = QtWidgets.QLabel(self.dict_transitions[key])
                transitionLabel0.setFont(
                    QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                transitionLabel0.setStyleSheet("color: green;")
                weightLayout = QtWidgets.QVBoxLayout()
                weightLayout.addWidget(transitionLabel0)
                weightsLayout.addLayout(weightLayout)
            self.anotherWindow.weightsScrollArea.setWidget(
                self.anotherWindow.weightsWidget)
            self.anotherWindow.OK2.setDisabled(True)
            self.anotherWindow.tresholdsWidget.setStyleSheet(
                "background-color: black;")

        if self.weights_flag:
            self.anotherWindow.OK3.setDisabled(True)
            self.anotherWindow.OK2.show()
            self.anotherWindow.weight.setText("Váhy prechodov")
            weightsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.weightsWidget = QtWidgets.QWidget()
            self.anotherWindow.weightsWidget.setLayout(weightsLayout)
            self.anotherWindow.weightsWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_transitions):
                weightLabel = QtWidgets.QLabel(self.dict_transitions[key])
                weightLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                weightLabel.setStyleSheet("color: green;")
                entry2 = QtWidgets.QLineEdit()
                entry2.setMaximumWidth(50)
                entry2.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(
                    "^(0(\.\d+)?|1)$"))) if not self.logical_flag else entry2.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(0|1)$")))
                entry2.setStyleSheet("color: white;")
                self.dict_weights[key] = entry2
                weightLayout = QtWidgets.QVBoxLayout()
                weightLayout.addWidget(weightLabel)
                weightLayout.addWidget(entry2)
                weightLayout.addStretch()
                weightsLayout.addLayout(weightLayout)
            self.anotherWindow.weightsScrollArea.setWidget(
                self.anotherWindow.weightsWidget)
            self.anotherWindow.OK2.clicked.connect(lambda: [self.set_weights(
                self.dict_weights), self.delete_text(self.dict_weights)])

        if self.tresholds_flag:
            self.anotherWindow.OK2.setDisabled(False)
            self.anotherWindow.OK3.setDisabled(False)
            tresholdsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.tresholdsWidget = QtWidgets.QWidget()
            self.anotherWindow.tresholdsWidget.setLayout(tresholdsLayout)
            self.anotherWindow.tresholdsWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_transitions):
                transitionLabel = QtWidgets.QLabel(self.dict_transitions[key])
                transitionLabel.setFont(QtGui.QFont(
                    "Arial", 10, QtGui.QFont.Bold))
                transitionLabel.setStyleSheet("color: green;")
                entry3 = QtWidgets.QLineEdit()
                entry3.setMaximumWidth(50)
                entry3.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(
                    "^(0(\.\d+)?|1)$"))) if not self.logical_flag else entry3.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^(0|1)$")))
                entry3.setStyleSheet("color: white;")
                self.dict_tresholds[key] = entry3
                transitionLayout = QtWidgets.QVBoxLayout()
                transitionLayout.addWidget(transitionLabel)
                transitionLayout.addWidget(entry3)
                transitionLayout.addStretch()
                tresholdsLayout.addLayout(transitionLayout)
            self.anotherWindow.tresholdsScrollArea.setWidget(
                self.anotherWindow.tresholdsWidget)
            self.anotherWindow.OK3.clicked.connect(lambda: [self.set_tresholds(
                self.dict_tresholds), self.delete_text(self.dict_tresholds)])

    def delete_text(self, entries):
        for _, value in entries.items():
            value.setText("")

    def set_values(self, array, entries, flag):
        for _, value in entries.items():
            if value.text() == '':
                if flag:
                    array.append(0)
                else:
                    array.append(0.0)
            else:
                try:
                    num = float(value.text().replace(',', '.'))
                    array.append(num)
                except ValueError:
                    QtWidgets.QMessageBox.warning(
                        self, "Invalid Input", "Please enter a valid number.")
                    return
        return array

    def set_marking(self, entries):
        M0 = []
        self.net.M0 = self.set_values(M0, entries, self.logical_flag)

    def set_tresholds(self, entries):
        tresholds = []
        self.net.tresholds = self.set_values(
            tresholds, entries, self.logical_flag)
        self.TR = self.net.tresholds

    def set_weights(self, entries):
        weights = []
        self.net.weights = self.set_values(weights, entries, self.logical_flag)

    def prev(self):
        if self.image_number > 1:
            #  set button active
            self.main_layout.nextButton.setEnabled(True)
            self.main_layout.nextButton.setStyleSheet("""
                QPushButton:enabled {
                    color: rgba(255,0,0,0.5);
                }
                QPushButton:enabled:!checked {
                    background-color: green;
                }
            """)
            if self.image_number == 2:
                self.main_layout.prevButton.setEnabled(False)
                self.main_layout.prevButton.setStyleSheet("""
                QPushButton:disabled {
                    color: green;
                }
                QPushButton:disabled:!checked {
                    background-color: rgba(255,0,0,0.5);
                }
            """)
            self.image_number -= 1
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(
            ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.actual_marking.setText(
                self.actual_marking_dict[self.image_number-1])
            self.main_layout.actual_marking.setStyleSheet(
                "color: green;")  # set color to red
            self.main_layout.actual_marking.adjustSize()
            counter = 0
            for i in range(0, len(self.step_dict[self.image_number])):
                counter += 1
                self.main_layout.steps.takeItem(self.k-1-i)
            self.k -= counter
        else:
            # set button inactive
            self.main_layout.prevButton.setEnabled(False)
            self.main_layout.prevButton.setStyleSheet("""
                QPushButton:disabled {
                    color: green;
                }
                QPushButton:disabled:!checked {
                    background-color: rgba(255,0,0,0.5);
                }
            """)
            self.image_number = 1

    def next(self):
        if self.image_number < len(self.image_dict):
            # set button active
            self.main_layout.prevButton.setEnabled(True)
            self.main_layout.prevButton.setStyleSheet("""
                QPushButton:enabled {
                    color: rgba(255,0,0,0.5);
                }
                QPushButton:enabled:!checked {
                    background-color: green;
                }
            """)
            if self.image_number == len(self.image_dict)-1:
                self.main_layout.nextButton.setEnabled(False)
                self.main_layout.nextButton.setStyleSheet("""
                QPushButton:disabled {
                    color: green;
                }
                QPushButton:disabled:!checked {
                    background-color: rgba(255,0,0,0.5);
                }
            """)
            self.image_number += 1
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            # set alignment of photo to the centre
            self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(
            ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.actual_marking.setText(
                self.actual_marking_dict[self.image_number-1])
            self.main_layout.actual_marking.setStyleSheet(
                "color: green;")  # set color to red
            self.main_layout.actual_marking.adjustSize()
            for i in self.step_dict[self.image_number-1]:
                self.k += 1
                self.main_layout.steps.addItem(str(i))
        else:
            # set button inactive
            self.main_layout.nextButton.setEnabled(False)
            self.image_number -= 1

    def clear(self):
        self.main_layout.fileNameLabel.setText("No file selected")
        if self.main_layout.steps != None:
            self.main_layout.steps.clear()
        if self.main_layout.photo != None:
            self.main_layout.photo.clear()
        if self.main_layout.actual_marking != None:
            self.main_layout.actual_marking.clear()
        if self.main_layout.marking != None:
            self.main_layout.marking.clear()
        self.main_layout.prevButton.setEnabled(False)
        self.main_layout.nextButton.setEnabled(True)
        self.main_layout.clearAll.setEnabled(False)

    def draw_net(self, weights=False, thresholds=False):
        graph_data = {
            'places': [],
            'transitions': [],
            'tresholds': self.net.getThresholds(),
            'weights': self.net.getWeights(),
            'edges': {},
        }
        for arc in self.net.getArcs():
            if isinstance(arc.src, Place):
                graph_data['places'].append(arc.getSourceId())
            else:
                graph_data['transitions'].append(arc.getSourceId())
            if isinstance(arc.dest, Place):
                graph_data['places'].append(arc.getDestinationId())
            else:
                graph_data['transitions'].append(arc.getDestinationId())
            graph_data['edges'][(
                arc.getSourceId(), arc.getDestinationId())] = arc.getMultiplicity()

        for i in graph_data['edges']:
            print(i[0])
            if isinstance(i[0], Transition):

                if i[0].label not in self.dict_final:
                    if not weights and not thresholds:

                        self.dict_final[i[0].label] = {
                            "typ": "t",
                            "suradnice": [],
                            "hodnoty": [{
                                "label": i[0].label,
                                "image": self.image_index,
                                "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                            }],
                            "sipky": {
                                i[1].label: graph_data['edges'][i]
                            }
                        }
                    if weights and not thresholds:
                        self.dict_final[i[0].label] = {
                            "typ": "t",
                            "suradnice": [],
                            "hodnoty": [{
                                "label": i[0].label,
                                "image": self.image_index,
                                "vaha": i[0].getWeight(),
                                "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                            }],
                            "sipky": {
                                i[1].label: graph_data['edges'][i]
                            }
                        }
                    if thresholds:
                        self.dict_final[i[0].label] = {
                            "typ": "t",
                            "suradnice": [],
                            "hodnoty": [{
                                "label": i[0].label,
                                "image": self.image_index,
                                "vaha": i[0].getWeight(),
                                "prah": i[0].getTreshold(),
                                "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                            }],
                            "sipky": {
                                i[1].label: graph_data['edges'][i]
                            }
                        }
                else:
                    if not weights and not thresholds:
                        if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i[0].label]["hodnoty"]):
                            self.dict_final[i[0].label]["hodnoty"].append({
                                "label": i[0].label,
                                "image": self.image_index,
                                "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False

                            })
                        if not self.dict_final[i[0].label]["sipky"].get(i[1].label):
                            self.dict_final[i[0].label]["sipky"][i[1]
                                                                 .label] = graph_data['edges'][i]

                    if weights and not thresholds:
                        if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i[0].label]["hodnoty"]):
                            self.dict_final[i[0].label]["hodnoty"].append({
                                "label": i[0].label,
                                "image": self.image_index,
                                "vaha": i[0].getWeight(),
                                "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                            })
                        if not self.dict_final[i[0].label]["sipky"].get(i[1].label):
                            self.dict_final[i[0].label]["sipky"][i[1]
                                                                 .label] = graph_data['edges'][i]

                    if thresholds:
                        if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i[0].label]["hodnoty"]):
                            self.dict_final[i[0].label]["hodnoty"].append({
                                "label": i[0].label,
                                "image": self.image_index,
                                "vaha": i[0].getWeight(),
                                "prah": i[0].getTreshold(),
                                "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                            })
                        if not self.dict_final[i[0].label]["sipky"].get(i[1].label):
                            self.dict_final[i[0].label]["sipky"][i[1]
                                                                 .label] = graph_data['edges'][i]

            if isinstance(i[0], Place):
                if i[0].label not in self.dict_final:
                    self.dict_final[i[0].label] = {
                        "typ": "p",
                        "suradnice": [],
                        "hodnoty": [{
                            "label": i[0].label,
                            "image": self.image_index,
                            "tokeny": i[0].tokens if self.fuzzy_flag or thresholds or weights else int(i[0].tokens)
                        }],
                        "sipky": {
                            i[1].label: graph_data['edges'][i]
                        }
                    }
                else:
                    if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i[0].label]["hodnoty"]):
                        self.dict_final[i[0].label]["hodnoty"].append({
                            "label": i[0].label,
                            "image": self.image_index,
                            "tokeny": i[0].tokens if self.fuzzy_flag or thresholds or weights else int(i[0].tokens)
                        })
                    if not self.dict_final[i[0].label]["sipky"].get(i[1].label):
                        self.dict_final[i[0].label]["sipky"][i[1]
                                                             .label] = graph_data['edges'][i]

        if self.image_index == 1:
            self.missing_places = []
            self.missing_transitions = []
            for i in graph_data['places']:
                if not self.dict_final.get(i.label):
                    self.missing_places.append(i)

            for i in graph_data['transitions']:
                if not self.dict_final.get(i.label):
                    self.missing_transitions.append(i)

        for i in self.missing_places:
            if not self.dict_final.get(i.label):
                self.dict_final[i.label] = {
                    "typ": "p",
                    "suradnice": [],
                    "hodnoty": [{
                        "label": i.label,
                        "image": self.image_index,
                        "tokeny": i.tokens if self.fuzzy_flag or thresholds or weights else int(i.tokens)
                    }],
                    "sipky": {}
                }
            else:
                if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i.label]["hodnoty"]):
                    self.dict_final[i.label]["hodnoty"].append({
                        "label": i.label,
                        "image": self.image_index,
                        "tokeny": i.tokens if self.fuzzy_flag or thresholds or weights else int(i.tokens)
                    })

        for i in self.missing_transitions:
            if not self.dict_final.get(i.label):
                if not weights and not thresholds:

                    self.dict_final[i.label] = {
                        "typ": "t",
                        "suradnice": [],
                        "hodnoty": [{
                            "label": i.label,
                            "image": self.image_index,
                            "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                        }]

                    }

                if weights and not thresholds:
                    self.dict_final[i.label] = {
                        "typ": "t",
                        "suradnice": [],
                        "hodnoty": [{
                            "label": i.label,
                            "image": self.image_index,
                            "vaha": i.getWeight(),
                            "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                        }]
                    }
                if thresholds:
                    self.dict_final[i.label] = {
                        "typ": "t",
                        "suradnice": [],
                        "hodnoty": [{
                            "label": i.label,
                            "image": self.image_index,
                            "vaha": i.getWeight(),
                            "prah": i.getTreshold(),
                            "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                        }]
                    }
            else:
                if not weights and not thresholds:
                    if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i.label]["hodnoty"]):
                        self.dict_final[i.label]["hodnoty"].append({
                            "label": i.label,
                            "image": self.image_index,
                            "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                        })

                if weights and not thresholds:
                    if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i.label]["hodnoty"]):
                        self.dict_final[i.label]["hodnoty"].append({
                            "label": i.label,
                            "image": self.image_index,
                            "vaha": i.getWeight(),
                            "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                        })

                if thresholds:
                    if not True in map(lambda value: True if value['image'] == self.image_index else False, self.dict_final[i.label]["hodnoty"]):
                        self.dict_final[i.label]["hodnoty"].append({
                            "label": i.label,
                            "image": self.image_index,
                            "vaha": i.getWeight(),
                            "prah": i.getTreshold(),
                            "farba": True if i[0].label in self.transitions_to_change[self.image_index] else False
                        })

        if self.image_index == 1:
            dict_keys = list(self.dict_final)
            x = 600
            y = 400
            rad = 300
            amount = len(self.dict_final)
            angle = 360/amount
            for i in range(1, amount+1):
                x1 = rad * cos(angle*i * pi/180)
                y1 = rad * sin(angle*i * pi/180)
                self.dict_final[dict_keys[i-1]]["suradnice"] = {
                    "main_coords": (round(x + x1), round(y + y1))}
        path = './images/' + str(self.image_number) + '.png'
        self.image_dict[self.image_number] = path
        print("path: ", path)
        self.generate_image()

        self.main_layout.nextButton.setEnabled(True)
        self.main_layout.nextButton.setStyleSheet("""
                QPushButton:enabled {
                    color: rgba(255,0,0,0.5);
                }
                QPushButton:enabled:!checked {
                    background-color: green;
                }
        """)
        self.main_layout.prevButton.setStyleSheet("""
                QPushButton:enabled {
                    color: rgba(255,0,0,0.5);
                }
                QPushButton:enabled:!checked {
                    background-color: green;
                }
        """)
        self.image_index += 1

    def generate_image(self):
        img = np.zeros((800, 1200, 3), np.uint8)
        img.fill(255)

        for i in self.dict_final:
            x1 = self.dict_final[i]["suradnice"]["main_coords"][0]
            y1 = self.dict_final[i]["suradnice"]["main_coords"][1]
            if x1 > 600:
                pos = "right"
            else:
                pos = "left"

            if self.dict_final[i]["typ"] == 'p':
                text = str(self.dict_final[i]['hodnoty']
                           [self.image_index-1]['tokeny'])
                text_size, _ = cv2.getTextSize(
                    text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                text_origin = (
                    int(x1 - text_size[0] / 2), int(y1 + text_size[1] / 2))
                cv2.putText(img, text, text_origin,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                cv2.circle(img, (x1, y1), 30, (0, 0, 0), 2)

                text_size, _ = cv2.getTextSize(
                    str(self.dict_final[i]['hodnoty'][0]['label']), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                if pos == "right":
                    text_pos = (x1 + 40, y1)
                elif pos == "left":
                    text_pos = (x1 - 40 - text_size[0], y1)
                elif pos == "bottom":
                    text_pos = (x1 - text_size[0] //
                                2, y1 + 50 + text_size[1] // 2)
                else:
                    text_pos = (x1 - text_size[0] //
                                2, y1 - 50 - text_size[1] // 2)
                cv2.putText(img, str(self.dict_final[i]['hodnoty'][0]['label']), text_pos,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                if self.dict_final[i]['sipky']:
                    for j in self.dict_final[i]['sipky']:
                        x2 = self.dict_final[j]["suradnice"]["main_coords"][0]
                        y2 = self.dict_final[j]["suradnice"]["main_coords"][1]
                        radius1 = 32
                        radius2 = 34
                        fixed_arrow_length = 5
                        arrow_tip_size = 5
                        angle = atan2(y2 - y1, x2 - x1)
                        point1_x = x1 + radius1 * cos(angle)
                        point1_y = y1 + radius1 * sin(angle)
                        point2_x = x2 - radius2 * cos(angle)
                        point2_y = y2 - radius2 * sin(angle)
                        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
                        mid_point = (int((point1_x + point2_x) / 2),
                                     int((point1_y + point2_y) / 2))
                        normalized_line_length = distance / fixed_arrow_length
                        normalized_arrow_tip_size = arrow_tip_size / normalized_line_length
                        cv2.arrowedLine(img, (int(point1_x), int(point1_y)),
                                        (int(point2_x), int(point2_y)),
                                        (0, 0, 0), 2, tipLength=normalized_arrow_tip_size)
                        text = str(self.dict_final[i]['sipky'][j])
                        text_size, _ = cv2.getTextSize(
                            text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        text_pos = (
                            mid_point[0] - text_size[0] // 2, mid_point[1] + text_size[1] // 2 - 3)
                        cv2.rectangle(img, (text_pos[0]-2, text_pos[1]+2), (text_pos[0] +
                                      text_size[0], text_pos[1] - text_size[1]), (255, 255, 255), -1)
                        cv2.putText(
                            img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
            else:
                color = (
                    0, 255, 0) if self.dict_final[i]["hodnoty"][self.image_index - 1]["farba"] else (0, 0, 255)
                cv2.rectangle(img, (x1 - 30, y1 - 30),
                              (x1 + 30, y1 + 30), color, 2)

                text_size, _ = cv2.getTextSize(
                    str(self.dict_final[i]['hodnoty'][0]['label']), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                if pos == "right":
                    text_pos = (x1 + 40, y1)
                elif pos == "left":
                    text_pos = (x1 - 40 - text_size[0], y1)
                elif pos == "bottom":
                    text_pos = (x1 - text_size[0] //
                                2, y1 + 50 + text_size[1] // 2)
                else:
                    text_pos = (x1 - text_size[0] //
                                2, y1 - 50 - text_size[1] // 2)
                
                threshold_text = self.dict_final[i]["hodnoty"][self.image_index - 1]["prah"] if self.dict_final[i]["hodnoty"][self.image_index - 1].get("prah") else None
                weights_text = self.dict_final[i]["hodnoty"][self.image_index - 1]["vaha"] if self.dict_final[i]["hodnoty"][self.image_index - 1].get("vaha") else None
                if threshold_text:
                    cv2.putText(img, f"T: {str(threshold_text)}", (x1-20, y1-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                if weights_text:
                    cv2.putText(img, f"W: {str(weights_text)}", (x1-20, y1+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

                cv2.putText(img, str(self.dict_final[i]['hodnoty'][0]['label']), text_pos,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                if self.dict_final[i]['sipky']:
                    for j in self.dict_final[i]['sipky']:
                        x2 = self.dict_final[j]["suradnice"]["main_coords"][0]
                        y2 = self.dict_final[j]["suradnice"]["main_coords"][1]
                        radius1 = 34
                        radius2 = 32
                        fixed_arrow_length = 5
                        arrow_tip_size = 5
                        angle = atan2(y2 - y1, x2 - x1)
                        point1_x = x1 + radius1 * cos(angle)
                        point1_y = y1 + radius1 * sin(angle)
                        point2_x = x2 - radius2 * cos(angle)
                        point2_y = y2 - radius2 * sin(angle)
                        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
                        mid_point = (int((point1_x + point2_x) / 2),
                                     int((point1_y + point2_y) / 2))
                        normalized_line_length = distance / fixed_arrow_length
                        normalized_arrow_tip_size = arrow_tip_size / normalized_line_length
                        cv2.arrowedLine(img, (int(point1_x), int(point1_y)),
                                        (int(point2_x), int(point2_y)),
                                        (0, 0, 0), 2, tipLength=normalized_arrow_tip_size)
                        text = str(self.dict_final[i]['sipky'][j])
                        text_size, _ = cv2.getTextSize(
                            text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        text_pos = (
                            mid_point[0] - text_size[0] // 2, mid_point[1] + text_size[1] // 2 - 3)
                        cv2.rectangle(img, (text_pos[0]-2, text_pos[1]+2), (text_pos[0] +
                                      text_size[0], text_pos[1] - text_size[1]), (255, 255, 255), -1)
                        cv2.putText(
                            img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

        cv2.imwrite(f"./images/{self.image_index}.png", img)

    def fill_matrixes(self, inputMatrix, outputMatrix):
        # fill each matrix with the proper data
        for arc in self.net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (self.net.getPlaceById(sourceId) is not None) and (self.net.getTransitionById(destinationId) is not None):
                source = self.net.getPlaceById(sourceId)
                destination = self.net.getTransitionById(destinationId)
            elif (self.net.getTransitionById(sourceId) is not None) and (self.net.getPlaceById(destinationId) is not None):
                source = self.net.getTransitionById(sourceId)
                destination = self.net.getPlaceById(destinationId)
            if type(source) == Place:
                sourceIdInNetList = self.net.getPlaces().index(source)
                destinationIdInNetList = self.net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()
            if type(source) == Transition:
                sourceIdInNetList = self.net.getTransitions().index(source)
                destinationIdInNetList = self.net.getPlaces().index(destination)
                outputMatrix[destinationIdInNetList,
                             sourceIdInNetList] = arc.getMultiplicity()
        return inputMatrix, outputMatrix

    def settting_image(self):
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(
        ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)

    def fill_dict_pre_logical_net(self, M):
        self.transitions_to_change = {}
        Wo = M[0].state
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        inputMatrix, outputMatrix = self.fill_matrixes(
            inputMatrix, outputMatrix)

        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [abs(1 - i) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(float(max(sub_result)))
                sub_result = []

            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            Uo = [abs(1 - i) for i in Vo]
            Wk = [int((outputMatrix @ Uo)[i] or Wo[i]) for i in range(len(Wo))]

            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            count_place = 0
            for place in self.net.getPlaces():
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        if self.image_number not in self.transitions_to_change:
                            self.transitions_to_change[self.image_number] = [
                                arc.src.label]
                        else:
                            self.transitions_to_change[self.image_number].append(
                                arc.src.label)
            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        print("transitions_to_change: ", self.transitions_to_change)

    def logical_petri_net(self, M):
        array_steps = []
        Wo = M[0].state
        self.main_layout.marking.setText(
            "( "+', '.join([str(int(elem)) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(int(elem))
                                                      for i, elem in enumerate(Wo)])+" )"

        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])

        inputMatrix, outputMatrix = self.fill_matrixes(
            inputMatrix, outputMatrix)
        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [abs(1 - i) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(float(max(sub_result)))
                sub_result = []

            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            Uo = [abs(1 - i) for i in Vo]
            Wk = [int((outputMatrix @ Uo)[i] or Wo[i]) for i in range(len(Wo))]

            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            previous_place = None
            count_place = 0
            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = self.net.getPlaceById(
                            arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)

            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem)
                                                      for i, elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number -
                                         1] = actual_step_marking
                self.draw_net(0, 0)
                self.image_number += 1
                print("Wk: ", Wk)
                self.net.Wk_final = Wk
            self.net.Wk_final = Wo

        self.settting_image()

    def fill_dict_pre_fuzzy_net(self, M):
        self.transitions_to_change = {}
        Wo = M[0].state
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        inputMatrix, outputMatrix = self.fill_matrixes(
            inputMatrix, outputMatrix)
        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [round(abs(1 - i), 2) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(float(max(sub_result)))
                sub_result = []

            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            Uo = [round(abs(1 - i), 2) for i in Vo]

            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(float(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                if Wo[i] > almost_result[i]:
                    Wk.append(Wo[i])
                else:
                    Wk.append(almost_result[i])

            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            count_place = 0
            for place in self.net.getPlaces():
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        if self.image_number not in self.transitions_to_change:
                            self.transitions_to_change[self.image_number] = [
                                arc.src.label]
                        else:
                            self.transitions_to_change[self.image_number].append(
                                arc.src.label)
            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        print("transitions_to_change: ", self.transitions_to_change)

    def fuzzy_petri_net(self, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.main_layout.marking.setText(
            "( "+', '.join([str(elem) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem)
                                                      for i, elem in enumerate(Wo)])+" )"
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        inputMatrix, outputMatrix = self.fill_matrixes(
            inputMatrix, outputMatrix)
        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [round(abs(1 - i), 2) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(float(max(sub_result)))
                sub_result = []

            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            Uo = [round(abs(1 - i), 2) for i in Vo]

            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(float(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                if Wo[i] > almost_result[i]:
                    Wk.append(Wo[i])
                else:
                    Wk.append(almost_result[i])

            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            previous_place = None
            count_place = 0

            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = self.net.getPlaceById(
                            arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)

            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem)
                                                      for i, elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number -
                                         1] = actual_step_marking
                self.draw_net(0, 0)
                self.image_number += 1
                print("Wk: ", Wk)
                self.net.Wk_final = Wk
            self.net.Wk_final = Wo
        self.settting_image()

    def fill_dict_pre_fuzzy_with_weights(self, M):
        self.transitions_to_change = {}
        Wo = M[0].state
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])

        # fill each matrix with the proper data
        for arc in self.net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (self.net.getPlaceById(sourceId) is not None) and (self.net.getTransitionById(destinationId) is not None):
                source = self.net.getPlaceById(sourceId)
                destination = self.net.getTransitionById(destinationId)
            elif (self.net.getTransitionById(sourceId) is not None) and (self.net.getPlaceById(destinationId) is not None):
                source = self.net.getTransitionById(sourceId)
                destination = self.net.getPlaceById(destinationId)
            if type(source) == Place:
                sourceIdInNetList = self.net.getPlaces().index(source)
                destinationIdInNetList = self.net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()
            if type(source) == Transition:
                sourceIdInNetList = self.net.getTransitions().index(source)
                destinationIdInNetList = self.net.getPlaces().index(destination)
                outputMatrix[destinationIdInNetList,
                             sourceIdInNetList] = self.net.getWeights()[sourceIdInNetList]

        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [round(abs(1 - i), 2) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(max(sub_result))
                sub_result = []
            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            Uo = [round(abs(1 - i), 2) for i in Vo]
            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(float(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                if Wo[i] > almost_result[i]:
                    Wk.append(Wo[i])
                else:
                    Wk.append(almost_result[i])
            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            count_place = 0
            for place in self.net.getPlaces():
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        if self.image_number not in self.transitions_to_change:
                            self.transitions_to_change[self.image_number] = [
                                arc.src.label]
                        else:
                            self.transitions_to_change[self.image_number].append(
                                arc.src.label)
            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        print("transitions_to_change: ", self.transitions_to_change)

    def fuzzy_petri_net_with_weights(self, M):
        array_steps = []
        Wo = M[0].state
        self.main_layout.marking.setText(
            "( "+', '.join([str(elem) for _, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem)
                                                      for _, elem in enumerate(Wo)])+" )"

        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])

        # fill each matrix with the proper data
        for arc in self.net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (self.net.getPlaceById(sourceId) is not None) and (self.net.getTransitionById(destinationId) is not None):
                source = self.net.getPlaceById(sourceId)
                destination = self.net.getTransitionById(destinationId)
            elif (self.net.getTransitionById(sourceId) is not None) and (self.net.getPlaceById(destinationId) is not None):
                source = self.net.getTransitionById(sourceId)
                destination = self.net.getPlaceById(destinationId)
            if type(source) == Place:
                sourceIdInNetList = self.net.getPlaces().index(source)
                destinationIdInNetList = self.net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()
            if type(source) == Transition:
                sourceIdInNetList = self.net.getTransitions().index(source)
                destinationIdInNetList = self.net.getPlaces().index(destination)
                outputMatrix[destinationIdInNetList,
                             sourceIdInNetList] = self.net.getWeights()[sourceIdInNetList]

        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [round(abs(1 - i), 2) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(max(sub_result))
                sub_result = []
            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            Uo = [round(abs(1 - i), 2) for i in Vo]
            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(float(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                if Wo[i] > almost_result[i]:
                    Wk.append(Wo[i])
                else:
                    Wk.append(almost_result[i])
            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            previous_place = None
            count_place = 0

            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = self.net.getPlaceById(
                            arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem)
                                                      for _, elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number -
                                         1] = actual_step_marking
                self.draw_net(1, 0)
                self.image_number += 1
                print("Wk: ", Wk)
                self.net.Wk_final = Wk
            self.net.Wk_final = Wo
        self.settting_image()

    def fill_dict_pre_fuzzy_with_weights_and_thresholds(self, M):
        self.transitions_to_change = {}
        Wo = M[0].state
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        inputMatrix, outputMatrix = self.fill_matrixes(
            inputMatrix, outputMatrix)
        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [round(abs(1 - i), 2) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(max(sub_result))
                sub_result = []
            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            # reacts to TR
            Uo = []
            negVo = [round(abs(1 - i), 2) for i in Vo]
            for i in range(len(negVo)):
                if negVo[i] >= self.net.tresholds[i]:
                    Uo.append(negVo[i])
                else:
                    Uo.append(0.0)
            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(float(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                if Wo[i] > almost_result[i]:
                    Wk.append(Wo[i])
                else:
                    Wk.append(almost_result[i])
            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            count_place = 0
            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        if self.image_number not in self.transitions_to_change:
                            self.transitions_to_change[self.image_number] = [
                                arc.src.label]
                        else:
                            self.transitions_to_change[self.image_number].append(
                                arc.src.label)
            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        print("transitions_to_change: ", self.transitions_to_change)

    def fuzzy_petri_net_with_weights_thresholds(self, M):
        array_steps = []
        Wo = M[0].state
        print("Wo: ", Wo)
        self.main_layout.marking.setText(
            "( "+', '.join([str(elem) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem)
                                                      for i, elem in enumerate(Wo)])+" )"
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        outputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        inputMatrix, outputMatrix = self.fill_matrixes(
            inputMatrix, outputMatrix)
        Wk = []
        i = 0
        while not np.array_equal(Wo, Wk):
            if i == 0:
                Wo = Wo
            else:
                Wo = Wk
            i += 1
            neg_Wo = [round(abs(1 - i), 2) for i in Wo]
            transponse_array = np.transpose(inputMatrix)
            Vo = []
            sub_result = []
            for i in transponse_array:
                for index, k in enumerate(i):
                    sub_result.append(min(k, neg_Wo[index]))
                Vo.append(max(sub_result))
                sub_result = []
            for i in range(len(Vo)):
                if Vo[i] > 1:
                    Vo[i] = 1.0
            # reacts to TR
            Uo = []
            negVo = [round(abs(1 - i), 2) for i in Vo]
            for i in range(len(negVo)):
                if negVo[i] >= self.net.tresholds[i]:
                    Uo.append(negVo[i])
                else:
                    Uo.append(0.0)
            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(float(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                if Wo[i] > almost_result[i]:
                    Wk.append(Wo[i])
                else:
                    Wk.append(almost_result[i])
            changed_places = []
            for num in range(len(Wo)):
                if Wk[num] != Wo[num]:
                    changed_places.append(True)
                else:
                    changed_places.append(False)
            previous_place = None
            count_place = 0
            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
                count_place += 1
                for arc in self.net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = self.net.getPlaceById(
                            arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            print("transitions_to_change: ", self.transitions_to_change)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem)
                                                      for i, elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number -
                                         1] = actual_step_marking
                self.draw_net(1, 1)
                self.image_number += 1
                print("Wk: ", Wk)
                self.net.Wk_final = Wk
            self.net.Wk_final = Wo
        self.settting_image()

    def error_message_box(self):
        dialog = QMessageBox(text="Siet je neohranicena")
        dialog.setWindowTitle("Message Dialog")
        dialog.setWindowIcon(QtGui.QIcon(
            'C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
        dialog.exec()   # Stores the return value for the button pressed

    def run_logical(self):
        self.net.M0 = [int(i) for i in self.net.M0]
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.dict_final = {}
            self.image_number = 1
            self.fill_dict_pre_logical_net(M)
            self.image_number = 1
            self.image_index = 1
            self.draw_net(0, 0)
            self.image_number += 1
            self.logical_petri_net(M)
            dir_path = os.path.dirname(self.file_path)
            l = 0
            for rank in self.root.iter('place'):
                for value in rank:
                    if value.tag == 'tokens':
                        value.text = str(int(self.net.Wk_final[l]))
                        l += 1
            self.tree.write(os.path.join(dir_path, self.file_name.split(
                '.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            self.error_message_box()

    def run_fuzzy(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.dict_final = {}
            self.image_number = 1
            self.fill_dict_pre_fuzzy_net(M)
            self.image_number = 1
            self.image_index = 1
            self.draw_net(0, 0)
            self.image_number += 1
            self.fuzzy_petri_net(M)
            dir_path = os.path.dirname(self.file_path)
            l = 0
            for rank in self.root.iter('place'):
                for value in rank:
                    if value.tag == 'tokens':
                        value.text = str(float(self.net.Wk_final[l]))
                        l += 1
            self.tree.write(os.path.join(dir_path, self.file_name.split(
                '.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            self.error_message_box()

    def run_fuzzy_with_weights(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.dict_final = {}
            self.image_number = 1
            self.fill_dict_pre_fuzzy_with_weights(M)
            self.image_number = 1
            self.image_index = 1
            self.draw_net(0, 0)
            self.image_number += 1
            self.fuzzy_petri_net_with_weights(M)
            dir_path = os.path.dirname(self.file_path)
            l = 0
            for rank in self.root.iter('place'):
                for value in rank:
                    if value.tag == 'tokens':
                        value.text = str(float(self.net.Wk_final[l]))
                        l += 1
            self.tree.write(os.path.join(dir_path, self.file_name.split(
                '.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            self.error_message_box()

    def run_fuzzy_with_weights_and_thresholds(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.dict_final = {}
            self.image_number = 1
            self.fill_dict_pre_fuzzy_with_weights_and_thresholds(M)
            self.image_number = 1
            self.image_index = 1
            self.draw_net(0, 0)
            self.image_number += 1
            self.fuzzy_petri_net_with_weights_thresholds(M)
            dir_path = os.path.dirname(self.file_path)
            l = 0
            for rank in self.root.iter('place'):
                for value in rank:
                    if value.tag == 'tokens':
                        value.text = str(float(self.net.Wk_final[l]))
                        l += 1
            self.tree.write(os.path.join(dir_path, self.file_name.split(
                '.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            self.error_message_box()


class DialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.ui = QFile(".\\gui\\patientWindow.ui")
        self.ui.open(QFile.ReadOnly)
        self.main_layout = self.loader.load(self.ui)
        self.ui.close()
        self.main_layout.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_layout.setStyleSheet(
            "QDialog::titleBar { background-color: black; }")
        self.main_layout.setWindowIcon(QtGui.QIcon(
            'C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
        self.main_layout.setWindowTitle("Výber pacienta")
        self.main_layout.show()
        self.database_output_table1 = []
        self.database_output_table2 = []
        self.main_layout.enroll.clicked.connect(self.open_main_application)
        self.main_layout.interrupt.clicked.connect(self.main_layout.close)
        self.patient_records = None
        self.patient_problems = None
        self.hashed = None
        self.main_layout.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def open_main_application(self):
        password = self.main_layout.password.text().encode('utf-8')
        hashed_with_salt = self.hashed[0][1]
        hashed_str, salt_str = hashed_with_salt.split("+++")
        salt = salt_str.encode('utf-8')
        hashed = bcrypt.hashpw(password, salt)
        if hashed_str.encode('utf-8') == hashed:
            self.main_layout.close()
            self.main_application = MainAplication()
            self.main_application.database_output_table1 = self.patient_records
            self.main_application.main_layout.table.setColumnCount(7)
            self.main_application.main_layout.table.setHorizontalHeaderLabels(
                ["Meno", "Priezvisko", "Vek", "Pohlavie", "Výška", "Váha", "Choroba"])
            header = self.main_application.main_layout.table.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            header.setStyleSheet("color: black;")
            self.main_application.main_layout.table.setRowCount(1)
            item_0 = QtWidgets.QTableWidgetItem(self.patient_records[1])
            item_0.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 0, item_0)

            item_1 = QtWidgets.QTableWidgetItem(self.patient_records[2])
            item_1.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 1, item_1)

            item_2 = QtWidgets.QTableWidgetItem(str(self.patient_records[3]))
            item_2.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 2, item_2)

            item_3 = QtWidgets.QTableWidgetItem(self.patient_records[4])
            item_3.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 3, item_3)

            item_4 = QtWidgets.QTableWidgetItem(str(self.patient_records[5]))
            item_4.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 4, item_4)

            item_5 = QtWidgets.QTableWidgetItem(str(self.patient_records[6]))
            item_5.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 5, item_5)

            item_6 = QtWidgets.QTableWidgetItem(self.patient_records[7])
            item_6.setForeground(QtGui.QColor("white"))
            self.main_application.main_layout.table.setItem(0, 6, item_6)

            self.main_application.database_output_table2 = self.patient_problems
            self.main_application.show()
        else:
            self.main_layout.check.setText("Zadali ste nesprávne heslo")
            self.main_layout.check.setStyleSheet("color: red")
            self.main_layout.password.clear()
            return

    def combo_changed(self, index):
        if index >= 0:
            patient_name = self.main_layout.patientPicker.itemText(index)
        else:
            # No item selected, use the first item
            patient_name = self.main_layout.patientPicker.itemText(0)
        selected_records = [
            i for i in self.database_output_table1 if i[1] + " " + i[2] == patient_name]
        if selected_records:
            self.patient_records = selected_records[0]
            self.patient_problems = next(
                (j for j in self.database_output_table2 if j[0] == self.patient_records[0]), None)
        else:
            self.patient_records = None
            self.patient_problems = None
            print("No records found for selected patient.")

    def parsing_database(self):
        for i in self.database_output_table1:
            self.main_layout.patientPicker.addItem(i[1] + " " + i[2])
        if self.main_layout.patientPicker.count() > 0:
            self.combo_changed(0)
        self.main_layout.patientPicker.currentIndexChanged.connect(
            self.combo_changed)


if __name__ == '__main__':
    result, result1, result2 = connect()
    app = QApplication(sys.argv)
    window = MainAplication()
    window.show()

    dialog = DialogWindow()
    dialog.database_output_table1 = result
    dialog.database_output_table2 = result1
    dialog.hashed = result2
    dialog.parsing_database()

    sys.exit(app.exec())
