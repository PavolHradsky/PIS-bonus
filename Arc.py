from Item import Item


class Arc:
    def __init__(self, src: Item, dest: Item, multiplicity: int):
        self.src: Item = src
        self.dest: Item = dest
        self.multiplicity: int = multiplicity

    def __str__(self):
        return f'Arc(Src: {self.src.name}, Dest: {self.dest.name}, Multiplicity: {self.multiplicity})'
