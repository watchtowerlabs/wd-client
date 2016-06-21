import os

from satnogsclient.observer import packet
from satnogsclient import packet_settings
from satnogsclient import settings as client_settings
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer import hldlc
from satnogsclient.observer import packet

large_data_id = 0

socket = Udpsocket('127.0.0.1',client_settings.LD_UPLINK_LISTEN_PORT)
gnuradio_sock = Udpsocket(client_settings.GNURADIO_IP,client_settings.GNURADIO_UDP_PORT) #Gnuradio's udp listen port

def uplink(filename, info):
    buf = bytearray(0)
    fo = open(filename, "wb")
    available_data_len = packet_settings.MAX_PKT_SIZE - packet_settings.ECSS_HEADER_SIZE - packet_settings.ECSS_DATA_HEADER_SIZE - packet_settings.ECSS_CRC_SIZE
    file_size = os.stat(filename)[6]  # get size of file
    remaining_bytes = file_size
    total_packets = file_size +1 / available_data_len
    if file_size+1 % available_data_len >0:
        total_packets = total_packets + 1
    packet_count = 0 
    data_size = 0
    while remaining_bytes > 0:
        if remaining_bytes >= available_data_len:
            data_size = available_data_len
            remaining_bytes = remaining_bytes - available_data_len
        else:
            data_size = remaining_bytes
            remaining_bytes = 0
        if packet_count == 0:
            ser_subtype = packet_settings.TC_LD_FIRST_UPLINK
            data_size = data_size -1
            remaining_bytes = remaining_bytes +1
            buf = bytearray(fo.read(data_size))
            buf.insert(0,large_data_id)
        elif packet_count == total_packets - 1:
            ser_subtype = packet_settings.TC_LD_LAST_UPLINK
            buf = bytearray(fo.read(data_size))
        else:
            ser_subtype = packet_settings.TC_LD_INT_UPLINK
            buf = bytearray(fo.read(data_size))
        ecss ={'type': 1,
             'app_id': info['app_id'],
             'size': data_size,
             'ack': 1,
             'ser_type': packet_settings.TC_LARGE_DATA_SERVICE,
             'ser_subtype':ser_subtype,
             'dest_id': info['dest_id'],
             'data': buf,
             'seq_count' : packet_count
             }
        hldlc_buf = bytearray(0)
        packet.pack_packet(ecss, hldlc_buf)
        gnuradio_sock.send(hldlc_buf)
        got_ack = 0
        retries = 0
        while retries <3 or got_ack == 0:
            try:
                ack = socket.recv_timeout(client_settings.LD_UPLINK_TIMEOUT)
                ecss_dict = []
                packet.unpack_packet(buf_in, ecss_dict)
                if ecss_dict['seq_count'] == packet_count and ecss_dict['data'][0] == large_data_id:
                    got_ack = 1
                else:
                    gnuradio_sock.send(hldlc_buf) # Resend previous frame
                    retries = retries + 1
            except:
                retries = retries + 1
                print 'Timeout'
        if got_ack == 1:
            if ser_subtype == packet_settings.TC_LD_LAST_UPLINK:
                global large_data_id
                large_data_id = large_data_id +1
                packet_count = packet_count + 1
        else:
            print 'Abort'
            return
                
        
        
    
