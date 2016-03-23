# -*- coding: utf-8 -*-
import logging
import math
import threading
import time

from datetime import datetime

import ephem
import pytz

from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.orbital import pinpoint


logger = logging.getLogger('satnogsclient')


class Worker:
    """Class to facilitate as a worker for rotctl/rigctl."""

    # sleep time of loop (in seconds)
    SLEEP_TIME = 0.1

    # loop flag
    _stay_alive = False

    # end when this timestamp is reached
    _observation_end = None

    # frequency of original signal
    _frequency = None

    observer_dict = {}
    satellite_dict = {}

    observer=None
    satellite=None

    def __init__(self, ip, port, time_to_stop=None, frequency=None):
        """Initialize worker class."""
        self._IP = ip
        self._PORT = port
        if frequency:
            self._frequency = frequency
        if time_to_stop:
            self._observation_end = time_to_stop

    @property
    def is_alive(self):
        """Returns if tracking loop is alive or not."""
        return self._stay_alive

    @is_alive.setter
    def is_alive(self, value):
        """Sets value if tracking loop is alive or not."""
        self._stay_alive = value

    def trackobject(self, observer_dict, satellite_dict):
        """
        Sets tracking object.
        Can also be called while tracking to manipulate observation.
        Returns whether or not setting tracking information succeeded
        """
        # observer object
        if all(map(lambda x: x in observer_dict, ['lat', 'lon', 'elev'])):
            logger.debug('Observer data: {0}'.format(observer_dict))
            self.observer = ephem.Observer()
            self.observer.lon = str(observer_dict['lon'])
            self.observer.lat = str(observer_dict['lat'])
            self.observer.elevation = float(observer_dict['elev'])
        else:
            logger.error('Something went wrong: {0}'.format(observer_dict))
            return False

        # satellite object
        if all(map(lambda x: x in satellite_dict, ['tle0', 'tle1', 'tle2'])):
            logger.debug('Satellite data: {0}'.format(satellite_dict))
            tle0 = str(satellite_dict['tle0'])
            tle1 = str(satellite_dict['tle1'])
            tle2 = str(satellite_dict['tle2'])
            try:
                self.satellite = ephem.readtle(tle0, tle1, tle2)
            except:
                logger.error('Something went wrong: {0}'.format(satellite_dict))
                logger.error(sys.exc_info()[0])
                return False
        else:
            return False
        return True

    def trackstart(self):
        """
        Starts the thread that communicates tracking info to remote socket.
        Stops by calling trackstop()
        """
        self.is_alive = True
        logger.info('Tracking initiated')
        if not all([self.observer_dict, self.satellite_dict]):
            raise ValueError('Satellite or observer dictionary not defined.')

        self.t = threading.Thread(target=self._communicate_tracking_info)
        self.t.daemon = True
        self.t.start()

        return self.is_alive

    def send_to_socket(self):
        # Needs to be implemented in freq/track workers implicitly
        raise NotImplementedError

    def _communicate_tracking_info(self):
        """
        Runs as a daemon thread, communicating tracking info to remote socket.
        Uses observer and satellite objects set by trackobject().
        Will exit when observation_end timestamp is reached.
        """
        sock = Commsocket(self._IP, self._PORT)
        sock.connect()

        # track satellite
        while self.is_alive:

            # check if we need to exit
            self.check_observation_end_reached()
            if (satellite is not None) and (observer is not None):
                p = pinpoint(self.observer, self.satellite)
                if p['ok']:
                    self.send_to_socket(p, sock)
                    time.sleep(self.SLEEP_TIME)
            else:
                logger.error('Something has gone terribly wrong, is trackstart being called without calling trackobject?')

        sock.disconnect()

    def trackstop(self):
        """
        Sets object flag to false and stops the tracking thread.
        """
        logger.info('Tracking stopped.')
        self.is_alive = False

    def check_observation_end_reached(self):
        if datetime.now(pytz.utc) > self._observation_end:
            self.trackstop()


class WorkerTrack(Worker):
    def send_to_socket(self, p, sock):
        # Read az/alt and convert to radians
        az = p['az'].conjugate() * 180 / math.pi
        alt = p['alt'].conjugate() * 180 / math.pi

        msg = 'P {0} {1}\n'.format(az, alt)
        logger.debug('Rotctld msg: {0}'.format(msg))
        sock.send(msg)


class WorkerFreq(Worker):
    def send_to_socket(self, p, sock):
        doppler_calc_freq = self._frequency * (1 - (p['rng_vlct'] / ephem.c))
        msg = 'F {0}\n'.format(doppler_calc_freq)
        logger.debug('Initial frequency: {0}'.format(self._frequency))
        logger.debug('Rigctld msg: {0}'.format(msg))
        sock.send(msg)
