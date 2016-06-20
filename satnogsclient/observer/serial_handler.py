import serial
import array
import time
import logging

from satnogsclient import packet_settings
from satnogsclient import settings as client_settings
from satnogsclient.observer import hldlc
from satnogsclient.observer import packet
from satnogsclient.observer.udpsocket import Udpsocket

logger = logging.getLogger('satnogsclient')
port = serial.Serial(client_settings.SERIAL_PORT, baudrate=9600, timeout=1.0)
ecss_feeder_sock = Udpsocket([]) # The socket with which we communicate with the ecss feeder thread

def write(buf):
    port.write(buf)
    
def read_from_serial():
    buf_in = bytearray(0)
    while True:
        c = port.read()
        if len(c) != 0:
            buf_in.append(c)
            if len(buf_in) == 1 and buf_in[0] != 0x7E:
                buf_in = bytearray(0)
            elif len(buf_in) > 1 and buf_in[len(buf_in) - 1] == 0x7E:
                hldlc_buf = bytearray(0)
                hldlc.HLDLC_deframe(buf_in, hldlc_buf)
                ecss_dict = []
                packet.ecss_depacketizer(hldlc_buf,ecss_dict)
                # dict must be sent to port
                buf_in = bytearray(0)
        ecss_feeder_sock.sendto(json.dumps(ecss_dict),('127.0.0.1',client_settings.ECSS_LISTENER_UDP_PORT))

    