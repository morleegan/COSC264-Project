
MAGICNO = 0x497E
PTYPE_DATA = 0
PTYPE_ACK = 1

class Packet:
    """The Packet"""
    
    def __init__(self, magicno, ptype, seqno, dataLen, data):
	# magicno: 0x497E if not print a failure message drop packet imediately
	self.magicno = magicno
	# ptype: dataPacket (0) or acknowledgementPacket (1)
	self.ptype = ptype
	# seqno: bit value 0 or 1
	self.seqno = seqno
	# dataLen: 0-512, num of user bytes
	self.dataLen = dataLen
	# data: depends on dataLength and contains the user data
	self.data = data
    
    def check_packet(self):
	"""Checks type of packet with length of packet"""
	if self.ptype == acknowledgementPacket and self.dataLen != 0:
	    # drop packet
	    pass
	
	if self.ptype == dataPacket and self.dataLen == 0:
	    # end of transmitted file
	    pass
    
    def check_magicno(self):
	"""Checks self.magicno = 0x497E else drops the packet"""
	if self.magicno != MAGICNO:
	    print("ERROR")
	    # drop packet imediately
