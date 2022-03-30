from Item import Item


class Place(Item):
    def __init__(self, name: str, tokens: int):
        super().__init__(name)
        self.tokens: int = tokens

    def __str__(self):
        return f'Place(Name: {self.name}, Tokens: {self.tokens})'
