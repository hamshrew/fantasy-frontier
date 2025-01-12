'''Handles configuration file loading, saving, and management.'''
import configparser
from enum import Enum
from typing import Dict

# 3rd party modules

# Local modules


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

    def __init__(self, config_file: str):
        '''Initialize the ConfigManager class.'''
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.defaults = {}
        self.types = {}
        self.load_config()
        self.validate_config()

    def load_config(self):
        '''Load the configuration file.'''
        self.config.read(self.config_file)

    def save_config(self):
        '''Save the configuration file.'''
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def validate_config(self):
        '''Validate the configuration file and assign types and defaults.'''
        pass

    def get(self, section: str, option: str) -> str:
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
        elif option_type == ConfigType.FLOAT:
            return self.config.getfloat(section, option, fallback=self.defaults[section][option])
        elif option_type == ConfigType.BOOL:
            return self.config.getboolean(section, option, fallback=self.defaults[section][option])
        return self.config.get(section, option, fallback=self.defaults[section][option])
