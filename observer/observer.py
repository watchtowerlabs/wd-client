# -*- coding: utf-8 -*-


class observer:

    _location = None
    _tle = None

    _rot_ip = None
    _rot_port = None
    _rot_interval = None

    _rig_ip = None
    _rig_port = None
    _rig_interval = None

    def __init__(self):
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
