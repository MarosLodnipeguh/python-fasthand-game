from models.event_names import EventName


class ClickEvent:
    def __init__(self, name: EventName, index: int = None):
        """
        Constructor of the ClickEvent class. Represents a click event on a card.
        :param name: name of the event. Described by the event_names.EventName enum.
        :param index: list index of the card's collection that was clicked. Default is None.
        """
        self.name = name
        self.index = index

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index
