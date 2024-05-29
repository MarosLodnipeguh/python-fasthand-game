class ClickEvent:
    def __init__(self, name, index):

        self.name = name # "choose card" "put card" (on a chosen gamestack), "draw card"
        self.index = index

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index