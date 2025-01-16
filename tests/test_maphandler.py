'''Tests the MapHandler class'''
import pytest
from jsonschema.exceptions import ValidationError

from ffrontier.game.maphandler import MapHandler


def test_map_handler_loads():
    map_handler = MapHandler('tests/testing_assets/test_map.csv')
    assert map_handler.map_file == 'tests/testing_assets/test_map.csv'
    assert map_handler.map_data == [{'coordinates': (0, 0), 'layers': [{'image': 'grass'}],
                                     'features': ['tree', 'rock'], 'border': 0,
                                     'color': (255, 255, 255, 255)},
                                    {'coordinates': (1, 0), 'layers': [{'image': 'water'}],
                                     'features': ['boat'], 'border': 0,
                                     'color': (255, 255, 255, 255)},
                                    {'coordinates': (-1, 1), 'layers': [],
                                     'features': [], 'border': 0,
                                     'color': (255, 255, 255, 255)},
                                    {'coordinates': (0, 0),
                                     'layers': [{'image': 'forest'}, {'image': 'accent'}],
                                     'features': ['tree', 'animal'], 'border': 0,
                                     'color': (255, 255, 255, 255)}]
    assert map_handler.flat is True


def test_map_handler_bad_validation():
    # This should raise an exception
    with pytest.raises(ValidationError) as e:  # noqa
        MapHandler('tests/testing_assets/test_map_bad.csv')


def test_map_handler_missing_file():
    # This should raise an exception
    with pytest.raises(FileNotFoundError) as e:  # noqa
        MapHandler('tests/testing_assets/test_map_missing.csv')
