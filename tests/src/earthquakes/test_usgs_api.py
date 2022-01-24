from earthquakes.usgs_api import (make_query_string, build_api_url, BASE_URL)
from datetime import datetime



def test_make_query_string():
    query = 'query?format=csv&latitude=1&longitude=2&maxradiuskm=3&minmagnitude=4&starttime=1954-12-05&endtime=1988-11-05'
    assert (query == make_query_string(1, 2, 3, 4, datetime(1954,12,5), datetime(1988,11,5)))


def test_build_api_url():
    url = BASE_URL + 'query?format=csv&latitude=1&longitude=2&maxradiuskm=3&minmagnitude=4&starttime=1788-11-05&endtime=1988-11-05'
    assert (url == build_api_url(1, 2, 3, 4, datetime(1988,11,5)))