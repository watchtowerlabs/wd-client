import logging
import socket
import binascii
import struct
import ctypes

from satnogsclient import packet_settings
from satnogsclient.observer.commsocket import Commsocket
from satnogsclient.observer.udpsocket import Udpsocket
from satnogsclient.observer import hldlc 

logger = logging.getLogger('satnogsclient')


                
def ecss_encoder(port):
    logger.info('Started ecss encoder')
    sock = Commsocket('127.0.0.1',port)
    sock.bind()
    sock.listen()
    while 1:
        conn = sock.accept()
        if conn:
            data = conn.recv(sock.tasks_buffer_size)
            ecss_packetizer(data)
                
def ecss_depacketizer(buf):
    size = len(buf)
    assert((buf != NULL) == true)
    assert((size > packet_settings.MIN_PKT_SIZE and size < packet_settings.MAX_PKT_SIZE) == true)
    tmp_crc1 = buf[size - 1];
    for i in range(0,size -2):
        tmp_src2 = tmp_src2 ^ buf[i]

    ver = buf[0] >> 5;

    pkt_type = (buf[0] >> 4) & 0x01;
    dfield_hdr = (buf[0] >> 3) & 0x01;

    pkt_app_id = buf[1];

    pkt_seq_flags = buf[2] >> 6;
    t = bytearray(2)
    t[0] = buf[2]
    t[1] = buf[3]
    t.reverse()
    pkt_seq_count = t & 0x3FFF;
    
    t = bytearray(2)
    t[0] = buf[4]
    t[1] = buf[5]
    t.reverse()

    pkt_len = t

    ccsds_sec_hdr = buf[6] >> 7;

    tc_pus = buf[6] >> 4;

    pkt_ack = 0x07 & buf[6];

    pkt_ser_type = buf[7];
    pkt_ser_subtype = buf[8];
    pkt_dest_id = buf[9];

    pkt_verification_state = packet_settings.SATR_PKT_INIT

    if not ((pkt_app_id < packet_settings.LAST_APP_ID) == true) :
        pkt_verification_state = packet_settings.SATR_PKT_ILLEGAL_APPID
        return packet_settings.SATR_PKT_ILLEGAL_APPID; 

    if not ((pkt_len == size - packet_settings.ECSS_HEADER_SIZE - 1) == true):
        pkt_verification_state = packet_settings.SATR_PKT_INV_LEN
        return packet_settings.SATR_PKT_INV_LEN; 
    pkt_len = pkt_len - packet_settings.ECSS_DATA_HEADER_SIZE - packet_settings.ECSS_CRC_SIZE + 1;

    if not ((tmp_crc1 == tmp_crc2) == true) :
        pkt_verification_state = packet_settings.SATR_PKT_INC_CRC
        return packet_settings.SATR_PKT_INC_CRC; 

    if not((packet_settings.SERVICES_VERIFICATION_TC_TM[pkt_ser_type][pkt_ser_subtype][pkt_type] == 1) == true) : 
        pkt_verification_state = packet_settings.SATR_PKT_ILLEGAL_PKT_TP
        return packet_settings.SATR_PKT_ILLEGAL_PKT_TP; 

    if not ((ver == packet_settings.ECSS_VER_NUMBER) == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR; 

    if not ((tc_pus == ECSS_PUS_VER) == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR;

    if not ((ccsds_sec_hdr == packet_settings.ECSS_SEC_HDR_FIELD_FLG) == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR;

    if not ((pkt_type == 'TC' or pkt_type == 'TM') == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR;

    if not ((dfield_hdr == packet_settings.ECSS_DATA_FIELD_HDR_FLG) == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR;

    if not ((pkt_ack == packet_settings.TC_ACK_NO or pkt_ack == packet_settings.TC_ACK_ACC) == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR;

    if not ((pkt_seq_flags == packet_settings.TC_TM_SEQ_SPACKET) == true) :
        pkt_verification_state = packet_settings.SATR_ERROR
        return packet_settings.SATR_ERROR; 
    pkt_data = bytearray(pkt_len)

    pktdata = buf[packet_settings.ECSS_DATA_OFFSET : size -2]
    
    return packet_settings.SATR_OK;
                
def ecss_decoder(port):
    logger.info('Started ecss decoder')
    sock = Commsocket('127.0.0.1',port)
    sock.bind()
    sock.listen()
    while 1:
        conn = sock.accept()
        if conn:
            data = conn.recv(sock.tasks_buffer_size)
            ecss_depacketizer(data)
         
         
            
def ecss_packetizer(ecss):
    sock = Commsocket(packet_settings.FRAME_RECEIVER_IP, packet_settings.FRAME_RECEIVER_PORT)
    assert((ecss['type'] == 0) or (ecss['type'] == 1) == True )
    assert((ecss['app_id'] < packet_settings.LAST_APP_ID) == True)
    data_size = ecss['size']
    packet_size = data_size + packet_settings.ECSS_DATA_HEADER_SIZE + packet_settings.ECSS_CRC_SIZE + packet_settings.ECSS_HEADER_SIZE
    buf = bytearray(packet_size)
    app_id = ecss['app_id']
    app_id_ms = app_id & 0xFF00
    app_id_ls = app_id & 0x00FF
    buf[0] = ( packet_settings.ECSS_VER_NUMBER << 5 | ecss['type'] 
               << 4 | packet_settings.ECSS_DATA_FIELD_HDR_FLG << 3 | app_id_ms);
    buf[1] = app_id_ls
    seq_flags = packet_settings.TC_TM_SEQ_SPACKET
    seq_count = ecss['count']
    seq_count_ms = seq_count & 0xFF00
    seq_count_ls = seq_count & 0x00FF
    buf[2] = (seq_flags << 6 | seq_count_ms)
    buf[3] = seq_count_ls
     
    if ecss['type'] == 0 :
        buf[6] = packet_settings.ECSS_PUS_VER << 4 ;
    elif ecss['type'] == 1 :
        buf[6] = ( packet_settings.ECSS_SEC_HDR_FIELD_FLG << 7 | packet_settings.ECSS_PUS_VER << 4 | ecss['ack']);    
    buf[7] = ecss['ser_type']
    buf[8] = ecss['ser_subtype']
    buf[9] = ecss['dest_id']
    
    buf_pointer = packet_settings.ECSS_DATA_OFFSET
    buf[buf_pointer:data_size] = ecss['data']
    data_w_headers = data_size + packet_settings.ECSS_DATA_HEADER_SIZE + packet_settings.ECSS_CRC_SIZE -1
    packet_size_ms = data_w_headers  & 0xFF00
    packet_size_ls = data_w_headers  & 0x00FF
    buf[4] = packet_size_ms
    buf[5] = packet_size_ls
    buf_pointer = buf_pointer + data_size
    
    for i in range(0,buf_pointer):
        buf[buf_pointer + 1] = buf[buf_pointer + 1] ^ buf[i]
    size = buf_pointer + 2
    assert((size > packet_settings.MIN_PKT_SIZE and size < packet_settings.MAX_PKT_SIZE) == True)
    hldlc.HLDLC_frame(buf)
    sock.send_not_recv(buf)
    return packet_settings.SATR_OK
    
def comms_off():
    sock = Udpsocket(packet_settings.FRAME_RECEIVER_IP, packet_settings.FRAME_RECEIVER_PORT)
    data = ctypes.create_string_buffer(25)
    data[0:9] = 'RF SW CMD'
    struct.pack_into("<I",data,9,0x593d55df)
    struct.pack_into("<I",data,13,0x4d2f84c0)
    struct.pack_into("<I",data,17,0x24d60191)
    struct.pack_into("<I",data,21,0x9287b5fd)
    d = bytearray(data)
    sock.send(d)    
    
def comms_on():
    sock = Udpsocket(packet_settings.FRAME_RECEIVER_IP, packet_settings.FRAME_RECEIVER_PORT)
    data = ctypes.create_string_buffer(25)
    data[0:9] = 'RF SW CMD'
    struct.pack_into("<I",data,9,0xda4942a9)
    struct.pack_into("<I",data,13,0xa7a45d61)
    struct.pack_into("<I",data,17,0x413981b)
    struct.pack_into("<I",data,21,0xa94ee2d3)
    d = bytearray(data)
    sock.send(d)    
