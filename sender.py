
import * from packet_class.py # Our initialization and checks    
import argparse  # for command line arguments
import socket  # for sockets
import select  # for listening nicely on sockets

MAX_READ_SIZE = 512
TIMEOUT = 1 # 1 second

def sender(port_sin, port_sout, c_sin, file_name):
    
    # checking port numbers
    if all((not (1024 <= x <= 64000)) and isinstance(x, int) \
           for x in (port_sin, port_sout)):
        print("Invalid Port numbers")
        exit(-1)
    
    # create sockets
    sock_sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #accept packets from C-sout
    sock_sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #send to C-sin
    
    # bind() sockets
    sock_sin.bind((IP, port_sin))
    sock_sout.bind((IP, port_sout))
    
    # connect() sout
    sock_sout.connect((IP, c_sin)) # set to default receiver to port_num of Csin
    
    # check if supplied filename exits and is readable else exit sender 
    if not (os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
        exit("Supplied file does not exist or is not readable")
    
    sender_next = 0     # local int var
    exit_flag = False   # local boolean flag
    
    	# enter loop
      	# attempt to read up to 512 bytes from open file to local buffer
      	with open(file_name, 'rb') as file_in:
        	sender_data = file_in.read(MAX_READ_SIZE)
    	# n = number of bytes read from file (up to 512 bytes)
     	n = sys.getsizeof(sender_data)
      
     	# create packet depending on n
     	if n == 0:
        	sender_packet = Packet(MAGICNO, dataPacket, sender_next, 0)
        	exit_flag = True
    	elif n > 0:
        	sender_packet = Packet(MAGICNO, dataPacket, sender_next, n, sender_data)
      
    	packet_buffer = sender_packet # ???
    	 
    		# inner loop
	        sent_packet_count = 0
	        sock_sout.send(packet_buffer)
	        # select() -timeout value of at most one second
	        socket_list = [sock_sin, sys.stdin]
	        read_sock, write_sock, error_sock = select.select(socket_list,[],[],TIMEOUT)
	        # if no response packet return to start of inner loop to re-transmit packet
	        # else check response packet (rcvd)
	        
	        
	        
	sock_sin.close()
    sock_sout.close()
