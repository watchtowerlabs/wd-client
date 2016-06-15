from satnogsclient import packet_settings

import socket


def HLDLC_deframe(buf_in):
    assert(buf_in != 0)
    assert(buf_in[0] == packet_settings.HLDLC_START_FLAG)
    assert(len(buf_in) <= packet_settings.UART_BUF_SIZE)
    size = len(buf_in)
    cnt = 0
    buf_out = bytearray(0)
    for i in range(1,size) :
        if buf_in[i] == packet_settings.HLDLC_START_FLAG:
            return packet_settings.SATR_EOT;
        elif buf_in[i] == packet_settings.HLDLC_CONTROL_FLAG:
            i = i+1
            if not (i < size - 1) == true:
                return packet_settings.SATR_ERROR
            if buf_in[i] == 0x5E:
                 buf_out.append(0x7E)
                 cnt = cnt+1
            elif buf_in[i] == 0x5D: 
                buf_out.append(0x7D)
                cnt = cnt+1
            else: 
                return packet_settings.SATR_ERROR
        else:
            buf_out.append(buf_in[i]);
            cnt=cnt+1
    return packet_settings.SATR_ERROR;

def HLDLC_frame(buf_in):

    assert(buf_in != 0)
    assert(len(buf_in) <= packet_settings.MAX_PKT_SIZE)

    cnt = 2;
    size = len(buf_in)
    buf_out = bytearray(0)

    for i in range(0,size) :
        if i == 0 :
            buf_out.append(packet_settings.HLDLC_START_FLAG)
            buf_out.append(buf_in[0])
        elif i == size - 1:
            if buf_in[i] == packet_settings.HLDLC_START_FLAG:
                buf_out.append(packet_settings.HLDLC_CONTROL_FLAG)
                buf_out.append(0x5E);
            elif buf_in[i] == packet_settings.HLDLC_CONTROL_FLAG:
                buf_out.append(packet_settings.HLDLC_CONTROL_FLAG)
                buf_out.append(0x5D)
            else:
                buf_out.append(buf_in[i])
            buf_out.append(packet_settings.HLDLC_START_FLAG)
            HLDLC_deframe(buf_out)
            return packet_settings.SATR_EOT
        elif buf_in[i] == packet_settings.HLDLC_START_FLAG: 
            buf_out.append(packet_settings.HLDLC_CONTROL_FLAG)
            buf_out.append(0x5E)
        elif buf_in[i] == packet_settings.HLDLC_CONTROL_FLAG:
            buf_out.append(packet_settings.HLDLC_CONTROL_FLAG)
            buf_out.append(0x5D)
        else:
            buf_out.append(buf_in[i])
    return packet_settings.SATR_ERROR;


