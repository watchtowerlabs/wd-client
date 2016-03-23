# -*- coding: utf-8 -*-
import logging
import sys

from datetime import datetime

import ephem
import pytz


logger = logging.getLogger('satnogsclient')


def pinpoint(observer, satellite, timestamp=None):
    """
    Provides azimuth and altitude of tracked object.

    args:
        observer: configured observation point object.
        satellite: configured satellite object.
        time: timestamp we want to use for pinpointing the observed object.

        returns:
            Dictionary containing azimuth, altitude and "ok" for error detection.
    """

    # time of observation
    if not timestamp:
        timestamp = datetime.now(pytz.utc)

    # observation calculation
    observer.date = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    satellite.compute(observer)
    calculated_data = {
        'alt': satellite.alt,
        'az': satellite.az,
        'rng': satellite.range,
        'rng_vlct': satellite.range_velocity,
        'ok': True
    }

    logger.debug('Calculated data: {0}'.format(calculated_data))
    return calculated_data
