from Item import Item

# inspired by https://github.com/Gmod4phun/PetriNetParser/blob/master/petrinetparser.py


class Arc:
    def __init__(self, id, src: Item, dest: Item, multiplicity):
        self.id = id
        self.src: Item = src
        self.dest: Item = dest
        self.multiplicity: float = multiplicity

    def getId(self):
        return self.id

    def getSourceId(self):
        return self.src

    def getDestinationId(self):

        return self.dest

    def getMultiplicity(self):
        return self.multiplicity

    def __str__(self):
        return f'Arc(Src: {self.src.name}, Dest: {self.dest.name}, Multiplicity: {self.multiplicity})'
