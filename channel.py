import argparse
import socket  # for sockets
import select  # for listening nicely on sockets
import random  # for uniform
from packet_class import *

PTYPE_DATA = 0
PTYPE_ACK = 1

MAGICNO = 0x497E
MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'



class Channel:
    """Channel Program"""
    def __init__(self, c_sin, c_sout, c_rout, c_rin, sin, rin, p_rate):
        self.c_sin = c_sin
        self.c_sout = c_sout
        self.c_rout = c_rout
        self.c_rin = c_rin
        self.sin = sin
        self.rin = rin
        self.p_rate = p_rate
        self.socket_sin = self.create_socket(self.c_sin)
        self.socket_sout = self.create_socket(self.c_sout)
        self.socket_rin = self.create_socket(self.c_rin)
        self.socket_rout = self.create_socket(self.c_rout)
        self.check_port()

    def create_socket(self, port):
        #  socket creation
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.bind((IP, port))
        return new_socket

    def connect_socket(self):
        self.socket_sout.connect((IP, self.sin))
        self.socket_rout.connect((IP, self.rin))

    def send_to(self):
        self.connect_socket()
        while True:
            socket_read, socket_write, error_socket = select.select(
                    [self.c_sin, self.c_rin], [], [])

            for sock in socket_read:
                if not sock.check_magicno():
                    #  if the socket does not have MAGICNO correct get next
                    continue
                received = sock.recv(MAX_READ_SIZE)
                random_var = random()
                if random_var < self.p_rate:
                    continue
                elif sock == self.socket_sin:
                    self.send_packet(self.socket_sin, received)
                elif sock == self.socket_rin:
                    self.send_packet(self.socket_rin, received)
                elif error_socket == TIMEOUT:
                    self.socket_close()

    def send_packet(self, socket1, received):
        try:
            # packet is sent on crout to rin
            socket1.send(received)
        except:
            print("Connection Failed")

    def check_p_rate(self):
        #  check p rate
        if not (0 <= self.p_rate < 1):
            exit(-1)

    def check_port(self):
        #  check port numbers
        if not all(1024 <= x <= 64000 and isinstance(x, int) is True
                   for x in (self.c_sin, self.c_sout, self.c_rin, self.c_rout)):
            exit(-1)

    def socket_close(self):
        self.socket_rin.close()
        self.socket_rout.close()
        self.socket_sin.close()
        self.socket_sout.close()


if __name__ == "__main__":

    args = argparse.ArgumentParser()
    args.add_argument("csout", help="Channel Sender out port", type=int)
    args.add_argument("csin", help="Channel Sender in port", type=int)
    args.add_argument("crout", help="Channel Receiver out port", type=int)
    args.add_argument("crin", help="Channel Receiver in port", type=int)
    args.add_argument("sin", help="Sender in port", type=int)
    args.add_argument("rin", help="Receiver in port", type=int)
    args.add_argument("prate", help="P rate", type=float)
    args = args.parse_args()

    channel = Channel(args.csin, args.csout, args.crout, args.crin,
                      args.sin, args.rin, args.prate)
