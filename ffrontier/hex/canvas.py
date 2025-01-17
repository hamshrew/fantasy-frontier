'''A canvas to display a grid of hexes'''
from typing import Tuple
from dataclasses import dataclass

import pygame

from ffrontier.hex import tileutils
from ffrontier.managers.asset_manager import AssetManager


@dataclass
class CanvasState:
    '''State of the canvas'''
    max_size: Tuple[int, int]
    offset: Tuple[int, int]
    vp_pos: Tuple[int, int]
    highlighted_tile: Tuple[int, int] | None
    is_dragging: bool


class HexCanvas:
    '''A canvas to display a grid of hexes'''
    assets: AssetManager
    tilemap: tileutils.TileMap
    canvas_state: CanvasState

    def __init__(self, assets: AssetManager, tilemap: tileutils.TileMap):
        '''Initialize the HexCanvas'''
        self.assets = assets
        self.tilemap = tilemap
        max_size = tilemap.get_map_size()
        max_size = (max_size[0] * tilemap.max_tile_size, max_size[1] * tilemap.max_tile_size)
        # Multiply the max size by the size of the hex to get the width and height,
        #  then center the screen on the viewport
        self.canvas_state = CanvasState(max_size=max_size,
                                        offset=(max_size[0] // 2, max_size[1] // 2),
                                        vp_pos=(max_size[0] // 2, max_size[1] // 2),
                                        highlighted_tile=None,
                                        is_dragging=False)

    # Make some accessors for the canvas state
    @property
    def max_size(self) -> Tuple[int, int]:
        '''Get the max size of the canvas'''
        return self.canvas_state.max_size

    @property
    def offset(self) -> Tuple[int, int]:
        '''Get the offset of the canvas'''
        return self.canvas_state.offset

    @property
    def vp_pos(self) -> Tuple[int, int]:
        '''Get the position of the viewport'''
        return self.canvas_state.vp_pos

    @vp_pos.setter
    def vp_pos(self, pos: Tuple[int, int]):
        '''Set the position of the viewport'''
        self.canvas_state.vp_pos = pos

    @property
    def highlighted_tile(self) -> Tuple[int, int] | None:
        '''Get the highlighted tile'''
        return self.canvas_state.highlighted_tile

    @highlighted_tile.setter
    def highlighted_tile(self, tile: Tuple[int, int] | None):
        '''Set the highlighted tile'''
        self.canvas_state.highlighted_tile = tile

    @property
    def is_dragging(self) -> bool:
        '''Get the dragging state'''
        return self.canvas_state.is_dragging

    @is_dragging.setter
    def is_dragging(self, dragging: bool):
        '''Set the dragging state'''
        self.canvas_state.is_dragging = dragging

    def draw(self, surface: pygame.Surface, rect_size: Tuple[int, int]):
        '''Draw the hex canvas'''
        surface.fill((0, 0, 0, 0))
        for tile in self.tilemap.tiles.values():
            # Don't draw tiles outside the rectangle
            tcenter = tile.center
            tcenter = (tcenter[0] + self.offset[0] + self.vp_pos[0],
                       tcenter[1] + self.offset[1] + self.vp_pos[1])
            if ((0 > tcenter[0] + tile.radius) or (tcenter[0] - tile.radius > rect_size[0]) or
                    (0 > tcenter[1] + tile.radius) or (tcenter[1] - tile.radius > rect_size[1])):
                continue
            tile.draw(surface, self.offset, tile.hex_info.color)
            if (self.highlighted_tile and
                    (tile.hex_info.q, tile.hex_info.r) == self.highlighted_tile):
                tile.draw(surface, self.offset, (0, 0, 255, 128), 0)
        # Draw a white line around the edge of the entire canvas
        pygame.draw.rect(surface, (255, 255, 255),
                         (1, 1, self.max_size[0] - 1, self.max_size[1] - 1), 1)

    def get_tile(self, x: int, y: int):
        '''Get the tile at the specified coordinates'''
        return self.tilemap.tiles[(x, y)]

    def handle_command(self, command: str, surface: pygame.Surface, rect_size: Tuple[int, int]):
        '''Handle a preprocessed(probably mapped) command'''
        if command == 'zoom_in':
            if self.assets.scale == self.assets.max_scale:
                return
            self.assets.scale_up()
        elif command == 'zoom_out':
            if self.assets.scale == self.assets.min_scale:
                return
            self.assets.scale_down()
        elif command == 'camera_up':
            self.vp_pos = (self.vp_pos[0], self.vp_pos[1] + 10)
        elif command == 'camera_down':
            self.vp_pos = (self.vp_pos[0], self.vp_pos[1] - 10)
        elif command == 'camera_left':
            self.vp_pos = (self.vp_pos[0] + 10, self.vp_pos[1])
        elif command == 'camera_right':
            self.vp_pos = (self.vp_pos[0] - 10, self.vp_pos[1])

        self._clamp_vp_pos(rect_size)
        self.draw(surface, rect_size)

    def _clamp_vp_pos(self, rect_size: Tuple[int, int]) -> None:
        '''Clamp the viewport position to the edges of the viewport rect'''
        clamp_x = rect_size[0] - self.max_size[0]
        clamp_y = rect_size[1] - self.max_size[1]

        # Separate logic for clamping in each dimension
        if clamp_x >= 0:  # Surface smaller or equal to viewport (width)
            vp_x = max(0, min(self.vp_pos[0], clamp_x))
        else:  # Surface larger than viewport (width)
            vp_x = max(clamp_x, min(self.vp_pos[0], 0))

        if clamp_y >= 0:  # Surface smaller or equal to viewport (height)
            vp_y = max(0, min(self.vp_pos[1], clamp_y))
        else:  # Surface larger than viewport (height)
            vp_y = max(clamp_y, min(self.vp_pos[1], 0))

        self.vp_pos = (vp_x, vp_y)

    # pylint: disable=too-many-branches
    def handle_event(self, event: pygame.event.Event,
                     surface: pygame.Surface,
                     rect_size: Tuple[int, int]):
        '''Handle events for the hex canvas'''
        # highlight the tile that the mouse is over
        if event.type == pygame.MOUSEMOTION:
            if self.canvas_state.is_dragging:
                self.vp_pos = (self.vp_pos[0] + event.rel[0],
                               self.vp_pos[1] + event.rel[1])

                self._clamp_vp_pos(rect_size)
                self.draw(surface, rect_size)
            else:
                highlighted_tile = self.tilemap.check_collision(event.pos,
                                                                (self.offset[0] +
                                                                 self.vp_pos[0],
                                                                 self.offset[1] +
                                                                 self.vp_pos[1]))
                if highlighted_tile != self.highlighted_tile:
                    self.highlighted_tile = highlighted_tile
                    self.draw(surface, rect_size)
            return

        if event.type == pygame.MOUSEWHEEL:
            # zoom in and out
            if event.y > 0:
                # Assets already has a check to limit zoom, but check again here to prevent
                # unneeded rendering.
                if self.assets.scale == self.assets.max_scale:
                    return
                self.assets.scale_up()
            else:
                if self.assets.scale == self.assets.min_scale:
                    return
                self.assets.scale_down()
            self.draw(surface, rect_size)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.canvas_state.is_dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.canvas_state.is_dragging:
                    self.canvas_state.is_dragging = False
