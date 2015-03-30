# -*- coding: utf-8 -*-
import os
from os import environ, path
from decouple import config




def _cast_or_none(func, value):
    try:
        return func(value)
    except:
        return None


# Read from settings.ini using python-decouple
GROUND_STATION_ID = config('STATION_ID',cast=int, default=0)
GROUND_STATION_LAT = config('STATION_LAT',cast=float, default=0)
GROUND_STATION_LON = config('STATION_LON',cast=float, default=0)
GROUND_STATION_ELEV = config('STATION_ELEV',cast=float, default=0)

ROT_IP = config('ROT_IP', default='127.0.0.1')
ROT_PORT = config('ROT_PORT', cast=int, default=4532)
RIG_IP =  config('RTL_TCP_IP', default='127.0.0.1')
RIG_PORT = config('RTL_TCP_PORT', cast=int, default=4532)

NETWORK_API_URL = config('NETWORK_API_URL', default='https://dev.satnogs.org/api/')
NETWORK_API_KEY = config('NETWORK_API_KEY', default='')
NETWORK_API_QUERY_INTERVAL = config('NETWORK_API_QUERY_INTERVAL', cast=int, default=5) #minutes
SCHEDULER_SLEEP_TIME = config('SCHEDULER_SLEEP_TIME', cast=int, default=5) #seconds



WORKINGDIR = config('WORKINGDIR', '/tmp/.satnogs')

DEMODULATION_COMMAND = config('DEMODULATION_COMMAND', default='rtl_fm')
ENCODING_COMMAND = config('ENCODING_COMMAND', default='oggenc')
DECODING_COMMAND = config('DECODING_COMMAND', default='multimon-ng')


# Setup

#PWD = path.dirname(path.realpath(__file__))

if not os.path.exists(WORKINGDIR ):
        os.makedirs(WORKINGDIR )

DEFAULT_SQLITE_PATH = path.join(WORKINGDIR, 'jobs.sqlite')
SQLITE_URL = environ.get('SATNOGS_SQLITE_URL', 'sqlite:///' + DEFAULT_SQLITE_PATH)

if GROUND_STATION_ID==0:
    raise ValueError('Invalid setting for Station. Have you set up your settings.ini file?')



