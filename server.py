#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time
import json

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dic_register= {}
    
    def register2json(self):
        json_file = open ("registered.json", "w")
        json.dump(self.dic_register, json_file)
        json_file.close()

    def json2registered(self): 
        try:
            with open ("registered.json", "r") as json_file:
               self.dic_register = json.load(json_file)
        except FileNotFoundError:
            self.dic_register = {}

    def time_out(self):
        lista = list(self.dic_register)
        for client in lista:
            time_expires = self.dic_register[client][1]
            gmt_actual = time.strftime("%Y-%m-%d %H:%M:%S", 
                                        time.gmtime(time.time()))
            if time_expires < gmt_actual:
                del self.dic_register[client]

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
                gmt_expires = time.strftime("%Y-%m-%d %H:%M:%S", 
                                        time.gmtime(time.time() + 
                                                    int(expires)))
                self.dic_register[direction]= [address, gmt_expires]
                print("Expire: " + expires)
                if int(expires) == 0:
                    del self.dic_register[direction]
        self.register2json()
        self.time_out()
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
