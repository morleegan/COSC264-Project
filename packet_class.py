PTYPE_DATA = 0
PTYPE_ACK = 1


class Packet:
    """The Packet"""
    MAGICNO = 0x497E

    def __init__(self, magicno: object, ptype: int, seqno: object, dataLen: object, data: object = None) -> object:
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
            data = []
        self.data = data

    def check_packet(self):
        """Checks type of packet with length of packet"""
        if self.ptype == acknowledgementPacket and self.dataLen != 0:
            # drop packet
            exit(-1)  # raise Exception("Corrupt Packet")

        if self.ptype == dataPacket and self.dataLen == 0:
            # end of transmitted file
            pass

    def check_magicno(self):
        """Checks self.magicno = 0x497E else drops the packet"""
        if self.magicno != MAGICNO:
            print("ERROR")
            return False
        else:
            return True

    def err_magicno(self):
        # drop packet imediately
        exit(-1)  # raise ValueError("ERROR: Expected value to be 0x497E")
