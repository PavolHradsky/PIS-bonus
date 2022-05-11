from typing import List
import networkx as nx
import matplotlib.pyplot as plt

from PetriNet import PetriNet
from functions import read_xml, list_is_greater
from Rpn import Rpn


def main():
    # places, transitions, arcs = read_xml(input("file name: "))
    places, transitions, arcs = read_xml("test.xml")
    net: PetriNet = PetriNet(places, transitions, arcs)

    M: List[Rpn] = []
    H: List = []

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
                    return 0
    print("Siet je ohranicena")
    print("Postup:")
    for h in H:
        print(h[0], h[1].name, h[2])

    G = nx.DiGraph()
    edges = {}

    for m in M:
        G.add_node(str(m.state))

    for h in H:
        G.add_edge(str(h[0]), str(h[2]))
        edges[(str(h[0]), str(h[2]))] = h[1].name

    pos = nx.circular_layout(G)
    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=200, alpha=0.8,
        labels={node: f'm{i}' for i, node in enumerate(G.nodes())}
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


if __name__ == '__main__':
    main()
