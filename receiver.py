from packet_class import *  # Our initialization and checks
import os
import socket  # or sockets

PTYPE_DATA = 0
PTYPE_ACK = 1

MAGICNO = 0x497E
MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'


class Receiver:
    """Receiver Program"""

    def __init__(self, rin, rout, crin, file_name):
        self.rin = rin
        self.rout = rout
        self.crin = crin
        self.file_name = file_name
        self.socket_rin = self.create_sockets(self.rin)
        self.socket_rout = self.create_sockets(self.rout)

    def create_sockets(self, port):
        #  socket creation
        self.check_ports()
        try:
            #  accepts packets from channel
            new_socket = socket.socket(socket.AF_INET,
                                       socket.SOCK_DGRAM)
        except:
            #  ailed to create socket... quit
            exit(-1)

        # bind() both sockets
        new_socket.bind((IP, port))

        return new_socket


    def receive_socket(self):

        # connect() rout set default to port_num of crin
        self.socket_rout.connect((IP, self.crin))

        self.check_file()
        open(self.file_name)
        expected = 0  # local int var

        # if initialization successful then loop
        success = True
        while success:
            # wait on rin for incoming packet (use blocking call)
            received = self.socket_rin.recv(MAX_READ_SIZE)

            # once have received packet do checks
            # when different prepare ack packet
            if not self.check_failure(received, expected):
                received_ack = Packet(MAGICNO, PTYPE_ACK, received.seqno,
                                      0)
                # send packet via rout to channel
                self.socket_rout.send(received_ack)
                continue  # return to beginning of loop

            if received.seqno == expected:
                received_ack = Packet(MAGICNO, PTYPE_ACK, received.seqno, 0)
                self.socket_rout.send(received_ack)
                # send received_ack via rout to channel
                expected += 1

            if received.dataLen > 0:  # if received packet contains data then
                # append data to output file
                self.file_name.append(received.data)
                continue  # stop processing

            elif received.dataLen == 0:
                exit(0)  # exit program
                self.close_sockets()

            else:
                continue  # return to start of loop

    def check_failure(self, received_pack, expected):
            #  if packet is lost
            if received_pack.check_magicno() and received_pack.ptype == \
                    PTYPE_DATA or received_pack.seqno != expected:
                return False

    def check_ports(self):
        if not 1024 < self.rin < 64000 or 1024 < self.rout < 64000:
            print("the port numbers were not between 1024 and 64000")
            exit(-1)

    def check_file(self):
        open(self.file_name)
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            exit(-1)

    def close_sockets(self):
        self.file_name.close()  # close output file
        self.socket_rout.close()  # close all sockets
        self.socket_rin.close()




