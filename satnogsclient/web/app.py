from flask import Flask, render_template, request, json, jsonify


from satnogsclient import settings as client_settings
from satnogsclient import packet_settings
from satnogsclient.scheduler import tasks
from satnogsclient.observer import packet
from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer import serial_handler
import logging
from flask.json import JSONDecoder
import binascii

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

@app.route('/raw', methods=['GET', 'POST'])
def get_raw():
    with open('/home/ctriant/hope', 'wb') as file_:
        file_.write(request.get_data());
    return request.get_data();

@app.route('/command', methods=['GET', 'POST'])
def get_command():
    requested_command = request.get_json();
    response = {}
    response['Response'] = 'This is a test response'
    if requested_command is not None:
        print 'Command received';
        if 'custom_cmd' in requested_command:
            if 'comms_tx_rf' in requested_command['custom_cmd']:
                response['Response'] = 'Comms is ' + requested_command['custom_cmd']['comms_tx_rf'];
                #TODO: Handle the comms_tx_rf request
                if ecss['command_type'] == 'comms_off' :
                    packet.comms_off();
                elif ecss['command_type'] == 'comms_on' :
                    packet.comms_on();
                return jsonify(response);
        elif 'ecss_cmd' in requested_command:
            response['Response'] = 'ECSS command send';
            ecss = {'app_id': int(requested_command['ecss_cmd']['PacketHeader']['PacketID']['ApplicationProcessID']),
                    'type': int(requested_command['ecss_cmd']['PacketHeader']['PacketID']['Type']),
                    'size' : 0,
                    'count' : 59,
                    'ser_type' : int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['ServiceType']),
                    'ser_subtype' : int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['ServiceSubType']),
                    'data' : bytearray(0),
                    'dest_id' : int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['SourceID']),
                    'ack': int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['Ack'])}
            buf = packet.construct_packet(ecss)
            serial_handler.write(buf)
            return jsonify(response);
    return render_template('control.j2')


@app.route('/')
def status():
    '''View status satnogs-client.'''
    return render_template('status.j2')

@app.route('/control/')
def control():
    '''Control status satnogs-client.'''
    return render_template('control.j2')


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
