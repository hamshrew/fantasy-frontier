'''Contains handling for variables related to the UI, such as screen size and viewport size.'''
from typing import Tuple


class UIVariableManager:
    '''Class to manage UI-related variables.'''
    screen_size: Tuple[int, int]
    viewport_size: Tuple[int, int]

    def __init__(self, screen_size: Tuple[int, int] = (800, 600),
                 viewport_size: Tuple[int, int] = (500, 600)) -> None:
        '''Initialize the UIVariableManager class.

            Args:
                screen_size (Tuple[int, int]): The size of the screen.
                viewport_size (Tuple[int, int]): The size of the viewport.

            Returns:
                None
        '''
        self.screen_size = screen_size
        self.viewport_size = viewport_size

    def set_screen_size(self, size: Tuple[int, int]) -> None:
        '''Set the screen size.'''
        self.screen_size = size

    def set_viewport_size(self, size: Tuple[int, int]) -> None:
        '''Set the viewport size.'''
        self.viewport_size = size
