class Piui:
    def __init__(self, name):
        self.name = name
        self.item = self.name.upper()

    @property
    def item(self):
        return self.name.upper()