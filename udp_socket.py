
import argparse
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
    args.add_argument("csout", help= "Channel Sender out port", type = int)
    args.add_argument("csin", help="Channel Sender in port", type=int)
    args.add_argument("crout", help="Channel Receiver out port", type=int)
    args.add_argument("crin", help="Channel Receiver in port", type=int)
    args.add_argument("sin", help="Sender in port", type=int)
    args.add_argument("sout", help="Sender out port", type=int)
    args.add_argument("rin", help="Receiver in port", type=int)
    args.add_argument("rout", help="Receiver out port", type=int)
    args.add_argument("prate", help="P rate", type=float)
    args.add_argument("file_in", help="Filename of sender", type=str)
    args.add_argument("file_out", help="Filename of receiver", type=str)
    args = args.parse_args()

    channel = Channel(args.csin, args.csout, args.crout, args.crin,
                      args.sin, args.rin, args.prate)
    channel.send_to()
    receiver = Receiver(args.rin, args.rout, args.crin, args.file_out)
    receiver.receive_socket()
    sender = Sender(args.sin, args.sout, args.csin, args.file_in)
    sender.outer_send()