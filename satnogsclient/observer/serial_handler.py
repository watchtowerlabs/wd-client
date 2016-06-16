import serial
import array
import time
import logging

from satnogsclient import packet_settings
from satnogsclient import settings as client_settings


logger = logging.getLogger('satnogsclient')


def write(buf):
    logger.info('Test: write in serial')
    port.write(buf)
    
def read_from_serial():
    port = serial.Serial(client_settings.SERIAL_PORT, baudrate=9600, timeout=1.0)
    logger.info('Test: opened port')
    start_byte = bytes(packet_settings.HLDLC_START_FLAG)
    receiving = False;
    stored = bytearray(0)
    buf_in = bytearray(0)
    while True:
        c = port.read()
        if len(c) != 0:
            buf_in.append(c)
            print "Test: read byte ", c , " ", buf_in 
            if len(buf_in) == 1 and buf_in[0] != 0x7E:
                buf_in = bytearray(0)
                print 'Test: error byte'
            elif len(buf_in) > 1 and buf_in[len(buf_in) - 1] == 0x7E:
                print "Test rec pkt ", buf_in 
                buf_in = bytearray(0)

            # elif buf_in.startswith(start_byte):
            #     if receiving == True:
            #         # i got start_byte without first getting the ending start_byte of previous frame
            #         stored = bytearray(0)
            #         receiving = False
            #         continue
            #     receiving = True;
            #     stored.extend(buf_in)
            #     if buf_in.endswith(start_byte):
            #         receiving = False
            #         reset_and_send(stored,buf_in)
            #         continue
            # if buf_in.endswith(start_byte):
            #     if receiving == True:
            #         receiving = False;
            #         reset_and_send(stored,buf_in)
            # else:
            #     if receiving == True:
            #         stored.extend(buf_in)

def reset_and_send(stored,buf_in):
    stored.extend(buf_in)
    # Here the "stored" array must be returned via a port or something
    stored = bytearray(0)   
    