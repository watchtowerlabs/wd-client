# -*- coding: utf-8 -*-
from urlparse import urljoin

import requests

from dateutil import parser

from satnogsclient import settings
from satnogsclient.observer.observer import Observer
from satnogsclient.scheduler import scheduler


def spawn_observation(*args, **kwargs):
    obj = kwargs.pop('obj')
    observer = Observer()
    tle = {
        'tle0': obj['tle0'],
        'tle1': obj['tle1'],
        'tle2': obj['tle2']
    }
    end = parser.parse(obj['end'])
    observer.location = {
        'lon': settings.GROUND_STATION_LON,
        'lat': settings.GROUND_STATION_LAT,
        'elev': settings.GROUND_STATION_ELEV
    }
    observer.setup(observation_id=obj['id'], tle=tle, observation_end=end, frequency=obj['frequency'])
    observer.observe()


def get_jobs():
    """Query SatNOGS Network API to GET jobs."""

    print 'Try getting Jobs from Network ..'

    url = urljoin(settings.NETWORK_API_URL, 'jobs')
    params = {'ground_station': settings.GROUND_STATION_ID}
    try:
        response = requests.get(url, params=params, verify=settings.CA_CERT)
    except:
        print 'HTTPs certificate verification failed..(ignore for now)'
        response = requests.get(url, params=params, verify=False)


    print response

    if not response.status_code == 200:
        raise Exception('Status code: {0} on request: {1}'.format(response.status_code, url))

    for job in scheduler.get_jobs():
        if job.name == spawn_observation.__name__:
            job.remove()

    for obj in response.json():
        start = parser.parse(obj['start'])
        job_id = str(obj['id'])
        kwargs = {'obj': obj}
        scheduler.add_job(spawn_observation, 'date', run_date=start, id=job_id, kwargs=kwargs)
