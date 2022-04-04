from typing import List
import networkx as nx
import matplotlib.pyplot as plt

from PetriNet import PetriNet
from functions import read_xml
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


    for m in M:
        print(m.state)
    for h in H:
        print(h[0], h[1].name, h[2])

    G = nx.DiGraph()
    edges = {}

    for m in M:
        G.add_node(str(m.state))

    print(G.nodes())

    for h in H:
        G.add_edge(str(h[0]), str(h[2]))
        edges[(str(h[0]), str(h[2]))] = h[1].name

    print(G.edges())

    pos = nx.circular_layout(G)
    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=200, alpha=0.8,
        labels={node: node for node in G.nodes()}
    )
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edges,
        font_color='red',
    )
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
