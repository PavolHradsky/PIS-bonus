from Item import Item


class Role:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label: str = label

    def __str__(self):
        return f'Place(Name: {self.name}, Labels: {self.label})'
