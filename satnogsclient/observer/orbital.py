# -*- coding: utf-8 -*-
from datetime import datetime
import pytz
import ephem


class Orbital:
    """
    Provides calculations for orbital tracking. Wraps around pyephem.
    """
    observer = None
    tle = None

    def __init__(self, observer_dict=None, satellite_dict=None):
        # observer object
        if observer_dict:
            ret = self._set_observer_dict(observer_dict)
            if not ret:
                return False

        # satellite object
        if satellite_dict:
            ret = self._set_satellite_dict(satellite_dict)
            if not ret:
                return False

        # no problems
        return True

    def _set_observer(self, observer_dict):
        """
        Uses the dictionary provided to set observer attributes used in pyephem calculations.
        """
        if observer_dict:
            if all([x in observer_dict for x in ['lat', 'lon', 'elev']]):
                self.observer = ephem.Observer()
                self.observer.lon = str(observer_dict['lon'])
                self.observer.lat = str(observer_dict['lat'])
                self.observer.elevation = float(observer_dict['elev'])
                return True
        return False

    def _set_satellite(self, satellite_dict):
        """
        Uses the dictionary provided to set satellite trajectory attributes used in pyephem calculations.
        """
        if satellite_dict:
            if all([x in satellite_dict for x in ['tle0', 'tle1', 'tle2']]):
                tle0 = str(satellite_dict['tle0'])
                tle1 = str(satellite_dict['tle1'])
                tle2 = str(satellite_dict['tle2'])
                try:
                    self.satellite = ephem.readtle(tle0, tle1, tle2)
                    return True
                except ValueError:
                    #return {'ok': False,, 'error': 'ephem object - tle values problematic: {}'.format(sys.exc_info()[0])}
                    return False
                except:
                    #return {'ok': False,, 'error': 'ephem object: {}'.format(sys.exc_info()[0])}
                    return False
        return False

    def pinpoint(self, observer_dict=None, satellite_dict=None, timestamp=None):
        """
        Provides azimuth and altitude of tracked object.

        args:
            observer_dict: dictionary with details of observation point.
            satellite_dict: dictionary with details of satellite.
            time: timestamp we want to use for pinpointing the observed object.

            returns:
                Dictionary containing azimuth, altitude and "ok" for error detection.
                If errors are present, 'error' is included with error reason.
        """
        # check and set observer object, if dict provided
        if observer_dict:
            ret = self._set_observer_dict(observer_dict)
            if not ret:
                print(())
                return {'ok': False, 'error': 'problem setting observer provided'}

        # check and set satellite object, if dict provided
        if satellite_dict:
            ret = self._set_satellite_dict(satellite_dict)
            if not ret:
                return {'ok': False, 'error': 'problem setting satellite provided'}

        # check if observer is set
        if not self.observer:
            return {'ok': False, 'error': 'observer not set'}

        # check if satellite is set
        if not self.satellite:
            return {'ok': False, 'error': 'satellite not set'}

        # time of observation
        if not timestamp:
            timestamp = datetime.now(pytz.utc)
        self.observer.date = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')

        # observation calculation
        self.satellite.compute(self.observer)
        return {'alt': self.satellite.alt, 'az': self.satellite.az,
                'rng': self.satellite.range, 'rng_vlct': self.satellite.range_velocity,
                'ok': True}
