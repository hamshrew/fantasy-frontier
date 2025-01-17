'''Handles all hex grid related operations'''
from dataclasses import dataclass
from typing import Tuple, List
import math

import pygame


@dataclass
class HexInfo:
    '''Stores information about a hexagon to simplify parameters'''
    q: int
    r: int
    flat: bool
    border: int
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)

    def collides(self, x: int, y: int, radius: int,
                 offset: Tuple[int, int] = (0, 0)) -> bool:
        '''Check if a point is inside the hexagon'''
        center = axial_to_pixel(self, radius, offset)
        point = (x, y)
        # See if the x and y are within the hexagon
        dist = math.dist(point, center)
        if dist > radius:
            return False
        # Flat-topped: vertices at 0°, 60°, 120°, etc.
        # Pointy-topped: vertices at 30°, 90°, 150°, etc.
        vertices = calc_points(center, radius, self.flat)

        for i in range(6):
            nvert = vertices[(i + 1) % 6]  # Next vertex (wrap around)
            # Edge vector
            edge_vect = (nvert[0] - vertices[i][0], nvert[1] - vertices[i][1])
            # Vector from vertex to point
            point_vect = (x - vertices[i][0], y - vertices[i][1])
            # Cross product
            cross = edge_vect[0] * point_vect[1] - edge_vect[1] * point_vect[0]
            if cross < 0:
                return False

        return True


def _axial_to_pixel_f(q: int, r: int, radius: int,
                      offset: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    y = round(radius * math.sqrt(3) * (r + q / 2)) + offset[1]
    x = round(radius * 3 / 2 * q) + offset[0]
    return x, y


def _axial_to_pixel_p(q: int, r: int, radius: int,
                      offset: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    x = round(radius * math.sqrt(3) * (q + r / 2)) + offset[0]
    y = round(radius * 3 / 2 * r) + offset[1]
    return x, y


def axial_to_pixel(hex_info: HexInfo, radius: int,
                   offset: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    '''Convert axial coordinates to pixel coordinates'''
    if hex_info.flat:
        return _axial_to_pixel_f(hex_info.q, hex_info.r, radius, offset)
    return _axial_to_pixel_p(hex_info.q, hex_info.r, radius, offset)


def axial_to_cube(hex_info: HexInfo) -> Tuple[int, int, int]:
    '''Convert axial coordinates to cube coordinates'''
    x = hex_info.q
    y = hex_info.r
    z = -x - y
    return x, y, z


def get_distance(hex1: HexInfo, hex2: HexInfo) -> int:
    '''Get the distance between two hexagons'''
    cube1 = axial_to_cube(hex1)
    cube2 = axial_to_cube(hex2)
    return (abs(cube1[0] - cube2[0]) + abs(cube1[1] - cube2[1]) + abs(cube1[2] - cube2[2])) // 2


def get_cube_distance(cube1: Tuple[int, int, int], cube2: Tuple[int, int, int]) -> int:
    '''Get the distance between two hexagons'''
    return (abs(cube1[0] - cube2[0]) + abs(cube1[1] - cube2[1]) + abs(cube1[2] - cube2[2])) // 2


def calc_points(center: Tuple[int, int], radius: int, flat: bool) -> List[Tuple[float, float]]:
    '''Calculate the points of a hexagon'''
    return [
        (center[0] + radius * math.cos(math.radians(60 * i - (0 if flat else 30))),
         center[1] + radius * math.sin(math.radians(60 * i - (0 if flat else 30))))
        for i in range(6)
    ]


# pylint: disable=too-many-arguments, too-many-positional-arguments
def draw_hex(surface: pygame.Surface,
             hex_info: HexInfo,
             radius: int,
             offset: Tuple[int, int] = (0, 0),
             color: Tuple[int, int, int, int] = (255, 255, 255, 255),
             border: int = 0) -> None:
    '''Draw a hexagon on the surface'''
    # Get the center of the hexagon from the HexInfo and run it through axial to pixel
    center = axial_to_pixel(hex_info, radius, offset)
    # Make a surface to draw the hexagon on
    hex_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    points = calc_points((radius, radius), radius, hex_info.flat)
    pygame.draw.polygon(hex_surface, color, points, border)
    surface.blit(hex_surface,
                 (center[0] - radius, center[1] - radius))


def mask_image(image: pygame.Surface, flat: bool) -> pygame.Surface:
    '''Mask an image into a hexagon with transparent corners'''
    mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    center = mask.get_rect().center
    radius = mask.get_width() // 2 if flat else mask.get_height() // 2
    points = [
        (center[0] + radius * math.cos(math.radians(60 * i - (0 if flat else 30))),
         center[1] + radius * math.sin(math.radians(60 * i - (0 if flat else 30))))
        for i in range(6)
        ]
    pygame.draw.polygon(mask, (255, 255, 255, 255), points, 0)
    masked_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    masked_image.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
    masked_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return masked_image


def mask_image_flat(image: pygame.Surface) -> pygame.Surface:
    '''Mask an image into a flat-topped hexagon with transparent corners'''
    return mask_image(image, True)


def mask_image_pointy(image: pygame.Surface) -> pygame.Surface:
    '''Mask an image into a pointy-topped hexagon with transparent corners'''
    return mask_image(image, False)
