import argparse
import sys
import socket
import select
import random

MAGICNO = 0x497E
PTYPE_DATA = 0
PTYPE_ACK = 1
MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'


class Packet:
    """The Packet Type"""

    def __init__(self, magicno, ptype, seqno, dataLen, data=None):
        # magicno: 0x497E if not print a failure message drop packet imediately
        self.magicno = magicno
        # ptype: dataPacket (0) or acknowledgementPacket (1)
        self.ptype = ptype
        # seqno: bit value 0 or 1
        self.seqno = seqno
        # dataLen: 0-512, num of user bytes
        self.dataLen = dataLen
        # data: depends on dataLength and contains the user data
        if data is None:
            self.data = []
        else:
            self.data.append(data)  # appending data

        """def check_ack_packet(self):
        #Checks the packet is an ack packet with length of ack packet
        if self.ptype == PTYPE_ACK:
            if self.dataLen != 0:
            # drop packet
                print("Corrupt Packet")
                return False
            # raise Exception("Corrupt Packet")
            else:
                return True"""

    def check_end_data_packet(self, data_packet):
        """Checks if end of transmission"""
        if self.ptype == data_packet and self.dataLen == 0:
            # end of transmitted file
            return True
        else:
            return False

    def check_magicno(self):
        """Checks self.magicno = 0x497E else drops the packet"""
        if self.magicno != MAGICNO:
            # drop packet imediately
            return False
        else:
            return True


def sender(port_sin, port_sout, port_csin, file_name):
    """Sender Program"""

    if all((not (1024 <= x <= 64000)) and isinstance(x, int) \
           for x in (port_sin, port_sout)):
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
    sock_sin.bind((IP, port_sin))
    sock_sout.bind((IP, port_sout))

    # connect() sout
    sock_sout.connect(
        (IP, port_csin))  # set to default receiver to port_num of Csin

    # check if supplied filename exits and is readable else exit sender
    file_in = open(file_name, 'rb')
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
            read_sock, write_sock, error_sock = select.select([sock_sin], [],
                                                              [], TIMEOUT)

            if not read_sock:  # if nothing on socket, continue waiting
                continue
            rcvd = read_sock.recv(MAX_READ_SIZE)  # rcvd=data of received packet

            """ if no response packet, return to
                start of inner loop to re-transmit packet"""
            if not rcvd:
                print("No response received, sending again")
                continue  # return to start of inner loop to send again

            elif rcvd:  # received response packet
                """ if checks fail return to start
                    of inner loop to re-transmit packet"""
                if rcvd.check_magicno() == True \
                        and rcvd.check_ack_packet == True:
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



def channel(c_sin, c_sout, c_rin, c_rout, sin, rin, p_rate):
    """Channel Program"""

    if not all(1024 <= x <= 64000 and isinstance(x, int) == True \
               for x in (c_sin, c_sout, c_rin, c_rout)):
        raise ValueError("Not correct port type")

    if not (0 <= p_rate < 1):
        raise ValueError("Not correct probability value")
    c_sin_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_sin_sock.bind((IP, c_sin))

    c_sout_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_sout_sock.bind((IP, c_sout))

    c_rin_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_rin_sock.bind((IP, c_rin))

    c_rout_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_rout_sock.bind((IP, c_rout))

    c_sout_sock.connect((IP, sin))
    c_rout_sock.connect((IP, rin))

    # enter infinite loop
    while True:
        # use select in blocking fashion to save CPU time
        read_sock, write_sock, error_sock = select.select([c_sin, c_rin], [],
                                                          [])
        for sock in read_sock:  # received packet on socket
            rcvd = sock.recv(MAX_READ_SIZE)
            if not sock.check_magicno():  # i know it shouldn't be packet... Believe it is actually sock or rcvd
                continue  # stop processing and return to start of loop

            u = random()  # uniformly distributed random variate
            if u < p_rate:
                continue  # stop processing and return to start of loop
            elif sock == c_sin:  # packet received on c_sin_sock:
                try:
                    c_rout_sock.send(rcvd)  # packet is sent on crout to rin
                except:
                    print("Connection Lost")
                    return
            elif sock == c_rin:  # packet received on c_rin_sock:
                try:
                    c_sout_sock.send(rcvd)  # packet is sent on csout to sin
                except:
                    print("Connection Lost")
                    return

    c_sin_sock.close()
    c_sout_sock.close()
    c_rin_sock.close()
    c_rout_sock.close()


def reciever(port_rin, port_rout, port_crin, file_name):
    """Receiver Program"""

    if not 1024 < port_rin < 64000 or 1024 < port_rout < 64000:
        print("the port numbers were not between 1024 and 64000")
        exit(-1)

    try:  # creating sockets
        sock_rin = socket.socket(socket.AF_INET,
                                 socket.SOCK_DGRAM)  # accepts packets from C-rout
        sock_rout = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)  # sends to C-rin
    except:
        raise Exception("Error: no sockets created")

    # bind() both sockets
    sock_rin.bind((IP, port_rin))
    sock_rout.bind((IP, port_rout))

    # connect() rout set default to port_num of crin 
    sock_rout.connect((IP, port_crin))

    # initialization / check file_name so if it does
    open(file_name)
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
            file_name.append(rcvd.data)  # append data to output file and
            continue  # stop processing

        elif rcvd.dataLen == 0:
            file_name.close()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # somehow read from command line
