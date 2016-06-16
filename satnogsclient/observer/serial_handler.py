import serial
import array
import time
import logging

from satnogsclient import packet_settings
from satnogsclient import settings as client_settings
from satnogsclient.observer import hldlc
from satnogsclient.observer import packet

logger = logging.getLogger('satnogsclient')
port = serial.Serial(client_settings.SERIAL_PORT, baudrate=9600, timeout=1.0)


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

    