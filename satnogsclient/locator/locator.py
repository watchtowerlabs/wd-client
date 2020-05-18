import logging
import logging.config
import time

import gps

from satnogsclient import settings

LOGGER = logging.getLogger(__name__)


class Locator(object):
    def __init__(self):
        self.timeout = settings.SATNOGS_GPSD_TIMEOUT

    @staticmethod
    def show_location(gpsd):
        LOGGER.debug('mode       %d ', gpsd.fix.mode)
        LOGGER.debug('status     %d ', gpsd.status)
        LOGGER.debug('latitude   %f', gpsd.fix.latitude)
        LOGGER.debug('longitude  %f', gpsd.fix.longitude)
        LOGGER.debug('altitude   %f', gpsd.fix.altitude)
        LOGGER.debug('hdop       %d', gpsd.hdop)

    def update_location(self):
        if settings.SATNOGS_GPSD_CLIENT_ENABLED is not True:
            return
        no_timeout = (self.timeout == 0)
        if (settings.SATNOGS_STATION_LAT is None or settings.SATNOGS_STATION_LON is None
                or settings.SATNOGS_STATION_ELEV is None):
            no_timeout = True
            LOGGER.info('No default coordinates, GPS timeout disabled')
        else:
            LOGGER.info('Last coordinates %f %f %d', settings.SATNOGS_STATION_LAT,
                        settings.SATNOGS_STATION_LON, settings.SATNOGS_STATION_ELEV)
        end_time = time.time() + self.timeout

        try:
            LOGGER.info('Connecting to GPSD %s:%d', settings.SATNOGS_GPSD_HOST,
                        settings.SATNOGS_GPSD_PORT)
            gpsd = gps.gps(mode=gps.WATCH_ENABLE,
                           host=settings.SATNOGS_GPSD_HOST,
                           port=settings.SATNOGS_GPSD_PORT)
            gpsd.next()
            LOGGER.info('Waiting for GPS (timeout %ds)', self.timeout)
            while gpsd.fix.mode != gps.MODE_3D and (time.time() < end_time or no_timeout):
                self.show_location(gpsd)
                gpsd.next()
        except StopIteration:
            LOGGER.info('GPSD connection failed')
            return
        if gpsd.fix.mode == gps.MODE_3D:
            settings.SATNOGS_STATION_LAT = gpsd.fix.latitude
            settings.SATNOGS_STATION_LON = gpsd.fix.longitude
            settings.SATNOGS_STATION_ELEV = gpsd.fix.altitude
            LOGGER.info('Updating coordinates %f %f %d', settings.SATNOGS_STATION_LAT,
                        settings.SATNOGS_STATION_LON, settings.SATNOGS_STATION_ELEV)
        else:
            LOGGER.info('GPS timeout, using last known coordinates')
