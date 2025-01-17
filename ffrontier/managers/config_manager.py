'''Handles configuration file loading, saving, and management.'''
import configparser
from enum import Enum
from typing import Dict
from pathlib import Path
import logging

# 3rd party modules

# Local modules
from ffrontier.managers.log_manager import LogManager


# Constants
# Make a type list using enums
class ConfigType(Enum):
    '''Enum for configuration types.'''
    STRING = 0
    INT = 1
    FLOAT = 2
    BOOL = 3


class ConfigManager:
    '''Class to manage configuration files.'''
    config: configparser.ConfigParser
    config_file: str
    defaults: Dict[str, Dict[str, str]]
    types: Dict[str, Dict[str, ConfigType]]
    log_manager: LogManager

    def __init__(self, config_file: str):
        '''Initialize the ConfigManager class.'''
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.defaults = {}
        self.types = {}
        self.log_manager = LogManager()
        self.load_config()
        self.validate_config()
        self.setup_logging()

    def load_config(self):
        '''Load the configuration file.'''
        self.config.read(self.config_file)

    def save_config(self):
        '''Save the configuration file.'''
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def validate_config(self):
        '''Validate the configuration file and assign types and defaults.'''
        self.validate_base_config()
        self.validate_logging_config()

    def validate_base_config(self) -> bool:
        '''Validates the base configuration.'''
        if 'base' not in self.config:
            self.config['base'] = configparser.SectionProxy(self.config, 'base')

        # Set defaults and types for the base configuration
        self.defaults['base'] = {
            'width': '800',
            'height': '600',
            'title': 'FFrontier',
            'fps': '60'
        }

        self.types['base'] = {
            'width': ConfigType.INT,
            'height': ConfigType.INT,
            'title': ConfigType.STRING,
            'fps': ConfigType.INT
        }

        cfg = self.config['base']

        # Set the default values for the base configuration
        if 'width' not in cfg:
            cfg['width'] = '800'
        if 'height' not in cfg:
            cfg['height'] = '600'
        if 'title' not in cfg:
            cfg['title'] = 'FFrontier'
        if 'fps' not in cfg:
            cfg['fps'] = '60'

        return True

    def validate_logging_config(self) -> bool:
        '''Validates the logging configuration.'''
        if 'logging' not in self.config:
            self.config['logging'] = configparser.SectionProxy(self.config, 'logging')

        # Set defaults and types for the logging configuration
        self.defaults['logging'] = {
            'loglevel': 'INFO',
            'gamelog': 'logs/game.log',
            'gameloglevel': 'INFO',
            'ailog': 'logs/ai.log',
            'ailoglevel': 'INFO',
            'guilog': 'logs/gui.log',
            'guiloglevel': 'INFO'
        }

        self.types['logging'] = {
            'loglevel': ConfigType.STRING,
            'gamelog': ConfigType.STRING,
            'gameloglevel': ConfigType.STRING,
            'ailog': ConfigType.STRING,
            'ailoglevel': ConfigType.STRING,
            'guilog': ConfigType.STRING,
            'guiloglevel': ConfigType.STRING
        }

        cfg = self.config['logging']

        # Set the default values for the logging configuration
        if 'loglevel' not in cfg:
            cfg['loglevel'] = 'INFO'

        # Set up the game logger
        if 'gamelog' not in cfg:
            cfg['gamelog'] = 'logs/game.log'
        if Path(cfg['gamelog']).parent.is_dir() is False:
            # Create the directory if it doesn't exist
            Path(cfg['gamelog']).parent.mkdir(parents=True, exist_ok=True)
        if 'gameloglevel' not in cfg:
            cfg['gameloglevel'] = 'INFO'

        # Set up the AI logger
        if 'ailog' not in cfg:
            cfg['ailog'] = 'logs/ai.log'
        if Path(cfg['ailog']).parent.is_dir() is False:
            Path(cfg['ailog']).parent.mkdir(parents=True, exist_ok=True)
        if 'ailoglevel' not in cfg:
            cfg['ailoglevel'] = 'INFO'

        # Set up the GUI logger
        if 'guilog' not in cfg:
            cfg['guilog'] = 'logs/gui.log'
        if Path(cfg['guilog']).parent.is_dir() is False:
            Path(cfg['guilog']).parent.mkdir(parents=True, exist_ok=True)
        if 'guiloglevel' not in cfg:
            cfg['guiloglevel'] = 'INFO'

        return True

    def get(self, section: str, option: str) -> str | int | float | bool:
        '''Get an option from a section.'''
        # Check if option exists in section by checking the defaults
        if section not in self.types:
            raise ValueError(f'Section "{section}" not defined.')
        if option not in self.types[section]:
            raise ValueError(f'Option "{option}" not defined in section "{section}".')
        # get the option type
        option_type = self.types[section][option]
        # return the correct type depending on the option type
        if option_type == ConfigType.INT:
            return self.config.getint(section, option, fallback=self.defaults[section][option])
        if option_type == ConfigType.FLOAT:
            return self.config.getfloat(section, option, fallback=self.defaults[section][option])
        if option_type == ConfigType.BOOL:
            return self.config.getboolean(section, option, fallback=self.defaults[section][option])
        return self.config.get(section, option, fallback=self.defaults[section][option])

    def setup_logging(self):
        '''Set up logging based on the configuration.'''
        self.log_manager.setup_logger('game',
                                      self.get('logging', 'gamelog'),
                                      self.get('logging', 'gameloglevel'))
        self.log_manager.setup_logger('ai',
                                      self.get('logging', 'ailog'),
                                      self.get('logging', 'ailoglevel'))
        self.log_manager.setup_logger('gui',
                                      self.get('logging', 'guilog'),
                                      self.get('logging', 'guiloglevel'))

    def get_logger(self, name: str) -> logging.Logger:
        '''Get a logger by name.'''
        return self.log_manager.get_logger(name)
