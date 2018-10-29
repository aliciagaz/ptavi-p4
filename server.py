#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys

class EchoHandler(socketserver.DatagramRequestHandler):
    dic_register= {}
    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            msg = line.decode('utf-8')
            print(msg)
            lista_msg = msg.split(" ")
            address = self.client_address[0]
            port = self.client_address[1]
            if lista_msg[0] == "REGISTER":
                direction= lista_msg[1][lista_msg[1].rfind(":") +1:]
                self.dic_register[direction]= [address]
                print("Cliente con IP " + str(address) +" y puerto " + str(port))
        
if __name__ == "__main__":
    
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), EchoHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
