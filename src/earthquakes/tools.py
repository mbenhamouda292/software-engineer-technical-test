import numpy as np
import pandas as pd

EARTH_RADIUS = 6378

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"


def get_haversine_distance(latitude1: float,
                           longitude1: float,
                           latitude2: float,
                           longitude2: float) -> float:
    latitude1, longitude1, latitude2, longitude2 = map(np.radians,
                                                       [latitude1,
                                                        longitude1,
                                                        latitude2,
                                                        longitude2])

    d_longitude = longitude1 - longitude2
    d_latitude = latitude1 - latitude2

    q = np.sin(d_latitude / 2.0) ** 2 + \
        np.cos(latitude1) * np.cos(latitude2) * np.sin(d_longitude / 2.0) ** 2

    distance = 2 * EARTH_RADIUS * np.arcsin(np.sqrt(q))

    return distance


def compute_payouts(earthquake_data: pd.DataFrame,
                    payout_structure) -> pd.DataFrame:

    earthquake_data_with_payout = earthquake_data.copy()
    earthquake_data_with_payout['payout'] = 0
    for payout_value in payout_structure:
        radius = float(payout_value['radius'].replace('km', ''))
        payout = float(payout_value['payout'].replace('%', ''))

        mask = (earthquake_data_with_payout['mag'] >= payout_value['magnitude']) & \
               (earthquake_data_with_payout['distance'] <= radius)

        earthquake_data_with_payout.loc[mask, 'payout'] = payout

    payout_events = earthquake_data_with_payout['payout']
    payout_events.index = pd.to_datetime(earthquake_data_with_payout['time'])
    payout_by_year = payout_events.groupby(payout_events.index.map(lambda x: x.year)).max()
    return payout_by_year


def compute_burning_cost(payouts: pd.DataFrame,
                         start_year: int,
                         end_year: int) -> float:
    
    mask = (payouts.index <= end_year) & (payouts.index >= start_year)
    return payouts.loc[mask].sum() / (end_year - start_year + 1)
