#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dic_register= {}
    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            msg = line.decode('utf-8')
            
            lista_msg = msg.split(" ")
            address = self.client_address[0]
            port = self.client_address[1]
            
            if lista_msg[0] == "REGISTER":
                direction= lista_msg[1][lista_msg[1].rfind(":") +1:]
                print("\n" + "--> " + "Cliente con IP " + str(address) +
                      " y puerto " + str(port))
                print("\n" + "Envía: " + msg)
            elif lista_msg[0] == "Expires:":
                expires = lista_msg[1]
                self.dic_register[direction]= [address, expires]
                print("Expire: " + expires)
                if int(expires) == 0:
                    del self.dic_register[direction]
        print(self.dic_register)
        print("----------------------------------------------------------")

if __name__ == "__main__":
    
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
