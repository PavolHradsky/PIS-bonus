from Item import Item

# inspired by https://github.com/Gmod4phun/PetriNetParser/blob/master/petrinetparser.py


class Place:
    def __init__(self, id, tokens: float, name: str):
        self.id = id
        self.tokens: float = tokens
        self.name: str = name
        self.label: str = name

    def getId(self):
        return self.name

    def __str__(self):
        return f'Place(Name: {self.id}, Tokens: {self.tokens}, Labels: {self.name})'
