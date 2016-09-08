
import argparse
from packet_class import *
from receiver import *
from sender import *
from channel import *

class UDPSocket:
    #  parent class

    def shared_function(self):
        #  accesses class properties
        pass

    def second_shared(param):
        # unable to access
        pass

if __name__ == "__main__":

    # This is where you'd do the argparse stuff

    args = argparse.ArgumentParser()

    args.add_argument("csin", help="Channel Sender in port", type=int)

    args = args.parse_args()

    sender = Sender(args.csin)
    channel = Channel(args.csin)
    receiver = Receiver(args.csin)