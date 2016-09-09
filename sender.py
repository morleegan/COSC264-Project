from packet_class import *  # Our initialization and checks
import socket  # for sockets
import os
import sys
import argparse

PTYPE_DATA = 0
PTYPE_ACK = 1

MAGICNO = 0x497E
MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'



class Sender:
    """Sender Program"""

    def __init__(self, port_sin, port_sout, port_csin, file_name):
        self.sin = port_sin
        self.sout = port_sout
        self.csin = port_csin
        self.file_name = file_name
        self.socket_sin = self.create_sockets(self.sin)
        self.socket_sout = self.create_sockets(self.sout)
        self.file_in = None
        self.exit_flag = False
        self.check_file()
        self.send_next = 0

    def create_sockets(self, port):
        self.check_ports()
        # create sockets
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            new_socket.bind((IP, port))
            return new_socket
        except:
            print("Failed to create socket.")
            exit(-1)

    def check_ports(self):
        if all((not (1024 <= x <= 64000)) and isinstance(x, int) \
               for x in (self.sin, self.sout)):
            print("Invalid Port numbers")
            exit(-1)

    def outer_send(self):
        self.socket_sout.connect((IP, self.csin))
        sent_count = 0

        while not self.exit_flag:
            buffer = self.file_in.read(MAX_READ_SIZE)
            buffer_size = sys.getsizeof(buffer, bytes)

            if buffer_size == 0:
                packet_sent = Packet(MAGICNO, PTYPE_DATA, self.send_next, 0)
                self.exit_flag = True
            elif buffer_size > 0:
                packet_sent = Packet(MAGICNO, PTYPE_DATA, self.send_next,
                                     buffer_size, buffer)
            else:
                print("Impossible: Exiting")
                exit(-1)

            self.inner_send(packet_sent, sent_count)
            sent_count += 1

    def inner_send(self, packet_sent, sent_count):
        processing = True
        while processing:
            if not self.send_packet(self.socket_sout, packet_sent):
                continue

            if not self.socket_sin:
                print("Not socket_in")
                continue

            received = self.socket_sin.recv(MAX_READ_SIZE)
            print("Packet Received")
            if not received:
                continue
            else:
                if received.check_magicno() and received.check_ack_packet():
                    if received.seqno == self.send_next:
                        self.send_next = 1 - self.send_next
                        if self.exit_flag:
                            self.close_sockets()
                            print("{d}").format(sent_count)
                            exit(0)
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

    def send_packet(self, socket1, received):
        try:
            # change packet into bytes to send
            received = received.serialize()
            socket1.send(received)
            print("Packet sent")
            return True
        except:
            print("Connection Failed")
            return False

    def check_file(self):
        # check if supplied filename exits and is readable else exit sender
        if not(os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
            self.file_in = open(self.file_name, 'rb')
        else:
            print("Supplied file does not exist or is not readable")
            exit(-1)

    def close_sockets(self):
        self.socket_sin.close()
        self.socket_sout.close()
        self.file_in.close()

if __name__ == "__main__":

    args = argparse.ArgumentParser()

    args.add_argument("sin", help="Sender in port", type=int)
    args.add_argument("sout", help="Sender out port", type=int)
    args.add_argument("csin", help="Channel Sender in port", type=int)
    args.add_argument("file_in", help="Filename of sender", type=str)

    args = args.parse_args()

    sender = Sender(args.sin, args.sout, args.csin, args.file_in)
    sender.outer_send()
