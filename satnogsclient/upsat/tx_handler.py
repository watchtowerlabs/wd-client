from satnogsclient.upsat import serial_handler
from satnogsclient.upsat import gnuradio_handler
import os
import logging

logger = logging.getLogger('satnogsclient')


def send_to_backend(buf):
    logger.debug('Send to backend called with backend %s', os.environ['BACKEND'])
    curr_backend = os.environ['BACKEND']
    print "what is backend? ", curr_backend
    if curr_backend != 'gnuradio' and curr_backend != 'serial':
        print "what is backend? ERROR ", curr_backend
        return 0
    if curr_backend == 'gnuradio':
        gnuradio_handler.write_to_gnuradio(buf)
        return 1
    if curr_backend == 'serial':
        print "going to write in serial"
        serial_handler.write_to_serial(buf)
        return 1
