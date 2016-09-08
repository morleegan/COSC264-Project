from packet_class import *  # Our initialization and checks
import socket  # for sockets
import select  # for listening nicely on sockets
import os
import sys

MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'

class Sender:

    def __init__(self, port_sin, port_sout, port_csin, file_name):
        self.s_in = port_sin
        self.s_out = port_sout
        self.c_sin = port_csin
        self.file_name = file_name

    def sender(self):
        """Sender Program"""
        if all((not (1024 <= x <= 64000)) and isinstance(x, int) \
               for x in (self.s_in, self.s_out)):
            print("Invalid Port numbers")
            exit(-1)

        # create sockets
        try:
            sock_sin = socket.socket(socket.AF_INET,
                                     socket.SOCK_DGRAM)  # accept packets from C-sout
            sock_sout = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM)  # send to C-sin
        except:
            print("Failed to create socket.")
            sys.exit()

        print("Socket created")

        # bind() sockets
        sock_sin.bind((IP, self.s_in))
        sock_sout.bind((IP, self.s_out))

        # connect() sout
        sock_sout.connect(
            (IP, self.s_in))  # set to default receiver to port_num of Csin

        # check if supplied filename exits and is readable else exit sender
        file_in = open(self.file_name, 'rb')
        if not (os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
            exit("Supplied file does not exist or is not readable")

        sender_next = 0  # local int var
        exit_flag = False  # local boolean flag
        sent_packet_count = 0

        # enter loop
        while not exit_flag:
            # attempt to read up to 512 bytes from open file to local buffer
            packet_buffer = file_in.read(MAX_READ_SIZE)
            n = sys.getsizeof(packet_buffer)  # number of bytes read from file

            # create packet depending on n
            if n == 0:
                sender_packet = Packet(MAGICNO, PTYPE_DATA, sender_next, 0)
                exit_flag = True
            elif n > 0:
                sender_packet = Packet(MAGICNO, PTYPE_DATA, sender_next, n,
                                       packet_buffer)
            else:
                print("n < 0, impossible")
                exit(-1)
            # switched sender data with buffer / you didn't need the extra statement

            # inner loop
            processing = True
            while processing:
                try:
                    sock_sout.send(sender_packet)
                    sent_packet_count += 1  # increase count of packets sent
                except:
                    print("Connection lost")
                    exit(-1)

                # select() -timeout value of at most one second
                # waiting for response on sock sin
                read_sock, write_sock, error_sock = select.select([sock_sin],
                                                                  [],
                                                                  [], TIMEOUT)

                if not read_sock:  # if nothing on socket, continue waiting
                    continue
                rcvd = read_sock.recv(
                    MAX_READ_SIZE)  # rcvd=data of received packet

                """ if no response packet, return to
                start of inner loop to re-transmit packet"""
                if not rcvd:
                    print("No response received, sending again")
                    continue  # return to start of inner loop to send again

                elif rcvd:  # received response packet
                    """ if checks fail return to start
                        of inner loop to re-transmit packet"""
                    if rcvd.check_magicno() and rcvd.check_ack_packet:
                        if rcvd.seqno == sender_next:
                            sender_next = 1 - sender_next
                            if exit_flag:
                                file_in.close()
                                sock_sin.close()
                                sock_sout.close()
                                print("{d}").format(sent_packet_count)
                                exit(0)

                            elif not exit_flag:
                                """" return to start of (outer)
                                    loop to read next block of data"""
                                continue
                        elif rcvd.seqno != sender_next:
                            continue  # return to start of inner loop to send again
                    else:
                        # return to start of inner loop to re-transmit packet
                        print("Packet failed checks")
                        continue  # return to start of inner loop to send again
