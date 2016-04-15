from flask import Flask, render_template, request, json, jsonify

from satnogsclient import settings as client_settings
from satnogsclient.scheduler import tasks
from satnogsclient.observer.commsocket import Commsocket
import logging
from flask.json import JSONDecoder

logger = logging.getLogger('satnogsclient')
app = Flask(__name__)


@app.route('/update_status', methods=['GET', 'POST'])
def get_status_info():
    current_pass_json = {}
    scheduled_pass_json = {}
    current_pass_json['azimuth'] = 'NA'
    current_pass_json['altitude'] = 'NA'
    current_pass_json['frequency'] = 'NA'
    current_pass_json['tle0'] = 'NA'
    current_pass_json['tle1'] = 'NA'
    current_pass_json['tle2'] = 'NA'
    #current_pass_json = jsonify(current_pass_json)
    scheduled_pass_json['Info'] = 'There are no scheduled observations.'
    #scheduled_pass_json = jsonify(scheduled_pass_json)

    current_pass_sock = Commsocket('127.0.0.1',5005)
    scheduled_pass_sock = Commsocket('127.0.0.1',5011)

    current_pass_check = current_pass_sock.connect()
    scheduled_pass_check = scheduled_pass_sock.connect()

    if scheduled_pass_check:
        scheduled_pass_json = scheduled_pass_sock.send("Requesting scheduled observations\n")
        scheduled_pass_json = json.loads(scheduled_pass_json)
    else:
        print 'No observation currently'

    if current_pass_check:
        current_pass_json = current_pass_sock.send("Requesting current observations\n")
        current_pass_json = json.loads(current_pass_json)
    else:
        print 'No observations currently'

    #return current_pass_json
    return jsonify(observation=dict(current=current_pass_json, scheduled=scheduled_pass_json))


@app.route('/')
def status():
    '''View status satnogs-client.'''
    return render_template('status.j2')
    

@app.route('/configuration/')
def configuration():
    '''View list of satnogs-client settings.'''
    filters = [
        lambda x: not x.startswith('_'),
        lambda x: x.isupper()
    ]

    entries = client_settings.__dict__.items()
    settings = filter(lambda (x, y): all(f(x) for f in filters), entries)

    ctx = {
        'settings': sorted(settings, key=lambda x: x[0])
    }

    return render_template('configuration.j2', **ctx)
