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


def loading_data(name_file, fuzzy_flag):
    places, transitions, arcs, role = read_xml(name_file, fuzzy_flag)
    net: PetriNet = PetriNet(places, transitions, arcs, role)
    return net


def draw_net(net):
    G = nx.DiGraph()
    edges = {}
    places = net.getPlaces()
    transitions = net.getTransitions()
    names = []
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
        edges[(arc.getSourceId(), arc.getDestinationId())] = arc.getMultiplicity()
    pos = nx.circular_layout(G)
    plt.figure()
    nx.draw_networkx_nodes(G, pos, places_list)
    nx.draw_networkx_nodes(G, pos, transitions,
                           node_shape='s', node_color='#ff0000')
    nx.draw_networkx_labels(
        G, pos, labels={n: n.label for n in G}, font_size=8
    )
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
    plt.axis('off')
    plt.show()


def logical_petri_net(net, M):
    Wo = M[0].state
    nRows = len(net.getPlaces())
    nColumns = len(net.getTransitions())
    inputMatrix = np.array([[0 for _ in range(nColumns)] for _ in range(nRows)])
    outputMatrix = np.array([[0 for _ in range(nColumns)] for _ in range(nRows)])

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
            inputMatrix[sourceIdInNetList, destinationIdInNetList] = arc.getMultiplicity()

        if type(source) == Transition:
            sourceIdInNetList = net.getTransitions().index(source)
            destinationIdInNetList = net.getPlaces().index(destination)
            outputMatrix[destinationIdInNetList, sourceIdInNetList] = arc.getMultiplicity()
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
        Vo = transponse_array @ neg_Wo
        for i in range(len(Vo)):
            if Vo[i] > 1:
                Vo[i] = 1.0
        Uo = [abs(1 - i) for i in Vo]
        Wk = [int((outputMatrix @ Uo)[i] or Wo[i]) for i in range(len(Wo))]
        print("Wk: ", Wk)


def fuzzy_petri_net(net, M):
    Wo = M[0].state
    neg_Wo = [round(abs(1 - i), 2) for i in Wo]
    print("M0: ", M[0].state)
    nRows = len(net.getPlaces())
    nColumns = len(net.getTransitions())
    inputMatrix = np.array([[0 for _ in range(nColumns)] for _ in range(nRows)])
    outputMatrix = np.array([[0 for _ in range(nColumns)] for _ in range(nRows)])

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
            inputMatrix[sourceIdInNetList, destinationIdInNetList] = arc.getMultiplicity()
        if type(source) == Transition:
            sourceIdInNetList = net.getTransitions().index(source)
            destinationIdInNetList = net.getPlaces().index(destination)
            outputMatrix[destinationIdInNetList, sourceIdInNetList] = arc.getMultiplicity()
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
        print("Wk: ", Wk)


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
    print("Siet je ohranicena")
    return M


def set_marking(entries, marking):
    for key, value in entries.items():
        marking[key] = value.get()
    net.M0 = [float(i) if i != '' else 0.0 for i in marking.values()]


def clear_text(text):
    text.delete(1, tk.END)


def set_initial_marking(net, root, fuzzy):
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
    ttk.Label(mainFrame, text="Miesta", font=("Arial", 11, 'bold')).grid(column=1, row=1)
    for i, key in enumerate(dict_places):
        ttk.Label(mainFrame, text=key, font=("Arial", 10, 'bold')).grid(column=1, row=i + 2)
        entries[key] = ttk.Entry(mainFrame, width=10)
        entries[key].grid(column=2, row=i + 2)

        # clear entry field after button click
        ttk.Button(mainFrame, text="OK", command=lambda: set_marking(entries, dict_places), width=5).grid(column=3,
                                                                                                          row=i + 2)
    ttk.Label(mainFrame, text="Prechody", font=("Arial", 11, 'bold')).grid(column=4, row=1)
    for i, key in enumerate(dict_transitions):
        ttk.Label(mainFrame, text=dict_transitions[key], font=("Arial", 10, 'bold')).grid(column=4, row=i + 2)
    # draw petri net into tkinter window
    figure1 = plt.Figure(figsize=(2, 2), dpi=100)
    ax1 = figure1.add_subplot(111)
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

    tree.write('output.xml', encoding="UTF-8", xml_declaration=True)
    print("final", net.M0)


def fuzzy_petri_net_with_weights(net, M):
    Wo = M[0].state
    print("Wo: ", Wo)
    neg_Wo = [round(abs(1 - i), 2) for i in Wo]
    print("M0: ", M[0].state)
    print(" M neg", neg_Wo)
    nRows = len(net.getPlaces())
    nColumns = len(net.getTransitions())
    inputMatrix = np.array([[0.0 for _ in range(nColumns)] for _ in range(nRows)])
    outputMatrix = np.array([[0.0 for _ in range(nColumns)] for _ in range(nRows)])

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
            inputMatrix[sourceIdInNetList, destinationIdInNetList] = arc.getMultiplicity()
        if type(source) == Transition:
            sourceIdInNetList = net.getTransitions().index(source)
            destinationIdInNetList = net.getPlaces().index(destination)
            #print("destinationIdInNetList", destinationIdInNetList)
            outputMatrix[destinationIdInNetList, sourceIdInNetList] = arc.getMultiplicity()
    Wk = []
    i = 0
    while not np.array_equal(Wo, Wk):
        if i == 0:
            Wo = Wo
        else:
            Wo = Wk
        i += 1
        neg_Wo = [round(abs(1 - i), 2) for i in Wo]
        print("inputmatrix", inputMatrix)
        print("outputmatrix",outputMatrix)
        transponse_array = np.transpose(inputMatrix)
        print("transponse: ", transponse_array)
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
        print("Wk: ", Wk)


if __name__ == '__main__':
    #file_name = input("Zadaj nazov suboru: ") + ".xml"
    file_name = "fuzzy_model.xml"
    # net = loading_data("fuzzy_model.xml", 1)
    tree = ET.parse(file_name)
    root = tree.getroot()
    if "fuzzy" in file_name:
        fuzzy = 1
    else:
        fuzzy = 0
    net = loading_data(file_name, fuzzy)
    set_initial_marking(net, root, fuzzy)
    net = loading_data("output.xml", fuzzy)
    option = "3"
    #option = input(
    #    "Vyber z možností: \n 1. Logická Petriho sieť \n 2. Fuzzy Petriho sieť \n 3. Fuzzy Petriho sieť s váhami a prahmi pravidiel\n")
    if option == "1":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            logical_petri_net(net, M)
        else:
            print("Siet je neohranicena")
    elif option == "2":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            fuzzy_petri_net(net, M)
            draw_net(net)
        else:
            print("Siet je neohranicena")
    elif option == "3":
        M = reachability(net)
        if M is not None:
            draw_net(net)
            fuzzy_petri_net_with_weights(net, M)
            draw_net(net)
        else:
            print("Siet je neohranicena")
    else:
        print("Zle zadana moznost")
