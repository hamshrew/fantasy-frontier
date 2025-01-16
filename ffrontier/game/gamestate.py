'''Handles the current state of the game, including the map and the players.'''

import pygame

from ffrontier.managers.config_manager import ConfigManager


class GameState:
    '''Handles the current state of the game, including the map and the players.'''
    cfg: ConfigManager
    turn: int

    def __init__(self, cfg: ConfigManager):
        '''Initializes the game state with the given map size and number of players.'''
        self.turn = 0
        self.cfg = cfg

    def next_turn(self):
        '''Go to the next turn.'''
        self.turn += 1

    def get_turn(self) -> int:
        '''Get the current turn.'''
        return self.turn

    def handle_event(self, event: pygame.event.Event):
        '''Handle events for the game state.'''
