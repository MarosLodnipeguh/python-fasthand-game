class ClickEvent:
    def __init__(self, name, index=None):
        self.name = name
        self.index = index

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index
