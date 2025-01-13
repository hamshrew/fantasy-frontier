'''Tests the MapHandler class'''
import pytest

from ffrontier.game.maphandler import MapHandler


def test_map_handler_loads():
    map_handler = MapHandler('tests/testing_assets/test_map.csv')
    assert map_handler.map_file == 'tests/testing_assets/test_map.csv'
    assert map_handler.map_data == [{'coordinates': (0, 0), 'terrain': 'grass',
                                     'features': 'tree;rock'},
                                    {'coordinates': (1, 0), 'terrain': 'water',
                                     'features': 'boat'},
                                    {'coordinates': (-1, 1), 'terrain': 'mountain',
                                     'features': ''},
                                    {'coordinates': (0, 0), 'terrain': 'forest',
                                     'features': 'tree;animal'}]


def test_map_handler_bad_csv():
    # This should raise an exception
    with pytest.raises(ValueError) as e:  # noqa
        MapHandler('tests/testing_assets/test_map_bad.csv')


def test_map_handler_missing_csv():
    # This should raise an exception
    with pytest.raises(FileNotFoundError) as e:  # noqa
        MapHandler('tests/testing_assets/test_map_missing.csv')
