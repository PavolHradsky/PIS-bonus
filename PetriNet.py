from typing import List

from Place import Place
from Transition import Transition
from Arc import Arc


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
