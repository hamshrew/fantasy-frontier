'''Tile-related classes and functions'''
from typing import Dict, Tuple, List

import pygame

from ffrontier.hex import hexgrid
from ffrontier.game.maphandler import MapHandler
import ffrontier.managers.asset_manager as am


# Constants
MAX_SIZE = 100


# exceptions
class IncompleteGridError(Exception):
    '''Raised when a grid is incomplete'''


class DuplicateTileError(Exception):
    '''Raised when a tile coordinate is duplicated'''


class Layer:
    '''A Layer for a tile, containing the image string and various properties like transparency'''
    image: str
    alpha: int

    def __init__(self, image: str, alpha: int = 255):
        self.image = image
        self.alpha = alpha
        if alpha < 0 or alpha > 255:
            raise ValueError('Alpha must be between 0 and 255')

    @staticmethod
    def from_dict(layer_data: Dict[str, str]) -> 'Layer':
        '''Create a Layer from a dictionary'''
        return Layer(layer_data['image'], int(layer_data.get('alpha', 255)))

    def blend(self, surface: pygame.Surface, assets: am.AssetManager):
        '''Blends the layer onto a surface'''
        image = assets.get_scaled_image(self.image)
        image.set_alpha(self.alpha)
        surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)


class Tile:
    '''Tile information'''
    hex_info: hexgrid.HexInfo
    asset_manager: am.AssetManager
    images: List[Layer]

    def __init__(self, hex_info: hexgrid.HexInfo,
                 images: List[Layer],
                 asset_manager: am.AssetManager):
        self.hex_info = hex_info
        self.asset_manager = asset_manager
        self.images = images

    @property
    def center(self) -> Tuple[int, int]:
        '''Get the center of the tile'''
        return hexgrid.axial_to_pixel(self.hex_info, self.asset_manager.scale // 2)

    @property
    def radius(self) -> int:
        '''Get the radius of the tile'''
        return self.asset_manager.scale // 2

    def draw(self, surface: pygame.Surface,
             offset: Tuple[int, int] = (0, 0),
             color: Tuple[int, int, int, int] = (255, 255, 255, 255),
             border: int | None = None):
        '''Draw the tile'''
        radius = self.asset_manager.scale // 2

        if len(self.images) > 0:
            # Create a surface to draw the image on
            image = pygame.Surface((self.asset_manager.scale,
                                    self.asset_manager.scale),
                                   pygame.SRCALPHA)

            for layer in self.images:
                layer.blend(image, self.asset_manager)

            # Place the image so that it overlaps the hexagon
            # get the center of the hexagon and recalculate to the top left corner
            center = hexgrid.axial_to_pixel(self.hex_info, radius, offset)
            surface.blit(image, (center[0] - image.get_width() / 2,
                                 center[1] - image.get_height() / 2),
                         special_flags=pygame.BLEND_RGBA_MAX)

        hexgrid.draw_hex(surface, self.hex_info,
                         radius, offset, color,
                         border if border is not None else self.hex_info.border)

    @property
    def coordinates(self) -> Tuple[int, int]:
        '''Get the coordinates of the tile'''
        return self.hex_info.q, self.hex_info.r

    @property
    def cube_coordinates(self) -> Tuple[int, int, int]:
        '''Get the cube coordinates of the tile'''
        return hexgrid.axial_to_cube(self.hex_info)

    def collides(self, x: int, y: int, radius: int, offset: Tuple[int, int] = (0, 0)) -> bool:
        '''Check if a point collides with the tile'''
        return self.hex_info.collides(x, y, radius, offset)


class TileMap:
    '''Map of tiles'''
    tiles: Dict[Tuple[int, int], Tile]
    offset: Tuple[int, int]

    def __init__(self,
                 asset_manager: am.AssetManager,
                 map_file: str):
        self.tiles = {}
        self.asset_manager = asset_manager
        # load the map data and construct tiles
        map_handler = MapHandler(map_file)
        for tile_data in map_handler.map_data:
            info = hexgrid.HexInfo(int(tile_data['coordinates'][0]),
                                   int(tile_data['coordinates'][1]),
                                   map_handler.flat,
                                   int(tile_data['border']),
                                   color=tile_data['color'])

            layer_list = [Layer.from_dict(layer) for layer in tile_data.get('layers', [])]

            tile = Tile(info,
                        layer_list,
                        asset_manager)
            self.add_tile(tile)
        self._validate_map()

    @property
    def max_tile_size(self) -> int:
        '''Get the maximum size of the tiles'''
        return self.asset_manager.max_scale

    def get_map_size(self) -> Tuple[int, int]:
        '''Get the size of the map'''
        min_q = min(coord[0] for coord in self.tiles)
        max_q = max(coord[0] for coord in self.tiles)
        min_r = min(coord[1] for coord in self.tiles)
        max_r = max(coord[1] for coord in self.tiles)
        return max_q - min_q + 1, max_r - min_r + 1

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

    def get_tile(self, coordinates: Tuple[int, int]) -> Tile:
        '''Get a tile by its coordinates'''
        return self.tiles[coordinates]

    def check_collision(self, point: Tuple[int, int],
                        offset: Tuple[int, int] = (0, 0)) -> Tuple[int, int] | None:
        '''Check if a point collides with a tile'''
        for tile in self.tiles.values():
            if tile.hex_info.collides(point[0], point[1], self.asset_manager.scale // 2, offset):
                return tile.coordinates
        return None

    def _validate_map(self):
        '''Validate the map data'''
        # This looks at tile coordinates and makes sure they have no holes

        # Find the radius of the map
        radius = 0
        for q, r in self.tiles.keys():  # pylint: disable=consider-iterating-dictionary
            radius = max(radius, hexgrid.get_cube_distance((0, 0, 0), (q, -q - r, r)))
        # Generate all expected coordinates based on the bounds
        expected_coords = set()
        for q in range(-radius, radius + 1):
            for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
                expected_coords.add((q, r))

        # Find missing coordinates
        missing_coords = expected_coords - self.tiles.keys()
        if missing_coords:
            raise IncompleteGridError(f"Holes detected: Missing coordinates {missing_coords}")
