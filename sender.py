from packet_class import *  # Our initialization and checks
# import argparse  # for command line arguments
import socket  # for sockets
import select  # for listening nicely on sockets
import os

MAX_READ_SIZE = 512
TIMEOUT = 1  # 1 second
IP = '127.0.0.1'
MAGICNO = 0x497E


def sender(port_sin, port_sout, c_sin, file_name):
    # checking port numbers
    if (1024 <= port_sin >= 64000) or not (isinstance(port_sin, int)) \
            or (1024 <= port_sout >= 64000) or not (isinstance(port_sout, int)):
        print("Invalid Port number")
        exit(-1)

    # create sockets
    sock_sin = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)  # accept packets from C-sout
    sock_sout = socket.socket(socket.AF_INET,
                              socket.SOCK_DGRAM)  # send to C-sin

    # bind() sockets
    sock_sin.bind((IP, port_sin))
    sock_sout.bind((IP, port_sout))

    # connect() sout
    sock_sout.connect(
        (IP, c_sin))  # set to default receiver to port_num of Csin

    # check if supplied filename exits and is readable else exit sender 
    if not (os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
        exit(-1)

    sender_next = 0  # local int var
    exit_flag = False  # local boolean flag

    # enter loop
    while True:
        # attempt to read up to 512 bytes from open file to local buffer
        with open(file_name, 'rb') as file_in:
            packet_buffer = file_in.read(MAX_READ_SIZE)

        # number of bytes read from file (up to 512 bytes)
        bytes_read = sys.getsizeof(packet_buffer)

        # create packet depending on n
        if bytes_read == 0:
            sender_packet = Packet(MAGICNO, 0, sender_next, 0, 0)
            exit_flag = True
        elif bytes_read > 0:
            sender_packet = Packet(MAGICNO, 0, sender_next, bytes_read,
                                   packet_buffer)
            #
            inner = True
            while inner:

                sent_packet_count = 0
                # sends packet
                sock_sout.send(sender_packet)
                sent_packet_count += 1

                # select() -timeout value of at most one second
                socket_list = [sock_sin, sys.stdin]
                read_sock, write_sock, error_sock, _ = select.select(
                    socket_list, [], [],
                    TIMEOUT)

                # checks before closing
                if read_sock:
                    if not (read_sock.magicno != MAGICNO or read_sock.ptype != 1
                            or read_sock.dataLen != 0 or read_sock.seqno != sender_next):
                        sender_next += 1

                        if exit_flag:
                            print('Total Packets Sent:', sent_packet_count)
                            file_name.close()
                            sock_sin.close()
                            sock_sout.close()
                        else:
                            inner = False
