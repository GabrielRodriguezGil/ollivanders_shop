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


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return (
            f"Item(name='{self.name}', sell_in={self.sell_in}, quality={self.quality})"
        )


class NormalItem(Interface, Item):
    def __init__(self, name, sell_in, quality):
        Item.__init__(self, name, sell_in, quality)

    def get_quality(self):
        return self.quality

    def update_quality(self):
        if self.quality == 0:
            self._set_sell_in()
        elif self.sell_in > 0:
            self._set_sell_in()
            self.quality -= 1
        else:
            self._set_sell_in()
            self.quality -= 2

    def _set_sell_in(self):
        self.sell_in -= 1
