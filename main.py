import Fuzzyfication
from PIL import Image, ImageDraw, ImageFont
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
import matplotlib
matplotlib.use('tkagg')

# global variables to store data from database
dict_values_patient = {}
dict_values_problem = {}


# This function obtains data from xml file and creates Petri net
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


# This function checks if Petri net is bounded
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

# This class represents main window of application


class MainApplication(QMainWindow):

    loader = QUiLoader()
    file_path = None
    file_name = None
    anotherWindow = None

    def __init__(self):
        super().__init__()
        self.main_layout = QWidget()
        self.ui = QFile("..\\PIS-bonus\\gui\\responsive.ui")
        self.ui.open(QFile.ReadOnly)
        self.main_layout = self.loader.load(self.ui)
        self.ui.close()
        self.setCentralWidget(self.main_layout)
        self.setWindowIcon(QtGui.QIcon('..\\PIS-bonus\\gui\\icon.jpg'))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            "QMainWindow::titleBar { background-color: black; }")
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Liecba pacienta")
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
        self.ui = QFile("..\\PIS-bonus\\gui\\anotherWindowFinal.ui")
        self.net = None
        self.root = None
        self.tresholds_flag = 0  # these flags tell us which type of Petri net we are using
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
        self.logical_validator = QtCore.QRegularExpression(
            "^(0|1)$")  # validators for line edits
        self.fuzzy_validator = QtCore.QRegularExpression(
            "^(0(\.\d+)?|1)$")  # validators for line edits
        self.fuzzyficated_M0 = []
        if self.image_number == 1:
            self.main_layout.prevButton.setEnabled(False)
        if len(self.dict_final) == 0:
            self.main_layout.nextButton.setEnabled(False)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.dialog_window = None  # initialize dialog window as None
        self.main_layout.closeEvent = self.closeEvent
        self.records_dict = {}
        self.records_dict_prev = {}
        self.prev_fired = []  # list of fired transitions in previous step
        self.fuzzification = 0
        self.flag = 0

    def closeEvent(self, event):
        if self.dialog_window is not None and self.dialog_window.isVisible():
            self.dialog_window.close()

        self.dialog_window = DialogWindow()
        self.close()
        result, result1, result2 = connect(
            0, 0, dict_values_patient, dict_values_problem)
        self.dialog_window.database_output_table1 = result
        self.dialog_window.database_output_table2 = result1
        self.dialog_window.hashed = result2
        self.dialog_window.parsing_database()
        event.ignore()

    # This function opens another window with settings of weights and tresholds
    def openAnotherWindow(self):
        self.anotherWindow = None
        self.ui.open(QFile.ReadOnly)
        self.anotherWindow = self.loader.load(self.ui)
        self.anotherWindow.setWindowIcon(
            QtGui.QIcon('..\\PIS-bonus\\gui\\icon.jpg'))
        self.anotherWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.anotherWindow.setStyleSheet(
            "QMainWindow::titleBar { background-color: black; }")
        self.anotherWindow.setGeometry(200, 200, 800, 600)
        self.anotherWindow.setWindowTitle("Nastavenie váh a prahov pravidiel")
        self.anotherWindow.table.setStyleSheet("background-color: black;")

        self.anotherWindow.fuzzyficate_run.setEnabled(True)
        self.anotherWindow.fuzzyficate_run.clicked.connect(
            self.fuzzyficate)
        self.anotherWindow.show()
        self.ui.close()

    # This function display the current time
    def update_time(self):
        # Get the current system time
        current_time = QTime.currentTime()
        # Format the time as HH:mm:ss
        formatted_time = current_time.toString('HH:mm:ss')
        # Update the time label
        self.main_layout.time_actual.setText(formatted_time)

    # This function flexibly changes the size of the window
    def resizeEvent(self, event):
        # set it separately for initial image
        if os.path.exists('../PIS-bonus/images/0.png') or len(self.image_dict) > 0:
            image_path = '../PIS-bonus/images/0.png' if os.path.exists(
                '../PIS-bonus/images/0.png') else self.image_dict[self.image_number]
            prem = QImage(image_path)
            pixmap = QPixmap.fromImage(prem)
            self.main_layout.photo.setPixmap(pixmap.scaled(
                self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
        event.accept()

    # This function is called when we want to load a new file from system into the program
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

    # This function just shows which option is selected in the combo box
    def combo_changed(self):
        print(self.main_layout.comboBox.currentText())

    def run(self):
        self.prev_fired = []
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
        # always remove all images from folder before running another file
        files = glob.glob('../PIS-bonus/images/*')
        if files != None:
            for f in files:
                os.remove(f)
        if self.file_path:
            self.openAnotherWindow()
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            self.anotherWindow.table.setColumnCount(9)
            self.anotherWindow.table.setHorizontalHeaderLabels(
                ["Záznam", "Pacient ID", " Systolický KT", "Diastolický KT", "Hladina cukru", "Cholesterol", "Tep", "EKG", "Bolesť v hrudi"])
            header = self.anotherWindow.table.horizontalHeader()
            header.setStyleSheet("background-color: black; color: black;")
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            row = 0
            for record in self.database_output_table2:
                self.anotherWindow.table.insertRow(row)

                item_0 = QtWidgets.QTableWidgetItem(str(record[0]))
                item_0.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 0, item_0)

                item_1 = QtWidgets.QTableWidgetItem(str(record[1]))
                item_1.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 1, item_1)

                item_2 = QtWidgets.QTableWidgetItem(str(record[2]))
                item_2.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 2, item_2)

                item_3 = QtWidgets.QTableWidgetItem(str(record[3]))
                item_3.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 3, item_3)

                item_4 = QtWidgets.QTableWidgetItem(str(record[4]))
                item_4.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 4, item_4)

                item_5 = QtWidgets.QTableWidgetItem(str(record[5]))
                item_5.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 5, item_5)

                item_6 = QtWidgets.QTableWidgetItem(str(record[6]))
                item_6.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 6, item_6)

                item_7 = QtWidgets.QTableWidgetItem(str(record[7]))
                item_7.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 7, item_7)

                item_8 = QtWidgets.QTableWidgetItem(str(record[8]))
                item_8.setForeground(QtGui.QColor("white"))
                self.anotherWindow.table.setItem(row, 8, item_8)

                row += 1
            self.net = loading_data(
                self.file_name, self.fuzzy_flag, self.weights_flag, self.tresholds_flag, 0)
            self.dict_final = {}
            self.dict_weights = {}
            self.dict_tresholds = {}
            self.dict_marks = {}
            self.dict_places = {}
            self.dict_transitions = {}
            self.draw_net_initial()  # draw net
            self.setting_image(1)  # set image
            self.dict_weights = {}
            self.dict_tresholds = {}
            self.dict_marks = {}
            self.dict_places = {}
            self.dict_transitions = {}
            self.dict_final = {}
            # setting inital flags from selected type of net
            if self.main_layout.comboBox.currentText() == "Logická Petriho sieť":
                self.logical_flag = 1
                self.fuzzy_flag = 0
                self.weights_flag = 0
                self.tresholds_flag = 0
                self.set_marking_initial(self.logical_validator)
                self.anotherWindow.navod.setText(
                    "true/false alebo 1/0 -> SAVE")
                self.anotherWindow.navod.setStyleSheet("color: green;")
                self.anotherWindow.enter.clicked.connect(self.run_final)
                self.anotherWindow.fuzzyficate_run.setEnabled(False)
                self.anotherWindow.table.hide()
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť":
                self.fuzzy_flag = 1
                self.logical_flag = 0
                self.weights_flag = 0
                self.tresholds_flag = 0
                self.set_marking_initial(self.fuzzy_validator)
                self.anotherWindow.navod.setText(
                    "Fuzzy hodnoty (0-1) -> napisat do vstupov -> OK -> SAVE alebo Fuzzifikacia button (udaje z databazy) -> SAVE \n" "alebo Ciselne namerane hodnoty / textove ohodnotenie -> napisat do vstupov -> Fuzzifikacia button -> SAVE")
                self.anotherWindow.navod.setStyleSheet("color: green;")
                self.anotherWindow.enter.clicked.connect(self.run_final)
                self.anotherWindow.fuzzyficate_run.setEnabled(True)
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť s váhami pravidiel":
                self.weights_flag = 1
                self.tresholds_flag = 0
                self.fuzzy_flag = 1
                self.logical_flag = 0
                self.set_marking_initial(self.fuzzy_validator)
                self.anotherWindow.navod.setText(
                    "Fuzzy hodnoty (0-1) -> napisat do vstupov -> OK -> SAVE alebo Fuzzifikacia button (udaje z databazy) -> hodnoty (0-1) do vah prechodov -> SAVE \n" "alebo Ciselne namerane hodnoty / textove ohodnotenie -> napisat do vstupov -> Fuzzifikacia button -> hodnoty (0-1) do vah prechodov -> SAVE")
                self.anotherWindow.navod.setStyleSheet("color: green;")
                self.anotherWindow.enter.clicked.connect(self.run_final)
                self.anotherWindow.fuzzyficate_run.setEnabled(True)
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť s váhami a prahmi pravidiel":
                self.tresholds_flag = 1
                self.weights_flag = 1
                self.fuzzy_flag = 1
                self.logical_flag = 0
                self.anotherWindow.navod.setText(
                    "Fuzzy hodnoty (0-1) -> napisat do vstupov -> OK -> SAVE alebo Fuzzifikacia button (udaje z databazy) -> hodnoty (0-1) do vah, prahov prechodov -> SAVE\n" "alebo Ciselne namerane hodnoty / textove ohodnotenie -> napisat do vstupov -> Fuzzifikacia button -> hodnoty (0-1) do vah, prahov prechodov -> SAVE")
                self.anotherWindow.navod.setStyleSheet("color: green;")
                self.set_marking_initial(self.fuzzy_validator)
                self.anotherWindow.enter.clicked.connect(self.run_final)
                self.anotherWindow.fuzzyficate_run.setEnabled(True)
        else:
            self.tree = None
            dialog = QMessageBox(text="Nevybrali ste žiadny súbor")
            dialog.setWindowTitle("Message Dialog")
            dialog.setWindowIcon(QtGui.QIcon('..\\PIS-bonus\\gui\\icon.jpg'))
            dialog.exec()   # Stores the return value for the button pressed

    # add label treshold and weight to each transition in xml file
    def write_to_file_transitions(self):
        for i, rank in enumerate(self.root.iter('transition')):
            new_tag = ET.SubElement(rank, 'treshold')
            new_tag.text = str(self.net.tresholds[i])
            new_tag = ET.SubElement(rank, 'weight')
            new_tag.text = str(self.net.weights[i])
    # This function updates XML file with new markings and weights and tresholds if they are set

    def run_final(self):
        l = 0
        self.dict_final = {}
        self.k = 0
        self.main_layout.prevButton.setEnabled(False)
        self.main_layout.nextButton.setEnabled(True)
        if self.main_layout.steps != None:
            self.main_layout.steps.clear()
        self.anotherWindow.close()
        for rank in self.root.iter('place'):
            for value in rank:
                if value.tag == 'tokens':
                    if self.fuzzy_flag or self.tresholds_flag or self.weights_flag:
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
        # create XML file with initial marking set by user
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

    # This function is used when fuzzyfication button is clicked
    def fuzzyficate(self):
        self.fuzzification = 1
        counter = 0
        self.flag = 0
        self.records_dict = {"Vek": None,
                             "Pohlavie": None,
                             "Vyska": None,
                             "Vaha": None,
                             "Systolicky krvny tlak": None,
                             "Diastolicky krvny tlak": None,
                             "Hladina cukru": None,
                             "Cholesterol": None,
                             "Tep": None,
                             "EKG": None,
                             "Bolest v hrudi": None
                             }
        for place in self.net.getPlaces():
            if place.name in self.records_dict:
                self.flag = 1
        if (self.fuzzy_flag or self.weights_flag or self.tresholds_flag) and self.flag == 1:
            for _, value in self.dict_marks.items():
                if value.text() == '':
                    counter += 1
            if counter == len(self.dict_marks):

                self.records_dict = {"Vek": None,
                                     "Pohlavie": None,
                                     "Vyska": None,
                                     "Vaha": None,
                                     "Systolicky krvny tlak": None,
                                     "Diastolicky krvny tlak": None,
                                     "Hladina cukru": None,
                                     "Cholesterol": None,
                                     "Tep": None,
                                     "EKG": None,
                                     "Bolest v hrudi": None
                                     }

                if len(self.database_output_table1) == 0 or len(self.database_output_table2) == 0:
                    self.anotherWindow.fuzzification_result.setText(
                        "Chybajuce data! Zadaj")
                    self.anotherWindow.fuzzification_result.setAlignment(
                        QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    # set color to fuzzification_result to red
                    self.anotherWindow.fuzzification_result.setStyleSheet(
                        "color: red;")
                    return
                for i, record in enumerate(self.database_output_table1[3:]):
                    self.records_dict[list(self.records_dict.keys())[
                        i]] = record

                for i, record in enumerate(self.database_output_table2[0][2:]):
                    self.records_dict[list(self.records_dict.keys())[
                        i+4]] = record
            else:
                self.records_dict = {"Vek": None,
                                     "Pohlavie": None,
                                     "Vyska": None,
                                     "Vaha": None,
                                     "Systolicky krvny tlak": None,
                                     "Diastolicky krvny tlak": None,
                                     "Hladina cukru": None,
                                     "Cholesterol": None,
                                     "Tep": None,
                                     "EKG": None,
                                     "Bolest v hrudi": None
                                     }

                for i, record in enumerate(self.database_output_table1[3:]):
                    self.records_dict[list(self.records_dict.keys())[
                        i]] = record

                for i, record in enumerate(self.database_output_table2[0][2:]):
                    self.records_dict[list(self.records_dict.keys())[
                        i+4]] = record

                for key, value in self.dict_marks.items():
                    if value.text() != '':
                        self.records_dict[key.label] = value.text()
                        for i, record in enumerate(self.database_output_table1[3:]):
                            if self.records_dict[list(self.records_dict.keys())[i]] != record:
                                array = list(self.database_output_table1)
                                array[3+i] = value.text()
                                self.database_output_table1 = tuple(array)

                        for i, record in enumerate(self.database_output_table2[0][2:]):
                            if self.records_dict[list(self.records_dict.keys())[i+4]] != record:
                                array = list(self.database_output_table2[0])
                                array[2+i] = value.text()
                                self.database_output_table2[0] = tuple(array)
            dict_values_patient['id'] = self.database_output_table1[0]
            dict_values_patient['name'] = self.database_output_table1[1]
            dict_values_patient['surname'] = self.database_output_table1[2]
            dict_values_patient['age'] = self.database_output_table1[3]
            dict_values_patient['sex'] = self.database_output_table1[4]
            dict_values_patient['height'] = self.database_output_table1[5]
            dict_values_patient['weight'] = self.database_output_table1[6]

            dict_values_problem['id'] = self.database_output_table2[0][0]
            dict_values_problem['pacient_id'] = self.database_output_table2[0][1]
            dict_values_problem['systolic_blood_pressure'] = self.database_output_table2[0][2]
            dict_values_problem['diastolic_blood_pressure'] = self.database_output_table2[0][3]
            dict_values_problem['blood_sugar'] = self.database_output_table2[0][4]
            dict_values_problem['cholesterol'] = self.database_output_table2[0][5]
            dict_values_problem['heart_rate'] = self.database_output_table2[0][6]
            dict_values_problem['ekg'] = self.database_output_table2[0][7]
            dict_values_problem['chest_pain'] = self.database_output_table2[0][8]

            connect(0, 1, dict_values_patient,
                    dict_values_problem)
            # iterate through places labels in the net and update the values from records dict if the place label is the same as the key then leave the value from dict if not then set the value to None
            places = [place.label for place in self.net.getPlaces()]
            for key, record in self.records_dict.items():
                for i, place in enumerate(places):
                    if place == key:
                        self.records_dict[key] = record
                        break
                    else:
                        self.records_dict[key] = None

            self.records_dict_prev = self.records_dict
            Fuzzyfication.get_final_result_fuzzy(self.records_dict)

        if (self.fuzzy_flag or self.weights_flag or self.tresholds_flag) and self.flag == 0:
            self.records_dict = {"Uziva ivabradin": None,
                                 "Uziva vericiguat": None,
                                 "sTK": None,
                                 "GFR": None,
                                 "fibrilacia predsieni": None,
                                 "symptomaticka bradykardia": None,
                                 "vek": None,
                                 "SF": None,
                                 "LBBB": None,
                                 "QRS": None,
                                 "symptomaticka hypotenzia": None,
                                 "Uzivany gliflozin": None,
                                 "Max davka": None,
                                 "K+": None,
                                 "TEP": None,
                                 "CHOCHP": None,
                                 "AV blok": None,
                                 "Kreatinin": None,
                                 "Nebivolol": None,
                                 "Uziva digoxin": None,
                                 "Hodnota digoxinu": None,
                                 "Pomaly rytmus": None,
                                 "eGRF": None,
                                 "SBP": None,
                                 "HR": None,
                                 "Zvysenie NTproBNP": None,
                                 "NYHA-II-III": None,
                                 'BB': None,
                                 'ARNI': None,
                                 'ACEI': None,
                                 "MRA": None
                                 }

            for key, value in self.dict_marks.items():
                if value.text() != '':
                    self.records_dict[key.label] = value.text()
            # iterate through places labels in the net and update the values from records dict if the place label is the same as the key then leave the value from dict if not then set the value to None
            places = [place.label for place in self.net.getPlaces()]
            for key, record in self.records_dict.items():
                for i, place in enumerate(places):
                    if place == key:
                        self.records_dict[key] = record
                        break
                    else:
                        self.records_dict[key] = None

            # remove keys with values where value is None (create new dict)
            self.records_dict = {key: value for key,
                                 value in self.records_dict.items() if value is not None}
            self.records_dict_prev = self.records_dict.copy()
            Fuzzyfication.get_final_result_logical(self.records_dict, self.net)

        self.fuzzyficated_M0 = [0 for _ in range(len(self.dict_places))]
        # iterate through places labels in the net and update the values from records dict
        counter = 0
        places = [place.label for place in self.net.getPlaces()]
        for key, record in self.records_dict.items():
            for i, place in enumerate(places):
                if place == key:
                    counter += 1
                    self.fuzzyficated_M0[i] = record
                    for place in self.net.getPlaces():
                        place.tokens = self.fuzzyficated_M0[self.net.getPlaces().index(
                            place)]
        counter1 = 0
        for i in self.records_dict.values():
            if i is not None:
                counter1 += 1

        if counter == 0 or counter1 == 0:
            self.anotherWindow.fuzzification_result.setText(
                "Fuzzyfikacia zlyhala")
            self.anotherWindow.fuzzification_result.setAlignment(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            # set color to fuzzification_result to red
            self.anotherWindow.fuzzification_result.setStyleSheet(
                "color: red;")
        else:
            self.anotherWindow.fuzzification_result.setText(
                "Fuzzyfikacia uspesna")
            self.net.M0 = [place.tokens for place in self.net.getPlaces()]
            self.anotherWindow.fuzzification_result.setAlignment(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.anotherWindow.fuzzification_result.setStyleSheet(
                "color: green;")
            self.anotherWindow.placesWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_places):
                placeLabel = QtWidgets.QLabel(key.label)
                placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                placeLabelM0 = QtWidgets.QLabel(str(self.fuzzyficated_M0[i]))
                placeLabelM0.setFont(QtGui.QFont(
                    "Arial", 10, QtGui.QFont.Bold))
                placeLabel.setStyleSheet("color: green;")
                placeLabelM0.setStyleSheet("color: green;")
                edit = self.list_edit_widgets[i]
                edit.setText(str(self.fuzzyficated_M0[i]))
                edit.setEnabled(False)
                if i == len(self.list_edit_widgets)-1:
                    break

            self.anotherWindow.OK1.setEnabled(True)
            self.anotherWindow.fuzzyficate_run.setEnabled(False)
        # self.flag = 0

    # This fuction sets the initial marking of the net
    def set_marking_initial(self, validator):
        self.dict_marks = {}
        self.dict_weights = {}
        self.dict_tresholds = {}
        self.list_edit_widgets = []
        places_with_outgoing_arcs = set()
        for arc in self.net.getArcs():
            if isinstance(arc.src, Place):
                places_with_outgoing_arcs.add(arc.src)
        places_with_no_outgoing_arcs = []
        for place in self.net.getPlaces():
            if place not in places_with_outgoing_arcs:
                places_with_no_outgoing_arcs.append(place)
        for place in self.net.getPlaces():
            self.dict_places[place] = place.tokens
        for transition in self.net.getTransitions():
            self.dict_transitions[transition] = transition.label
        placesLayout = QtWidgets.QVBoxLayout()
        self.anotherWindow.placesWidget.setLayout(placesLayout)
        self.anotherWindow.placesWidget.setStyleSheet(
            "background-color: black;")
        for i, key in enumerate(self.dict_places):
            placeLabel = QtWidgets.QLabel(key.label)
            placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            placeLabel.setStyleSheet("color: green;")
            # when place has no outgoing arcs then it is not possible to set marking
            if key.label not in [place.label for place in places_with_no_outgoing_arcs]:
                entry = QtWidgets.QLineEdit()
                entry.setMaximumWidth(50)
                # entry.setValidator(QtGui.QRegularExpressionValidator(validator))
                entry.setStyleSheet("color: white;")
                self.list_edit_widgets.append(entry)
                # self.list_edit_widgets.append(placeLabel)
                self.dict_marks[key] = entry
                placeLayout = QtWidgets.QVBoxLayout()
                placeLayout.addWidget(placeLabel)
                placeLayout.addWidget(entry)
                placeLayout.addStretch()
                placesLayout.addLayout(placeLayout)
            else:
                entry = QtWidgets.QLineEdit()
                entry.setMaximumWidth(50)
                self.dict_marks[key] = entry
                placeLayout = QtWidgets.QVBoxLayout()
                placeLayout.addWidget(placeLabel)
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
            self.anotherWindow.OK2.setEnabled(False)
            self.anotherWindow.OK3.setEnabled(False)
            weightsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.weightsWidget.setLayout(weightsLayout)
            self.anotherWindow.weight.setText("Prechody")
            self.anotherWindow.weightsWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_transitions):
                transitionLabel0 = QtWidgets.QLabel(key.label)
                transitionLabel0.setFont(
                    QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                transitionLabel0.setStyleSheet("color: green;")
                weightLayout = QtWidgets.QVBoxLayout()
                weightLayout.addWidget(transitionLabel0)
                weightsLayout.addLayout(weightLayout)
            self.anotherWindow.weightsScrollArea.setWidget(
                self.anotherWindow.weightsWidget)
            self.anotherWindow.tresholdsWidget.setStyleSheet(
                "background-color: black;")
            self.anotherWindow.widget_2.hide()

        if self.weights_flag:
            self.anotherWindow.OK3.setDisabled(True)
            self.anotherWindow.OK2.show()
            self.anotherWindow.OK2.setEnabled(True)
            self.anotherWindow.weight.setText("Váhy prechodov")
            weightsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.weightsWidget = QtWidgets.QWidget()
            self.anotherWindow.weightsWidget.setLayout(weightsLayout)
            self.anotherWindow.weightsWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_transitions):
                weightLabel = QtWidgets.QLabel(key.label)
                weightLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                weightLabel.setStyleSheet("color: green;")
                entry2 = QtWidgets.QLineEdit()
                entry2.setMaximumWidth(50)
                entry2.setValidator(
                    QtGui.QRegularExpressionValidator(validator))
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
            self.anotherWindow.widget_2.show()
            self.anotherWindow.OK2.setDisabled(False)
            self.anotherWindow.OK3.setDisabled(False)
            tresholdsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.tresholdsWidget = QtWidgets.QWidget()
            self.anotherWindow.tresholdsWidget.setLayout(tresholdsLayout)
            self.anotherWindow.tresholdsWidget.setStyleSheet(
                "background-color: black;")
            for i, key in enumerate(self.dict_transitions):
                transitionLabel = QtWidgets.QLabel(key.label)
                transitionLabel.setFont(QtGui.QFont(
                    "Arial", 10, QtGui.QFont.Bold))
                transitionLabel.setStyleSheet("color: green;")
                entry3 = QtWidgets.QLineEdit()
                entry3.setMaximumWidth(50)
                entry3.setValidator(
                    QtGui.QRegularExpressionValidator(validator))
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

    # This function deletes all text from the entries
    def delete_text(self, entries):
        for _, value in entries.items():
            value.setText("")

    # This function sets the marking of the places, if the user has chosen logical marking else weights and tresholds are set for the transitions
    def set_values(self, entries, logical_flag, weights_flag, tresholds_flag):
        for item, value in entries.items():
            if value.text() == '':
                if logical_flag:
                    item.tokens = 0
                else:
                    item.tokens = 0.0
                if weights_flag:
                    item.weight = 0.0
                if tresholds_flag:
                    item.treshold = 0.0
            else:
                try:
                    if logical_flag:
                        if value.text() == "true":
                            num = 1
                        elif value.text() == "false":
                            num = 0
                        elif value.text() == "II" or value.text() == "III":
                            num = 1
                        elif value.text() != "true" or value.text() != "false" or value.text() != "II" or value.text() != "III":
                            num = int(value.text())
                        else:
                            return
                    else:
                        if value.text() == "true":
                            num = 1.0
                        elif value.text() == "false":
                            num = 0.0
                        elif value.text() == "II" or value.text() == "III":
                            num = 10.
                        elif value.text() != "true" or value.text() != "false" or value.text() != "II" or value.text() != "III":
                            num = float(value.text().replace(',', '.'))
                        else:
                            return

                    item.tokens = num
                    if weights_flag:
                        item.weight = num
                    if tresholds_flag:
                        item.treshold = num
                except ValueError:
                    QtWidgets.QMessageBox.warning(
                        self, "Invalid Input", "Please enter a valid number.")
                    return

    def set_marking(self, entries):
        self.set_values(entries, self.logical_flag,
                        self.weights_flag, self.tresholds_flag)
        self.net.M0 = [place.tokens for place in self.net.getPlaces()]

    def set_tresholds(self, entries):
        self.set_values(entries, self.logical_flag,
                        self.weights_flag, self.tresholds_flag)
        self.net.tresholds = [
            transition.treshold for transition in self.net.getTransitions()]
        self.TR = self.net.tresholds

    def set_weights(self, entries):
        self.set_values(entries, self.logical_flag,
                        self.weights_flag, self.tresholds_flag)
        self.net.weights = [
            transition.weight for transition in self.net.getTransitions()]
    # switching on photos in window

    def prev(self):
        if self.image_number > 1:
            #  set button active
            self.main_layout.nextButton.setEnabled(True)
            if self.image_number == 2:
                self.main_layout.prevButton.setEnabled(False)
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
            self.image_number = 1

    def next(self):
        if self.image_number < len(self.image_dict):
            # set button active
            self.main_layout.prevButton.setEnabled(True)
            if self.image_number == len(self.image_dict)-1:
                self.main_layout.nextButton.setEnabled(False)

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

    # clear all data
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

    # store all data during simulation to dictionary for further use to draw graph/net
    def draw_net_initial(self, weights=False, thresholds=False):
        graph_data = {
            'places': [],
            'transitions': [],
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
            if isinstance(i[0], Transition):
                if i[0].label not in self.dict_final:
                    if not weights and not thresholds:
                        self.dict_final[i[0].label] = {
                            "typ": "t",
                            "suradnice": [],
                            "hodnoty": [{
                                "label": i[0].label,
                            }],
                            "sipky": {
                                i[1].label: graph_data['edges'][i]
                            }
                        }
                else:
                    if not weights and not thresholds:
                        self.dict_final[i[0].label]["hodnoty"].append({
                            "label": i[0].label,
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
                        }],
                        "sipky": {
                            i[1].label: graph_data['edges'][i]
                        }
                    }
                else:
                    self.dict_final[i[0].label]["hodnoty"].append({
                        "label": i[0].label,
                    })
                    if not self.dict_final[i[0].label]["sipky"].get(i[1].label):
                        self.dict_final[i[0].label]["sipky"][i[1]
                                                             .label] = graph_data['edges'][i]
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
                    }],
                    "sipky": {}
                }
            else:
                self.dict_final[i.label]["hodnoty"].append({
                    "label": i.label,
                })

        for i in self.missing_transitions:
            if not self.dict_final.get(i.label):
                if not weights and not thresholds:
                    self.dict_final[i.label] = {
                        "typ": "t",
                        "suradnice": [],
                        "hodnoty": [{
                            "label": i.label,
                        }]
                    }
            else:
                if not weights and not thresholds:
                    self.dict_final[i.label]["hodnoty"].append({
                        "label": i.label,
                    })

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
        self.generate_image_initial()
        self.dict_final = {}
        self.missing_places = []
        self.missing_transitions = []

    # own function to draw net
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
        path = '../PIS-bonus/images/' + str(self.image_number) + '.png'
        self.image_dict[self.image_number] = path

        self.generate_image()

        self.main_layout.nextButton.setEnabled(True)
        self.image_index += 1

    # this function is used to generate image from the values in dictionary for initial state
    # I had to create image for label and then paste it on the main image because of the diacritics
    def generate_image_initial(self):
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
                cv2.circle(img, (x1, y1), 30, (0, 0, 0), 2)
                img_pil = Image.fromarray(img)
                draw = ImageDraw.Draw(img_pil)
                font = ImageFont.truetype("arial.ttf", 20)
                text = str(self.dict_final[i]['hodnoty'][0]['label'])
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_size = (text_bbox[2] - text_bbox[0],
                             text_bbox[3] - text_bbox[1])
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
                draw.text(text_pos, text, (0, 0, 0), font=font)
                img = np.array(img_pil)
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
                color = (0, 0, 255)
                cv2.rectangle(img, (x1 - 30, y1 - 30),
                              (x1 + 30, y1 + 30), color, 2)
                img_pil = Image.fromarray(img)
                draw = ImageDraw.Draw(img_pil)
                font = ImageFont.truetype("arial.ttf", 20)
                text = str(self.dict_final[i]['hodnoty'][0]['label'])
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_size = (text_bbox[2] - text_bbox[0],
                             text_bbox[3] - text_bbox[1])
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

                draw.text(text_pos, text, (0, 0, 0), font=font)
                img = np.array(img_pil)

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
        cv2.imwrite(f"../PIS-bonus/images/0.png", img)

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

                img_pil = Image.fromarray(img)
                draw = ImageDraw.Draw(img_pil)
                font = ImageFont.truetype("arial.ttf", 20)
                text = str(self.dict_final[i]['hodnoty'][0]['label'])
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_size = (
                    text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

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

                draw.text(text_pos, text, (0, 0, 0), font=font)
                img = np.array(img_pil)

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
                img_pil = Image.fromarray(img)
                draw = ImageDraw.Draw(img_pil)
                font = ImageFont.truetype("arial.ttf", 20)
                text = str(self.dict_final[i]['hodnoty'][0]['label'])
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_size = (
                    text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

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

                draw.text(text_pos, text, (0, 0, 0), font=font)
                img = np.array(img_pil)

                threshold_text = self.dict_final[i]["hodnoty"][self.image_index -
                                                               1]["prah"] if self.dict_final[i]["hodnoty"][self.image_index - 1].get("prah") else None
                weights_text = self.dict_final[i]["hodnoty"][self.image_index -
                                                             1]["vaha"] if self.dict_final[i]["hodnoty"][self.image_index - 1].get("vaha") else None
                if threshold_text:
                    cv2.putText(img, f"T:{str(threshold_text)}", (x1-25, y1-14),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
                if weights_text:
                    cv2.putText(img, f"W:{str(weights_text)}", (x1-25, y1+20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

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

        cv2.imwrite(f"../PIS-bonus/images/{self.image_index}.png", img)

    # This function is used to create the input and output matrixes of the net
    def fill_matrixes(self, inputMatrix, outputMatrix):
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
                if self.weights_flag or self.tresholds_flag:
                    outputMatrix[destinationIdInNetList,
                                 sourceIdInNetList] = self.net.getWeights()[sourceIdInNetList]
                else:
                    outputMatrix[destinationIdInNetList,
                                 sourceIdInNetList] = arc.getMultiplicity()
        return inputMatrix, outputMatrix

    # This function set the image of the net to the window
    def setting_image(self, first):
        if first:
            prem = QImage('../PIS-bonus/images/0.png')
        else:
            self.image_number = 1
            prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(
        ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)

    # This function is used to create the dictionary of the net
    def fill_dict_pre_logical_net(self, M):
        self.prev_fired = []
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

            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(int(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                Wk.append(int(max(Wo[i], almost_result[i])))
            places = self.net.getPlaces()
            for i, place in enumerate(places):
                place.tokens = Wo[i]

            fired_transitions = []
            for transition in self.net.getTransitions():
                ingoing_places = self.net.getIncoming(transition)
                if sum([place.tokens for place in ingoing_places]) == len(ingoing_places):
                    fired_transition = transition
                    if fired_transition.label not in self.prev_fired:
                        fired_transitions.append(fired_transition)
                        self.prev_fired.append(fired_transition.label)

            fired_transitions = [
                transition.label for transition in fired_transitions]
            self.transitions_to_change[self.image_number] = fired_transitions

            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        places = self.net.getPlaces()
        for i, place in enumerate(places):
            place.tokens = M[0].state[i]

    # This function represents algorithm of logical petri net
    def logical_petri_net(self, M):
        final_state_logcal_net = None
        self.prev_fired = []
        array_steps = []
        Wo = M[0].state
        self.main_layout.marking.setText(
            "( "+', '.join([str(int(elem)) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.main_layout.actual_marking.setText(
            "( "+', '.join([str(int(elem)) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.actual_marking.adjustSize()

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
                    Vo[i] = 1
            Uo = [int(abs(1 - i)) for i in Vo]

            almost_result = []
            sub_result = []
            for i in outputMatrix:
                for index, k in enumerate(i):
                    sub_result.append(min(k, Uo[index]))
                almost_result.append(int(max(sub_result)))
                sub_result = []
            Wk = []
            for i in range(len(Wo)):
                Wk.append(int(max(Wo[i], almost_result[i])))

            previous_place = None

            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
            array = [
                transition for transition in self.transitions_to_change.values()]
            for arc in self.net.getArcs():
                if arc.getSourceId().__class__ == Place:
                    previous_place = self.net.getPlaceById(
                        arc.getSourceId()).label
                if arc.src.label in array[self.image_number-2]:
                    result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", arc.dest.tokens
                    final_state_logcal_net = arc.dest.name
                    array_steps.append(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem)
                                                      for i, elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number -
                                         1] = actual_step_marking
                self.draw_net(0, 0)
                self.image_number += 1
                self.net.Wk_final = Wk
            self.net.Wk_final = Wo
        if final_state_logcal_net is None:
            self.main_layout.defuzzyfication_label.setText("Nezname pravidlo")
            self.main_layout.defuzzyfication_label.setStyleSheet("color: red;")
        else:
            self.main_layout.defuzzyfication_label.setText(
                str(final_state_logcal_net))
            self.main_layout.defuzzyfication_label.setStyleSheet(
                "color: green;")
        self.setting_image(0)

    def fill_dict_pre_fuzzy_net(self, M):
        self.prev_fired = []
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
                Wk.append(max(Wo[i], almost_result[i]))

            places = self.net.getPlaces()
            for i, place in enumerate(places):
                place.tokens = Wo[i]

            fired_transitions = []
            for transition in self.net.getTransitions():
                ingoin = self.net.getIncoming(transition)
                if min([place.tokens for place in ingoin]) != 0:
                    fired_transition = transition
                    if fired_transition.label not in self.prev_fired:
                        fired_transitions.append(fired_transition)
                        self.prev_fired.append(fired_transition.label)

            fired_transitions = [
                transition.label for transition in fired_transitions]
            self.transitions_to_change[self.image_number] = fired_transitions
            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        places = self.net.getPlaces()
        for i, place in enumerate(places):
            place.tokens = M[0].state[i]

    # This function represents algorithm of fuzzy petri net
    def fuzzy_petri_net(self, M):
        Wo = M[0].state
        final_state_fuzzy_net = None
        self.prev_fired = []
        array_steps = []
        self.main_layout.marking.setText(
            "( "+', '.join([str(elem) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.main_layout.actual_marking.setText(
            "( "+', '.join([str(elem) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.actual_marking.adjustSize()

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
                Wk.append(max(Wo[i], almost_result[i]))
            previous_place = None

            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]

            array = [
                transition for transition in self.transitions_to_change.values()]
            for arc in self.net.getArcs():
                if arc.getSourceId().__class__ == Place:
                    previous_place = self.net.getPlaceById(
                        arc.getSourceId()).label
                if arc.src.label in array[self.image_number-2]:
                    result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", arc.dest.tokens
                    final_state_fuzzy_net = arc.dest.name
                    array_steps.append(result_string)
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

        if final_state_fuzzy_net is None:
            self.main_layout.defuzzyfication_label.setText("Nezname pravidlo")
            self.main_layout.defuzzyfication_label.setStyleSheet("color: red;")
        else:
            self.main_layout.defuzzyfication_label.setText(
                str(final_state_fuzzy_net))
            self.main_layout.defuzzyfication_label.setStyleSheet(
                "color: green;")
        if self.fuzzification:
            self.defuzzyfication_decision(Wk[len(Wk)-1])
        self.fuzzification = 0
        self.setting_image(0)

    def fill_dict_pre_fuzzy_with_weights(self, M):
        self.transitions_to_change = {}
        Wo = M[0].state
        self.prev_fired = []
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
                Wk.append(max(Wo[i], almost_result[i]))

            places = self.net.getPlaces()
            for i, place in enumerate(places):
                place.tokens = Wo[i]

            fired_transitions = []
            for transition in self.net.getTransitions():
                ingoin = self.net.getIncoming(transition)
                if min([place.tokens for place in ingoin]) != 0:
                    fired_transition = transition
                    if fired_transition.label not in self.prev_fired:
                        fired_transitions.append(fired_transition)
                        self.prev_fired.append(fired_transition.label)

            fired_transitions = [
                transition.label for transition in fired_transitions]
            self.transitions_to_change[self.image_number] = fired_transitions

            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        places = self.net.getPlaces()
        for i, place in enumerate(places):
            place.tokens = M[0].state[i]

    # This function represents algorithm of fuzzy petri net with weights
    def fuzzy_petri_net_with_weights(self, M):
        array_steps = []
        Wo = M[0].state
        final_state_fuzzy_net = None
        self.prev_fired = []
        self.main_layout.marking.setText(
            "( "+', '.join([str(elem) for _, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.main_layout.actual_marking.setText(
            "( "+', '.join([str(elem) for _, elem in enumerate(Wo)])+" )")
        self.main_layout.actual_marking.adjustSize()

        self.actual_marking_dict[0] = "( "+', '.join([str(elem)
                                                      for _, elem in enumerate(Wo)])+" )"

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
                Wk.append(max(Wo[i], almost_result[i]))

            previous_place = None

            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
            array = [
                transition for transition in self.transitions_to_change.values()]

            for arc in self.net.getArcs():
                if arc.getSourceId().__class__ == Place:
                    previous_place = self.net.getPlaceById(
                        arc.getSourceId()).label
                if arc.src.label in array[self.image_number-2]:
                    result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", arc.dest.tokens
                    final_state_fuzzy_net = arc.dest.name
                    array_steps.append(result_string)

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

        if final_state_fuzzy_net is None:
            self.main_layout.defuzzyfication_label.setText("Nezname pravidlo")
            self.main_layout.defuzzyfication_label.setStyleSheet("color: red;")
        else:
            self.main_layout.defuzzyfication_label.setText(
                str(final_state_fuzzy_net))
            self.main_layout.defuzzyfication_label.setStyleSheet(
                "color: green;")

        if self.fuzzification:
            self.defuzzyfication_decision(Wk[len(Wk)-1])
        self.fuzzification = 0
        self.setting_image(0)

    def fill_dict_pre_fuzzy_with_weights_and_thresholds(self, M):
        self.transitions_to_change = {}
        Wo = M[0].state
        nRows = len(self.net.getPlaces())
        self.prev_fired = []
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
                Wk.append(max(Wo[i], almost_result[i]))

            places = self.net.getPlaces()
            for i, place in enumerate(places):
                place.tokens = Wo[i]

            fired_transitions = []
            for transition in self.net.getTransitions():
                ingoin = self.net.getIncoming(transition)
                if min([place.tokens for place in ingoin]) != 0:
                    fired_transition = transition
                    if fired_transition.label not in self.prev_fired:
                        fired_transitions.append(fired_transition)
                        self.prev_fired.append(fired_transition.label)

            fired_transitions = [
                transition.label for transition in fired_transitions]
            self.transitions_to_change[self.image_number] = fired_transitions

            if Wk != Wo:
                self.image_number += 1
        self.transitions_to_change[self.image_number] = "END"
        places = self.net.getPlaces()
        for i, place in enumerate(places):
            place.tokens = M[0].state[i]

    def fuzzy_petri_net_with_weights_thresholds(self, M):
        array_steps = []
        Wo = M[0].state
        print("Wo: ", Wo)
        final_state_fuzzy_net = None
        self.prev_fired = []
        self.main_layout.marking.setText(
            "( "+', '.join([str(elem) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.main_layout.actual_marking.setText(
            "( "+', '.join([str(elem) for i, elem in enumerate(Wo)])+" )")
        self.main_layout.actual_marking.adjustSize()

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
                Wk.append(max(Wo[i], almost_result[i]))

            previous_place = None

            for place in self.net.getPlaces():
                place.tokens = Wk[self.net.getPlaces().index(place)]
            array = [
                transition for transition in self.transitions_to_change.values()]

            for arc in self.net.getArcs():
                if arc.getSourceId().__class__ == Place:
                    previous_place = self.net.getPlaceById(
                        arc.getSourceId()).label
                if arc.src.label in array[self.image_number-2]:
                    result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", arc.dest.tokens
                    final_state_fuzzy_net = arc.dest.name
                    array_steps.append(result_string)

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

        if final_state_fuzzy_net is None:
            self.main_layout.defuzzyfication_label.setText("Nezname pravidlo")
            self.main_layout.defuzzyfication_label.setStyleSheet("color: red;")
        else:
            self.main_layout.defuzzyfication_label.setText(
                str(final_state_fuzzy_net))
            self.main_layout.defuzzyfication_label.setStyleSheet(
                "color: green;")
        if self.fuzzification:
            self.defuzzyfication_decision(Wk[len(Wk)-1])
        self.fuzzification = 0
        self.setting_image(0)

    # This method is used to defuzzyfication decision
    def defuzzyfication_decision(self, result):
        if self.flag == 0:
            for place in self.net.getPlaces():
                if place.label == 'NYHA-II-III' and 'LBBB' not in self.records_dict:
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Zvazit zavedenie ICD")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: yellow;")
                    else:
                        self.main_layout.defuzzyfication_label.setText(
                            "Nezname pravidlo")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: red;")

                if place.label == 'LBBB':
                    if place.tokens == 1:
                        for key, value in self.records_dict.items():
                            if key == "QRS":
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Doporučene CRT")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")
                                if value == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Malo by byt zvazene CRT")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: orange;")

                    if place.tokens == 0:
                        for key, value in self.records_dict.items():
                            if key == "QRS":
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Malo by byt zvazene CRT")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: orange;")
                                if value == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Moze byt zvazene CRT")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: yellow;")

                if place.label == "Uzivany gliflozin":
                    if place.tokens == 0 and ("empa" not in self.records_dict_prev.values() or "dapa" not in self.records_dict_prev.values()):
                        for key, value in self.records_dict.items():
                            if key == "GFR":
                                if value == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Nemozno pridat gliflozin")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: green;")
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Pridajte empagliflozin")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")
                            if key == "sTK":
                                if value == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Nemozno pridat gliflozin")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: green;")
                            if key == "symptomaticka hypotenzia":
                                if value == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Nemozno pridat gliflozin")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: green;")

                    if place.tokens == 1 and ("empa" in self.records_dict_prev.values() or "dapa" in self.records_dict_prev.values()):
                        for key, value in self.records_dict.items():
                            if key == "GFR":
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Pokračujte v terapii.")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")

                    if place.tokens == 0 and ("empa" in self.records_dict_prev.values() or "dapa" in self.records_dict_prev.values()):
                        for key, value in self.records_dict.items():
                            if key == "GFR":
                                if value == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Vysadiť gliflozin")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: yellow;")

                    if place.tokens == 0 and ("dapa" in self.records_dict_prev.values() and "empa" not in self.records_dict_prev.values()):
                        for key, value in self.records_dict.items():
                            if key == "GFR":
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Prejst na empa")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: yellow;")

                    if place.tokens == 1 and ("empa" in self.records_dict_prev.values() and "dapa" not in self.records_dict_prev.values()):
                        for key, value in self.records_dict.items():
                            if key == "GFR":
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Pokračujte v terapii.")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")

                    if place.tokens == 1 and "Max davka" in self.records_dict:
                        for key, value in self.records_dict.items():
                            if key == "Max davka":
                                if value == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - " + "Pokračujte v terapii.")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")

                if place.label == "eGRF":
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - " + "Sznizit ACEi/ARB/ARNI, MRA")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: yellow;")

                if place.label == "K+" and ("MRA" not in [place.label for place in self.net.getPlaces()] and "ACEI" not in [place.label for place in self.net.getPlaces()] and "ARNI" not in [place.label for place in self.net.getPlaces()]):
                    for key, value in self.records_dict.items():
                        if key == "K+":
                            if value == 0:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - " + "Sznizit ACEi/ARB/ARNI, MRA")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: yellow;")

                if place.label == "SBP":
                    if place.tokens == 0:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - " + "Snizit ACEi/ARB/ARNI, MRA")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: yellow;")
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - " + "Pokracovat alebo zvysit BB")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: red;")

                if place.label == "HR":
                    if place.tokens == 0:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - " + " Znizit alebo vysadit BB")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: yellow;")

                if place.label == "Zvysenie NTproBNP":
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - " + "Zvysit diuretika a znizit alebo vysadit BB")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: yellow;")

                if place.label == "Uziva vericiguat":
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Vysadiť, redukovať vericiguat")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: orange;")
                    if place.tokens == 0:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Nezačať s terapiou")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: green;")

                    if place.tokens == 0 and "sTK" not in self.records_dict and "GFR" not in self.records_dict and "symptomaticka hypotenzia" not in self.records_dict:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Začať s terapiou")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: red;")

                if place.label == "Uziva ivabradin":
                    if place.tokens == 0:
                        if 'GFR' not in self.records_dict_prev and 'SF' not in self.records_dict_prev and 'symptomaticka bradykardia' not in self.records_dict_prev and 'vek' not in self.records_dict_prev and 'fibrilacia predsieni' not in self.records_dict_prev:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Začať s terapiou")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: red;")
                        elif "vek" in self.records_dict:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Začať s nižšou dávkou")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: yellow;")
                        else:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Nezačať s terapiou")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: green;")
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Vysadiť alebo redukovať ivabradin")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: red;")

                if place.label == "Uziva digoxin":
                    if place.tokens == 0:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Nezačať s terapiou")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: green;")
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Vysadiť alebo redukovať digoxin")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: red;")

                if place.label == "Hodnota digoxinu" and "Uziva digoxin" not in self.records_dict:
                    if place.tokens == 0:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Pokracovat")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: green;")
                    if place.tokens == 1:
                        self.main_layout.defuzzyfication_label.setText(
                            str(result) + " - Zvýšiť dávku")
                        self.main_layout.defuzzyfication_label.setStyleSheet(
                            "color: red;")

                if place.label == "ACEI":
                    if place.tokens == 0:
                        for key, value in self.records_dict.items():
                            if key == "K+":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Nemožnosť pridať ACEi")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")
                            if key == "GFR":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Nemožnosť pridať ACEi")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")
                            if key == "sTK":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Nemožnosť pridať ACEi")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")

                    if place.tokens == 1:
                        for key, value in self.records_dict.items():
                            if key == "K+" or key == "symptomaticka hypotenzia" or key == "GFR":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Vysadiť alebo znížiť ACEi")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: red;")
                            if key == "Max davka" and self.records_dict_prev["Max davka"] == "true":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Pokračujte v liečbe.")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")
                            if key == "Max davka" and self.records_dict_prev["Max davka"] == "false":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Zvýšiť dávku.")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: red;")

                if place.label == "BB":
                    if place.tokens == 0:
                        for key, value in self.records_dict.items():
                            if key == "TEP" or key == "sTK" or key == "CHOCHP" or key == "AV blok":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Nepridať BB")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")
                            if key == "Kreatinin":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Pridať BB okrem nebivolol.")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: red;")

                    if place.tokens == 1:
                        for key, value in self.records_dict.items():
                            if key == "TEP" or key == "AV blok" or key == "symptomaticka hypotenzia":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Vysadiť alebo znížiť BB")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: yellow;")
                            if key == "Nebivolol" or key == "Kreatinin":
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Nahradiť nebivolol")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: orange;")
                            if key == "Max davka" and self.records_dict[key] == 1:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Zvýšiť dávku.")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: red;")
                            if key == "Max davka" and self.records_dict[key] == 0:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Pokračujte v liečbe.")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")

                if place.label == "MRA":

                    for key, value in self.records_dict.items():

                        if "K+" in self.records_dict and "Max davka" not in self.records_dict:
                            if value == 0:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result-result/2) + " - Udržiavajte aktuálnu dávku")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: green;")
                            if value == 1:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result+result/2) + " - Vysaďte MRA")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: red;")
                        elif key == "Max davka" and "GFR" in self.records_dict:
                            if value == 1:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Zvýšiť dávku")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: orange;")
                        elif key == "Max davka" and "K+" in self.records_dict:
                            if value == 1:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Zvýšiť dávku")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: orange;")
                        elif key == "GFR" and "Max davka" not in self.records_dict and "K+" not in self.records_dict:
                            if value == 1:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result+result/2) + " - Vysaďte MRA")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: red;")
                        elif key == "Max davka" and "K+" not in self.records_dict and "GFR" not in self.records_dict:
                            if value == 0:
                                self.main_layout.defuzzyfication_label.setText(
                                    str(result) + " - Pokračujte v terapii.")
                                self.main_layout.defuzzyfication_label.setStyleSheet(
                                    "color: yellow;")

                if place.label == "ARNI":
                    if place.tokens == 0:
                        for key, value in self.records_dict.items():
                            if key == "GFR" or key == "sTK" or key == "symptomaticka hypotenzia" or key == "K+":
                                if key == "GFR" and result == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - Začať s ARNI")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")
                                elif key == "GFR" and result == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - Nezačať s ARNI")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: green;")
                                elif key == "sTK" and result == 1:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - Začať s ARNI")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: red;")
                                elif key == "sTK" and result == 0:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - Nezačať s ARNI")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: green;")
                                else:
                                    self.main_layout.defuzzyfication_label.setText(
                                        str(result) + " - ponechať ACEi")
                                    self.main_layout.defuzzyfication_label.setStyleSheet(
                                        "color: green;")

                    if place.tokens == 1:
                        if "Max davka" in self.records_dict and self.records_dict["Max davka"] == 0:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Pokračovať v liečbe")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: yellow;")
                        elif "Max davka" in self.records_dict and self.records_dict["Max davka"] == 1:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Navýšiť dávku ARNI")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: orange;")
                        elif "Max davka" not in self.records_dict:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Vysadiť ARNI")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: orange;")
                        else:
                            self.main_layout.defuzzyfication_label.setText(
                                str(result) + " - Pokračovať v liečbe")
                            self.main_layout.defuzzyfication_label.setStyleSheet(
                                "color: green;")
        # this is defuzzification for values from database (Github)
        if self.flag == 1:
            if 0.0 <= result <= 0.25:
                self.main_layout.defuzzyfication_label.setText(
                    str(result) + " - Very low")
                self.main_layout.defuzzyfication_label.setStyleSheet(
                    "color: green;")
            elif 0.25 < result <= 0.45:
                self.main_layout.defuzzyfication_label.setText(
                    str(result) + " - Low")
                self.main_layout.defuzzyfication_label.setStyleSheet(
                    "color: yellow;")
            elif 0.45 < result <= 0.65:
                self.main_layout.defuzzyfication_label.setText(
                    str(result) + " - High")
                self.main_layout.defuzzyfication_label.setStyleSheet(
                    "color: orange;")
            elif 0.65 < result <= 0.85:
                self.main_layout.defuzzyfication_label.setText(
                    str(result) + " - Very high")
                self.main_layout.defuzzyfication_label.setStyleSheet(
                    "color: red;")
            elif 0.85 < result <= 1.0:
                self.main_layout.defuzzyfication_label.setText(
                    str(result) + " - Critical")
                self.main_layout.defuzzyfication_label.setStyleSheet(
                    "color: red;")

        self.main_layout.defuzzyfication_label.adjustSize()
        self.records_dict = {}
        self.records_dict_prev = {}

    # Error message box if net is not valid
    def error_message_box(self):
        dialog = QMessageBox(text="Siet je neohranicena")
        dialog.setWindowTitle("Message Dialog")
        dialog.setWindowIcon(QtGui.QIcon('..\\PIS-bonus\\gui\\icon.jpg'))
        dialog.exec()   # Stores the return value for the button pressed

    def run_logical(self):
        self.net.M0 = [int(i) for i in self.net.M0]
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('../PIS-bonus/images/*')
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
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('../PIS-bonus/images/*')
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
        files = glob.glob('../PIS-bonus/images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.dict_final = {}
            self.image_number = 1
            self.fill_dict_pre_fuzzy_with_weights(M)
            self.image_number = 1
            self.image_index = 1
            self.draw_net(1, 0)
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
        files = glob.glob('../PIS-bonus/images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.dict_final = {}
            self.image_number = 1
            self.fill_dict_pre_fuzzy_with_weights_and_thresholds(M)
            self.image_number = 1
            self.image_index = 1
            self.draw_net(1, 1)
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

# This is dialog window with patient selection and sign in with password


class DialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.ui = QFile(
            "..\\PIS-bonus\\gui\\patientWindow.ui")
        self.ui.open(QFile.ReadOnly)
        self.main_layout = self.loader.load(self.ui)
        self.ui.close()
        self.main_layout.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_layout.setStyleSheet(
            "QDialog::titleBar { background-color: black; }")
        self.main_layout.setWindowIcon(
            QtGui.QIcon('..\\PIS-bonus\\gui\\icon.jpg'))
        self.main_layout.setWindowTitle("Výber pacienta")
        self.main_layout.show()
        self.database_output_table1 = []
        self.database_output_table2 = []
        self.main_layout.enroll.clicked.connect(self.open_main_application)
        self.main_layout.interrupt.clicked.connect(self.main_layout.close)
        self.patient_records = None
        self.patient_problems = []
        self.hashed = None
        self.main_layout.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def open_main_application(self):
        password = self.main_layout.password.text().encode('utf-8')
        hashed_with_salt = self.hashed[0][1]
        # added random +++ to salt
        hashed_str, salt_str = hashed_with_salt.split("+++")
        salt = salt_str.encode('utf-8')
        hashed = bcrypt.hashpw(password, salt)
        if hashed_str.encode('utf-8') == hashed:
            self.main_layout.close()
            self.main_application = MainApplication()
            files = glob.glob('../PIS-bonus/images/*')
            if files != None:
                for f in files:
                    os.remove(f)
            files = glob.glob('../PIS-bonus/images_fuzzyfication/*')
            if files != None:
                for f in files:
                    os.remove(f)
            self.close()
            self.main_application.database_output_table1 = self.patient_records
            self.main_application.main_layout.table.setColumnCount(
                len(self.patient_records)-1)
            self.main_application.main_layout.table.setHorizontalHeaderLabels(
                ["Meno", "Priezvisko", "Vek", "Pohlavie", "Výška", "Váha"])
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

            self.main_application.database_output_table2 = self.patient_problems
            self.main_application.show()
        else:
            self.main_layout.check.setText("Zadali ste nesprávne heslo")
            self.main_layout.check.setStyleSheet("color: red")
            self.main_layout.password.clear()
            return

    # Function to choose patient from database
    def combo_changed(self, index):
        if index >= 0:
            self.patient_problems = []
            patient_name = self.main_layout.patientPicker.itemText(index)
        else:
            # No item selected, use the first item
            self.patient_problems = []
            patient_name = self.main_layout.patientPicker.itemText(0)
        selected_records = [
            i for i in self.database_output_table1 if i[1] + " " + i[2] == patient_name]
        if selected_records:
            self.patient_records = selected_records[0]
            for record in self.database_output_table2:
                if record[1] == self.patient_records[0]:
                    self.patient_problems.append(record)
        else:
            self.patient_records = None
            self.patient_problems = []
            print("No records found for selected patient.")

    # Function for parsing database
    def parsing_database(self):
        for i in self.database_output_table1:
            self.main_layout.patientPicker.addItem(i[1] + " " + i[2])
        if self.main_layout.patientPicker.count() > 0:
            self.combo_changed(0)
        self.main_layout.patientPicker.currentIndexChanged.connect(
            self.combo_changed)


if __name__ == '__main__':
    # Ask if we want to add patient to the database
    print("Pridat pacienta? (y/n)")
    answer = input()
    if answer == "y":
        print("Meno pacienta:")
        dict_values_patient["name"] = input()
        print("Priezvisko pacienta:")
        dict_values_patient["surname"] = input()
        print("Vek pacienta (young, middle age, old, very old):")
        dict_values_patient["age"] = input()
        print("Pohlavie pacienta (M/F):")
        dict_values_patient["sex"] = input()
        print("Vyska pacienta (short, medium, tall):")
        dict_values_patient["height"] = input()
        print("Vaha pacienta (light, medium, heavy):")
        dict_values_patient["weight"] = input()

        print("Pridat problem pacienta? (y/n)")
        answer = input()
        if answer == "y":
            print("Hodnota systolickeho tlaku (low, medium, high, very high)")
            dict_values_problem["systolic_blood_pressure"] = input()
            print("Hodnota diastolickeho tlaku (low, medium, high, very high))")
            dict_values_problem["diastolic_blood_pressure"] = input()
            print("Hodnota cukru v krvi (low, medium, high)")
            dict_values_problem["blood_sugar"] = input()
            print(
                "Hodnota cholesterolu (low, medium high, high, very high, extremely high)")
            dict_values_problem["cholesterol"] = input()
            print("Hodnota tepu (low, medum, high)")
            dict_values_problem["heart_rate"] = input()
            print("Hodnota EKG (normal, abnormal, hypertrophy)")
            dict_values_problem["EKG"] = input()
            print("Bolest v hrudi (typical, atypical, non-anginal, asymptomatic)")
            dict_values_problem["chest_pain"] = input()
        result, result1, result2 = connect(
            1, 0, dict_values_patient, dict_values_problem)
    else:
        # connects database
        result, result1, result2 = connect(0, 0, None, None)
    app = QApplication(sys.argv)
    dialog = DialogWindow()
    dialog.database_output_table1 = result
    dialog.database_output_table2 = result1
    dialog.hashed = result2
    dialog.parsing_database()
    sys.exit(app.exec())
