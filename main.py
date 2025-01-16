'''Main file for the game. This is where the game loop will be.'''
# Importing built-in libraries
import math

# Importing third-party libraries
import pygame
import pygame_gui

# Importing local files
from ffrontier.managers.ui_manager import UIVariableManager
from ffrontier.ui.city_ui import CityUI
from ffrontier.game.gamestate import GameState
from ffrontier.managers.config_manager import ConfigManager
from ffrontier.hex.canvas import HexCanvas
from ffrontier.managers.asset_manager import AssetManager
from ffrontier.hex import hexgrid
from ffrontier.hex import tileutils

# Constants


# Messing around to test things
# Hex stuff
def axial_to_pixel(q, r, size):
    y = size * math.sqrt(3) * (r + q/2)
    x = size * 3/2 * q
    return (x, y)


def draw_hex(surface, center, size, color):
    points = [
        (center[0] + size * math.cos(math.radians(60 * i)),
         center[1] + size * math.sin(math.radians(60 * i)))
        for i in range(6)
    ]

    pygame.draw.polygon(surface, color, points, 2)


def axial_to_pixel_p(q, r, size):
    x = round(size * math.sqrt(3) * (q + r/2))
    y = round(size * 3/2 * r)
    return (x, y)


def draw_hex_p(surface, center, size, color):
    points = [
        (center[0] + size * math.cos(math.radians(60 * i - 30)),
         center[1] + size * math.sin(math.radians(60 * i - 30)))
        for i in range(6)
    ]

    pygame.draw.polygon(surface, color, points, 1)


# Check if the file is being run directly and not imported.
# If it is being run directly, run the game loop.
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Fantasy Frontier')
    clock = pygame.time.Clock()

    # Initialize the UI manager
    manager = pygame_gui.UIManager((800, 600))

    # Initialize the UI variable manager
    ui_manager = UIVariableManager()

    # Assets
    asset_manager = AssetManager('ffrontier/assets/configs/city_assets.json',
                                 mask=hexgrid.mask_image_flat)

    # Load the map data
    tilemap = tileutils.TileMap(asset_manager, 'ffrontier/assets/maps/city/basic1.ffm')

    # Initialize the HexCanvas class

    canvas = HexCanvas(asset_manager, tilemap)

    # Initialize the CityUI class
    city_ui = CityUI(manager, ui_manager, canvas)

    running = True
    size = 20

    # Load the configuration file
    config_manager = ConfigManager('config.ini')

    # Initialize the game state
    gstate = GameState(config_manager)

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                running = False
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_PLUS or
                                                  (event.key == pygame.K_EQUALS and
                                                   pygame.key.get_mods() & pygame.KMOD_SHIFT))):
                size += 5
                if size > 100:
                    size = 100
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_MINUS or
                                                  (event.key == pygame.K_MINUS))):
                size -= 5
                if size < 5:
                    size = 5

            manager.process_events(event)
            city_ui.handle_event(event, gstate)

        manager.update(time_delta)
        city_ui.draw(screen)

        pygame.display.flip()

    pygame.quit()
