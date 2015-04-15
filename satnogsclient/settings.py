# -*- coding: utf-8 -*-
import os
from os import environ, path




def _cast_or_none(func, value):
    try:
        return func(value)
    except:
        return None

GROUND_STATION_ID = _cast_or_none(int, environ.get('SATNOGS_STATION_ID', None))
GROUND_STATION_LAT = _cast_or_none(float, environ.get('SATNOGS_STATION_LAT', None))
GROUND_STATION_LON = _cast_or_none(float, environ.get('SATNOGS_STATION_LON', None))
GROUND_STATION_ELEV = _cast_or_none(float, environ.get('SATNOGS_STATION_ELEV', None))

PWD = path.dirname(path.realpath(__file__))
OUTPUT_PATH = environ.get('SATNOGS_OUTPUT_PATH', '/tmp/.satnogs')
if not os.path.exists(OUTPUT_PATH ):
    os.makedirs(OUTPUT_PATH )

CA_CERT =path.join(PWD, 'sub.class1.server.ca.pem')
DEFAULT_SQLITE_PATH = path.join(OUTPUT_PATH, 'jobs.sqlite')
SQLITE_URL = environ.get('SATNOGS_SQLITE_URL', 'sqlite:///' + DEFAULT_SQLITE_PATH)
DEMODULATION_COMMAND = environ.get('SATNOGS_DEMODULATION_COMMAND', 'rtl_fm')
ENCODING_COMMAND = environ.get('SATNOGS_ENCODING_COMMAND', 'oggenc')
DECODING_COMMAND = environ.get('SATNOGS_DECODING_COMMAND', 'multimon-ng')

NETWORK_API_URL = environ.get('SATNOGS_API_URL', 'https://dev.satnogs.org/api/')
NETWORK_API_QUERY_INTERVAL = 5  # In minutes
SCHEDULER_SLEEP_TIME = 10  # In seconds

ROT_IP = environ.get('SATNOGS_ROT_IP', '127.0.0.1')
ROT_PORT = int(environ.get('SATNOGS_ROT_PORT', 4533))
RIG_IP = environ.get('SATNOGS_RIG_IP', '127.0.0.1')
RIG_PORT = int(environ.get('SATNOGS_RIG_PORT', 4532))
