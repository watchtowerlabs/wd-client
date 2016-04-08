# -*- coding: utf-8 -*-
import logging
import socket


logger = logging.getLogger('satnogsclient')


class Udpsocket:
    """
    Handles connectivity with remote ctl demons
    Namely: rotctl and rigctl
    
    """

    _BUFFER_SIZE = 2048
    _connected = False

    def __init__(self, ip, port):
        self._UDP_IP = ip
        self._UDP_PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
       

    @property
    def ip(self):
        return self._UDP_IP

    @ip.setter
    def ip(self, new_ip):
        self._UDP_IP = new_ip

    @property
    def port(self):
        return self._UDP_PORT

    @port.setter
    def port(self, new_port):
        self._UDP_PORT = new_port

    @property
    def buffer_size(self):
        return self._BUFFER_SIZE

    @buffer_size.setter
    def buffer_size(self, new_buffer_size):
        self._BUFFER_SIZE = new_buffer_size

    @property
    def is_connected(self):
        return self._connected
    
    def get_sock(self):
        return self.s

    def send(self, message):
        self.s.sendto(message,(self._UDP_IP , self._UDP_PORT))
        
    def listen_non_block(self):
        
        data, addr = self.s.recvfrom(1024)
        return data

