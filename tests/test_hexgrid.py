'''Tests for the hexgrid library functions'''
import ffrontier.hex.hexgrid as hexgrid


def test_axial_to_pixel():
    '''Test axial to pixel conversion'''
    assert hexgrid.axial_to_pixel(hexgrid.HexInfo(0, 0, True, 0), 10) == (0, 0)
    assert hexgrid.axial_to_pixel(hexgrid.HexInfo(1, 0, True, 0), 10) == (15, 9)
    assert hexgrid.axial_to_pixel(hexgrid.HexInfo(0, 1, True, 0), 10) == (0, 17)
    assert hexgrid.axial_to_pixel(hexgrid.HexInfo(1, 1, True, 0), 10) == (15, 26)
    assert hexgrid.axial_to_pixel(hexgrid.HexInfo(1, 1, False, 0), 10) == (26, 15)


def test_axial_to_cube():
    '''Test axial to cube conversion'''
    assert hexgrid.axial_to_cube(hexgrid.HexInfo(0, 0, True, 0)) == (0, 0, 0)
    assert hexgrid.axial_to_cube(hexgrid.HexInfo(1, 0, True, 0)) == (1, 0, -1)
    assert hexgrid.axial_to_cube(hexgrid.HexInfo(0, 1, True, 0)) == (0, 1, -1)
    assert hexgrid.axial_to_cube(hexgrid.HexInfo(1, 1, True, 0)) == (1, 1, -2)
    assert hexgrid.axial_to_cube(hexgrid.HexInfo(1, 1, False, 0)) == (1, 1, -2)
