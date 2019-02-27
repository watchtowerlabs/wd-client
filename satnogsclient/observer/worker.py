# -*- coding: utf-8 -*-
from satnogsclient.web.weblogger import WebLogger
import logging
import math
import threading
import time
import json
import os
import signal

from datetime import datetime, timedelta

import ephem
import pytz

from flask_socketio import SocketIO
from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.orbital import pinpoint

from satnogsclient import settings


logging.setLoggerClass(WebLogger)
logger = logging.getLogger('default')
assert isinstance(logger, WebLogger)
socketio = SocketIO(message_queue='redis://')


class Worker(object):

    """Class to facilitate as a worker for rotctl/rigctl."""

    # sleep time of loop (in seconds)
    _sleep_time = 0.1

    # loop flag
    _stay_alive = False

    # end when this timestamp is reached
    _observation_end = None

    # frequency of original signal
    _frequency = None

    _azimuth = None
    _altitude = None
    _gnu_proc = None

    observer_dict = {}
    satellite_dict = {}

    def __init__(self, ip, port, time_to_stop=None, frequency=None, proc=None,
                 sleep_time=None):
        """Initialize worker class."""
        self._IP = ip
        self._PORT = port
        if frequency:
            self._frequency = frequency
        if time_to_stop:
            self._observation_end = time_to_stop
        if proc:
            self._gnu_proc = proc
        if sleep_time:
            self._sleep_time = sleep_time

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
        """
        self.observer_dict = observer_dict
        self.satellite_dict = satellite_dict

    def trackstart(self, port, start_thread):
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

        if start_thread:
            self.r = threading.Thread(
                target=self._status_interface, args=(port,))
            self.r.daemon = True
            self.r.start()

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

            p = pinpoint(self.observer_dict, self.satellite_dict)
            if p['ok']:
                dict = {'azimuth': p['az'].conjugate() * 180 / math.pi,
                        'altitude': p['alt'].conjugate() * 180 / math.pi,
                        'frequency': self._frequency * (1 - (p['rng_vlct'] / ephem.c)),
                        'tle0': self.satellite_dict['tle0'],
                        'tle1': self.satellite_dict['tle1'],
                        'tle2': self.satellite_dict['tle2']}
                socketio.emit('update_rotator', dict, namespace='/update_status')
                self.send_to_socket(p, sock)
                time.sleep(self._sleep_time)

        sock.disconnect()

    def _status_interface(self, port):
        sock = Commsocket('127.0.0.1', port)
        # sock.get_sock().bind(('127.0.0.1',port))
        sock.bind()
        sock.listen()
        while self.is_alive:
            conn = sock.accept()
            if conn:
                conn.recv(sock.buffer_size)
                dict = {'azimuth': "{0:.2f}".format(self._azimuth),
                        'altitude': "{0:.2f}".format(self._altitude),
                        'frequency': self._frequency,
                        'tle0': self.satellite_dict['tle0'],
                        'tle1': self.satellite_dict['tle1'],
                        'tle2': self.satellite_dict['tle2']}
                conn.send(json.dumps(dict))
                conn.close()

    def trackstop(self):
        """
        Sets object flag to false and stops the tracking thread.
        """
        logger.info('Tracking stopped.')
        self.is_alive = False
        if self._gnu_proc:
            os.killpg(os.getpgid(self._gnu_proc.pid), signal.SIGINT)

    def check_observation_end_reached(self):
        if datetime.now(pytz.utc) > self._observation_end:
            self.trackstop()


class WorkerTrack(Worker):
    _midpoint = None
    _flip = False

    @staticmethod
    def find_midpoint(observer_dict, satellite_dict, start):
        # Workaround for https://github.com/brandon-rhodes/pyephem/issues/105
        start -= timedelta(minutes=1)

        observer = ephem.Observer()
        observer.lon = str(observer_dict["lon"])
        observer.lat = str(observer_dict["lat"])
        observer.elevation = observer_dict["elev"]
        observer.date = ephem.Date(start)

        satellite = ephem.readtle(
            str(satellite_dict["tle0"]), str(satellite_dict["tle1"]),
            str(satellite_dict["tle2"]))

        timestamp_max = pytz.utc.localize(
            ephem.Date(observer.next_pass(satellite)[2]).datetime())
        pin = pinpoint(observer_dict, satellite_dict, timestamp_max)
        azi_max = pin["az"].conjugate() * 180 / math.pi
        alt_max = pin["alt"].conjugate() * 180 / math.pi

        return (azi_max, alt_max, timestamp_max)

    @staticmethod
    def normalize_angle(num, lower=0, upper=360):
        res = num
        if num > upper or num == lower:
            num = lower + abs(num + upper) % (abs(lower) + abs(upper))
        if num < lower or num == upper:
            num = upper - abs(num - lower) % (abs(lower) + abs(upper))
        res = lower if num == upper else num
        return res

    @staticmethod
    def flip_coordinates(azi, alt, timestamp, midpoint):
        midpoint_azi, midpoint_alt, midpoint_timestamp = midpoint
        if timestamp >= midpoint_timestamp:
            azi = midpoint_azi + (midpoint_azi - azi)
            alt = midpoint_alt + (midpoint_alt - alt)
            return (WorkerTrack.normalize_angle(azi),
                    WorkerTrack.normalize_angle(alt))
        return (azi, alt)

    def trackobject(self, observer_dict, satellite_dict):
        super(WorkerTrack, self).trackobject(observer_dict, satellite_dict)

        if settings.SATNOGS_ROT_FLIP and settings.SATNOGS_ROT_FLIP_ANGLE:
            self._midpoint = WorkerTrack.find_midpoint(observer_dict,
                                                       satellite_dict,
                                                       datetime.now(pytz.utc))
            logger.info("Antenna midpoint: AZ{0:.2f} EL{1:.2f} {2}".format(*self._midpoint))
            self._flip = (self._midpoint[1] >= settings.SATNOGS_ROT_FLIP_ANGLE)
            logger.info("Antenna flip: {0}".format(self._flip))

    def send_to_socket(self, pin, sock):
        # Read az/alt of sat and convert to radians
        azi = pin['az'].conjugate() * 180 / math.pi
        alt = pin['alt'].conjugate() * 180 / math.pi
        if self._flip:
            azi, alt = WorkerTrack.flip_coordinates(azi, alt,
                                                    datetime.now(pytz.utc),
                                                    self._midpoint)
        self._azimuth = azi
        self._altitude = alt
        # read current position of rotator, [0] az and [1] el
        position = sock.send("p\n").split('\n')
        # if the need to move exceeds threshold, then do it
        if (position[0].startswith("RPRT") or
            abs(azi - float(position[0])) > settings.SATNOGS_ROT_THRESHOLD or
                abs(alt - float(position[1])) > settings.SATNOGS_ROT_THRESHOLD):
                    msg = 'P {0} {1}\n'.format(azi, alt)
                    logger.debug('Rotctld msg: {0}'.format(msg))
                    sock.send(msg)


class WorkerFreq(Worker):

    def send_to_socket(self, p, sock):
        doppler_calc_freq = self._frequency * (1 - (p['rng_vlct'] / ephem.c))
        msg = 'F {0}\n'.format(int(doppler_calc_freq))
        logger.debug('Initial frequency: {0}'.format(self._frequency))
        logger.debug('Rigctld msg: {0}'.format(msg))
        sock.send(msg)
