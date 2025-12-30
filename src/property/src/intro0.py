class Piui:
    def __init__(self, name):
        self.name = name

    @property
    def item(self):
        return self.name.upper()