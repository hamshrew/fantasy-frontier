'''Handles the map data file/structure.'''
from typing import List, Dict, Tuple

import csv


class MapHandler:
    '''Handles the map data file/structure.'''
    map_file: str
    map_data: List[Dict[str, str | Tuple[int, int]]]
    flat: bool

    def __init__(self, map_file: str):
        '''Initialize the map.'''
        self.map_file = map_file
        self.map_data = []
        self.flat = True
        self._load_map()

    def _load_map(self) -> None:
        '''Load and validate the map data.'''
        try:
            with open(self.map_file, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Check the header data for the necessary columns
                assert reader.fieldnames is not None
                if 'coordinates' not in reader.fieldnames:
                    raise ValueError('Map data missing coordinates column')
                if 'terrain' not in reader.fieldnames:
                    raise ValueError('Map data missing terrain column')
                if 'features' not in reader.fieldnames:
                    raise ValueError('Map data missing features column')
                for row in reader:
                    # Check types and convert the data as necessary
                    mdata: Dict[str, str | Tuple[int, int]] = {}
                    coords = row['coordinates'].split(',')
                    if len(coords) != 2:
                        raise ValueError(f'Invalid coordinates: {coords}')
                    mdata['coordinates'] = (int(coords[0]), int(coords[1]))
                    mdata['terrain'] = str(row['terrain'])
                    mdata['features'] = str(row['features'])
                    self.map_data.append(mdata)
        except FileNotFoundError as e:
            raise FileNotFoundError(f'Error loading map file {self.map_file}: {e}') from e
        except AssertionError as e:
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
