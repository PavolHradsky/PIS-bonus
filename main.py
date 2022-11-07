from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from PetriNet import PetriNet
from Place import Place
from Transition import Transition
from functions import read_xml, list_is_greater
from Rpn import Rpn


def loading_data(name_file):
    places, transitions, arcs, role = read_xml(name_file)
    net: PetriNet = PetriNet(places, transitions, arcs, role)
    return net


def net_solvable(net):
    M: List[Rpn] = []
    H: List = []
    M.append(Rpn(net.M0))
    G = nx.DiGraph()
    edges = {}
    places = net.getPlaces()
    transitions = net.getTransitions()
    for arc in net.getArcs():
        G.add_edge(arc.getSourceId(), arc.getDestinationId())
        edges[(arc.getSourceId(), arc.getDestinationId())] = arc.getMultiplicity()
    pos = nx.circular_layout(G)
    plt.figure()
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=1000, node_color='white', font_size=10,
            labels={node: f'{place.name}' for i, node in enumerate(G.nodes()) for j, place in enumerate(places) if i == j}
            )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
    plt.axis('off')
    plt.show()


""""
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
    print("Postup:")
     
    for h in H:
        print(h[0], h[1].name, h[2])

    G = nx.DiGraph()
    edges = {}
    places = net.getPlaces()

    for m in M:
        G.add_node(str(m.state))

    for h in H:
        G.add_edge(str(h[0]), str(h[2]))
        edges[(str(h[0]), str(h[2]))] = h[1].label

    pos = nx.circular_layout(G)
    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=200, alpha=0.8,
        labels={node: f'{place.name}' for i, node in enumerate(G.nodes()) for j, place in enumerate(places) if i == j}
    )
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edges,
        font_color='red',
    )
    plt.axis('off')
    plt.show()

    print("Znackovanie:")
    for i, node in enumerate(G.nodes()):
        print(f'm{i}: {node}')
    return M
    """

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
    print(" M neg", neg_Wo)
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
        Vo = transponse_array @ neg_Wo
        for i in range(len(Vo)):
            if Vo[i] > 1:
                Vo[i] = 1.0
        Uo = [round(abs(1 - i), 2) for i in Vo]

        Wk = [((outputMatrix @ Uo)[i] or Wo[i]) for i in range(len(Wo))]
        print("Wk: ", Wk)


if __name__ == '__main__':
    net = loading_data(input("Zadaj nazov suboru: ") + ".xml")
    option = input("Vyber z možností: \n 1. Logická Petriho sieť \n 2. Fuzzy Petriho sieť \n")
    if option == "1":
        M = net_solvable(net)
        if M is not None:
            logical_petri_net(net, M)
        else:
            print("Siet je neohranicena")
    elif option == "2":
        M = net_solvable(net)
        if M is not None:
            fuzzy_petri_net(net, M)
        else:
            print("Siet je neohranicena")
    else:
        print("Zle zadana moznost")
