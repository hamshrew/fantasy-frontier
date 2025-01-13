'''Tests tilemap and tile functionality'''
import pytest

from ffrontier.hex.tile import Tile, TileMap, IncompleteGridError, DuplicateTileError
from ffrontier.hex.hexgrid import HexInfo


def test_tile():
    '''Test the Tile class'''
    hex_info = HexInfo(0, 0, False, 0)
    tile = Tile(hex_info, 'grass', None)
    assert tile.hex_info.q == 0
    assert tile.hex_info.r == 0
    assert tile.hex_info.flat is False
    assert tile.hex_info.border == 0
    assert tile.image == 'grass'


def test_tile_map(mocker):
    # Set up the mock for MapHandler
    MockDependency = mocker.patch('ffrontier.hex.tile.MapHandler')
    mock_instance = MockDependency.return_value
    mock_instance.map_data = [{'coordinates': (0, 0), 'terrain': 'grass',
                               'features': 'tree;rock'},
                              {'coordinates': (1, 0), 'terrain': 'water',
                               'features': 'boat'},
                              {'coordinates': (-1, 1), 'terrain': 'mountain',
                               'features': ''},
                              {'coordinates': (0, 1), 'terrain': 'forest',
                               'features': 'tree;animal'},
                              {'coordinates': (-1, 0), 'terrain': 'forest',
                               'features': 'tree;animal'}]
    # Create a mock asset manager
    mock_asset_manager = mocker.MagicMock()
    tile_map = TileMap(mock_asset_manager, 'fake_map_file')

    # Assertions
    MockDependency.assert_called_once_with('fake_map_file')  # Ensure MapHandler is instantiated
    assert len(tile_map.tiles) == 5
    assert tile_map.tiles[(0, 0)].hex_info.q == 0
    assert tile_map.tiles[(0, 0)].hex_info.r == 0
    assert tile_map.tiles[(0, 0)].hex_info.flat is False
    assert tile_map.tiles[(0, 0)].hex_info.border == 0
    assert tile_map.tiles[(0, 0)].image == 'grass'


def test_tile_map_incomplete_grid(mocker):
    # Set up the mock for MapHandler
    MockDependency = mocker.patch('ffrontier.hex.tile.MapHandler')
    mock_instance = MockDependency.return_value
    mock_instance.map_data = [{'coordinates': (0, 0), 'terrain': 'grass',
                               'features': 'tree;rock'},
                              {'coordinates': (1, 0), 'terrain': 'water',
                               'features': 'boat'},
                              {'coordinates': (-1, 1), 'terrain': 'mountain',
                               'features': ''},
                              {'coordinates': (-2, 4), 'terrain': 'mountain',
                               'features': ''},
                              {'coordinates': (0, 1), 'terrain': 'forest',
                               'features': 'tree;animal'}]

    # Create a mock asset manager
    mock_asset_manager = mocker.MagicMock()

    with pytest.raises(IncompleteGridError) as e:  # noqa
        tile_map = TileMap(mock_asset_manager, 'fake_map_file')  # noqa
        # Assertions
        MockDependency.assert_called_once_with('fake_map_file')  # Ensure MapHandler is instantiated


def test_tile_map_duplicate_coordinates(mocker):
    # Set up the mock for MapHandler
    MockDependency = mocker.patch('ffrontier.hex.tile.MapHandler')
    mock_instance = MockDependency.return_value
    mock_instance.map_data = [{'coordinates': (0, 0), 'terrain': 'grass',
                               'features': 'tree;rock'},
                              {'coordinates': (1, 0), 'terrain': 'water',
                               'features': 'boat'},
                              {'coordinates': (-1, 1), 'terrain': 'mountain',
                               'features': ''},
                              {'coordinates': (0, 0), 'terrain': 'forest',
                               'features': 'tree;animal'}]

    # Create a mock asset manager
    mock_asset_manager = mocker.MagicMock()
    with pytest.raises(DuplicateTileError) as e:  # noqa
        tile_map = TileMap(mock_asset_manager, 'fake_map_file')  # noqa
        # Assertions
        MockDependency.assert_called_once_with('fake_map_file')  # Ensure MapHandler is instantiated
