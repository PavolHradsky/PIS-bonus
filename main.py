import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
from PetriNet import PetriNet
from Place import Place
from Transition import Transition
from functions import read_xml, list_is_greater
from Rpn import Rpn
import tkinter as tk
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QMessageBox
from PySide6.QtCore import QFile, QIODevice
import os
import glob
from PySide6.QtGui import QPixmap, QImage, QResizeEvent
import matplotlib 
matplotlib.use('tkagg')
from database import connect

def loading_data(name_file, fuzzy_flag,weights_flag,threshold_flag, flag):
    places, transitions, arcs, role = read_xml(name_file, fuzzy_flag,weights_flag,threshold_flag, flag)
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


class MainAplication(QtWidgets.QMainWindow):
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
        self.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Petri nets")
        self.image_number = 1

        # bind events to buttons
        self.main_layout.loadFile.clicked.connect(self.open_dialog)
        # comboBox
        self.main_layout.comboBox.addItems(["Logická Petriho sieť", 
                                       "Fuzzy Petriho sieť", 
                                       "Fuzzy Petriho sieť s váhami pravidiel", 
                                       "Fuzzy Petriho sieť s váhami a prahmi pravidiel"])
        self.main_layout.comboBox.currentIndexChanged.connect(self.combo_changed)
        self.main_layout.runButton.clicked.connect(self.run)
        self.main_layout.prevButton.clicked.connect(self.prev)
        self.main_layout.nextButton.clicked.connect(self.next)
        self.main_layout.clearAll.clicked.connect(self.clear)
        self.main_layout.clearAll.setEnabled(False)
        self.image_dict = {}
        self.step_dict = {}
        self.actual_marking_dict = {}
        self.TR = []
        self.k = 0
        self.tree = None
        self.ui = QFile(".\\gui\\anotherWindowFinal.ui")
        self.ui.open(QFile.ReadOnly)
        self.anotherWindow = self.loader.load(self.ui)
        self.anotherWindow.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
        self.anotherWindow.setGeometry(200, 200, 800, 600)
        self.anotherWindow.setWindowTitle("Initial marking")
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

        if self.image_number == 1:
            self.main_layout.prevButton.setEnabled(False)

    # resize event
    
    def resizeEvent(self, event):
        # setImage
        if len(self.image_dict)>0:
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
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
        if self.file_path:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            if "fuzzy" in self.file_name:
                self.fuzzy_flag = 1
            else:
                self.fuzzy_flag = 0
            self.net = loading_data(self.file_name, self.fuzzy_flag, self.weights_flag, self.tresholds_flag,0)
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
            dialog.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
            ret = dialog.exec()   # Stores the return value for the button pressed
    
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
                        self.net.tresholds = [0 for _ in range(len(self.dict_transitions))]
                    if len(self.net.weights) == 0:
                        self.net.weights = [0 for _ in range(len(self.dict_weights))]
                    # create new tag to xml to each transition
                    for i, rank in enumerate(self.root.iter('transition')):
                        # addd new tag
                        new_tag = ET.SubElement(rank, 'treshold')
                        # add value to new tag
                        new_tag.text = str(self.net.tresholds[i])

                        new_tag = ET.SubElement(rank, 'weight')
                        # add value to new tag
                        new_tag.text = str(self.net.weights[i])
                else:
                    if len(self.net.tresholds) != 0 and len(self.net.weights) == 0:
                        # create new tag to xml to each transition
                        if len(self.net.weights) == 0:
                            self.net.weights = [0 for _ in range(len(self.dict_weights))]

                        for i, rank in enumerate(self.root.iter('transition')):
                            # addd new tag
                            new_tag = ET.SubElement(rank, 'treshold')
                            # add value to new tag
                            new_tag.text = str(self.net.tresholds[i])

                            new_tag = ET.SubElement(rank, 'weight')
                            # add value to new tag
                            new_tag.text = str(self.net.weights[i])

                    if len(self.net.tresholds) == 0 and len(self.net.weights) != 0:
                        if len(self.net.tresholds) == 0:
                            self.net.tresholds = [0 for _ in range(len(self.dict_transitions))]
                        # create new tag to xml to each transition
                        for i, rank in enumerate(self.root.iter('transition')):
                            # addd new tag
                            new_tag = ET.SubElement(rank, 'trehsold')
                            # add value to new tag
                            new_tag.text = str(self.net.tresholds[i])

                            new_tag = ET.SubElement(rank, 'weight')
                            # add value to new tag
                            new_tag.text = str(self.net.weights[i])

                    if  len(self.net.tresholds) != 0 and len(self.net.weights) != 0:
                        # create new tag to xml to each transition
                        for i, rank in enumerate(self.root.iter('transition')):
                            # addd new tag
                            new_tag = ET.SubElement(rank, 'treshold')
                            # add value to new tag
                            new_tag.text = str(self.net.tresholds[i])

                            new_tag = ET.SubElement(rank, 'weight')
                            # add value to new tag
                            new_tag.text = str(self.net.weights[i])


            if self.weights_flag:
               
                if len(self.net.weights) == 0:
                    self.net.weights = [0 for _ in range(len(self.dict_weights))]
                    for i, rank in enumerate(self.root.iter('transition')):
                        # addd new tag
                        new_tag = ET.SubElement(rank, 'weight')
                        # add value to new tag
                        new_tag.text = str(self.net.weights[i])
                             
                else:
                    for i, rank in enumerate(self.root.iter('transition')):
                        # addd new tag
                        new_tag = ET.SubElement(rank, 'weight')
                        # add value to new tag
                        new_tag.text = str(self.net.weights[i])

        dir_path = os.path.dirname(self.file_path)

        self.tree.write(os.path.join(dir_path, self.file_name.split('.')[0] + "_initial" + "_marking.xml"),
                encoding="UTF-8", xml_declaration=True)
        print("Počiatočné označkovanie: ", self.net.M0)

        if self.logical_flag and not self.fuzzy_flag and not self.weights_flag and not self.tresholds_flag:
            self.net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 0,0,0,1)
            self.run_logical()
        elif self.fuzzy_flag and not self.weights_flag and not self.tresholds_flag and not self.logical_flag:
            self.net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1,0,0,1)
            self.run_fuzzy()
        elif self.weights_flag and not self.tresholds_flag and self.fuzzy_flag and not self.logical_flag:
            self.net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1,1,0,1) 
            self.run_fuzzy_with_weights()
        elif self.weights_flag and self.tresholds_flag and self.fuzzy_flag and not self.logical_flag:
            self.net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1,1,1,1)
            self.run_fuzzy_with_weights_and_thresholds()
    

    # TODO do this in qdesigner ???
    def set_marking_initial1(self):
        for place in self.net.getPlaces():
            self.dict_places[place.label] = place.tokens
        for transition in self.net.getTransitions():
            self.dict_transitions[transition.getId()] = transition.label

    
        placesLayout = QtWidgets.QVBoxLayout()
        placesLabel = QtWidgets.QLabel("Miesta")
        placesLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        placesLayout.addWidget(placesLabel) 

        for i, key in enumerate(self.dict_places):
            placeLabel = QtWidgets.QLabel(key)
            placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            entry = QtWidgets.QLineEdit()
            self.dict_marks[key] = entry
            placeLayout = QtWidgets.QHBoxLayout()
            placeLayout.addWidget(placeLabel)
            placeLayout.addWidget(entry)
            placesLayout.addLayout(placeLayout)
        okButton = QtWidgets.QPushButton("OK")
        okButton.clicked.connect(lambda: [self.set_marking(self.dict_marks), self.delete_text(self.dict_marks)])
        placesLayout.addWidget(okButton)
        self.anotherWindow.main.addLayout(placesLayout)

        transitionsLayout0 = QtWidgets.QVBoxLayout()
        transitionsLabel0 = QtWidgets.QLabel("Prechody")
        transitionsLabel0.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        transitionsLayout0.addWidget(transitionsLabel0)
        for i, key in enumerate(self.dict_transitions):
            transitionLabel0 = QtWidgets.QLabel(self.dict_transitions[key])
            transitionLabel0.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            transitionLayout0 = QtWidgets.QHBoxLayout()
            transitionLayout0.addWidget(transitionLabel0)
            transitionsLayout0.addLayout(transitionLayout0)
          
        self.anotherWindow.main.addLayout(transitionsLayout0)
        
        if self.weights_flag or self.tresholds_flag:
            weightsLayout = QtWidgets.QVBoxLayout()
            weightsLabel = QtWidgets.QLabel("Váhy prechodov")
            weightsLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
            weightsLayout.addWidget(weightsLabel)
            for i, key in enumerate(self.dict_transitions):
                weightLabel = QtWidgets.QLabel(self.dict_transitions[key])
                weightLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                entry2 = QtWidgets.QLineEdit()
                self.dict_weights[key] = entry2
                weightLayout = QtWidgets.QHBoxLayout()
                weightLayout.addWidget(weightLabel)
                weightLayout.addWidget(entry2)
                weightsLayout.addLayout(weightLayout)
            okButton2 = QtWidgets.QPushButton("OK")
            okButton2.clicked.connect(lambda: [self.set_weights(self.dict_weights), self.delete_text(self.dict_weights)])
            weightsLayout.addWidget(okButton2)
            self.anotherWindow.main.addLayout(weightsLayout)

        if self.tresholds_flag:
            transitionsLayout = QtWidgets.QVBoxLayout()
            transitionsLabel = QtWidgets.QLabel("Prahy prechodov")
            transitionsLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
            transitionsLayout.addWidget(transitionsLabel)
            
            for i, key in enumerate(self.dict_transitions):
                transitionLabel = QtWidgets.QLabel(self.dict_transitions[key])
                transitionLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                if self.tresholds_flag:
                    entry3 = QtWidgets.QLineEdit()
                    self.dict_tresholds[key] = entry3
                    transitionLayout = QtWidgets.QHBoxLayout()
                    transitionLayout.addWidget(transitionLabel)
                    transitionLayout.addWidget(entry3)
                    transitionsLayout.addLayout(transitionLayout)
            okButton3 = QtWidgets.QPushButton("OK")
            okButton3.clicked.connect(lambda: [self.set_tresholds(self.dict_tresholds), self.delete_text(self.dict_tresholds)])
            transitionsLayout.addWidget(okButton3)
            self.anotherWindow.main.addLayout(transitionsLayout)


    def set_marking_initial(self):
        for place in self.net.getPlaces():
            self.dict_places[place.label] = place.tokens
        for transition in self.net.getTransitions():
            self.dict_transitions[transition.getId()] = transition.label
        placesLayout = QtWidgets.QVBoxLayout()
        self.anotherWindow.placesWidget.setLayout(placesLayout)
        # Iterate over the dictionary and add each QLabel and QLineEdit to a QHBoxLayout
        for i, key in enumerate(self.dict_places):
            placeLabel = QtWidgets.QLabel(key)
            placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            entry = QtWidgets.QLineEdit()
            self.dict_marks[key] = entry
            placeLayout = QtWidgets.QHBoxLayout()
            placeLayout.addWidget(placeLabel)
            placeLayout.addWidget(entry)
            placesLayout.addLayout(placeLayout)

        # Set the QWidget as the widget for the QScrollArea
        self.anotherWindow.placesScrollArea.setWidget(self.anotherWindow.placesWidget)
        self.anotherWindow.OK1.clicked.connect(lambda: [self.set_marking(self.dict_marks), self.delete_text(self.dict_marks)])
        
        if self.fuzzy_flag and not self.weights_flag and not self.tresholds_flag:
            weightsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.weightsWidget.setLayout(weightsLayout)
            self.anotherWindow.weight.setText("Prechody")
            for i, key in enumerate(self.dict_transitions):
                transitionLabel0 = QtWidgets.QLabel(self.dict_transitions[key])
                transitionLabel0.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                weightLayout = QtWidgets.QHBoxLayout()
                weightLayout.addWidget(transitionLabel0)
                weightsLayout.addLayout(weightLayout)
            self.anotherWindow.weightsScrollArea.setWidget(self.anotherWindow.weightsWidget)
            self.anotherWindow.OK2.hide()
        
        if self.weights_flag or self.tresholds_flag:
            weightsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.weightsWidget.setLayout(weightsLayout)
            for i, key in enumerate(self.dict_transitions):
                weightLabel = QtWidgets.QLabel(self.dict_transitions[key])
                weightLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                entry2 = QtWidgets.QLineEdit()
                self.dict_weights[key] = entry2
                weightLayout = QtWidgets.QHBoxLayout()
                weightLayout.addWidget(weightLabel)
                weightLayout.addWidget(entry2)
                weightsLayout.addLayout(weightLayout)
            self.anotherWindow.weightsScrollArea.setWidget(self.anotherWindow.weightsWidget)
            self.anotherWindow.OK2.clicked.connect(lambda: [self.set_weights(self.dict_weights), self.delete_text(self.dict_weights)])
        
        if self.tresholds_flag:
            tresholdsLayout = QtWidgets.QVBoxLayout()
            self.anotherWindow.tresholdsWidget = QtWidgets.QWidget()
            self.anotherWindow.tresholdsWidget.setLayout(tresholdsLayout)
            for i, key in enumerate(self.dict_transitions):
                transitionLabel = QtWidgets.QLabel(self.dict_transitions[key])
                transitionLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                entry3 = QtWidgets.QLineEdit()
                self.dict_tresholds[key] = entry3
                transitionLayout = QtWidgets.QHBoxLayout()
                transitionLayout.addWidget(transitionLabel)
                transitionLayout.addWidget(entry3)
                tresholdsLayout.addLayout(transitionLayout)
            self.anotherWindow.tresholdsScrollArea.setWidget(self.anotherWindow.tresholdsWidget)
            self.anotherWindow.OK3.clicked.connect(lambda: [self.set_tresholds(self.dict_tresholds), self.delete_text(self.dict_tresholds)])
    
    def delete_text(self,entries):
        for _, value in entries.items():
            value.setText("")

    def set_marking(self, entries):
        self.net.M0 = [float(value.text()) if value.text() != '' else 0.0 for _,value in entries.items()]

    def set_tresholds(self,entries):
        if entries.items():
            self.net.tresholds = [float(value.text()) if value.text() != '' else 0.0 for _,value in entries.items()]
            self.TR = self.net.tresholds

    def set_weights(self, entries):
        self.net.weights = [float(value.text()) if value.text() != '' else 0.0 for _,value in entries.items()]


    def prev(self):
        if self.image_number > 1:
            #   set button active
            self.main_layout.nextButton.setEnabled(True)
            if self.image_number == 2:
                self.main_layout.prevButton.setEnabled(False)
            self.image_number -= 1
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.actual_marking.setText(self.actual_marking_dict[self.image_number-1])
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
            self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.actual_marking.setText(self.actual_marking_dict[self.image_number-1])
            self.main_layout.actual_marking.adjustSize()
            for i in self.step_dict[self.image_number-1]:
                self.k += 1
                self.main_layout.steps.addItem(str(i))
        else:
            # set button inactive
            self.main_layout.nextButton.setEnabled(False)
            self.image_number -=1


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
        G = nx.DiGraph()
        edges = {}
        places = self.net.getPlaces()
        transitions = self.net.getTransitions()
        places_list = []
        tresholds_list = self.net.getThresholds()
        weights_list = self.net.getWeights()
        transitions_list = []
        for arc in self.net.getArcs():
            G.add_edge(arc.getSourceId(), arc.getDestinationId())
            if arc.src.__class__ == Place:
                places_list.append(arc.getSourceId())
            else:
                transitions_list.append(arc.getSourceId())
            if arc.dest.__class__ == Place:
                places_list.append(arc.getDestinationId())
            else:
                transitions_list.append(arc.getDestinationId())
            edges[(arc.getSourceId(), arc.getDestinationId())
                ] = arc.getMultiplicity()
        pos = nx.circular_layout(G)
        
        fig = plt.figure()
        nx.draw_networkx_nodes(G, pos, places)
        nx.draw_networkx_labels(
            G, pos, labels={n: n.tokens for n in places_list}, font_size=6
        )
        
        nx.draw_networkx_nodes(G, pos, transitions, node_shape='s', node_color='#ff0000')
        if weights and not thresholds:
            nx.draw_networkx_labels(
                G, pos,
                labels={
                    n: f"{n.label}\nweight: {weights_list[transitions.index(n)]}"
                    for n in transitions
                },
                font_size=6,
            )
        elif weights and thresholds:
            for l in pos:
                pos[l][1] += 0.08
            nx.draw_networkx_labels(
                G, pos,
                labels={
                    n: f"{n.label}\nweight: {weights_list[transitions.index(n)]}\nthreshold: {tresholds_list[transitions.index(n)]}"
                    for n in transitions
                },
                font_size=6,
            )
        else:
            nx.draw_networkx_labels(
                G, pos, labels={n: n.label for n in transitions}, font_size=6
            )

        for l in pos:
            pos[l][1] += 0.08
        nx.draw_networkx_labels(
            G, pos, labels={n: n.label for n in places}, font_size=6
        )

        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
        plt.axis('off')
        path = './images/' + str(self.image_number) + '.png'
        fig.savefig(path)
        self.image_dict[self.image_number] = path
        print("path: ", path)
    
    def logical_petri_net(self, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.main_layout.marking.setText("( "+', '.join([str(int(elem)) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(int(elem)) for i,elem in enumerate(Wo)])+" )"
        
        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                            for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
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
                            sourceIdInNetList] = arc.getMultiplicity()
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

            # Vo = transponse_array @ neg_Wo
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
                        previous_place = self.net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(0,0)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
       


    def fuzzy_petri_net(self, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.main_layout.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )"

        nRows = len(self.net.getPlaces())
        nColumns = len(self.net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                            for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
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
                            sourceIdInNetList] = arc.getMultiplicity()
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
                        previous_place = self.net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(0,0)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
      
    
    def fuzzy_petri_net_with_weights(self, M):
        array_steps = []
        Wo = M[0].state
        self.main_layout.marking.setText("( "+', '.join([str(elem) for _,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem) for _,elem in enumerate(Wo)])+" )"

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
                        previous_place = self.net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for _,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(1,0)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
      


    def fuzzy_petri_net_with_weights_thresholds(self, M):
        array_steps = []
        Wo = M[0].state
        print("Wo: ", Wo)
        self.main_layout.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )"

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
                            sourceIdInNetList] = arc.getMultiplicity()
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
                        previous_place = self.net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:          
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(1,1)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
    

    def run_logical(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.draw_net(0,0)
            self.image_number += 1
            self.net = self.logical_petri_net(M)
            dir_path = os.path.dirname(self.file_path)
            self.tree.write(os.path.join(dir_path, self.file_name.split('.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            dialog.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
            ret = dialog.exec()   # Stores the return value for the button pressed
            

    def run_fuzzy(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.draw_net(0,0)
            self.image_number += 1
            self.net = self.fuzzy_petri_net(M)
            dir_path = os.path.dirname(self.file_path)
            self.tree.write(os.path.join(dir_path, self.file_name.split('.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            dialog.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
            ret = dialog.exec()   # Stores the return value for the button pressed


    def run_fuzzy_with_weights(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.draw_net(1,0)
            self.image_number += 1
            self.net = self.fuzzy_petri_net_with_weights(M)
            dir_path = os.path.dirname(self.file_path)
            self.tree.write(os.path.join(dir_path, self.file_name.split('.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            dialog.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
            ret = dialog.exec()   # Stores the return value for the button pressed

    def run_fuzzy_with_weights_and_thresholds(self):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(self.net)
        if M is not None:
            self.draw_net(1,1)
            self.image_number += 1
            self.net = self.fuzzy_petri_net_with_weights_thresholds(M)
            dir_path = os.path.dirname(self.file_path)
            self.tree.write(os.path.join(dir_path, self.file_name.split('.')[0] + "_final_marking.xml"), encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            dialog.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\gui\\icon.jpg'))
            ret = dialog.exec()   # Stores the return value for the button pressed

if __name__ == '__main__':
    #connect()
    app = QtWidgets.QApplication(sys.argv)
    window = MainAplication()  
    window.show()
    sys.exit(app.exec())
    
