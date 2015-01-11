# -*- coding: utf-8 -*-
""" Functional implementation of required orbital tracking functionality.

Observer and satellite passed objects are both dictionaries.

Observer dict contains:
    lat
    lon
    elev

Satellite dict contains:
    tle0
    tle1
    tle2
"""

import ephem
from datetime import datetime
import sys


def pinpoint(observer_dict, satellite_dict, timestamp=None):
    """ Provides azimuth and altitude of tracked object.

        args:
            observer_dict: dictionary with details of observation point.
            satellite_dict: dictionary with details of satellite.
            time: timestamp we want to use for pinpointing the observed object.

        returns:
            Dictionary containing azimuth and altitude. Also contains "ok" for error detection.
    """
    # observer object
    if 'lat' in observer_dict and 'lon' in observer_dict and 'elev' in observer_dict:
        observer = ephem.Observer()
        observer.lon = str(observer_dict['lon'])
        observer.lat = str(observer_dict['lat'])
        observer.elevation = observer_dict['elev']
    else:
        return {'ok': False}

    # satellite object
    if 'tle0' in satellite_dict and 'tle1' in satellite_dict and 'tle2' in satellite_dict:
        tle0 = str(satellite_dict['tle0'])
        tle1 = str(satellite_dict['tle1'])
        tle2 = str(satellite_dict['tle2'])
        try:
            satellite = ephem.readtle(tle0, tle1, tle2)
        except ValueError:
            print(("error:", "ephem object", "tle values", sys.exc_info()[0]))
            return False
        except:
            print(("error:", "ephem object", sys.exc_info()[0]))
            return False
    else:
        return {'ok': False}

    # time of observation
    if timestamp is None:
        timestamp = datetime.now()

    # observation calculation
    observer.date = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    satellite.compute(observer)
    return {'alt': satellite.alt, 'az': satellite.az,
            'rng': satellite.range, 'rng_vlct': satellite.range_velocity,
            'ok': True}
