import pyasge


class Maptile:
    def __init__(self):
        self.properties = {'cost': 0}
        self.sprite = pyasge.Sprite()

    def load(self, filename: str) -> None:
        self.sprite.loadTexture(filename)
