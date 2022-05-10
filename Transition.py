from Item import Item


class Transition(Item):
    def __init__(self, name: str, label: str):
        super().__init__(name)
        self.label = label

    def __str__(self):
        return f'Transition(Name: {self.name})'
