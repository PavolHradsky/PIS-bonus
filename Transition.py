from Item import Item
# inspired by https://github.com/Gmod4phun/PetriNetParser/blob/master/petrinetparser.py


class Transition:
    def __init__(self, name: str, label: str, weight: str, treshold: str):
        self.name = name
        self.label = label
        self.weight = weight
        self.treshold = treshold

    def __str__(self):
        return f'Transition(Name: {self.name})'

    def getId(self):
        return self.name

    def getWeight(self):
        return self.weight

    def getTreshold(self):
        return self.treshold
