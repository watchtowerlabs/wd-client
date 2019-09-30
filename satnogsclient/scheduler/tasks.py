from __future__ import absolute_import, division, print_function

import logging
import os
import signal
import subprocess

import requests
from dateutil import parser

from satnogsclient import settings
from satnogsclient.locator import locator
from satnogsclient.observer.observer import Observer
from satnogsclient.scheduler import SCHEDULER

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

LOGGER = logging.getLogger(__name__)


def signal_term_handler():
    process = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    out, err = process.communicate()  # pylint: disable=W0612
    for line in out.decode().splitlines():
        if 'satnogs-client' in line:
            pid = int(line.split(None, 2)[1])
            os.kill(pid, signal.SIGKILL)


signal.signal(signal.SIGINT, signal_term_handler)


def spawn_observer(**kwargs):
    obj = kwargs.pop('obj')
    tle = {'tle0': obj['tle0'], 'tle1': obj['tle1'], 'tle2': obj['tle2']}
    end = parser.parse(obj['end'])

    observer = Observer()
    observer.location = {
        'lon': settings.SATNOGS_STATION_LON,
        'lat': settings.SATNOGS_STATION_LAT,
        'elev': settings.SATNOGS_STATION_ELEV
    }
    frequency = 100e6
    # Get the baudrate. In case of CW baudrate equals the WPM
    baud = 0
    if 'baud' in obj:
        baud = obj['baud']
    frequency = obj['frequency']
    script_name = settings.GNURADIO_FM_SCRIPT_FILENAME
    if 'mode' in obj and obj['mode']:
        if obj['mode'] == "CW":
            script_name = settings.GNURADIO_CW_SCRIPT_FILENAME
        elif obj['mode'] == "APT":
            script_name = settings.GNURADIO_APT_SCRIPT_FILENAME
        elif obj['mode'].startswith('BPSK'):
            script_name = settings.GNURADIO_BPSK_SCRIPT_FILENAME
        elif obj['mode'] == 'GFSK Rktr':
            script_name = settings.GNURADIO_GFSK_RKTR_SCRIPT_FILENAME
        elif obj['mode'].startswith('FSK') or obj['mode'].startswith('GFSK'):
            script_name = settings.GNURADIO_FSK_SCRIPT_FILENAME
        elif obj['mode'].startswith('MSK') or obj['mode'].startswith('GMSK'):
            script_name = settings.GNURADIO_MSK_SCRIPT_FILENAME
        elif obj['mode'].endswith('AFSK1k2'):
            script_name = settings.GNURADIO_AFSK1K2_SCRIPT_FILENAME
        elif obj['mode'].endswith('DUV'):
            script_name = settings.GNURADIO_AMSAT_DUV_SCRIPT_FILENAME

    setup_kwargs = {
        'observation_id': obj['id'],
        'tle': tle,
        'observation_end': end,
        'frequency': frequency,
        'baud': baud,
        'script_name': script_name
    }

    LOGGER.debug('Observer args: %s', setup_kwargs)
    setup = observer.setup(**setup_kwargs)

    if setup:
        LOGGER.info('Spawning observer worker.')
        observer.observe()
    else:
        raise RuntimeError('Error in observer setup.')


def post_data():
    """PUT observation data back to Network API."""
    LOGGER.info('Post data started')
    base_url = urljoin(settings.SATNOGS_NETWORK_API_URL, 'observations/')
    headers = {'Authorization': 'Token {0}'.format(settings.SATNOGS_API_TOKEN)}

    for fil in next(os.walk(settings.SATNOGS_OUTPUT_PATH))[2]:
        file_path = os.path.join(*[settings.SATNOGS_OUTPUT_PATH, fil])
        if (fil.startswith('receiving_satnogs') or fil.startswith('receiving_waterfall')
                or fil.startswith('receiving_data') or os.stat(file_path).st_size == 0):
            continue
        if fil.startswith('satnogs'):
            observation = {'payload': open(file_path, 'rb')}
        elif fil.startswith('waterfall'):
            observation = {'waterfall': open(file_path, 'rb')}
        elif fil.startswith('data'):
            observation = {'demoddata': open(file_path, 'rb')}
        else:
            LOGGER.debug('Ignore file: %s', fil)
            continue
        if '_' not in fil:
            continue
        observation_id = fil.split('_')[1]
        LOGGER.info('Trying to PUT observation data for id: %s', observation_id)
        url = urljoin(base_url, observation_id)
        if not url.endswith('/'):
            url += '/'
        LOGGER.debug('PUT file %s to network API', fil)
        LOGGER.debug('URL: %s', url)
        LOGGER.debug('Headers: %s', headers)
        LOGGER.debug('Observation file: %s', observation)
        response = requests.put(url,
                                headers=headers,
                                files=observation,
                                verify=settings.SATNOGS_VERIFY_SSL,
                                stream=True,
                                timeout=45)
        if response.status_code == 200:
            LOGGER.info('Success: status code 200')
            if settings.SATNOGS_COMPLETE_OUTPUT_PATH != "":
                os.rename(os.path.join(settings.SATNOGS_OUTPUT_PATH, fil),
                          os.path.join(settings.SATNOGS_COMPLETE_OUTPUT_PATH, fil))
            else:
                os.remove(os.path.join(settings.SATNOGS_OUTPUT_PATH, fil))
        elif response.status_code == 404:
            LOGGER.error('Bad status code: %s', response.status_code)
            os.rename(os.path.join(settings.SATNOGS_OUTPUT_PATH, fil),
                      os.path.join(settings.SATNOGS_INCOMPLETE_OUTPUT_PATH, fil))
        else:
            LOGGER.error('Bad status code: %s', response.status_code)


def get_jobs():
    """Query SatNOGS Network API to GET jobs."""
    gps_locator = locator.Locator(settings.SATNOGS_NETWORK_API_QUERY_INTERVAL * 60)
    gps_locator.update_location()
    LOGGER.info('Get jobs started')
    url = urljoin(settings.SATNOGS_NETWORK_API_URL, 'jobs/')
    params = {
        'ground_station': settings.SATNOGS_STATION_ID,
        'lat': settings.SATNOGS_STATION_LAT,
        'lon': settings.SATNOGS_STATION_LON,
        'alt': int(settings.SATNOGS_STATION_ELEV)
    }
    headers = {'Authorization': 'Token {0}'.format(settings.SATNOGS_API_TOKEN)}
    LOGGER.debug('URL: %s', url)
    LOGGER.debug('Params: %s', params)
    LOGGER.debug('Headers: %s', headers)
    LOGGER.info('Trying to GET observation jobs from the network')
    response = requests.get(url,
                            params=params,
                            headers=headers,
                            verify=settings.SATNOGS_VERIFY_SSL,
                            timeout=45)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        LOGGER.error(http_error)
        return

    latest_jobs = [str(job['id']) for job in response.json()]
    for job in SCHEDULER.get_jobs():
        if job.name == spawn_observer.__name__:
            if job.id not in latest_jobs:
                job.remove()

    for obj in response.json():
        start = parser.parse(obj['start'])
        job_id = str(obj['id'])
        kwargs = {'obj': obj}
        LOGGER.info('Adding new job: %s', job_id)
        LOGGER.debug('Observation obj: %s', obj)
        SCHEDULER.add_job(spawn_observer,
                          'date',
                          run_date=start,
                          id='{0}'.format(job_id),
                          kwargs=kwargs,
                          replace_existing=True)


def status_listener():
    LOGGER.info('Starting scheduler...')
    SCHEDULER.start()
    SCHEDULER.remove_all_jobs()
    interval = settings.SATNOGS_NETWORK_API_QUERY_INTERVAL
    SCHEDULER.add_job(get_jobs, 'interval', minutes=interval)
    msg = 'Registering `get_jobs` periodic task ({0} min. interval)'.format(interval)
    LOGGER.info(msg)
    interval = settings.SATNOGS_NETWORK_API_POST_INTERVAL
    msg = 'Registering `post_data` periodic task ({0} min. interval)'.format(interval)
    LOGGER.info(msg)
    SCHEDULER.add_job(post_data, 'interval', minutes=interval)


def get_observation_list():
    obs_list = SCHEDULER.get_jobs()
    return obs_list


def get_observation(job_id):
    obs = SCHEDULER.get_job(job_id)
    return obs
