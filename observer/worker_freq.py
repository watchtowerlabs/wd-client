# -*- coding: utf-8 -*-
""" Class to facilitate frequency shifting loop.
"""

import trackersocket
import orbital
import time
import threading
import json
from datetime import datetime
import doppler


class WorkerFreq():

    # socket to connect to
    _IP = '127.0.0.1'  # default is localhost
    _PORT = 4534  # default receiver port

    # sleep time of loop
    SLEEP_TIME = 0.1  # in seconds  # TODO: get this from config?
    # loop flag
    _stay_alive = False

    # debug flag
    _debugmode = False

    # end when this timestamp is reached
    _observation_end = None

    # frequency of original signal
    _frequency = None

    observer_dict = {}
    satellite_dict = {}

    def __init__(self, ip=None, port=None, frequency=None, time_to_stop=None):
        """ We can pass receiver ip and port at initialisation.
        """
        if ip:
            self._IP = ip
        if port:
            self._PORT = port
        if frequency:
            self._frequency = frequency
        if time_to_stop:
            self._observation_end = time_to_stop

    def isalive(self):
        """ Returns if tracking loop is alive or not.
        """
        return self._stay_alive

    def trackobject(self, observer_dict, satellite_dict):
        """ Sets tracking object.
            Can also be called while tracking, to manipulate observation.
        """
        self.observer_dict = json.loads(observer_dict)
        self.satellite_dict = json.loads(satellite_dict)

    def trackstart(self):
        """ Starts the thread that communicates tracking info to remote socket.

            Stops by calling trackstop()
        """
        self._stay_alive = True
        t = threading.Thread(target=self._communicate_tracking_info)
        t.daemon = True
        t.start()
        return True

    def _communicate_tracking_info(self):
        """ Runs as a daemon thread, communicating tracking info to remote socket.

            Uses observer and satellite objects set by trackobject().

            Will exit when observation_end timestamp is reached.
        """
        if self._debugmode:
            print(('alive:', self._stay_alive))
        else:
            sock = trackersocket.trackersocket()
            sock.connect(self._IP, self._PORT)  # change to correct address

        # track satellite
        while self._stay_alive:
            #check if we need to exit
            self.check_observation_end_reached()

            if self._debugmode:
                #print type(self.observer_dict), self.observer_dict
                #print type(self.satellite_dict), self.satellite_dict
                print(('Tracking', self.satellite_dict['tle0'], 'from', self.observer_dict['elev']))
            else:
                p = orbital.pinpoint(self.observer_dict, self.satellite_dict)
                if p['ok']:
                    shift = self.calculate_frequency_shift(self._frequency, p['rng'], p['rng_vlct'])
                    s = str(shift) #TODO: FORMAT THIS AS REQUIRED
                    sock.send(s + str('\n'))
                    time.sleep(self.SLEEP_TIME)
            # exiting
        if self._debugmode:
            print('Frequency shifting thread exited.')
        else:
            sock.disconnect()

    def calculate_frequency_shift(frequency, distance, angular_velocity):
        return doppler(frequency, distance, angular_velocity)

    def trackstop(self):
        """ Sets object flag to false and stops the tracking thread.
        """
        self._stay_alive = False

    def check_observation_end_reached(self):
        #TODO: keep this, but incorporate it in a mechanism that:
        # a) calculates sleep time multiples
        # b) subtracts every time thread sleeps
        # c) is recalculated every time the sleep time interval is changed
        if datetime.now() > self._observation_end:
            self.trackstop()
