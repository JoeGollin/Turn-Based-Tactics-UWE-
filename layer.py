import pyasge
from tile import Maptile


class MapLayer:
    def __init__(self):
        self.name = ""
        self.tiles = [
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()],
            [Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(),
             Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile(), Maptile()]]

        self.initTilePos()

    def initTilePos(self) -> None:
        y_pos = 0
        for row in self.tiles:
            x_pos = 0
            for tile in row:
                tile.sprite.y = y_pos
                tile.sprite.x = x_pos
                x_pos = x_pos + 64
            y_pos = y_pos + 64

    def render(self, renderer: pyasge.Renderer) -> None:
        for row in self.tiles:
            for tile in row:
                if tile.sprite.texture:
                    renderer.render(tile.sprite)
