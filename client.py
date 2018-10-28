#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys

SERVER = sys.argv[1]
PORT = int(sys.argv[2])
LINE = " ".join(sys.argv[3:])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
