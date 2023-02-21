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
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile, QIODevice
from PyQt6.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QMessageBox, QLabel, QListWidget, QVBoxLayout
import os
import glob
from PySide6.QtGui import QPixmap, QImage

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


def set_marking(entries, marking,net):
    for key, value in entries.items():
        marking[key] = value.get()
    net.M0 = [float(i) if i != '' else 0.0 for i in marking.values()]


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
        self.window.setFixedSize(800, 600)
        self.window.setWindowTitle("Initial marking")
        self.ui.close()
        self.window.enter.clicked.connect(self.window.close)

    # rewrite  set_initial_marking to anotherWindow in pyqt6 and add to another window
    def set_marking_initial(self,net, root, fuzzy, file_name, tree):
        dict_roles = {}
        dict_places = {}
        dict_transitions = {}
        for place in net.getPlaces():
            dict_places[place.label] = place.tokens
        for transition in net.getTransitions():
            dict_transitions[transition.getId()] = transition.label
        for role in net.getRoles():
            dict_roles[role.getId()] = role.name
        self.window.show()
        # make entry label for each key in dict_places in window
        entries = {}
        self.window.label_2.setText("Miesta")
        for i, key in enumerate(dict_places):
            self.window.label_2.setText(key)
            entries[key] = self.window.lineEdit
            self.window.enter.clicked.connect(lambda: [set_marking(entries, dict_places,net), delete_text(entries)])

        # list also tranistions
        self.window.label_3.setText("Prechody")
        for i, key in enumerate(dict_transitions):
            self.window.label_3.setText(key)
    
    def delete_text(self, entries):
        for key, value in entries.items():
            value.delete(0, 'end')
    
    def set_marking(self, entries, marking,net):
        for key, value in entries.items():
            marking[key] = value.get()
        net.M0 = [float(i) if i != '' else 0.0 for i in marking.values()]

        l = 0
        for rank in root.iter('place'):
            for value in rank:
                if value.tag == 'tokens':
                    if fuzzy:
                        value.text = str(float(net.M0[l]))
                    else:
                        value.text = str(int(net.M0[l]))
                    l += 1

        tree.write(file_name + "_marking.xml",
                encoding="UTF-8", xml_declaration=True)
        print("Počiatočné označkovanie: ", net.M0)

def delete_text(entries):
    for key, value in entries.items():
        value.delete(0, 'end')

def set_initial_marking(net, root, fuzzy, file_name,tree):
    dict_roles = {}
    dict_places = {}
    dict_transitions = {}
    for place in net.getPlaces():
        dict_places[place.label] = place.tokens
    for transition in net.getTransitions():
        dict_transitions[transition.getId()] = transition.label
    for role in net.getRoles():
        dict_roles[role.getId()] = role.name
    # make entry for each key in dict_places in tkinter
    win = tk.Tk()
    win.geometry("600x400")
    mainFrame = ttk.Frame(win)
    mainFrame.grid(column=1, row=1)

    entries = {}
    ttk.Label(mainFrame, text="Miesta", font=(
        "Arial", 11, 'bold')).grid(column=1, row=1)
    for i, key in enumerate(dict_places):
        ttk.Label(mainFrame, text=key, font=(
            "Arial", 10, 'bold')).grid(column=1, row=i + 2)
        entries[key] = ttk.Entry(mainFrame, width=10)
        entries[key].grid(column=2, row=i + 2)
        # clear entry field after button click
        ttk.Button(mainFrame, text="OK", command=lambda: [set_marking(entries, dict_places,net), delete_text(entries)], width=5).grid(column=3,
                                                                                                          row=i + 2)
    ttk.Label(mainFrame, text="Prechody", font=(
        "Arial", 11, 'bold')).grid(column=4, row=1)
    for i, key in enumerate(dict_transitions):
        ttk.Label(mainFrame, text=dict_transitions[key], font=(
            "Arial", 10, 'bold')).grid(column=4, row=i + 2)

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

    tree.write(file_name + "_marking.xml",
               encoding="UTF-8", xml_declaration=True)
    print("Počiatočné označkovanie: ", net.M0)


class MainWindow(QtWidgets.QMainWindow):
    loader = QUiLoader()
    file_path = None
    file_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = QFile(".\gui\mainwindow.ui")
        self.ui.open(QFile.ReadOnly)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.window = self.loader.load(self.ui)
        self.window.setWindowIcon(QtGui.QIcon('C:\\Users\\peter\\OneDrive\\Počítač\\Github\\PIS-bonus\\icon.jpg'))
        self.ui.close()
        self.window.setGeometry(200, 200, 800, 600)
        self.window.setFixedSize(800, 600)
        self.window.setWindowTitle("Petri nets")
        self.window.show()
        self.image_number = 1

        # bind events to buttons
        self.window.loadFile.clicked.connect(self.open_dialog)
        # comboBox
        self.window.comboBox.addItems(["Logická Petriho sieť", 
                                       "Fuzzy Petriho sieť", 
                                       "Fuzzy Petriho sieť s váhami pravidiel", 
                                       "Fuzzy Petriho sieť s váhami a prahmi pravidiel"])
        self.window.comboBox.currentIndexChanged.connect(self.combo_changed)
        self.window.runButton.clicked.connect(self.run)
        self.window.prevButton.clicked.connect(self.prev)
        self.window.nextButton.clicked.connect(self.next)
        self.window.clearAll.clicked.connect(self.clear)
        self.window.clearAll.setEnabled(False)
        self.image_dict = {}
        self.step_dict = {}
        self.actual_marking_dict = {}
        self.k = 0
        if self.image_number == 1:
            self.window.prevButton.setEnabled(False)
        
       

    def open_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'c:\\', "XML files (*.xml)")
        if fname[0]:
            self.file_name = re.search(r'[^/\\&\?]+\.\w+$', fname[0]).group(0)
            self.window.fileNameLabel.setText(self.file_name)
            self.file_path = fname[0]
        else:
            self.window.fileNameLabel.setText("No file selected")
            self.file_path = None
            self.file_name = None
        self.window.clearAll.setEnabled(True)

    def combo_changed(self):
        print(self.window.comboBox.currentText())

    def run(self):
        if self.file_path:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            if "fuzzy" in self.file_name:
                fuzzy = 1
            else:
                fuzzy = 0
            net = loading_data(self.file_name, fuzzy)
            w = AnotherWindow()
            w.set_marking_initial(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",tree)
            set_initial_marking(net, root, fuzzy, self.file_name.split('.')[0] + "_initial",tree)
            net = loading_data(self.file_name.split('.')[0] + "_initial_marking.xml", fuzzy)

            if self.window.comboBox.currentText() == "Logická Petriho sieť":
                self.run_logical(net, tree, self.file_path)
            elif self.window.comboBox.currentText() == "Fuzzy Petriho sieť":
                self.run_fuzzy(net, tree, self.file_path)
            elif self.window.comboBox.currentText() == "Fuzzy Petriho sieť s váhami pravidiel":
                self.run_fuzzy_with_weights(net, tree, self.file_path)
            elif self.window.comboBox.currentText() == "Fuzzy Petriho sieť s váhami a prahmi pravidiel":
                self.run_fuzzy_with_weights_and_thresholds(net, tree, self.file_path)
        else:
            self.tree = None
            dialog = QMessageBox(text="Nevybrali ste žiadny súbor")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed


    def prev(self):
        if self.image_number > 1:
            #   set button active
            self.window.nextButton.setEnabled(True)
            if self.image_number == 2:
                self.window.prevButton.setEnabled(False)
            self.image_number -= 1
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            self.window.photo.setPixmap(pixmap.scaled(self.window.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.window.actual_marking.setText(self.actual_marking_dict[self.image_number-1])
            self.window.actual_marking.adjustSize()
            for i in range(0, len(self.step_dict[self.image_number])):
                self.window.steps.takeItem(self.image_number+1-i-self.k)
                if i > 0:
                    self.k += 1
        else:
            # set button inactive
            self.window.prevButton.setEnabled(False)
            self.image_number = 1


    def next(self):
        self.k = 0
        if self.image_number < len(self.image_dict):
            # set button active
            self.window.prevButton.setEnabled(True)
            if self.image_number == len(self.image_dict)-1:
                self.window.nextButton.setEnabled(False)
            self.image_number += 1
            prem = QImage(self.image_dict[self.image_number])
            pixmap = QPixmap.fromImage(prem)
            self.window.photo.setPixmap(pixmap.scaled(self.window.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.window.actual_marking.setText(self.actual_marking_dict[self.image_number-1])
            self.window.actual_marking.adjustSize()
            for i in self.step_dict[self.image_number-1]:
                self.window.steps.addItem(str(i))
        else:
            # set button inactive
            self.window.nextButton.setEnabled(False)
            self.image_number -=1


    def clear(self):
        self.window.fileNameLabel.setText("No file selected")
        if self.window.steps != None:
            self.window.steps.clear()
        if self.window.photo != None:
            self.window.photo.clear()
        if self.window.actual_marking != None:
            self.window.actual_marking.clear()
        if self.window.marking != None:
            self.window.marking.clear()
        self.window.prevButton.setEnabled(False)
        self.window.nextButton.setEnabled(True)
        self.window.clearAll.setEnabled(False)


    def draw_net(self, net):
        G = nx.DiGraph()
        edges = {}
        places = net.getPlaces()
        transitions = net.getTransitions()
        places_list = []
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
            G, pos, labels={n: n.label for n in transitions}, font_size=6
        )
        
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
        self.window.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.window.marking.adjustSize()
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
                self.draw_net(net)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.window.photo.setPixmap(pixmap.scaled(self.window.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        return net


    def fuzzy_petri_net(self, net, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.window.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.window.marking.adjustSize()
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
                self.draw_net(net)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.window.photo.setPixmap(pixmap.scaled(self.window.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        return net
    
    def fuzzy_petri_net_with_weights(self, net, M):
        array_steps = []
        Wo = M[0].state
        # print("Počiatočné ohodnotenie: ", Wo)
        self.window.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.window.marking.adjustSize()
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
                self.draw_net(net)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.window.photo.setPixmap(pixmap.scaled(self.window.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        return net


    def fuzzy_petri_net_with_weights_thresholds(self, net, M):
        array_steps = []
        Wo = M[0].state
        TR = [0.0, 0.8, 0.2, 0.0, 0.0, 0.0]
        # print("Počiatočné označkovanie: ", M[0].state)
        self.window.marking.setText("( "+', '.join([str(elem) for i,elem in enumerate(Wo)])+" )")
        self.window.marking.adjustSize()
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
                if negVo[i] >= TR[i]:
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
                self.draw_net(net)
                self.image_number += 1
                print("Wk: ", Wk)
        self.image_number = 1
        prem = QImage(self.image_dict[self.image_number])
        pixmap = QPixmap.fromImage(prem)
        self.window.photo.setPixmap(pixmap.scaled(self.window.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
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
            self.draw_net(net)
            self.image_number += 1
            net = self.logical_petri_net(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            #self.draw_net(net)
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
            self.draw_net(net)
            self.image_number += 1
            #print(self.image_number)
            net = self.fuzzy_petri_net(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            #print(self.image_number)
            #self.draw_net(net)
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
            self.draw_net(net)
            self.image_number += 1
            net = self.fuzzy_petri_net_with_weights(net, M)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            #self.draw_net(net)
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
            image_number = 1
            self.draw_net(net,image_number)
            image_number +=1
            net = self.fuzzy_petri_net_with_weights_thresholds(net, M, image_number)
            tree.write(file_name.split('.')[
                        0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            #self.draw_net(net,image_number)
        else:
            dialog = QMessageBox(text="Siet je neohranicena")
            dialog.setWindowTitle("Message Dialog")
            ret = dialog.exec()   # Stores the return value for the button pressed

def get(input):
    text = input.text()
    print(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()  
    
    sys.exit(app.exec())
    
