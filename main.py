'''Main file for the game. This is where the game loop will be.'''
# Importing built-in libraries
from typing import Tuple

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
from ffrontier.hex import tileutils
from ffrontier.managers.controls_manager import ControlsManager

# Constants


# Check if the file is being run directly and not imported.
# If it is being run directly, run the game loop.
if __name__ == '__main__':
    pygame.init()

    # Load the configuration file
    cfg = ConfigManager('config.ini')

    resolution: Tuple[int, int] = (int(cfg.get("base", "width")),
                                   int(cfg.get("base", "height")))

    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Fantasy Frontier')
    clock = pygame.time.Clock()

    # Initialize the UI manager
    manager = pygame_gui.UIManager(resolution)

    # Initialize the UI variable manager
    ui_manager = UIVariableManager(resolution, (resolution[0] - 200, resolution[1]))

    # Assets
    asset_manager = AssetManager('ffrontier/assets/configs/city_assets.json')

    # Load the map data
    tilemap = tileutils.TileMap(asset_manager, 'ffrontier/assets/maps/city/basic1.ffm')

    # Initialize the HexCanvas class

    canvas = HexCanvas(asset_manager, tilemap)

    # Initialize controls manager
    controls = ControlsManager()

    # Temporarily set up some controls
    controls.add_context("city_ui")
    controls.add_mapping("city_ui", pygame.K_w, "camera_up", pygame.KEYDOWN)
    controls.add_mapping("city_ui", pygame.K_s, "camera_down", pygame.KEYDOWN)
    controls.add_mapping("city_ui", pygame.K_a, "camera_left", pygame.KEYDOWN)
    controls.add_mapping("city_ui", pygame.K_d, "camera_right", pygame.KEYDOWN)
    controls.add_mapping("city_ui", pygame.K_EQUALS, "zoom_in", pygame.KEYDOWN, pygame.KMOD_RSHIFT)
    controls.add_mapping("city_ui", pygame.K_EQUALS, "zoom_in", pygame.KEYDOWN, pygame.KMOD_LSHIFT)
    controls.add_mapping("city_ui", pygame.K_MINUS, "zoom_out", pygame.KEYDOWN)

    controls.set_context("city_ui")
    assert controls.current_context is not None

    # Initialize the CityUI class
    city_ui = CityUI(manager, ui_manager, canvas)

    running = True

    # Initialize the game state
    gstate = GameState(cfg)

    # Set pygame key repeat
    pygame.key.set_repeat(200, 50)

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                running = False
            command = None
            if event.type == pygame.KEYDOWN:
                command = controls.process_event(event)

            manager.process_events(event)
            city_ui.handle_event(event, gstate)
            if command is not None:
                city_ui.handle_command(command, gstate)

        manager.update(time_delta)
        city_ui.draw(screen)

        pygame.display.flip()

    pygame.quit()
