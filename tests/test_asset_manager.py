'''Tests for the asset manager'''
import ffrontier.hex.hexgrid as hexgrid
import ffrontier.managers.asset_manager as asset_manager
import pygame
import pytest
import numpy as np


def compare_images_fast(image1: pygame.Surface, image2: pygame.Surface) -> bool:
    '''Compare two images quickly using numpy. Very minor differences may not be detected.'''
    # Check if sizes are the same
    if image1.get_size() != image2.get_size():
        print("Sizes are different")
        return False

    # Convert surfaces to arrays
    array1 = pygame.surfarray.array3d(image1)
    array2 = pygame.surfarray.array3d(image2)

    # Compare arrays, return result. Use approximate comparison
    return np.allclose(array1, array2, atol=1)


def test_image_loading():
    '''Test image loading'''
    am = asset_manager.AssetManager()
    # Load grasslands image
    am.load_image('tests/testing_assets/grasslands.png', 'grasslands')
    assert 'grasslands' in am.images


def test_image_loading_fail():
    '''Test image loading failure'''
    am = asset_manager.AssetManager()
    # Load non-existent image
    with pytest.raises(FileNotFoundError):
        am.load_image('tests/testing_assets/nonexistent.png', 'nonexistent')
    assert 'nonexistent' not in am.images


def test_image_scaling():
    '''Test image scaling'''
    am = asset_manager.AssetManager()
    # Load grasslands image
    am.load_image('tests/testing_assets/grasslands.png', 'grasslands', scale=50)
    assert 'grasslands' in am.images
    assert 'grasslands' in am.scaled_images
    assert am.images['grasslands'].get_size() == (889, 889)
    assert am.scaled_images['grasslands'].get_size() == (50, 50)


def test_image_rescaling():
    '''Test image rescaling'''
    am = asset_manager.AssetManager()
    # Load grasslands image
    am.load_image('tests/testing_assets/grasslands.png', 'grasslands', scale=50)
    # Rescale grasslands image
    am.rescale_image('grasslands', 100)
    assert am.images['grasslands'].get_size() == (889, 889)
    assert am.scaled_images['grasslands'].get_size() == (100, 100)


def test_image_masking():
    '''Test image masking'''
    am = asset_manager.AssetManager()
    # Load grasslands image
    am.load_image('tests/testing_assets/grasslands.png', 'grasslands', mask=hexgrid.mask_image_flat)
    image = am.images['grasslands']
    assert 'grasslands' in am.images
    assert am.images['grasslands'].get_size() == (889, 889)
    assert 'grasslands' not in am.scaled_images
    # Load the premasked image
    am.load_image('tests/testing_assets/grasslands_masked.png', 'grasslands_masked')
    # Check if the images are the same
    assert compare_images_fast(image, am.images['grasslands_masked'])


def test_image_scale_and_mask():
    '''Test image scaling and masking'''
    am = asset_manager.AssetManager()
    # Load grasslands image
    am.load_image('tests/testing_assets/grasslands.png', 'grasslands', scale=50,
                  mask=hexgrid.mask_image_flat)
    image = am.images['grasslands']
    assert 'grasslands' in am.images
    assert am.images['grasslands'].get_size() == (889, 889)
    assert 'grasslands' in am.scaled_images
    # Load the premasked image
    am.load_image('tests/testing_assets/grasslands_masked.png', 'grasslands_masked')
    # Check if the images are the same
    assert compare_images_fast(image, am.images['grasslands_masked'])
    # Load the premasked and scaled image
    am.load_image('tests/testing_assets/grasslands_scaled_masked.png', 'grasslands_scaled_masked')
    # Check if the images are the same
    assert compare_images_fast(am.scaled_images['grasslands'],
                               am.images['grasslands_scaled_masked'])


def test_asset_file_not_found():
    '''Test asset file not found'''
    # Load non-existent asset file
    with pytest.raises(FileNotFoundError):
        am = asset_manager.AssetManager('tests/testing_assets/nonexistent_assets.ini')
        assert not am.images
        assert not am.scaled_images
        assert not am.sounds


def test_asset_file():
    '''Test asset file loading'''
    am = asset_manager.AssetManager('tests/testing_assets/test_assets.ini')
    assert 'grasslands' in am.images


def test_image_rescale_file_loading():
    '''Test image rescale file loading'''
    am = asset_manager.AssetManager('tests/testing_assets/test_assets.ini', scale=50,
                                    mask=hexgrid.mask_image_flat)
    assert 'grasslands' in am.scaled_images
    assert am.scaled_images['grasslands'].get_size() == (50, 50)
    # Compare to the premasked and scaled image
    am.load_image('tests/testing_assets/grasslands_scaled_masked.png', 'grasslands_scaled_masked')
    assert compare_images_fast(am.scaled_images['grasslands'],
                               am.images['grasslands_scaled_masked'])
