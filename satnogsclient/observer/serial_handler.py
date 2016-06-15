import serial
import array
import time

from satnogsclient import packet_settings
from satnogsclient import settings as client_settings




def write(buf):
    port = serial.Serial(client_settings.SERIAL_PORT, baudrate=9600, timeout=1.0)
    port.write(buf)
    
def read_from_serial():
    port = serial.Serial(client_settings.SERIAL_PORT, baudrate=9600, timeout=1.0)
    start_byte = bytes(packet_settings.HLDLC_START_FLAG)
    receiving = False;
    stored = bytearray(0)
    while True:
        buf_in = bytearray(port.read(packet_settings.MAX_PKT_SIZE))
        if buf_in.startswith(start_byte):
            if receiving == True:
                # i got start_byte without first getting the ending start_byte of previous frame
                stored = bytearray(0)
                receiving = False
                continue
            receiving = True;
            stored.extend(buf_in)
            if buf_in.endswith(start_byte):
                receiving = False
                reset_and_send(stored,buf_in)
                continue
        if buf_in.endswith(start_byte):
            if receiving == True:
                receiving = False;
                reset_and_send(stored,buf_in)
        else:
            if receiving == True:
                stored.extend(buf_in)

def reset_and_send(stored,buf_in):
    stored.extend(buf_in)
    # Here the "stored" array must be returned via a port or something
    stored = bytearray(0)   
    