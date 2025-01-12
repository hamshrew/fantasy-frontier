'''Handles the current state of the game, including the map and the players.'''


class GameState:
    '''Handles the current state of the game, including the map and the players.'''

    def __init__(self):
        '''Initializes the game state with the given map size and number of players.'''
        self.turn = 0
        self.phase = 'move'
