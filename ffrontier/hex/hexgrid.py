'''Handles all hex grid related operations'''
from dataclasses import dataclass
import math

import pygame


@dataclass
class HexInfo:
    '''Stores information about a hexagon to simplify parameters'''
    q: int
    r: int
    flat: bool
    border: int


def _axial_to_pixel_f(q: int, r: int, radius: int) -> tuple[int, int]:
    y = round(radius * math.sqrt(3) * (r + q / 2))
    x = round(radius * 3 / 2 * q)
    return x, y


def _axial_to_pixel_p(q: int, r: int, radius: int) -> tuple[int, int]:
    x = round(radius * math.sqrt(3) * (q + r / 2))
    y = round(radius * 3 / 2 * r)
    return x, y


def axial_to_pixel(hex_info: HexInfo, radius: int) -> tuple[int, int]:
    if hex_info.flat:
        return _axial_to_pixel_f(hex_info.q, hex_info.r, radius)
    else:
        return _axial_to_pixel_p(hex_info.q, hex_info.r, radius)


def axial_to_cube(hex_info: HexInfo) -> tuple[int, int, int]:
    x = hex_info.q
    y = hex_info.r
    z = -x - y
    return x, y, z


def draw_hex(surface: pygame.Surface,
             hex_info: HexInfo,
             radius: int,
             color: tuple[int, int, int]) -> None:
    '''Draw a hexagon on the surface'''
    # Get the center of the hexagon from the HexInfo and run it through axial to pixel
    center = axial_to_pixel(hex_info, radius)
    points = [
        (center[0] + radius * math.cos(math.radians(60 * i - (0 if hex_info.flat else 30))),
         center[1] + radius * math.sin(math.radians(60 * i - (0 if hex_info.flat else 30))))
        for i in range(6)
    ]

    pygame.draw.polygon(surface, color, points, hex_info.border)


def mask_image(image: pygame.Surface, flat: bool) -> pygame.Surface:
    '''Mask an image into a hexagon with transparent corners'''
    mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    center = mask.get_rect().center
    radius = mask.get_width() // 2 if flat else mask.get_height() // 2
    print(flat, center, radius)
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