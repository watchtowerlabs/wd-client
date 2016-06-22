from flask import Flask, render_template, request, json, jsonify


from satnogsclient import settings as client_settings
from satnogsclient import packet_settings
from satnogsclient.scheduler import tasks
from satnogsclient.observer import packet
from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer import serial_handler
from satnogsclient.observer import gnuradio_handler
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

    current_pass_sock = Commsocket('127.0.0.1',client_settings.CURRENT_PASS_TCP_PORT)
    scheduled_pass_sock = Commsocket('127.0.0.1',client_settings.TASK_FEEDER_TCP_PORT)

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

@app.route('/control_rx', methods=['GET', 'POST'])
def get_control_rx():
    sock = Udpsocket(('127.0.0.1',client_settings.CLIENT_LISTENER_UDP_PORT))
    try:
        conn = sock.send_listen("Requesting received packets", ('127.0.0.1',client_settings.ECSS_FEEDER_UDP_PORT))
        data = conn[0]
        packet_list = json.loads(data)
    except:
        logger.error("An error with the ECSS feeder occured")
    """
    The received 'packet_list' is a json string containing packets. Actually it is a list of dictionaries:
    each dictionary has the ecss fields of the received packet. In order to get each dictionary 2 things must be done
    The first json.loads(packet_list) will give a list of json strings representing the dictionaries.
    Next, for each item in list, json.dumps(item) will give the ecss dictionary
    """
    ecss_rx_packet = {};
    ecss_rx_packet['ECSS_RX'] = 'Hello world! Space calling';
    print '----------------------------------------------------';
    print(jsonify(ecss_rx_packet));
    return jsonify(ecss_rx_packet);

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
                #TODO: Handle the comms_tx_rf request
                if requested_command['custom_cmd']['comms_tx_rf'] == 'comms_off' :
                    packet.comms_off();
                    response['Response'] = 'COMMS_OFF command sent';
                elif requested_command['custom_cmd']['comms_tx_rf'] == 'comms_on' :
                    packet.comms_on();
                    response['Response'] = 'COMMS_ON command sent';
                return jsonify(response);
        elif 'ecss_cmd' in requested_command:
            response['Response'] = 'ECSS command send';
            ecss = {'app_id': int(requested_command['ecss_cmd']['PacketHeader']['PacketID']['ApplicationProcessID']),
                    'type': int(requested_command['ecss_cmd']['PacketHeader']['PacketID']['Type']),
                    'size' : 0,
                    'seq_count' : 59,
                    'ser_type' : int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['ServiceType']),
                    'ser_subtype' : int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['ServiceSubType']),
                    'data' :requested_command['ecss_cmd']['PacketDataField']['ApplicationData'],#bytearray(0),
                    'dest_id' : int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['SourceID']),
                    'ack': int(requested_command['ecss_cmd']['PacketDataField']['DataFieldHeader']['Ack'])}
            print "CMD", ecss
            
            buf = packet.construct_packet(ecss)
            if requested_command['backend'] == 'serial':
                print "CMD to Serial"
                serial_handler.write(buf)
            #else gnu radio
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
