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
        self.csin = port_csin
        self.file_name = file_name
        self.socket_sin = self.create_sockets(port_sin)
        self.socket_sout = self.create_sockets(port_sout)
        self.file_in = None
        self.exit_flag = False
        self.check_file()
        self.send_next = 0

        self.packet_queue = []

    def create_sockets(self, port):
        self.check_ports(port)
        # create sockets
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            new_socket.bind((IP, port))
            # if port == self.sin:
            new_socket.settimeout(1)
            return new_socket
        except:
            print("Failed to create socket.")
            exit(-1)

    @staticmethod
    def check_ports(port):
        if all((not (1024 <= x <= 64000)) and isinstance(x, int) \
               for x in [port]):
            print("Invalid Port numbers")
            exit(-1)

    def load_packets(self):
        file_data = self.file_in.read()
        file_index = 0
        fine_length = len(file_data) + MAX_READ_SIZE
        while file_index > fine_length:
            buffer = file_data[file_index:file_index + MAX_READ_SIZE]
            new_packet = Packet(MAGICNO,
                                PTYPE_DATA,
                                self.send_next,
                                len(buffer),
                                buffer)
            self.packet_queue.append(new_packet)

            file_index += MAX_READ_SIZE

    def outer_send(self):
        self.socket_sout.connect((IP, self.csin))
        sent_count = 0
        counter = 1
        while not self.exit_flag:
            print(counter)
            if counter > len(self.packet_queue) or \
                            self.packet_queue[counter].dataLen() == 0:
                last = Packet(MAGICNO, PTYPE_DATA, self.send_next, 0)
                self.inner_send(last, sent_count)
                self.close_sockets()
                exit(0)

            self.inner_send(self.packet_queue[counter], sent_count)
            sent_count += 1
            counter += 1

    def inner_send(self, packet_sent, sent_count):
        processing = True
        while processing:
            if not Sender.send_packet(self.socket_sout, packet_sent):
                continue

            received = self.rec_packet()
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

                elif not self.exit_flag:
                    processing = False


    @staticmethod
    def send_packet(socket1, received):
        try:
            # change packet into bytes to send
            received = received.serialize()
            socket1.send(received)
            print("Packet sent")
            return True
        except:
            print("Connection Failed")
            return False

    def rec_packet(self):
        try:
            received_bytes = self.socket_sin.recv(MAX_READ_SIZE)
            received = Packet.deserialize(received_bytes)
            print("Successfully Received")
            return received
        except:
            print("Failed to Receive")

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
