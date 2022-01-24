import numpy as np
from earthquakes.tools import get_haversine_distance
from earthquakes.tools import EARTH_RADIUS


def test_get_haversine_distance():
    assert np.allclose(get_haversine_distance(40, 40, 41 ,41), 139.842114446699, 1e-5)
    assert np.allclose(get_haversine_distance(40, 45, 40 ,45), 0, 1e-5)
    assert np.allclose(get_haversine_distance(40, 40, 41 ,40), EARTH_RADIUS * np.pi/180, 1e-5)