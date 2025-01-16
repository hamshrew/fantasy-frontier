'''Handles the map data file/structure.'''
from typing import Dict, List, Tuple, TypedDict
import csv
import json

import jsonschema

from ffrontier.utils.parsing import hex_to_rgba

# Constants
MAP_CONFIG_SCHEMA = {
    'type': 'object',
    'properties': {
        'orientation': {'type': 'boolean'}
    },
    'required': ['orientation']
}

MAP_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "coordinates": {"type": "array",
                        "items": {"type": "integer"},
                        "minItems": 2,
                        "maxItems": 2},
        "layers": {
            "type": "array",
            "items": {"type": "object",
                      "properties": {"image": {"type": "string"},
                                     "alpha": {"type": "integer"}},
                      "required": ["image"]}
        },
        "features": {"type": "array", "items": {"type": "string"}},
        "border": {"type": "integer"},
        "color": {"type": "string"}
    },
    "required": ["coordinates"]
}


class TileData(TypedDict):
    '''TypedDict for tile data.'''
    coordinates: Tuple[int, int]
    layers: List[Dict[str, str]]
    features: List[str]
    border: int
    color: Tuple[int, int, int, int]


class MapHandler:
    '''Handles the map data file/structure.'''
    map_file: str
    map_data: List[TileData]
    flat: bool

    def __init__(self, map_file: str):
        '''Initialize the map.'''
        self.map_file = map_file
        self.map_data = []
        self._load_map()

    def _validate_map(self) -> None:
        '''Validate the map data.'''

    def _load_map(self) -> None:
        '''Load and validate the map data.'''
        try:
            with open(self.map_file, 'r', encoding='utf-8') as file:
                # the first line is the orientation of the map
                lines = file.readlines()

                if len(lines) < 2:
                    raise ValueError('Map file is missing orientation and data')

                jsonschema.validate(json.loads(lines[0]), MAP_CONFIG_SCHEMA)

                config: dict = json.loads(lines[0])

                orientation = config.get('orientation', None)
                if orientation is None:
                    raise ValueError('Map file is missing orientation')

                self.flat = orientation

                tiles = [json.loads(line) for line in lines[1:]]

                for tile in tiles:
                    jsonschema.validate(tile, MAP_DATA_SCHEMA)
                    mdata: TileData = {
                        'coordinates': (0, 0),
                        'layers': [],
                        'features': [],
                        'border': 0,
                        'color': (255, 255, 255, 255)
                    }

                    mdata['coordinates'] = tuple(tile['coordinates'])
                    mdata['layers'] = tile.get('layers', [])
                    mdata['features'] = tile.get('features', [])
                    mdata['border'] = tile.get('border', 0)
                    mdata['color'] = hex_to_rgba(tile.get('color', '#ffffff'))

                    self.map_data.append(mdata)
        except FileNotFoundError as e:
            raise FileNotFoundError(f'Error loading map file {self.map_file}: {e}') from e
        except AssertionError as e:
            raise ValueError(f'Error loading map file {self.map_file}: {e}') from e
        except json.JSONDecodeError as e:
            raise ValueError(f'Error loading map file {self.map_file}: {e}') from e

    def is_flat(self) -> bool:
        '''Check if the map is flat.'''
        return self.flat

    def save_map(self) -> None:
        '''Save the map data.'''
        # Write to a CSV file
        with open(self.map_file, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['coordinates', 'terrain', 'features'])
            writer.writeheader()
            for row in self.map_data:
                writer.writerow(row)
