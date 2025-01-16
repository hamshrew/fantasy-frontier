'''Utility functions for parsing various bits of data.'''
from typing import Tuple


def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    '''Convert a hex color to RGBA, with optional alpha.'''
    hex_color = hex_color.lstrip('#')
    # Check for correct length
    if len(hex_color) not in (6, 8):
        raise ValueError(f'Invalid hex color: {hex_color}')

    # Check that the hex color is valid
    if not all(c in '0123456789ABCDEFabcdef' for c in hex_color):
        raise ValueError(f'Invalid hex color: {hex_color}')

    # Convert to RGBA
    if len(hex_color) == 6:
        r, g, b, a = tuple([int(hex_color[i:i+2], 16) for i in (0, 2, 4)] + [255])
    else:
        r, g, b, a = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
    return (r, g, b, a)
