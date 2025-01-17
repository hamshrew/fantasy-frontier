'''Definition and details of the AssetManager class.'''
from typing import Any, Callable, Dict, Set, Optional
import json

# 3rd party modules
import pygame
import jsonschema

# Local modules
from ffrontier.hex import hexgrid


# Constants
MAX_SCALE = 400
MIN_SCALE = 20


class AssetManager:
    '''Class to manage assets like images, sounds, and fonts.'''
    images: Dict[str, pygame.Surface]
    scaled_images: Dict[str, pygame.Surface]
    sounds: Dict[str, pygame.mixer.Sound]
    fonts: Dict[str, pygame.font.Font]
    scale: int
    in_use: Set[str]

    def __init__(self, asset_file: Optional[str] = None, scale: int = 50,
                 mask: Optional[Callable[[pygame.Surface], pygame.Surface]] = None):
        '''Initialize the AssetManager class.'''
        self.images = {}
        self.scaled_images = {}
        self.sounds = {}
        self.fonts = {}
        self.scale = scale
        self.in_use = set()
        if asset_file:
            self.load_assets(asset_file, scale, mask)

    @property
    def max_scale(self) -> int:
        '''Return the maximum scale.'''
        return MAX_SCALE

    @property
    def min_scale(self) -> int:
        '''Return the minimum scale.'''
        return MIN_SCALE

    def load_assets(self, asset_file: str, scale: Optional[int] = None,
                    mask: Optional[Callable[[pygame.Surface], pygame.Surface]] = None) -> None:
        '''Loads the list of assets from the assets.json file and puts them into the manager.'''
        with open(asset_file, encoding='utf-8') as file:
            asset_data: Dict[str, Any] = json.load(file)
            jsonschema.validate(asset_data, asset_schema)
            # override mask if it is given
            if 'orientation' in asset_data:
                if mask is None:
                    if asset_data['orientation'] is True:
                        mask = hexgrid.mask_image_flat
                    else:
                        mask = hexgrid.mask_image_pointy
            for image in asset_data['images']:
                self.load_image(image['path'], image['name'], scale, mask)
            for sound in asset_data['sounds']:
                self.load_sound(sound['path'], sound['name'])
            for font in asset_data['fonts']:
                self.fonts[font['name']] = pygame.font.Font(font['path'], 16)

    def load_image(self, path: str, name: str, scale: Optional[int] = None,
                   mask: Optional[Callable[[pygame.Surface], pygame.Surface]] = None):
        '''
        Load an image from a file and store it in the images dictionary.
        Optionally scale and mask the image. If the image name exists, this will replace it.

            Args:
                path: str: The path to the image file.
                name: str: The name to store the image under.
                scale: Optional[int]: The scale to resize the image to.
                mask: Optional[Callable[[pygame.Surface], pygame.Surface]]:
                    A function to mask the image.

            Raises:
                FileNotFoundError: If the image file is not found.

            Returns:
                None

        '''
        try:
            self.images[name] = pygame.image.load(path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f'Error loading image file {path}: {e}') from e
        if mask is not None:
            # Call the mask function on the image
            self.images[name] = mask(self.images[name])
        if scale:
            self.scaled_images[name] = pygame.transform.scale(self.images[name], (scale, scale))

    def rescale_image(self, name, scale):
        '''Rescale a specific image in the scaled_images dictionary.'''
        self.scaled_images[name] = pygame.transform.scale(self.images[name], (scale, scale))

    def rescale_images(self, scale=None):
        '''Rescale all images in the scaled_images dictionary.'''
        if scale:
            if scale == self.scale:
                return
            self.scale = scale
        for name in self.in_use:
            self.scaled_images[name] = pygame.transform.scale(self.images[name],
                                                              (self.scale, self.scale))

    def load_sound(self, path, name):
        '''Load a sound from a file and store it in the sounds dictionary.'''
        self.sounds[name] = pygame.mixer.Sound(path)

    def get_image(self, name):
        '''Return an image from the images dictionary.'''
        return self.images[name]

    def get_scaled_image(self, name: str) -> pygame.Surface:
        '''Return a scaled image from the scaled_images dictionary.'''
        # Check if the image exists
        if name not in self.images:
            # Throw an error if the image does not exist
            raise ValueError(f'Image {name} does not exist')
        if name not in self.scaled_images:
            # Scale the image if it has not been scaled
            self.rescale_image(name, self.scale)
        self.in_use.add(name)
        # if the image is not the correct size, rescale it
        if self.scaled_images[name].get_width() != self.scale:
            self.rescale_image(name, self.scale)
        return self.scaled_images[name]

    def reset_in_use(self):
        '''Reset the in_use list.'''
        self.in_use.clear()

    def scale_up(self):
        '''Scale up the images by 5.'''
        self.scale += 5
        self.scale = min(self.scale, MAX_SCALE)
        self.rescale_images()

    def scale_down(self):
        '''Scale down the images by 5.'''
        self.scale -= 5
        self.scale = max(self.scale, MIN_SCALE)
        self.rescale_images()


asset_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "orientation": {
            "type": "boolean",
            "default": True},
        "images": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["name", "path"]
            }
        },
        "sounds": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["name", "path"]
            }
        },
        "fonts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["name", "path"]
            }
        }
    },
    "required": ["images", "sounds", "fonts"]
}
