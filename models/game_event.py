class GameEvent:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index