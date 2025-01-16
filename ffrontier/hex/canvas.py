'''A canvas to display a grid of hexes'''
from typing import Tuple

import pygame

from ffrontier.hex import tileutils
from ffrontier.managers.asset_manager import AssetManager


class HexCanvas:
    '''A canvas to display a grid of hexes'''
    assets: AssetManager
    tilemap: tileutils.TileMap
    max_size: Tuple[int, int]
    offset: Tuple[int, int]
    highlighted_tile: Tuple[int, int] | None

    def __init__(self, assets: AssetManager, tilemap: tileutils.TileMap):
        '''Initialize the HexCanvas'''
        self.assets = assets
        self.tilemap = tilemap
        max_size = tilemap.get_map_size()
        # Multiply the max size by the size of the hex to get the width and height
        self.max_size = (max_size[0] * tileutils.MAX_SIZE, max_size[1] * tileutils.MAX_SIZE)
        # Center the hex grid on the screen
        self.offset = (self.max_size[0] // 2, self.max_size[1] // 2)
        self.highlighted_tile = None

    def draw(self, surface: pygame.Surface):
        '''Draw the hex canvas'''
        for tile in self.tilemap.tiles.values():
            if (self.highlighted_tile and
                    (tile.hex_info.q, tile.hex_info.r) == self.highlighted_tile):
                tile.draw(surface, self.offset, tile.hex_info.color)
                tile.draw(surface, self.offset, (0, 0, 255, 128), 0)
            else:
                tile.draw(surface, self.offset, tile.hex_info.color)

    def get_tile(self, x: int, y: int):
        '''Get the tile at the specified coordinates'''
        return self.tilemap.tiles[(x, y)]

    def handle_event(self, event: pygame.event.Event, surface: pygame.Surface):
        '''Handle events for the hex canvas'''
        # highlight the tile that the mouse is over
        if event.type == pygame.MOUSEMOTION:
            self.highlighted_tile = self.tilemap.check_collision(event.pos, self.offset)
            surface.fill((0, 0, 0, 0))
            self.draw(surface)
