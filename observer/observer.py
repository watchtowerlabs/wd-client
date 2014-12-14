# -*- coding: utf-8 -*-


class observer:

    _location = None
    _tle = None
    _observation_end = None
    _frequency = None

    _rot_ip = None
    _rot_port = None
    _rot_interval = None

    _rig_ip = None
    _rig_port = None
    _rig_interval = None

    #_start_timestamp = None  # it is requested that the observation starts now()
    _end_timestamp = None

    def __init__(self):
        #TODO: run setup in initialisation and throw exception in case of problem
        pass

    @property
    def location(self, location):
        if location:
            self._location = location
        return location

    @property
    def tle(self, tle):
        if tle:
            self._tle = tle
        return self._tle

    @property
    def rot_ip(self, ip):
        if ip:
            self._rot_ip = ip
        return self._rot_ip

    @property
    def rot_port(self, port):
        if port:
            self._rot_port = port
        return self._rot_port

    @property
    def rig_ip(self, ip):
        if ip:
            self._rig_ip = ip
        return self._rig_ip

    @property
    def rig_port(self, port):
        if port:
            self._rig_port = port
        return self._rig_port

    @property
    def rot_interval(self, interval):
        if interval:
            self._rot_interval = interval
        return self._rot_interval

    @property
    def rig_interval(self, interval):
        if interval:
            self._rot_interval = interval
        return self._rot_interval

    @property
    def observation_end(self, timestamp):
        if timestamp:
            self._observation_end = timestamp
        return self._observation_end

    @property
    def frequency(self, frequency):
        if frequency:
            self._frequency = frequency
        return self._frequency

    def setup(self, tle, observation_end, frequency):
        """ Sets up required internal variables

            returns True if setup is ok
            returns False if setup had problems
        """
        setup_ok = True

        setup_ok and (tle == self.tle(tle))
        setup_ok and (observation_end == self.observation_end(observation_end))
        setup_ok and (frequency == self.frequency(frequency))

        return setup_ok

    def observe(self):
        """ starts threads for rotcrl and rigctl
        """
        # check for end timestamp

        # start thread for rotctl
        self.run_rot()

        # start thread for rigctl
        self.run_rig()

    def run_rot(self):
        pass

    def run_rig(self):
        pass
