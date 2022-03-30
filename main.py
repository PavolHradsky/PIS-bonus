import xml.etree.ElementTree as ET
from typing import List


class Item:
    def __init__(self, name):
        self.name: str = name


class Transition(Item):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return f'Transition(Name: {self.name})'


class Place(Item):
    def __init__(self, name: str, tokens: int):
        super().__init__(name)
        self.tokens: int = tokens

    def __str__(self):
        return f'Place(Name: {self.name}, Tokens: {self.tokens})'


class Arc:
    def __init__(self, src: Item, dest: Item, multiplicity: int):
        self.src: Item = src
        self.dest: Item = dest
        self.multiplicity: int = multiplicity

    def __str__(self):
        return f'Arc(Src: {self.src.name}, Dest: {self.dest.name}, Multiplicity: {self.multiplicity})'


class PetriNet:
    def __init__(self, places: List[Place], transitions: List[Transition], arcs: List[Arc]):
        self.P: List[Place] = places
        self.T: List[Transition] = transitions
        self.F: List[str] = [i.src.name + i.dest.name for i in arcs]
        self.W: List[Arc] = arcs
        self.M0: List[int] = [i.tokens for i in places]

    def step(self, tr: Transition, m: List[int]):
        m_next = m.copy()
        for w in self.W:
            if w.dest == tr:
                if not m[self.P.index(w.src)] >= w.multiplicity:
                    return None
                m_next[self.P.index(w.src)] -= w.multiplicity
        for w in self.W:
            if w.src == tr:
                m_next[self.P.index(w.dest)] += w.multiplicity
        if m != m_next:
            return m_next
        return None


def get_item_by_name(transitions: List[Transition], places: List[Place], name: str) -> Item:
    for item in transitions:
        if item.name == name:
            return item

    for item in places:
        if item.name == name:
            return item


def read_xml():
    tree = ET.parse('test.xml')
    root = tree.getroot()

    transitions: List[Transition] = []
    places: List[Place] = []
    arcs: List[Arc] = []

    for transition in root.findall("transition"):
        transitions.append(Transition(transition.find("id").text))

    for place in root.findall("place"):
        places.append(Place(place.find("id").text, int(place.find("tokens").text)))

    for arc in root.findall("arc"):
        arcs.append(
            Arc(get_item_by_name(transitions, places, arc.find("sourceId").text),
                get_item_by_name(transitions, places, arc.find("destinationId").text),
                int(arc.find("multiplicity").text)
                ))

    return places, transitions, arcs


def main():
    places, transitions, arcs = read_xml()
    net: PetriNet = PetriNet(places, transitions, arcs)
    m1 = net.step(transitions[0], net.M0)
    m2 = net.step(transitions[3], m1)
    m3 = net.step(transitions[5], m2)
    m4 = net.step(transitions[2], m3)
    pass


if __name__ == '__main__':
    main()
