import asyncio
import urllib.request
from datetime import datetime

import aiohttp
import pandas as pd

DEFAULT_FORMAT = 'csv'
BASE_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/'
TIME_RANGE = 200
LATITUDE = 'latitude'
LONGITUDE = 'longitude'
FORMAT = 'format'
START_DATE = 'starttime'
END_TIME = 'endtime'
QUERY = 'query'
MAX_RADIUS = 'maxradiuskm'
MIN_MAGNITUDE = 'minmagnitude'

DATE_FORMAT = '%Y-%m-%d'


def get_earthquake_data(latitude: float,
                        longitude: float,
                        radius: float,
                        minimum_magnitude: float,
                        end_date: datetime) -> pd.DataFrame:
    url = build_api_url(latitude,
                        longitude,
                        radius,
                        minimum_magnitude,
                        end_date)
    data = pd.read_csv(urllib.request.urlopen(url))
    return data


def build_api_url(latitude: float,
                 longitude: float,
                 radius: float,
                 minimum_magnitude: float,
                 end_date: datetime) -> str:
    start_time = datetime(end_date.year - TIME_RANGE, end_date.month, end_date.day)
    query = make_query_string(latitude,
                              longitude,
                              radius,
                              minimum_magnitude,
                              start_time,
                              end_date)

    url = BASE_URL + query
    return url


def make_query_string(latitude: float,
                      longitude: float,
                      radius: float,
                      minimum_magnitude: float,
                      start_date: datetime,
                      end_date) -> str:
    query_string = 'query'

    argument_list = list()
    argument_list.append((FORMAT, DEFAULT_FORMAT))
    argument_list.append((LATITUDE, latitude))
    argument_list.append((LONGITUDE, longitude))
    argument_list.append((MAX_RADIUS, radius))
    argument_list.append((MIN_MAGNITUDE, minimum_magnitude))
    argument_list.append((START_DATE, start_date.strftime(DATE_FORMAT)))
    argument_list.append((END_TIME, end_date.strftime(DATE_FORMAT)))

    query_string += make_argument_string(argument_list)

    return query_string


def make_argument_string(argument_list):
    argument_string = ''

    for arg in argument_list:
        if argument_string:
            argument_string += '&'
        else:
            argument_string += '?'
        argument_string += arg[0] + '=' + str(arg[1])

    return argument_string


async def get_earthquake_data_async(session,
                                    latitude: float,
                                    longitude: float,
                                    radius: float,
                                    minimum_magnitude: float,
                                    end_date) -> pd.DataFrame:
    url = build_api_url(latitude,
                        longitude,
                        radius,
                        minimum_magnitude,
                        end_date)
    async with session.get(url) as response:
        s = await response.text()
        df = pd.DataFrame([x.split(',') for x in s.split('\n')])
        return df


async def get_earthquake_data_for_multiple_locations(assets,
                                                     radius: float,
                                                     minimum_magnitude: float,
                                                     end_date) -> pd.DataFrame:
    """ Asynchronous fetching of multiple earthquake usgc queries """
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for asset in assets:
            tasks.append(asyncio.create_task(get_earthquake_data_async(session,
                                                                       asset[0],
                                                                       asset[1],
                                                                       radius,
                                                                       minimum_magnitude,
                                                                       end_date)))
        dataframes = []
        for task in tasks:
            dataframes.append(await task)
        return pd.concat(dataframes)
