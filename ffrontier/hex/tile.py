'''Tile-related classes and functions'''
from typing import Dict, Tuple, List

import pygame

from ffrontier.hex import hexgrid
from ffrontier.game.maphandler import MapHandler
import ffrontier.managers.asset_manager as am


# exceptions
class IncompleteGridError(Exception):
    '''Raised when a grid is incomplete'''


class DuplicateTileError(Exception):
    '''Raised when a tile coordinate is duplicated'''


class Tile:
    '''Tile information'''
    hex_info: hexgrid.HexInfo
    asset_manager: am.AssetManager
    image: str
    center: Tuple[int, int]
    points: List[Tuple[int, int]]

    def __init__(self, hex_info: hexgrid.HexInfo,
                 image: str,
                 asset_manager: am.AssetManager):
        self.hex_info = hex_info
        self.asset_manager = asset_manager
        self.image = image

    def draw(self, surface: pygame.Surface,
             offset: Tuple[int, int] = (0, 0),
             color: Tuple[int, int, int] = (255, 255, 255)):
        '''Draw the tile'''
        radius = self.asset_manager.scale // 2
        hexgrid.draw_hex(surface, self.hex_info,
                         radius, offset, color)
        scaled_image: pygame.Surface = self.asset_manager.get_scaled_image(self.image)
        # Place the image so that it overlaps the hexagon
        # get the center of the hexagon and recalculate to the top left corner
        center = hexgrid.axial_to_pixel(self.hex_info, radius, offset)
        surface.blit(scaled_image, (center[0] - scaled_image.get_width() / 2,
                                    center[1] - scaled_image.get_height() / 2))

    @property
    def coordinates(self) -> Tuple[int, int]:
        '''Get the coordinates of the tile'''
        return self.hex_info.q, self.hex_info.r

    @property
    def cube_coordinates(self) -> Tuple[int, int, int]:
        '''Get the cube coordinates of the tile'''
        return hexgrid.axial_to_cube(self.hex_info)


class TileMap:
    '''Map of tiles'''
    tiles: Dict[Tuple[int, int], Tile]
    offset: Tuple[int, int]

    def __init__(self,
                 asset_manager: am.AssetManager,
                 map_file: str,
                 flat: bool = False):
        self.tiles = {}
        self.asset_manager = asset_manager
        # load the map data and construct tiles
        map_handler = MapHandler(map_file)
        for tile_data in map_handler.map_data:
            info = hexgrid.HexInfo(int(tile_data['coordinates'][0]),
                                   int(tile_data['coordinates'][1]),
                                   flat,
                                   0)
            tile = Tile(info,
                        str(tile_data['terrain']),
                        asset_manager)
            self.add_tile(tile)
        self._validate_map()

    def add_tile(self, tile: Tile):
        '''Add a tile to the map'''
        # Check if the tile is already in the map
        if (tile.hex_info.q, tile.hex_info.r) in self.tiles:
            raise DuplicateTileError(f'Tile ({tile.hex_info.q}, {tile.hex_info.r}) already exists')
        self.tiles[(tile.hex_info.q, tile.hex_info.r)] = tile

    def draw(self, surface: pygame.Surface):
        '''Draw the map'''
        for tile in self.tiles.values():
            tile.draw(surface)

    def _validate_map(self):
        '''Validate the map data'''
        # This looks at tile coordinates and makes sure they have no holes

        # Calculate min/max bounds for q and r from the tile dictionary
        min_q = min(coord[0] for coord in self.tiles)
        max_q = max(coord[0] for coord in self.tiles)
        min_r = min(coord[1] for coord in self.tiles)
        max_r = max(coord[1] for coord in self.tiles)

        # Generate all expected coordinates based on the bounds
        expected_coords = set()
        for q in range(min_q, max_q + 1):
            for r in range(min_r, max_r + 1):
                # Ensure the coordinates are valid in axial space (q + r + s = 0)
                s = -q - r
                if s in range(min_q, max_q + 1):  # Check if s is within valid bounds
                    expected_coords.add((q, r))

        # Find missing coordinates
        missing_coords = expected_coords - self.tiles.keys()
        if missing_coords:
            raise IncompleteGridError(f"Holes detected: Missing coordinates {missing_coords}")
