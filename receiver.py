
import * from packet_class.py # Our initialization and checks 
import sys 
import argparse
import socket  # for sockets
import select  # for listening nicely on sockets

    PATH = './file.txt'
    IP = 127.0.0.1

def reciever(port_rin, port_rout, file_name):
     

    if not 1024 < port_rin < 64000 or 1024 < port_rout < 64000
        print("the port numbers were not between 1024 and 64000")
        exit(-1)
     
    sock_rin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #accepts packets from C-rout
    sock_rout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #sends to C-rin
    
    # bind() both sockets
    sock_rin.bind(IP, port_rin)
    sock_rout.bind(IP, port_rout)
 
    # connect() rout set default to port_num of crin 
    
    #intialization / check file_name so if it does
    open(file_name)
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        exit(-1) 
    expected = 0 #local int var 
