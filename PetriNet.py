from typing import List

from Place import Place
from Transition import Transition
from Arc import Arc
from Role import Role


class PetriNet:
    def __init__(self, places: List[Place], transitions: List[Transition], arcs: List[Arc], roles: List[Role]):
        """
        class PetriNet represents petri net in form PN=(P, T, F, W, M0) where
            P is set of places
            T is set of transitions
            F is set of arcs in form (item.name + item.name)
            W is set of weights of arcs, represented as objects Arc
                with attributes src, dest and multiplicity, where src and dest
                are objects of transitions and places
            M0 is initial marking of places represented as tuple of integers
                where every int stands for count of tokens in place with same index
        :param places: list of places
        :param transitions: list of transitions
        :param arcs: list of arcs
        """
        self.P: List[Place] = places
        self.T: List[Transition] = transitions
        self.R: List[Role] = roles
        self.W: List[Arc] = arcs
        self.M0: List[int] = [i.tokens for i in places]
        self.Wk_final = []
        self.tresholds = []
        self.weights = []
        self.inputMatrix = None
        self.outputMatrix = None
        self.incidenceMatrix = None

    def getPlaces(self):
        return self.P

    def getTransitions(self):
        return self.T

    def getArcs(self):
        return self.W

    def getWeights(self):
        return self.weights

    def getRoles(self):
        return self.R

    def final_Wk(self):
        return self.Wk_final

    def getThresholds(self):
        return self.tresholds

    def getPlaceById(self, id):
        for obj in self.getPlaces():
            if obj.getId() == id.name:

                return obj
        return None

    def getTransitionById(self, id):
        for obj in self.getTransitions():
            if obj.getId() == id.name:
                return obj
        return None

    def step(self, tr: Transition, m: List[int]):
        """
        method step is calculating new marking from given marking (if its possible)
        after using given transition
        :param tr: transition to use
        :param m: initial marking for this step (for example M0)
        :return: new marking or None, if transition cant be used
        """
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
