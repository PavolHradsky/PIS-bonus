from PetriNet import PetriNet
from functions import read_xml


def main():
    places, transitions, arcs = read_xml()
    net: PetriNet = PetriNet(places, transitions, arcs)
    m1 = net.step(transitions[0], net.M0)
    m2 = net.step(transitions[3], m1)
    m3 = net.step(transitions[5], m2)
    m4 = net.step(transitions[2], m3)
    print(m4)


if __name__ == '__main__':
    main()
