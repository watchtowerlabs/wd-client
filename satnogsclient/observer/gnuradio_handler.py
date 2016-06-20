import array
import time
import logging
import json

from satnogsclient import packet_settings
from satnogsclient import settings as client_settings
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer import hldlc
from satnogsclient.observer import packet

logger = logging.getLogger('satnogsclient')

udp_local_sock = Udpsocket(('127.0.0.1',client_settings.UDP_CLIENT_PORT)) # Port in which client listens for frames from gnuradio
ecss_feeder_sock = Udpsocket([]) # The socket with which we communicate with the ecss feeder thread

def write(buf):
    udp_local_sock.sendto(buf, (client_settings.GNURADIO_IP,client_settings.GNURADIO_UDP_PORT))
    
def read_from_gnuradio():
    while True:
        conn = udp_local_sock.recv()
        buf_in = conn[0]
        hldlc_buf = bytearray(0)
        hldlc.HLDLC_deframe(buf_in, hldlc_buf)
        ecss_dict = []
        packet.ecss_depacketizer(hldlc_buf,ecss_dict)
        ecss_feeder_sock.sendto(json.dumps(ecss_dict),('127.0.0.1',client_settings.ECSS_LISTENER_UDP_PORT))