import time
from tkinter import ttk
from typing import List
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

def loading_data(name_file, fuzzy_flag):
    places, transitions, arcs, role = read_xml(name_file, fuzzy_flag)
    net: PetriNet = PetriNet(places, transitions, arcs, role)
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

# another window 
class AnotherWindow(QWidget):
    loader = QUiLoader()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = QFile(".\\gui\\anotherwindow.ui")
        self.ui.open(QFile.ReadOnly)
        self.window = self.loader.load(self.ui)
        self.window.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\icon.jpg'))
        self.window.setGeometry(200, 200, 800, 600)
        self.window.setFixedSize(1280, 720)
        self.window.setWindowTitle("Initial marking")
        self.ui.close()
        self.window.show()
        self.logical_flag = False
        self.fuzzy_flag = False
        self.fuzzy_weights_flag = False
        self.fuzzy_weights_tresholds_flag = False
        self.window.enter.clicked.connect(MainAplication.run_final)
       
    def set_marking_initial(self, net, root, fuzzy, file_name, tree, weights, tresholds):
        dict_weights = {}
        dict_places = {}
        dict_transitions = {}

        for place in net.getPlaces():
            dict_places[place.label] = place.tokens
        for transition in net.getTransitions():
            dict_transitions[transition.getId()] = transition.label
        for i, arc in net.getMultiplicities().items():
            dict_weights[i] = arc

        entries = {}
        entries2 = {}
        entries3 = {}
        placesLabel = QtWidgets.QLabel("Miesta")
        placesLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.window.main.addWidget(placesLabel) 
     
        placesLayout = QtWidgets.QVBoxLayout()
        for i, key in enumerate(dict_places):
            placeLabel = QtWidgets.QLabel(key)
            placeLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            entry = QtWidgets.QLineEdit()
            entries[key] = entry
            okButton = QtWidgets.QPushButton("OK")
            okButton.clicked.connect(lambda: [set_marking(entries, net,1), delete_text(entries,1)])
            placeLayout = QtWidgets.QHBoxLayout()
            placeLayout.addWidget(placeLabel)
            placeLayout.addWidget(entry)
            placeLayout.addWidget(okButton)
            placesLayout.addLayout(placeLayout)
        
        self.window.main.addLayout(placesLayout)
        
        transitionsLabel = QtWidgets.QLabel("Prechody")
        transitionsLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.window.main.addWidget(transitionsLabel)

        transitionsLayout = QtWidgets.QVBoxLayout()
        for i, key in enumerate(dict_transitions):
            transitionLabel = QtWidgets.QLabel(dict_transitions[key])
            transitionLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            if tresholds:
                entry2 = QtWidgets.QLineEdit()
                entries2[key] = entry2
                okButton2 = QtWidgets.QPushButton("OK")
                okButton2.clicked.connect(lambda: [set_tresholds(entries2, net,1), delete_text(entries2,1)])
                transitionLayout = QtWidgets.QHBoxLayout()
                transitionLayout.addWidget(transitionLabel)
                transitionLayout.addWidget(entry2)
                transitionLayout.addWidget(okButton2)
                transitionsLayout.addLayout(transitionLayout)
            else:
                transitionsLayout.addWidget(transitionLabel)
        self.window.main.addLayout(transitionsLayout)
        
        if weights or tresholds:
            weightsLabel = QtWidgets.QLabel("Váhy")
            weightsLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
            self.window.main.addWidget(weightsLabel)

            weightsLayout = QtWidgets.QVBoxLayout()
            for i, key in enumerate(dict_weights):
                weightLabel = QtWidgets.QLabel(dict_weights[key])
                weightLabel.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                entry3 = QtWidgets.QLineEdit()
                entries3[key] = entry3
                okButton3 = QtWidgets.QPushButton("OK")
                okButton3.clicked.connect(lambda: [set_weights(entries3, net,1), delete_text(entries3,1)])
                weightLayout = QtWidgets.QHBoxLayout()
                weightLayout.addWidget(weightLabel)
                weightLayout.addWidget(entry3)
                weightLayout.addWidget(okButton3)
                weightsLayout.addLayout(weightLayout)
            self.window.main.addLayout(weightsLayout)

        l = 0
        for rank in root.iter('place'):
            for value in rank:
                if value.tag == 'tokens':
                    if fuzzy:
                        value.text = str(float(net.M0[l]))
                    else:
                        value.text = str(int(net.M0[l]))
                    l += 1
        if fuzzy:
            if tresholds:
                self.fuzzy_weights_tresholds_flag = True
                if len(net.tresholds) == 0:
                    net.tresholds = [0 for _ in range(len(dict_transitions))]
                    # create new tag to xml to each transition
                    for i, rank in enumerate(root.iter('transition')):
                        # addd new tag
                        new_tag = ET.SubElement(rank, 'treshold')
                        # add value to new tag
                        new_tag.text = str(net.tresholds[i])
                else:
                    # create new tag to xml to each transition
                    for i, rank in enumerate(root.iter('transition')):
                        # addd new tag
                        new_tag = ET.SubElement(rank, 'treshold')
                        # add value to new tag
                        new_tag.text = str(net.tresholds[i])
            if weights:
                self.fuzzy_weights_flag = True
                l = 0
                if len(net.multiplicities) == 0:
                    net.multiplicities = [1 for _ in range(len(dict_weights))]
                    for rank in root.iter('arc'):
                        for value in rank:
                            if value.tag == 'multiplicity':
                                value.text = str(net.multiplicities[l])
                                l += 1
                else:
                    for rank in root.iter('arc'):
                        for value in rank:
                            if value.tag == 'multiplicity':
                                value.text = str(net.multiplicities[l])
                                l += 1
            else:
                self.fuzzy_flag = True
        else:
            self.logical_flag = True

        tree.write(file_name + "_marking.xml",
                encoding="UTF-8", xml_declaration=True)
        print("Počiatočné označkovanie: ", net.M0)
        

def delete_text(entries,flag):
    for _, value in entries.items():
        if flag == 0:
            value.delete(0, 'end')
        else:
            value.clear()


def set_marking(entries,net, flag):
    if flag == 0:
        net.M0 = [float(value.get()) if value.get() != '' else 0.0 for _,value in entries.items()]
    else:
        net.M0 = [float(value.text()) if value.text() != '' else 0.0 for _,value in entries.items()]


def set_tresholds(entries,net, flag):
    if flag == 0:
        net.tresholds = [float(value.get()) if value.get() != '' else 0.0 for _,value in entries.items()]
    else:
        net.tresholds = [float(value.text()) if value.text() != '' else 0.0 for _,value in entries.items()]
    

def set_weights(entries,net, flag):
    if flag == 0:
        net.multiplicities = [float(value.get()) if value.get() != '' else 1.0 for _,value in entries.items()]
    else:
        net.multiplicities = [float(value.text()) if value.text() != '' else 1.0 for _,value in entries.items()]


def set_initial_marking(net, root, fuzzy, file_name,tree, weights,tresholds):
    dict_weights = {}
    dict_places = {}
    dict_transitions = {}

    for place in net.getPlaces():
        dict_places[place.label] = place.tokens
    for transition in net.getTransitions():
        dict_transitions[transition.getId()] = transition.label
    for i, arc in net.getMultiplicities().items():
        dict_weights[i] = arc
    # make entry for each key in dict_places in tkinter
    win = tk.Tk()
    win.geometry("600x400")
    mainFrame = ttk.Frame(win)
    mainFrame.grid(column=1, row=1)

    entries = {}
    entries2 = {}
    entries3 = {}
    ttk.Label(mainFrame, text="Miesta", font=(
        "Arial", 11, 'bold')).grid(column=1, row=1)
    for i, key in enumerate(dict_places):
        ttk.Label(mainFrame, text=key, font=(
            "Arial", 10, 'bold')).grid(column=1, row=i + 2)
        
        entry = ttk.Entry(mainFrame, width=10)
    
        entries[key] = entry
        entries[key].grid(column=2, row=i + 2)
        # clear entry field after button click
        ttk.Button(mainFrame, text="OK", command=lambda: [set_marking(entries,net,0), delete_text(entries,0)], width=5).grid(column=3,
                                                                                                          row=i + 2)
    ttk.Label(mainFrame, text="Prechody", font=(
        "Arial", 11, 'bold')).grid(column=4, row=1)
    for i, key in enumerate(dict_transitions):
        ttk.Label(mainFrame, text=dict_transitions[key], font=(
            "Arial", 10, 'bold')).grid(column=4, row=i + 2)
        if tresholds:
            entries2[key] = ttk.Entry(mainFrame, width=10)
            entries2[key].grid(column=5, row=i + 2)
            ttk.Button(mainFrame, text="OK", command=lambda: [set_tresholds(entries2,net,0), delete_text(entries2,0)], width=5).grid(column=6,
                                                                                                     row=i + 2)
    if weights or tresholds:
        ttk.Label(mainFrame, text="Váhy", font=(
            "Arial", 11, 'bold')).grid(column=7, row=1)
        for i, key in enumerate(dict_weights):
            ttk.Label(mainFrame, text=dict_weights[key], font=(
                "Arial", 10, 'bold')).grid(column=7, row=i + 2)
            entries3[key] = ttk.Entry(mainFrame, width=10)
            entries3[key].grid(column=8, row=i + 2)
            ttk.Button(mainFrame, text="OK", command=lambda: [set_weights(entries3,net,0), delete_text(entries3,0)], width=5).grid(column=9,
                                                                                                     row=i + 2)
    win.mainloop()
    l = 0
    for rank in root.iter('place'):
        for value in rank:
            if value.tag == 'tokens':
                if fuzzy:
                    value.text = str(float(net.M0[l]))
                else:
                    value.text = str(int(net.M0[l]))
                l += 1
    if fuzzy:
        if tresholds:
            if len(net.tresholds) == 0:
                net.tresholds = [0 for _ in range(len(dict_transitions))]
                 # create new tag to xml to each transition
                for i, rank in enumerate(root.iter('transition')):
                    # addd new tag
                    new_tag = ET.SubElement(rank, 'treshold')
                    # add value to new tag
                    new_tag.text = str(net.tresholds[i])
            else:
                # create new tag to xml to each transition
                for i, rank in enumerate(root.iter('transition')):
                    # addd new tag
                    new_tag = ET.SubElement(rank, 'treshold')
                    # add value to new tag
                    new_tag.text = str(net.tresholds[i])
        if weights:
            l = 0
            if len(net.multiplicities) == 0:
                net.multiplicities = [1 for _ in range(len(dict_weights))]
                for rank in root.iter('arc'):
                    for value in rank:
                        if value.tag == 'multiplicity':
                            value.text = str(net.multiplicities[l])
                            l += 1
            else:
                for rank in root.iter('arc'):
                    for value in rank:
                        if value.tag == 'multiplicity':
                            value.text = str(net.multiplicities[l])
                            l += 1

    tree.write(file_name + "_marking.xml",
               encoding="UTF-8", xml_declaration=True)
    print("Počiatočné označkovanie: ", net.M0)


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


        self.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\icon.jpg'))
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Petri nets")
       
        #self.window.show()
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
        self.logical_flag = False
        self.fuzzy_flag = False
        self.fuzzy_weights_flag = False
        self.fuzzy_weights_tresholds_flag = False
        self.tree = None
        self.anotherWindow = AnotherWindow()
        #self.tree = None

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
            root = self.tree.getroot()
            if "fuzzy" in self.file_name:
                fuzzy = 1
            else:
                fuzzy = 0
            net = loading_data(self.file_name, fuzzy)
            if self.main_layout.comboBox.currentText() == "Logická Petriho sieť":
                self.logical_flag = True
                self.anotherWindow = AnotherWindow()
                self.anotherWindow.set_marking_initial(net, root, fuzzy, self.file_name.split('.')[0] + "_initial", self.tree,0,0)
                
                #set_initial_marking(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",tree,0,0)
       
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť":
                self.fuzzy_flag = True
                self.anotherWindow = AnotherWindow()
                self.anotherWindow.set_marking_initial(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",self.tree,0,0)
                
                #set_initial_marking(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",tree,0,0)

            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť s váhami pravidiel":
                self.fuzzy_weights_flag = True
                self.anotherWindow = AnotherWindow()
                self.anotherWindow.set_marking_initial(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",self.tree,1,0)
                
                #set_initial_marking(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",tree,1,0)
     
            elif self.main_layout.comboBox.currentText() == "Fuzzy Petriho sieť s váhami a prahmi pravidiel":
            
                self.anotherWindow.set_marking_initial(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",self.tree,1,1)
                #set_initial_marking(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",tree,1,1)
                self.TR = net.tresholds
                #self.fuzzy_weights_tresholds_flag = True
                #net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1)
                #self.run_fuzzy_with_weights_and_thresholds(net, tree, self.file_path)

        else:
            #self.tree = None
            dialog = QMessageBox(text="Nevybrali ste žiadny súbor")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed
    
    def run_final(self):
        if self.anotherWindow.logical_flag:
            net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 0)
            self.run_logical(net, self.tree, self.file_path)
        elif self.anotherWindow.fuzzy_flag:
            net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1)
            self.run_fuzzy(net, self.tree, self.file_path)
        elif self.anotherWindow.fuzzy_weights_flag:
            net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1) 
            self.run_fuzzy_with_weights(net, self.tree, self.file_path)
        elif self.anotherWindow.fuzzy_weights_tresholds_flag:
            net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", 1)
            self.run_fuzzy_with_weights_and_thresholds(net, self.tree, self.file_path)
    

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


    def draw_net(self, net,weights,thresholds):
        G = nx.DiGraph()
        edges = {}
        places = net.getPlaces()
        transitions = net.getTransitions()
        places_list = []
        tresholds_list = net.getThresholds()
        transitions_list = []
        for arc in net.getArcs():
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
        
        nx.draw_networkx_nodes(G, pos, transitions,
                                node_shape='s', node_color='#ff0000')
        nx.draw_networkx_labels(
                G, pos, labels={n: n.label for n in transitions}, font_size=6)
        
        if thresholds:
            nx.draw_networkx_labels(
                G, pos, labels={n: n for n in tresholds_list}, font_size=6)
        
        for l in pos:  # raise text positions
            pos[l][1] += 0.08  # probably small value enough
        nx.draw_networkx_labels(
            G, pos, labels={n: n.label for n in places}, font_size=6
        )
    
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
        plt.axis('off')
        #plt.show()
        path = './images/' + str(self.image_number) + '.png'
        fig.savefig(path)
        
        self.image_dict[self.image_number] = path
        print("path: ", path)
    
    def logical_petri_net(self,net, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.main_layout.marking.setText("( "+', '.join([str(int(elem)) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(int(elem)) for i,elem in enumerate(Wo)])+" )"
        
        nRows = len(net.getPlaces())
        nColumns = len(net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                            for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])

        # fill each matrix with the proper data
        for arc in net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (net.getPlaceById(sourceId) is not None) and (net.getTransitionById(destinationId) is not None):
                source = net.getPlaceById(sourceId)
                destination = net.getTransitionById(destinationId)
            elif (net.getTransitionById(sourceId) is not None) and (net.getPlaceById(destinationId) is not None):
                source = net.getTransitionById(sourceId)
                destination = net.getPlaceById(destinationId)

            if type(source) == Place:
                sourceIdInNetList = net.getPlaces().index(source)
                destinationIdInNetList = net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()

            if type(source) == Transition:
                sourceIdInNetList = net.getTransitions().index(source)
                destinationIdInNetList = net.getPlaces().index(destination)
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
            for place in net.getPlaces():
                place.tokens = Wk[net.getPlaces().index(place)]
                count_place += 1
                for arc in net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(net,0,0)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
        return net


    def fuzzy_petri_net(self, net, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.main_layout.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )"

        nRows = len(net.getPlaces())
        nColumns = len(net.getTransitions())
        inputMatrix = np.array([[0 for _ in range(nColumns)]
                            for _ in range(nRows)])
        outputMatrix = np.array([[0 for _ in range(nColumns)]
                                for _ in range(nRows)])
        # fill each matrix with the proper data
        for arc in net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (net.getPlaceById(sourceId) is not None) and (net.getTransitionById(destinationId) is not None):
                source = net.getPlaceById(sourceId)
                destination = net.getTransitionById(destinationId)
            elif (net.getTransitionById(sourceId) is not None) and (net.getPlaceById(destinationId) is not None):
                source = net.getTransitionById(sourceId)
                destination = net.getPlaceById(destinationId)
            if type(source) == Place:
                sourceIdInNetList = net.getPlaces().index(source)
                destinationIdInNetList = net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()
            if type(source) == Transition:
                sourceIdInNetList = net.getTransitions().index(source)
                destinationIdInNetList = net.getPlaces().index(destination)
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
            for place in net.getPlaces():
                place.tokens = Wk[net.getPlaces().index(place)]
                count_place += 1
                for arc in net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(net,0,0)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
        return net
    
    def fuzzy_petri_net_with_weights(self, net, M):
        array_steps = []
        Wo = M[0].state
        self.main_layout.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )"

        nRows = len(net.getPlaces())
        nColumns = len(net.getTransitions())
        inputMatrix = np.array([[0.0 for _ in range(nColumns)]
                            for _ in range(nRows)])
        outputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])

        # fill each matrix with the proper data
        for arc in net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (net.getPlaceById(sourceId) is not None) and (net.getTransitionById(destinationId) is not None):
                source = net.getPlaceById(sourceId)
                destination = net.getTransitionById(destinationId)
            elif (net.getTransitionById(sourceId) is not None) and (net.getPlaceById(destinationId) is not None):
                source = net.getTransitionById(sourceId)
                destination = net.getPlaceById(destinationId)
            if type(source) == Place:
                sourceIdInNetList = net.getPlaces().index(source)
                destinationIdInNetList = net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()
            if type(source) == Transition:
                sourceIdInNetList = net.getTransitions().index(source)
                destinationIdInNetList = net.getPlaces().index(destination)
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
            for place in net.getPlaces():
                place.tokens = Wk[net.getPlaces().index(place)]
                count_place += 1
                for arc in net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(net,1,0)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
        return net


    def fuzzy_petri_net_with_weights_thresholds(self, net, M):
        array_steps = []
        Wo = M[0].state
        self.main_layout.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.main_layout.marking.adjustSize()
        self.actual_marking_dict[0] = "( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )"

        nRows = len(net.getPlaces())
        nColumns = len(net.getTransitions())
        inputMatrix = np.array([[0.0 for _ in range(nColumns)]
                            for _ in range(nRows)])
        outputMatrix = np.array([[0.0 for _ in range(nColumns)]
                                for _ in range(nRows)])

        # fill each matrix with the proper data
        for arc in net.getArcs():
            sourceId = arc.getSourceId()
            destinationId = arc.getDestinationId()
            source = None
            destination = None
            if (net.getPlaceById(sourceId) is not None) and (net.getTransitionById(destinationId) is not None):
                source = net.getPlaceById(sourceId)
                destination = net.getTransitionById(destinationId)
            elif (net.getTransitionById(sourceId) is not None) and (net.getPlaceById(destinationId) is not None):
                source = net.getTransitionById(sourceId)
                destination = net.getPlaceById(destinationId)
            if type(source) == Place:
                sourceIdInNetList = net.getPlaces().index(source)
                destinationIdInNetList = net.getTransitions().index(destination)
                inputMatrix[sourceIdInNetList,
                            destinationIdInNetList] = arc.getMultiplicity()
            if type(source) == Transition:
                sourceIdInNetList = net.getTransitions().index(source)
                destinationIdInNetList = net.getPlaces().index(destination)
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
                if negVo[i] >= self.TR[i]:
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
            for place in net.getPlaces():
                place.tokens = Wk[net.getPlaces().index(place)]
                count_place += 1
                for arc in net.getArcs():
                    if arc.getSourceId().__class__ == Place:
                        previous_place = net.getPlaceById(arc.getSourceId()).label
                    if arc.dest.name == place.name and changed_places[count_place - 1]:
                        result_string = previous_place, " -> ", arc.src.label, " -> ", arc.dest.name, " : ", place.tokens
                        array_steps.append(result_string)
                        print(result_string)
            if Wk != Wo:          
                self.step_dict[self.image_number-1] = array_steps
                array_steps = []
                actual_step_marking = "( "+', '.join([str(elem) for i,elem in enumerate(Wk)])+" )"
                self.actual_marking_dict[self.image_number-1] = actual_step_marking
                self.draw_net(net,1,1)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.main_layout.photo.setPixmap(pixmap.scaled(self.main_layout.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.main_layout.photo.setAlignment(QtCore.Qt.AlignCenter)
        return net
    

    def run_logical(self, net, tree, file_name):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(net)
        if M is not None:
            self.draw_net(net,0,0)
            self.image_number += 1
            net = self.logical_petri_net(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed
            

    def run_fuzzy(self, net, tree, file_name):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(net)
        if M is not None:
            self.draw_net(net,0,0)
            self.image_number += 1
            net = self.fuzzy_petri_net(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed


    def run_fuzzy_with_weights(self, net, tree, file_name):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(net)
        if M is not None:
            self.draw_net(net,1,0)
            self.image_number += 1
            net = self.fuzzy_petri_net_with_weights(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed

    def run_fuzzy_with_weights_and_thresholds(self, net, tree, file_name):
        self.image_number = 1
        self.image_dict = {}
        self.step_dict = {}
        files = glob.glob('./images/*')
        for f in files:
            os.remove(f)
        M = reachability(net)
        if M is not None:
            self.draw_net(net,1,1)
            self.image_number += 1
            net = self.fuzzy_petri_net_with_weights_thresholds(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainAplication()  
    window.show()
    sys.exit(app.exec())
    
