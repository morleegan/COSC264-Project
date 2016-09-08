
import socket  # for sockets
import select  # for listening nicely on sockets
import random  # for uniform
from packet_class.py import *


MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'


class Channel:
    """Channel Program"""
    def __init__(self,c_sin, c_sout, c_rout, c_rin, sin, rin, p_rate):
        self.c_sin = c_sin
        self.c_sout = c_sout
        self.c_rout = c_rout
        self.c_rin = c_rin
        self.sin = sin
        self.rin = rin
        self.p_rate = p_rate

    def channel(self):

        if not all(1024 <= x <= 64000 and isinstance(x, int) == True \
                   for x in (self.c_sin, self.c_sout, self.c_rin, self.c_rout)):
            raise ValueError("Not correct port type")

        if not (0 <= self.p_rate < 1):
            raise ValueError("Not correct probability value")
        c_sin_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_sin_sock.bind((IP, self.c_sin))

        c_sout_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_sout_sock.bind((IP, self.c_sout))

        c_rin_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_rin_sock.bind((IP, self.c_rin))

        c_rout_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_rout_sock.bind((IP, self.c_rout))

        c_sout_sock.connect((IP, self.sin))
        c_rout_sock.connect((IP, self.rin))

        # enter infinite loop
        while True:
            # use select in blocking fashion to save CPU time
            read_sock, write_sock, error_sock = select.select([self.c_sin,
                                                               self.c_rin],
                                                              [], [])
            for sock in read_sock:  # received packet on socket
                rcvd = sock.recv(MAX_READ_SIZE)
                if not sock.check_magicno():
                    continue  # stop processing and return to start of loop

                u = random().uniform()  # uniformly distributed random variate
                if u < self.p_rate:
                    continue  # stop processing and return to start of loop
                elif sock == self.c_sin:  # packet received on c_sin_sock:
                    try:
                        c_rout_sock.send(rcvd)  # packet is sent on crout to rin
                    except:
                        print("Connection Lost")
                        return
                elif sock == self.c_rin:  # packet received on c_rin_sock:
                    try:
                        c_sout_sock.send(rcvd)  # packet is sent on csout to sin
                    except:
                        print("Connection Lost")
                        return

        c_sin_sock.close()
        c_sout_sock.close()
        c_rin_sock.close()
        c_rout_sock.close()



