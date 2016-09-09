PTYPE_DATA = 0
PTYPE_ACK = 1

MAGICNO = 0x497E
MAX_READ_SIZE = 512  # bytes
TIMEOUT = 1  # 1 second
PATH = './file.txt'
IP = '127.0.0.1'


class Packet:
    """The Packet Type"""

    def __init__(self, magicno, p_type, seqno, dataLen, data=None):
        # magicno: 0x497E if not print a failure message drop packet imediately
        self.magicno = magicno
        # ptype: dataPacket (0) or acknowledgementPacket (1)
        self.p_type = p_type
        # seqno: bit value 0 or 1
        self.seqno = seqno
        # dataLen: 0-512, num of user bytes
        self.dataLen = dataLen
        # data: depends on dataLength and contains the user data
        self.data = data

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
        if self.p_type == data_packet and self.dataLen == 0:
            # end of transmitted file
            return True
        else:
            return False

    def check_magicno(self):
        """Checks self.magicno = 0x497E else drops the packet"""
        if self.magicno != MAGICNO:
            # drop packet immediately
            return False
        else:
            return True

    def serialize(self):
        byte_magicno = self.magicno.to_bytes(2, byteorder='big')
        byte_p_type = self.p_type.to_bytes(1, byteorder='big')
        byte_seqno = self.seqno.to_bytes(1, byteorder='big')
        byte_data_len = self.dataLen.to_bytes(2, byteorder='big')

        byte_s = byte_magicno + byte_p_type + byte_seqno \
                    + byte_data_len + self.data
        return byte_s

    def deserialize(self):

        pass
