
from packet_class import * # Our initialization and checks
import argparse  # for command line arguments
import socket  # for sockets
import select  # for listening nicely on sockets
import random  # for uniform packet loss

IP = '127.0.0.1'

class channel:
    #parameters/ check all 
    #create/ bind the sockets 

    def __init__(self, c_sin, c_sout, c_rin, c_rout, sin, rin, p_rate):
        #parameters/ check all
        if not all(1024 <= x <= 64000 and isinstance(x, int) == True \
               for x in (c_sin, c_sout, c_rin, c_rout)):
            raise ValueError("Not correct port type")
        if not (0 <= p_rate < 1):
            raise ValueError("Not correct probability value")

        #create/ bind the sockets
        c_sin_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_sin_sock.bind(IP, c_sin)

        c_sout_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_sout_sock.bind(IP, c_sout)

        c_rin_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_rin_sock.bind(IP, c_rin)

        c_rout_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_rout_sock.bind(IP, c_rout)

        #connect all out sockets
        c_sout_sock.connect(IP, sin)
        c_rout_sock.connect(IP, rin)

        #set default port numbers used by sender
        #set them as distinct
        #infinite loop/ main
            loop_inf = 0
            while(loop_inf)

if __name__ == '__main__':

    # close all sockets
    c_sin_sock.close()
    c_sout_sock.close()
    c_rin_sock.close()
    c_rout_sock.close()

