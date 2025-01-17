'''Manager that handles setup and retrieval of loggers.'''
import logging


class LogManager:
    '''Manager that handles setup and retrieval of loggers.'''
    def __init__(self):
        self.loggers = {}

    def get_logger(self, name: str) -> logging.Logger:
        '''Get a logger by name.'''
        if name not in self.loggers:
            raise ValueError(f'Logger {name} not found in loggers')
        return self.loggers[name]

    def setup_logger(self, name: str, log_file: str, level: str) -> None:
        '''Set up a logger.'''
        if name in self.loggers:
            raise ValueError(f'Logger {name} already exists')
        logger = logging.getLogger(name)
        logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        self.loggers[name] = logger
