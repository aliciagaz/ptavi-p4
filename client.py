#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys

SERVER = sys.argv[1]
PORT = int(sys.argv[2])
REGISTER = sys.argv[3]
DIRECTION = sys.argv[4]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    if REGISTER == "register":
        MSG = ("REGISTER sip:" + DIRECTION + " SIP/2.0\r\n")
        print("Enviando:", MSG)
        my_socket.send(bytes(MSG, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))
      
print("Socket terminado.")
