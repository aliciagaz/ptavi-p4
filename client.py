#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""
import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    REGISTER = sys.argv[3]
    DIRECTION = sys.argv[4]
    EXPIRES = sys.argv[5]

except IndexError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    if REGISTER == "register":
        MSG = ("REGISTER sip:" + DIRECTION + " SIP/2.0\r\n" +
               "Expires: " + str(EXPIRES) + "\r\n\r\n")
        print("Enviando:", MSG)
        my_socket.send(bytes(MSG, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
