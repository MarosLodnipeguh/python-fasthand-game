class GameEvent:
    def __init__(self, type, index):
        self.type = type
        self.index = index

    def get_type(self):
        return self.type

    def get_index(self):
        return self.index