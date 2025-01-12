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

    def __init__(self, manager: pygame_gui.UIManager, ui_manager: UIVariableManager):
        '''Initialize the CityUI class.'''
        self.manager = manager
        self.ui_manager = ui_manager

    def _create_buttons(self):
        '''Create the buttons for the city management UI.'''
        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                              text='Button',
                                              manager=self.manager)
        self.menu_buttons.update({'button': button})

    def handle_event(self, event: pygame.event.Event, game_state: GameState):
        '''Handle events for the city management UI.'''
        pass
