''' Assignment COSC 264 
    Morgan Peters 53781684 
    and 
    Nicole Steinke 46721931
    50/50 
    '''

    ''' Three Programs (UDP) - SOCK_DGRAM  
            Sender 
                starts w the file 
                splits into packets
                sin/sout
                (two sockets)      
            Channel 
                Proper Protocol 
                    Send- Wait Protocol 
                        complete and in order
                    four sockets 
                        Csin Csout Crin Crout  
            Receiver
                two sockets 
                recieve packets 
            

'''
'''
    class Packet(magicno = 0x497E, typ, seqno, dataLen, data):
        
    #define PTYPE_DATA 0 
    #define PTYPE_ACK 1

    typedef struct { 
        int magicno;    //0x497E if not print a failure message drop packet imediately 
        int type;       //data (0) or acknowledgement (1)
        int seqno;      //bit value 0 or 1 
        int dataLen;    //0-512, # of user bits 
            /if type = awk and != 0 drop packet / if type = data and =0 empty data packet end of transmitted file 
        char data   //depends on dataLengeth 
        } Packet;

    '''
