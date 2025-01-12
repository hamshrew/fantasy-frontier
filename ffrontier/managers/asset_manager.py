'''Definition and details of the AssetManager class.'''
from typing import Callable

# 3rd party modules
import pygame

# Local modules


class AssetManager:
    '''Class to manage assets like images, sounds, and fonts.'''

    def __init__(self):
        '''Initialize the AssetManager class.'''
        self.images = {}
        self.scaled_images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, path: str, name: str, scale: int = None,
                   mask: Callable[[pygame.Surface], pygame.Surface] = None):
        '''Load an image from a file and store it in the images dictionary.
        Optionally scale and mask the image.'''
        self.images[name] = pygame.image.load(path)
        if mask:
            # Call the mask function on the image
            self.images[name] = mask(self.images[name])
        if scale:
            self.scaled_images[name] = pygame.transform.scale(self.images[name], (scale, scale))

    def rescale_image(self, name, scale):
        '''Rescale a specific image in the scaled_images dictionary.'''
        self.scaled_images[name] = pygame.transform.scale(self.images[name], (scale, scale))

    def load_sound(self, path, name):
        '''Load a sound from a file and store it in the sounds dictionary.'''
        self.sounds[name] = pygame.mixer.Sound(path)

    def get_image(self, name):
        '''Return an image from the images dictionary.'''
        return self.images[name]

    def get_scaled_image(self, name):
        '''Return a scaled image from the scaled_images dictionary.'''
        return self.scaled_images[name]
