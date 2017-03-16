import logging
import cPickle
import subprocess

from satnogsclient.upsat import packet_settings
from satnogsclient import settings as client_settings
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.upsat import packet


logger = logging.getLogger('satnogsclient')

backend_listener_sock = Udpsocket(('0.0.0.0', client_settings.BACKEND_LISTENER_PORT))  # Port in which client listens for frames from gnuradio
ui_listener_sock = Udpsocket(('127.0.0.1', client_settings.BACKEND_FEEDER_PORT))
ecss_feeder_sock = Udpsocket([])  # The socket with which we communicate with the ecss feeder thread
backend_feeder_sock = Udpsocket([])
ld_socket = Udpsocket([])
ld_uplink_socket = Udpsocket([])
ld_downlink_socket = Udpsocket([])


def write_to_gnuradio(buf):
    backend_feeder_sock.sendto(buf, (client_settings.GNURADIO_IP, client_settings.GNURADIO_UDP_PORT))


def read_from_gnuradio():
    logger.info('Started gnuradio listener process')
    while True:
        conn = backend_listener_sock.recv()
        buf_in = bytearray(conn[0])
        ecss_dict = {}
        ret = packet.deconstruct_packet(buf_in, ecss_dict, "gnuradio")
        ecss_dict = ret[0]
        pickled = cPickle.dumps(ecss_dict)
        if len(ecss_dict) == 0:
            logger.error('Ecss Dictionary not properly constructed. Error occured')
            continue
        try:
            if ecss_dict['ser_type'] == packet_settings.TC_LARGE_DATA_SERVICE:
                if ecss_dict['ser_subtype'] <= 8:  # 8 is sthe maximum service subtype corresponding to Large Data downlink
                    ld_downlink_socket.sendto(pickled, ('127.0.0.1', client_settings.LD_DOWNLINK_LISTEN_PORT))
                else:
                    ld_uplink_socket.sendto(pickled, ('127.0.0.1', client_settings.LD_UPLINK_LISTEN_PORT))
            else:
                ecss_feeder_sock.sendto(pickled, ('127.0.0.1', client_settings.ECSS_FEEDER_UDP_PORT))
        except KeyError:
            logger.error('Ecss Dictionary not properly constructed. Error occured. Key \'ser_type\' not in dictionary')


def exec_gnuradio(observation_file, waterfall_file, freq, user_args, script_name):
    arguments = {'filename': observation_file,
                 'waterfall': waterfall_file,
                 'rx_device': client_settings.SATNOGS_RX_DEVICE,
                 'center_freq': str(freq),
                 'user_args': user_args,
                 'script_name': script_name}
    if user_args != '':
        if '--rx-freq=' in user_args:
            rx_freq = user_args.split('--rx-freq=')[1].split(' ')[0] 
        else:
            rx_freq = arguments['center_freq'];
        if '--rx-sdr-device=' in user_args:
            device = user_args.split('--rx-sdr-device=')[1].split(' ')[0]
        else:
            device = arguments['rx_device']
    arg_string = ' '
    arg_string += '--rx-sdr-device=' + device + ' '
    arg_string += '--file-path=' + arguments['filename'] + ' '
    arg_string += '--waterfall-file-path=' + arguments['waterfall'] + ' '
    arg_string += '--rx-freq=' + rx_freq + ' '
    logger.info('Starting GNUradio python script')
    proc = subprocess.Popen([arguments['script_name'] + " " + arg_string], shell=True)
    return proc
