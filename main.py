from tkinter import ttk
from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PetriNet import PetriNet
from Place import Place
from Transition import Transition
from functions import read_xml, list_is_greater
from Rpn import Rpn
import tkinter as tk
from PySide6 import QtCore, QtWidgets, QtGui
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

def loading_data(name_file, fuzzy_flag):
    places, transitions, arcs, role = read_xml(name_file, fuzzy_flag)
    net: PetriNet = PetriNet(places, transitions, arcs, role)
    return net


def draw_net(net):
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
    plt.figure()
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
    plt.show()


def logical_petri_net(net, M):
    Wo = M[0].state
    print("Počiatočné ohodnotenie: ", Wo)
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
                    print(previous_place, " -> ", arc.src.label,
                          " -> ", arc.dest.name, " : ", place.tokens)
        draw_net(net)
        print("Wk: ", Wk)
    return net


def fuzzy_petri_net(net, M):
    Wo = M[0].state
    print("Počiatočné ohodnotenie: ", Wo)
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
                    print(previous_place, " -> ", arc.src.label,
                          " -> ", arc.dest.name, " : ", place.tokens)
        draw_net(net)
        print("Wk: ", Wk)
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


def set_marking(entries, marking):
    for key, value in entries.items():
        marking[key] = value.get()
    net.M0 = [float(i) if i != '' else 0.0 for i in marking.values()]


def clear_text(text):
    text.delete(1, tk.END)


def set_initial_marking(net, root, fuzzy, file_name):
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
        ttk.Button(mainFrame, text="OK", command=lambda: set_marking(entries, dict_places), width=5).grid(column=3,
                                                                                                          row=i + 2)
    ttk.Label(mainFrame, text="Prechody", font=(
        "Arial", 11, 'bold')).grid(column=4, row=1)
    for i, key in enumerate(dict_transitions):
        ttk.Label(mainFrame, text=dict_transitions[key], font=(
            "Arial", 10, 'bold')).grid(column=4, row=i + 2)
    # draw petri net into tkinter window
    figure1 = plt.Figure(figsize=(2, 2), dpi=100)

    canvas = FigureCanvasTkAgg(figure1, mainFrame)
    canvas.get_tk_widget().grid(column=5, row=10, rowspan=10)

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


def fuzzy_petri_net_with_weights(net, M):
    Wo = M[0].state
    print("Počiatočné ohodnotenie: ", Wo)
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
                    print(previous_place, " -> ", arc.src.label,
                          " -> ", arc.dest.name, " : ", place.tokens)
        print("Wk: ", Wk)
    return net


def fuzzy_petri_net_with_weights_thresholds(net, M):
    Wo = M[0].state
    TR = [0.0, 0.8, 0.2, 0.0, 0.0, 0.0]
    print("Počiatočné označkovanie: ", M[0].state)
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
                    print(previous_place, " -> ", arc.src.label,
                          " -> ", arc.dest.name, " : ", place.tokens)

        print("Wk: ", Wk)
    return net


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui_file_name = "mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()
    # add action to button
    window.pushButton.clicked.connect(lambda: loading_data(window.lineEdit.text(), window.checkBox.isChecked()))


    sys.exit(app.exec())
    #app = QtWidgets.QApplication([])

    #widget = MyWidget()
    #widget.resize(800, 600)
    #widget.show()

    #sys.exit(app.exec())
    file_name = input("Zadaj nazov suboru: ") + ".xml"
    tree = ET.parse(file_name)
    root = tree.getroot()
    if "fuzzy" in file_name:
        fuzzy = 1
    else:
        fuzzy = 0
    net = loading_data(file_name, fuzzy)
    set_initial_marking(net, root, fuzzy, file_name.split('.')[0] + "_initial")
    net = loading_data(file_name.split('.')[0] + "_initial_marking.xml", fuzzy)
    option = input(
        "Vyber z možností: \n 1. Logická Petriho sieť \n 2. Fuzzy Petriho sieť \n 3. Fuzzy Petriho sieť s váhami pravidiel\n"
        "4. Fuzzy Petriho sieť s váhami a prahmi pravidiel\n")
    if option == "1":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            net = logical_petri_net(net, M)
            tree.write(file_name.split('.')[
                       0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            draw_net(net)
        else:
            print("Siet je neohranicena")
    elif option == "2":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            net = fuzzy_petri_net(net, M)
            tree.write(file_name.split('.')[
                       0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            draw_net(net)
        else:
            print("Siet je neohranicena")
    elif option == "3":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            net = fuzzy_petri_net_with_weights(net, M)
            tree.write(file_name.split('.')[
                       0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            draw_net(net)
        else:
            print("Siet je neohranicena")
    elif option == "4":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            net = fuzzy_petri_net_with_weights_thresholds(net, M)
            tree.write(file_name.split('.')[
                       0] + "_final_marking.xml", encoding="UTF-8", xml_declaration=True)
            draw_net(net)
        else:
            print("Siet je neohranicena")
    else:
        print("Zle zadana moznost")
