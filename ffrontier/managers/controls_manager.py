'''This file contains the necessary classes to manage the controls of the game,
including changing key bindings.'''
from typing import Dict, Optional

import pygame


class ControlContext:
    '''Class to manage key bindings for a specific context.'''
    name: str
    keydown_mappings: Dict[int, str]
    keyup_mappings: Dict[int, str]

    def __init__(self, name: str = 'default'):
        # Separate mappings for KEYDOWN and KEYUP events
        self.name = name
        self.keydown_mappings = {}
        self.keyup_mappings = {}

    def add_mapping(self, key: int, command: str, event_type: int) -> None:
        '''Add a mapping for a specific event type (KEYDOWN or KEYUP).'''
        if event_type == pygame.KEYDOWN:
            self.keydown_mappings[key] = command
        elif event_type == pygame.KEYUP:
            self.keyup_mappings[key] = command
        else:
            raise ValueError('Unsupported event type. Use pygame.KEYDOWN or pygame.KEYUP.')

    def get_command(self, key: int, event_type: int) -> Optional[str]:
        '''Retrieve the command associated with a key and event type.'''
        if event_type == pygame.KEYDOWN:
            return self.keydown_mappings.get(key)
        elif event_type == pygame.KEYUP:
            return self.keyup_mappings.get(key)
        return None


class ControlsManager:
    '''Class to manage key bindings and input handling.'''
    contexts: Dict[str, ControlContext]
    current_context: Optional[ControlContext]

    def __init__(self):
        self.contexts = {}
        self.current_context = None

    def set_context(self, context_name: str) -> None:
        '''Set the current context for input handling.'''
        if context_name not in self.contexts:
            raise ValueError(f'Context "{context_name}" not defined.')
        self.current_context = self.contexts[context_name]

    def add_context(self, context_name: str) -> None:
        '''Create a new context.'''
        if context_name not in self.contexts:
            self.contexts[context_name] = ControlContext()

    def add_mapping(self, context_name: str, key: int, command: str, event_type: int) -> None:
        '''Add a key-command mapping to a specific context.'''
        if context_name not in self.contexts:
            self.add_context(context_name)
        self.contexts[context_name].add_mapping(key, command, event_type)

    def process_event(self, event: pygame.event.Event) -> Optional[str]:
        '''
        Process a pygame event and return the associated command, if any.
        Returns None if no command is associated.
        '''
        if self.current_context is None:
            raise ValueError('Current context is not set.')
        action = self.current_context.get_command(event.key, event.type)
        if action is None:
            # Call the default context if no action is found
            if 'default' in self.contexts:
                action = self.contexts['default'].get_command(event.key, event.type)
        return action
