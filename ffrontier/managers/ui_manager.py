'''Contains handling for variables related to the UI, such as screen size and viewport size.'''
from typing import Tuple


class UIVariableManager:
    '''Class to manage UI-related variables.'''
    screen_size: Tuple[int, int]
    viewport_size: Tuple[int, int]

    def __init__(self):
        '''Initialize the UIVariableManager class.'''
        self.screen_size = (800, 600)
        self.viewport_size = (800, 600)

    def set_screen_size(self, size: Tuple[int, int]) -> None:
        '''Set the screen size.'''
        self.screen_size = size

    def set_viewport_size(self, size: Tuple[int, int]) -> None:
        '''Set the viewport size.'''
        self.viewport_size = size
