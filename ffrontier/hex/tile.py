'''Tile-related classes and functions'''
from dataclasses import dataclass

import pygame

import ffrontier.hex.hexgrid as hexgrid
import ffrontier.managers.asset_manager as asset_manager


@dataclass
class Tile:
    hex_info: hexgrid.HexInfo

    '''Tile information'''
    def __init__(self, q: int, r: int,
                 flat: bool, border: int,
                 image: str,
                 asset_manager: asset_manager.AssetManager):
        self.hex_info = hexgrid.HexInfo(q, r, flat, border)
        self.asset_manager = asset_manager

    def draw(self, surface: pygame.Surface, radius, color):
        '''Draw the tile'''
        hexgrid.draw_hex(surface, self.hex_info, radius, color)
        scaled_image = self.asset_manager.get_scaled_image(self.image)
        # Place the image so that it overlaps the hexagon
        # get the center of the hexagon and recalculate to the top left corner
        center = hexgrid.axial_to_pixel(self.hex_info, radius)
        surface.blit(scaled_image, (center[0] - scaled_image.get_width() / 2,
                                    center[1] - scaled_image.get_height() / 2))
