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

    def create_sockets(self,port):
        #socket creation
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
        socket_rout = self.create_sockets(self.rout)
        socket_rin = self.create_sockets(self.rin)

        # connect() rout set default to port_num of crin
        socket_rout.connect((IP, self.crin))

        self.check_file()
        expected = 0  # local int var

        # if initialization successful then loop
        success = True
        while success:
            # wait on rin for incoming packet (use blocking call)
            rcvd = sock_rin.recv(MAX_READ_SIZE)

            # once have received packet do checks
            if rcvd.check_magicno() and rcvd.ptype == PTYPE_DATA or \
                            rcvd.seqno != expected:
                # when different prepare ack packet
                rcvd_ack = Packet(MAGICNO, PTYPE_ACK, rcvd.seqno, 0)
                sock_rout.send(rcvd_ack)  # send packet via rout to channel
                continue  # stop processing

            if rcvd.seqno == expected:
                rcvd_ack = Packet(MAGICNO, PTYPE_ACK, rcvd.seqno, 0)
                sock_rout.send(
                    rcvd_ack)  # send rcvd_ack via rout to channel
                expected = 1 - expected

            if rcvd.dataLen > 0:  # if received packet contains data then
                self.file_name.append(
                    rcvd.data)  # append data to output file and
                continue  # stop processing

            elif rcvd.dataLen == 0:
                exit(0)  # exit program
                self.close_sockets()

            else:
                continue  # return to start of loop

    def check_ports(self):
        if not 1024 < self.rin < 64000 or 1024 < self.rout < 64000:
            print("the port numbers were not between 1024 and 64000")
            exit(-1)

    def check_file(self):
        open(self.file_name)
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            exit(-1)

    def close_sockets(self, socket1, socket2):
        self.file_name.close()  # close output file
        socket1.close()  # close all sockets
        socket2.close()


