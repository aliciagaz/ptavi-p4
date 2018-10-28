#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys

class EchoHandler(socketserver.DatagramRequestHandler):
    
    def handle(self):
        
        address = self.client_address[0]
        port = self.client_address[1]
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            print("Cliente con IP " + str(address) +" y puerto " + str(port))
            print("El cliente manda: ", line.decode('utf-8'))
if __name__ == "__main__":
    
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), EchoHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
