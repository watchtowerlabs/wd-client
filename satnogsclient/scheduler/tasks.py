# -*- coding: utf-8 -*-
import logging
import os
import time
import sys
from datetime import datetime, timedelta
from satnogsclient import ecss_settings
from dateutil import parser
from urlparse import urljoin
from multiprocessing import Process, Queue
import json

import pytz
import requests

from satnogsclient import settings
from satnogsclient.observer.observer import Observer
from satnogsclient.receiver import SignalReceiver
from satnogsclient.scheduler import scheduler
from satnogsclient.observer.commsocket import Commsocket
from boto.dynamodb.condition import NULL



logger = logging.getLogger('satnogsclient')


def spawn_observer(*args, **kwargs):
    obj = kwargs.pop('obj')
    tle = {
        'tle0': obj['tle0'],
        'tle1': obj['tle1'],
        'tle2': obj['tle2']
    }
    end = parser.parse(obj['end'])

    observer = Observer()
    observer.location = {
        'lon': settings.GROUND_STATION_LON,
        'lat': settings.GROUND_STATION_LAT,
        'elev': settings.GROUND_STATION_ELEV
    }

    setup_kwargs = {
        'observation_id': obj['id'],
        'tle': tle,
        'observation_end': end,
        'frequency': obj['frequency']
    }

    logger.debug('Observer args: {0}'.format(setup_kwargs))
    setup = observer.setup(**setup_kwargs)

    if setup:
        logger.info('Spawning observer worker.')
        observer.observe()
    else:
        raise RuntimeError('Error in observer setup.')


def spawn_receiver(*args, **kwargs):
    obj = kwargs.pop('obj')
    logger.debug('Receiver args: {0}'.format(obj))
    receiver = SignalReceiver(obj['id'], obj['frequency'])
    logger.info('Spawning receiver worker.')
    receiver.run()
    end = parser.parse(obj['end'])

    while True:
        if datetime.now(pytz.utc) < end:
            time.sleep(1)
        else:
            receiver.stop()
            break


def post_data():
    """PUT observation data back to Network API."""
    base_url = urljoin(settings.NETWORK_API_URL, 'data/')
    headers = {'Authorization': 'Token {0}'.format(settings.API_TOKEN)}

    for f in os.walk(settings.OUTPUT_PATH).next()[2]:
        # Ignore files in receiving state
        if f.startswith('receiving'):
            continue
        observation_id = f.split('_')[1]
        logger.info('Trying to PUT observation data for id: {0}'.format(observation_id))
        file_path = os.path.join(*[settings.OUTPUT_PATH, f])
        observation = {'payload': open(file_path, 'rb')}
        url = urljoin(base_url, observation_id)
        if not url.endswith('/'):
            url += '/'
        logger.debug('PUT file {0} to network API'.format(f))
        logger.debug('URL: {0}'.format(url))
        logger.debug('Headers: {0}'.format(headers))
        logger.debug('Observation file: {0}'.format(observation))
        response = requests.put(url, headers=headers,
                                files=observation,
                                verify=settings.VERIFY_SSL)
        if response.status_code == 200:
            logger.info('Success: status code 200')
            dst = os.path.join(settings.COMPLETE_OUTPUT_PATH, f)
        else:
            logger.error('Bad status code: {0}'.format(response.status_code))
            dst = os.path.join(settings.INCOMPLETE_OUTPUT_PATH, f)
        os.rename(os.path.join(settings.OUTPUT_PATH, f), dst)


def get_jobs():
    """Query SatNOGS Network API to GET jobs."""
    url = urljoin(settings.NETWORK_API_URL, 'jobs/')
    params = {'ground_station': settings.GROUND_STATION_ID}
    headers = {'Authorization': 'Token {0}'.format(settings.API_TOKEN)}
    logger.debug('URL: {0}'.format(url))
    logger.debug('Params: {0}'.format(params))
    logger.debug('Headers: {0}'.format(headers))
    logger.info('Trying to GET observation jobs from the network')
    response = requests.get(url, params=params, headers=headers, verify=settings.VERIFY_SSL)


    if not response.status_code == 200:
        raise Exception('Status code: {0} on request: {1}'.format(response.status_code, url))

    for job in scheduler.get_jobs():
        if job.name in [spawn_observer.__name__, spawn_receiver.__name__]:
            job.remove()
            
    sock = Commsocket('127.0.0.1',5010)
    
    tasks = []
    for obj in response.json():
        tasks.append(obj)
        start = parser.parse(obj['start'])
        job_id = str(obj['id'])
        kwargs = {'obj': obj}
        receiver_start = start - timedelta(seconds=settings.DEMODULATOR_INIT_TIME)
        logger.info('Adding new job: {0}'.format(job_id))
        logger.debug('Observation obj: {0}'.format(obj))
        scheduler.add_job(spawn_observer,
                          'date',
                          run_date=start,
                          id='observer_{0}'.format(job_id),
                          kwargs=kwargs)
        scheduler.add_job(spawn_receiver,
                          'date',
                          run_date=receiver_start,
                          id='receiver_{0}'.format(job_id),
                          kwargs=kwargs)
    tasks.reverse()

    while sys.getsizeof(json.dumps(tasks)) > sock.tasks_buffer_size:
        tasks.pop()
    
    b = sock.connect()
    if b:
        sock.send_not_recv(json.dumps(tasks))    
    else:
        print 'Task listener thread not online'
    
        
def task_feeder(port1,port2):
    logger.info('Started task feeder')
    print port1,' ',port2
    sock = Commsocket('127.0.0.1',port1)
    sock.bind()
    q = Queue(maxsize=1)
    p = Process(target=task_listener, args=(port2,q))
    p.daemon = True
    p.start()
    sock.listen()
    while 1:
        conn = sock.accept()
        if conn:
            data = conn.recv(sock.tasks_buffer_size)
            if not q.empty():
                conn.send(q.get())
            else:
                conn.send('[]')
    p.join()

    
def task_listener(port,queue):
    logger.info('Started task listener')
    print port
    sock = Commsocket('127.0.0.1',port)
    sock.bind()
    sock.listen()
    while 1:
        conn = sock.accept()
        if conn:
            data = conn.recv(sock.tasks_buffer_size)
            if not queue.empty():
                queue.get()
                queue.put(data)
            else:
                queue.put(data)
                
def ecss_encoder(port):
    logger.info('Started ecss encoder')
    sock = Commsocket('127.0.0.1',port)
    sock.bind()
    sock.listen()
    while 1:
        conn = sock.accept()
        if conn:
            data = conn.recv(sock.tasks_buffer_size)
            packetizer(data)
                
def packetizer(buf):
    size = len(buf)
    assert((buf != NULL) == true)
    assert((size > ecss_settings.MIN_PKT_SIZE and size < ecss_settings.MAX_PKT_SIZE) == true)
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

    pkt_verification_state = ecss_settings.SATR_PKT_INIT

    if not ((pkt_app_id < ecss_settings.LAST_APP_ID) == true) :
        pkt_verification_state = ecss_settings.SATR_PKT_ILLEGAL_APPID
        #return SATR_PKT_ILLEGAL_APPID; 

    if not ((pkt_len == size - ecss_settings.ECSS_HEADER_SIZE - 1) == true):
        pkt_verification_state = ecss_settings.SATR_PKT_INV_LEN
        #return SATR_PKT_INV_LEN; 
    pkt_len = pkt_len - ecss_settings.ECSS_DATA_HEADER_SIZE - ecss_settings.ECSS_CRC_SIZE + 1;

    if not ((tmp_crc1 == tmp_crc2) == true) :
        pkt_verification_state = ecss_settings.SATR_PKT_INC_CRC
        #return SATR_PKT_INC_CRC; 

    if not((ecss_settings.SERVICES_VERIFICATION_TC_TM[pkt_ser_type][pkt_ser_subtype][pkt_type] == 1) == true) : 
        pkt_verification_state = ecss_settings.SATR_PKT_ILLEGAL_PKT_TP
        #return SATR_PKT_ILLEGAL_PKT_TP; 

    if not ((ver == ecss_settings.ECSS_VER_NUMBER) == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR; 

    if not ((tc_pus == ECSS_PUS_VER) == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR;

    if not ((ccsds_sec_hdr == ecss_settings.ECSS_SEC_HDR_FIELD_FLG) == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR;

    if not ((pkt_type == 'TC' or pkt_type == 'TM') == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR;

    if not ((dfield_hdr == ecss_settings.ECSS_DATA_FIELD_HDR_FLG) == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR;

    if not ((pkt_ack == ecss_settings.TC_ACK_NO or pkt_ack == ecss_settings.TC_ACK_ACC) == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR;

    if not ((pkt_seq_flags == ecss_settings.TC_TM_SEQ_SPACKET) == true) :
        pkt_verification_state = ecss_settings.SATR_ERROR
        #return SATR_ERROR; 
    pkt_data = bytearray(pkt_len)

    pktdata = buf[ecss_settings.ECSS_DATA_OFFSET : size -2]
    
    #return SATR_OK;
                
def ecss_decoder(port):
    logger.info('Started ecss decoder')
    sock = Commsocket('127.0.0.1',port)
    sock.bind()
    sock.listen()
    while 1:
        conn = sock.accept()
        if conn:
            data = conn.recv(sock.tasks_buffer_size)
            depacketizer(data)
         
         
            
def depacketizer(ecss):
    assert((ecss['type'] == 0) or (ecss['type'] == 1) == True )
    assert((ecss['app_id'] < ecss_settings.LAST_APP_ID) == True)
    data_size = ecss['size']
    packet_size = data_size + ecss_settings.ECSS_DATA_HEADER_SIZE + ecss_settings.ECSS_CRC_SIZE + ecss_settings.ECSS_HEADER_SIZE
    buf = bytearray(packet_size)
    app_id = ecss['app_id']
    app_id_ms = app_id & 0xFF00
    app_id_ls = app_id & 0x00FF
    buf[0] = ( ecss_settings.ECSS_VER_NUMBER << 5 | ecss['type'] 
               << 4 | ecss_settings.ECSS_DATA_FIELD_HDR_FLG << 3 | app_id_ms);
    buf[1] = app_id_ls
    seq_flags = ecss_settings.TC_TM_SEQ_SPACKET
    seq_count = ecss['count']
    seq_count_ms = seq_count & 0xFF00
    seq_count_ls = seq_count & 0x00FF
    buf[2] = (seq_flags << 6 | seq_count_ms)
    buf[3] = seq_count_ls
     
    if ecss['type'] == 0 :
        buf[6] = ecss_settings.ECSS_PUS_VER << 4 ;
    elif ecss['type'] == 1 :
        buf[6] = ( ecss_settings.ECSS_SEC_HDR_FIELD_FLG << 7 | ecss_settings.ECSS_PUS_VER << 4 | ecss['ack']);    
    buf[7] = ecss['ser_type']
    buf[8] = ecss['ser_subtype']
    buf[9] = ecss['dest_id']
    
    buf_pointer = ecss_settings.ECSS_DATA_OFFSET
    buf[buf_pointer:data_size] = ecss['data']
    data_w_headers = data_size + ecss_settings.ECSS_DATA_HEADER_SIZE + ecss_settings.ECSS_CRC_SIZE -1
    packet_size_ms = data_w_headers  & 0xFF00
    packet_size_ls = data_w_headers  & 0x00FF
    buf[4] = packet_size_ms
    buf[5] = packet_size_ls
    buf_pointer = buf_pointer + data_size
    
    for i in range(0,buf_pointer):
        buf[buf_pointer + 1] = buf[buf_pointer + 1] ^ buf[i]
    size = buf_pointer + 2
    assert((size > ecss_settings.MIN_PKT_SIZE and size < ecss_settings.MAX_PKT_SIZE) == True)
    print binascii.hexlify(buf)
            
