class OllivanderShop:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item.update_quality()

    def getItems(self):
        return self.items


class Interface:
    def update_quality(self):
        pass
