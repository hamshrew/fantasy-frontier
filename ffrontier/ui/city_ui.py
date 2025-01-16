'''This file contains the necessary classes to manage the UI in city management mode.'''
from typing import Dict
import pygame
import pygame_gui

from ffrontier.managers.ui_manager import UIVariableManager
from ffrontier.game.gamestate import GameState
from ffrontier.hex.canvas import HexCanvas


class CityUIPanel:
    '''Class to manage the UI panel.'''
    manager: pygame_gui.UIManager
    panel: pygame_gui.elements.UIPanel
    buttons: Dict[str, pygame_gui.elements.UIButton]
    info_panel: pygame_gui.elements.UITextBox

    def __init__(self, manager: pygame_gui.UIManager, panel_rect: pygame.Rect):
        self.manager = manager
        self.panel = pygame_gui.elements.UIPanel(relative_rect=panel_rect, manager=self.manager)
        self.buttons = {}
        self.info_panel = pygame_gui.elements.UITextBox(
            html_text='Info Panel',
            relative_rect=pygame.Rect((10, 70), (panel_rect.width - 20, panel_rect.height - 80)),
            manager=self.manager,
            container=self.panel
        )

        self._create_buttons()

    def _create_buttons(self):
        '''Create buttons for the UI panel.'''
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Button',
            manager=self.manager,
            container=self.panel
        )
        self.buttons['button'] = button

    def update_info_panel(self, text: str) -> None:
        '''Update the info panel with new text.'''
        self.info_panel.set_text(text)

    def handle_event(self, event: pygame.event.Event) -> None:
        '''Handle events related to the panel.'''
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.buttons.get('button'):
                self.update_info_panel('Button pressed')


class CityUI:
    '''Class to manage the city management UI.'''
    manager: pygame_gui.UIManager
    ui_manager: UIVariableManager
    menu_buttons: Dict[str, pygame_gui.elements.UIButton]
    ui_panel_rect: pygame.Rect
    viewport_rect: pygame.Rect
    viewport: pygame.Surface
    ui_panel: CityUIPanel
    canvas: HexCanvas

    def __init__(self, manager: pygame_gui.UIManager,
                 ui_manager: UIVariableManager,
                 canvas: HexCanvas):
        '''Initialize the CityUI class.'''
        self.manager = manager
        self.ui_manager = ui_manager
        self.viewport_rect = pygame.Rect((0, 0), self.ui_manager.viewport_size)
        self.ui_panel_rect = pygame.Rect((self.viewport_rect.width, 0),
                                         (self.ui_manager.screen_size[0] - self.viewport_rect.width,
                                          self.ui_manager.screen_size[1]))
        self.ui_panel = CityUIPanel(manager=self.manager, panel_rect=self.ui_panel_rect)
        self.canvas = canvas
        self.viewport = pygame.Surface(canvas.max_size)

    def handle_event(self, event: pygame.event.Event,
                     game_state: GameState) -> None:
        '''Handle events for the city management UI.'''
        game_state.handle_event(event)
        self.ui_panel.handle_event(event)
        self.canvas.handle_event(event, self.viewport)

    def draw(self, surface: pygame.Surface):
        '''Draw the city management UI.'''
        self.canvas.draw(self.viewport)
        surface.blit(self.viewport, self.viewport_rect.topleft)
        if self.canvas.highlighted_tile is not None:
            self.ui_panel.update_info_panel(str(self.canvas.highlighted_tile))
        else:
            self.ui_panel.update_info_panel('No tile selected')
        self.manager.draw_ui(surface)
