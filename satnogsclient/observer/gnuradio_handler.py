import array
import time
import logging

from satnogsclient import packet_settings
from satnogsclient import settings as client_settings
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer import hldlc
from satnogsclient.observer import packet

logger = logging.getLogger('satnogsclient')

gnuradio_sock = Udpsocket(client_settings.GNURADIO_IP,client_settings.GNURADIO_UDP_PORT) #Gnuradio's udp listen port
udp_local_sock = Udpsocket('127.0.0.1',client_settings.UDP_CLIENT_PORT) # Port in which client listens for frames from gnuradio

def write(buf):
    gnuradio_sock.send(buf)
    
def read_from_gnuradio():
    while True:
        buf_in = udp_local_sock.listen()
        hldlc_buf = bytearray(0)
        hldlc.HLDLC_deframe(buf_in, hldlc_buf)
        ecss_dict = []
        packet.ecss_depacketizer(hldlc_buf,ecss_dict)
    