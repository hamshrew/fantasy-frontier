'''This file contains the necessary classes to manage the UI in city management mode.'''
from typing import Dict
import pygame
import pygame_gui

from ffrontier.managers.ui_manager import UIVariableManager
from ffrontier.game.gamestate import GameState


class CityUI:
    '''Class to manage the city management UI.'''
    manager: pygame_gui.UIManager
    ui_manager: UIVariableManager
    menu_buttons: Dict[str, pygame_gui.elements.UIButton]
    ui_panel_rect: pygame.Rect
    viewport_rect: pygame.Rect
    viewport: pygame.Surface
    ui_panel: pygame_gui.elements.UIPanel

    def __init__(self, manager: pygame_gui.UIManager, ui_manager: UIVariableManager):
        '''Initialize the CityUI class.'''
        self.manager = manager
        self.ui_manager = ui_manager
        self.viewport_rect = pygame.Rect((0, 0), self.ui_manager.viewport_size)
        self.ui_panel_rect = pygame.Rect((self.viewport_rect.width, 0),
                                         (self.ui_manager.screen_size[0] - self.viewport_rect.width,
                                          self.ui_manager.screen_size[1]))
        self.ui_panel = pygame_gui.elements.UIPanel(relative_rect=self.ui_panel_rect,
                                                    manager=self.manager)
        self._create_buttons()

    def _create_buttons(self):
        '''Create the buttons for the city management UI.'''
        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                              text='Button',
                                              manager=self.manager,
                                              container=self.ui_panel)
        info_panel = pygame_gui.elements.UITextBox(
            html_text='Info Panel',
            relative_rect=pygame.Rect((10, 70),
                                      (self.ui_panel_rect.width - 20,
                                       self.ui_panel_rect.height - 80)),
            manager=self.manager,
            container=self.ui_panel
            )
        self.menu_buttons = {'button': button, 'info_panel': info_panel}

    def update_info_panel(self, text: str) -> None:
        '''Update the info panel.'''
        self.menu_buttons['info_panel'].set_text(text)

    def handle_event(self, event: pygame.event.Event, game_state: GameState):
        '''Handle events for the city management UI.'''
        game_state.get_turn()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in self.menu_buttons.values():
                self.update_info_panel('Button pressed')

    def draw(self, surface: pygame.Surface):
        '''Draw the city management UI.'''
        self.manager.draw_ui(surface)
