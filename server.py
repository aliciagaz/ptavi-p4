#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa principal para un servidor UDP simple
"""
import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dic_register = {}

    def register2json(self):
        """
        Convierte nuestro registro (diccionario) en un fichero JSON
        """
        fich_json = open("registered.json", "w")
        json.dump(self.dic_register, fich_json)
        fich_json.close()

    def json2registered(self):
        """
        Comprueba que haya un fichero llamado registered.json y si existe,
        lee su contenido y lo mete en un diccionario de usuarios registrados
        """
        try:
            with open("registered.json", "r") as fich_json:
                self.dic_register = json.load(fich_json)
        except FileNotFoundError:
            self.dic_register = {}

    def time_out(self):
        """
        Comprueba si algún usuario ha caducado y si es así, lo borra del
        diccionario
        """
        lista = list(self.dic_register)
        for client in lista:
            time_expires = self.dic_register[client][1]
            gmt_actual = time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.gmtime(time.time()))
            if time_expires < gmt_actual:
                del self.dic_register[client]

    def handle(self):
        """
        Es el manejador del servidor, cuando llega un mensaje del cliente
        éste lo procesa. Si empieza por REGISTER guarda el usuario en nuestro
        diccionario y si empieza por EXPIRE podemos ver el tiempo de caducidad
        """
        self.json2registered()
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        for line in self.rfile:
            msg = line.decode('utf-8')

            lista_msg = msg.split(" ")
            address = self.client_address[0]
            port = self.client_address[1]

            if lista_msg[0] == "REGISTER":
                direction = lista_msg[1][lista_msg[1].rfind(":") + 1:]
                print("\n" + "--> " + "Cliente con IP " + str(address) +
                      " y puerto " + str(port))
                print("\n" + "Envía: " + msg)
            elif lista_msg[0] == "Expires:":
                expires = lista_msg[1]
                gmt_expires = time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.gmtime(time.time() +
                                                        int(expires)))
                self.dic_register[direction] = [address, gmt_expires]
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
