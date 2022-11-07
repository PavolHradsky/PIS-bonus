from Item import Item


class Transition:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label

    def __str__(self):
        return f'Transition(Name: {self.name})'

    def getId(self):
        return self.name
