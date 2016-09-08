
from packet_class import * # Our initialization and checks
import os
import socket  # or sockets

MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'


class Receiver:
    def __init__(self, rin, rout, crin, file_name):
        self.rin = rin
        self.rout = rout
        self.crin = crin
        self.file_name = file_name

    def receiver(self):
        """Receiver Program"""
        if not 1024 < self.rin < 64000 or 1024 < self.rout < 64000:
            print("the port numbers were not between 1024 and 64000")
            exit(-1)

        try:  # creating sockets
            # accepts packets from C-rout
            sock_rin = socket.socket(socket.AF_INET,
                                     socket.SOCK_DGRAM)
            # sends to C-rin
            sock_rout = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM)
        except:
            raise Exception("Error: no sockets created")

        # bind() both sockets
        sock_rin.bind((IP, self.rin))
        sock_rout.bind((IP, self.rout))

        # connect() rout set default to port_num of crin
        sock_rout.connect((IP, self.crin))

        # initialization / check file_name so if it does
        open(self.file_name)
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            exit(-1)

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
                sock_rout.send(rcvd_ack)  # send rcvd_ack via rout to channel
                expected = 1 - expected

            if rcvd.dataLen > 0:  # if received packet contains data then
                self.file_name.append(rcvd.data)  # append data to output file and
                continue  # stop processing

            elif rcvd.dataLen == 0:
                self.file_name.close()
                sock_rin.close()  # close output file
                sock_rout.close()  # close all sockets
                exit(0)  # exit program

            else:
                continue  # return to start of loop

        """
        you shouldn't need this the program will close in the loop
        close(file_name) # close output file
        close(sock_rin)  # close all sockets
        close(sock_rout)
        """