from flask import Flask, render_template, request, json, jsonify
import binascii
import struct
import ctypes

from satnogsclient import settings as client_settings
from satnogsclient import ecss_settings
from satnogsclient.scheduler import tasks
from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.udpsocket import Udpsocket
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
                comms_status = requested_command['custom_cmd']['comms_tx_rf'];
                #TODO: Handle the comms_tx_rf request
                sock = Udpsocket('147.52.17.78', 16886)
                ecss = {'command_type':comms_status,
                        'app_id': 1,
                        'type': 1,
                        'size' : 0,
                        'count' : 59,
                        'ser_type' : 17,
                        'ser_subtype' : 1,
                        'data' : bytearray(0),
                        'dest_id' : 2,
                        'ack': 0}
                if ecss['command_type'] == 'comms_off' :
                    data = ctypes.create_string_buffer(25)
                    data[0:9] = 'RF SW CMD'
                    struct.pack_into("<I",data,9,0x593d55df)
                    struct.pack_into("<I",data,13,0x4d2f84c0)
                    struct.pack_into("<I",data,17,0x24d60191)
                    struct.pack_into("<I",data,21,0x9287b5fd)
                    d = bytearray(data)
                    print list(d)
                    sock.send(d)
                elif ecss['command_type'] == 'comms_on' :
                    data = ctypes.create_string_buffer(25)
                    data[0:9] = 'RF SW CMD'
                    struct.pack_into("<I",data,9,0xda4942a9)
                    struct.pack_into("<I",data,13,0xa7a45d61)
                    struct.pack_into("<I",data,17,0x413981b)
                    struct.pack_into("<I",data,21,0xa94ee2d3)
                    d = bytearray(data)
                    print list(d)
                    sock.send(d)
                else :
                    assert((ecss['type'] == 0) or (ecss['type'] == 1) == True )
                    assert((ecss['app_id'] < ecss_settings.LAST_APP_ID) == True)
                    data_size = ecss['size']
                    packet_size = data_size + ecss_settings.ECSS_DATA_HEADER_SIZE + ecss_settings.ECSS_CRC_SIZE + ecss_settings.ECSS_HEADER_SIZE
                    buf = bytearray(packet_size)
                    app_id = ecss['app_id']
                    app_id_ms = app_id & 0xFF00
                    app_id_ls = app_id & 0x00FF
                    buf[0] = ( ecss_settings.ECSS_VER_NUMBER << 5 | ecss['type']
                           << 4 | ecss_settings.ECSS_DATA_FIELD_HDR_FLG << 3 | app_id_ms);
                    buf[1] = app_id_ls
                    seq_flags = ecss_settings.TC_TM_SEQ_SPACKET
                    seq_count = ecss['count']
                    seq_count_ms = seq_count & 0xFF00
                    seq_count_ls = seq_count & 0x00FF
                    buf[2] = (seq_flags << 6 | seq_count_ms)
                    buf[3] = seq_count_ls

                    if ecss['type'] == 0 :
                        buf[6] = ecss_settings.ECSS_PUS_VER << 4 ;
                    elif ecss['type'] == 1 :
                        buf[6] = ( ecss_settings.ECSS_SEC_HDR_FIELD_FLG << 7 | ecss_settings.ECSS_PUS_VER << 4 | ecss['ack']);
                    buf[7] = ecss['ser_type']
                    buf[8] = ecss['ser_subtype']
                    buf[9] = ecss['dest_id']

                    buf_pointer = ecss_settings.ECSS_DATA_OFFSET
                    buf[buf_pointer:data_size] = ecss['data']
                    data_w_headers = data_size + ecss_settings.ECSS_DATA_HEADER_SIZE + ecss_settings.ECSS_CRC_SIZE -1
                    packet_size_ms = data_w_headers  & 0xFF00
                    packet_size_ls = data_w_headers  & 0x00FF
                    buf[4] = packet_size_ms
                    buf[5] = packet_size_ls
                    buf_pointer = buf_pointer + data_size

                    for i in range(0,buf_pointer):
                        buf[buf_pointer + 1] = buf[buf_pointer + 1] ^ buf[i]
                    size = buf_pointer + 2
                    assert((size > ecss_settings.MIN_PKT_SIZE and size < ecss_settings.MAX_PKT_SIZE) == True)
                    print binascii.hexlify(buf)

                    sock.send(buf)
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
