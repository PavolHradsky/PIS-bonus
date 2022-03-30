from Item import Item


class Transition(Item):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return f'Transition(Name: {self.name})'
