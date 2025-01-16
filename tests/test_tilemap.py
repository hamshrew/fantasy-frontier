'''Tests tilemap and tile functionality'''
import pytest

from ffrontier.hex.tileutils import Tile, TileMap, IncompleteGridError, DuplicateTileError, Layer
from ffrontier.hex.hexgrid import HexInfo


def test_tile():
    '''Test the Tile class'''
    hex_info = HexInfo(0, 0, False, 0)
    tile = Tile(hex_info, [Layer('grass')], None)
    assert tile.hex_info.q == 0
    assert tile.hex_info.r == 0
    assert tile.hex_info.flat is False
    assert tile.hex_info.border == 0
    assert tile.images[0].image == 'grass'


test_map_data = [{'coordinates': (0, 0), 'layers': [{'image': 'grass'}],
                  'features': 'tree;rock', 'border': 0,
                  'color': (255, 255, 255, 255)},
                 {'coordinates': (1, 0), 'layers': [{'image': 'water'}],
                  'features': 'boat', 'border': 0,
                  'color': (255, 255, 255, 255)},
                 {'coordinates': (-1, 1), 'layers': [{'image': 'mountain'}],
                  'features': '', 'border': 0,
                  'color': (255, 255, 255, 255)},
                 {'coordinates': (0, 1), 'layers': [{'image': 'forest'}],
                  'features': 'tree;animal', 'border': 0,
                  'color': (255, 255, 255, 255)},
                 {'coordinates': (-1, 0),
                  'layers': [{'image': 'forest'}, {'image': 'accent'}],
                  'features': 'tree;animal', 'border': 0,
                  'color': (255, 255, 255, 255)}]


def test_tile_map(mocker):
    # Set up the mock for MapHandler
    MockDependency = mocker.patch('ffrontier.hex.tileutils.MapHandler')
    mock_instance = MockDependency.return_value
    mock_instance.flat = False
    mock_instance.map_data = test_map_data
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
    assert tile_map.tiles[(0, 0)].images[0].image == 'grass'


def test_tile_map_incomplete_grid(mocker):
    # Set up the mock for MapHandler
    MockDependency = mocker.patch('ffrontier.hex.tileutils.MapHandler')
    mock_instance = MockDependency.return_value
    mock_instance.map_data = test_map_data[:3]

    # Create a mock asset manager
    mock_asset_manager = mocker.MagicMock()

    with pytest.raises(IncompleteGridError) as e:  # noqa
        tile_map = TileMap(mock_asset_manager, 'fake_map_file')  # noqa
        # Assertions
        MockDependency.assert_called_once_with('fake_map_file')  # Ensure MapHandler is instantiated


def test_tile_map_duplicate_coordinates(mocker):
    # Set up the mock for MapHandler
    MockDependency = mocker.patch('ffrontier.hex.tileutils.MapHandler')
    mock_instance = MockDependency.return_value
    dup_map_data = test_map_data.copy()
    dup_map_data[4]['coordinates'] = (0, 0)
    mock_instance.map_data = dup_map_data

    # Create a mock asset manager
    mock_asset_manager = mocker.MagicMock()
    with pytest.raises(DuplicateTileError) as e:  # noqa
        tile_map = TileMap(mock_asset_manager, 'fake_map_file')  # noqa
        # Assertions
        MockDependency.assert_called_once_with('fake_map_file')  # Ensure MapHandler is instantiated


def test_collision_flat():
    '''Test the collision detection of a flat-top hexagon'''
    hex_info = HexInfo(0, 0, True, 0)
    assert hex_info.collides(9, 0, 10) is True
    assert hex_info.collides(0, 9, 10) is False


def test_collision_pointy():
    '''Test the collision detection of a pointy-top hexagon'''
    hex_info = HexInfo(0, 0, False, 0)
    assert hex_info.collides(9, 0, 10) is False
    assert hex_info.collides(0, 9, 10) is True
