from typing import List

from PetriNet import PetriNet
from functions import read_xml
from Rpn import Rpn
import Relh



def main():
    # places, transitions, arcs = read_xml(input("file name: "))
    places, transitions, arcs = read_xml("test.xml")
    net: PetriNet = PetriNet(places, transitions, arcs)
    # print(net.M0)
    # m1 = net.step(transitions[0], net.M0)
    # print(m1)
    # m2 = net.step(transitions[1], m1)
    # print(m2)

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



if __name__ == '__main__':
    main()
