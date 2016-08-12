''' Assignment COSC 264 
    Morgan Peters 53781684 
    and 
    Nicole Steinke 46721931

    '''

    ''' Three Programs (UDP) - SOCK_DGRAM  
            Sender 
                starts w the file 
                splits into packets
                sin/sout
                (two sockets)  
            
            Beginning sender: 
                3 command line parameters 
                    2 port number 
                        check i for int and 1024 < i < 64000
                         rin/ rout = port_nums  
                         rout sends to crin 
                         rin accepts packets from crout 
                    1 file name 
                create() 
                bind() 
                connect(sout, default = port_num_csin)
                checks for file_name 
                    if DNE exit()
                next = 0 //local int
                exitFlag = FALSE //boolean flag 
                while()
                        read in to buffer //up to 512 bytes 
                        bytes_read == 0 
                            magicno = 0x497E
                            type = dataPacket 
                            seqno = next
                            dataLen = 0 
                            exitFlag == TRUE 
                            //set empty data field 
                        bytes_read > 0 
                            magicno = 0x497E
                            type = dataPacket 
                            seqno = next
                            dataLen = bytes_read
                            exitFlag == TRUE
                            //append(bytes_read) into it
                        while()
                            send PacketBuffer with sout 
                            select() //wait one second for response from sin
                                if no response resend packet //return to beginning of loop 
                                else 
                                    if rcvd.magicno != 0x497E
                                    or if rcvd.type != acknowledgementPacket
                                    or if rcvd.dataLen != 0 
                                    if rcvd.seqno != next
                                        restart transmission
                                    else 
                                        next = 1- next
                                        if exitFlag == TRUE
                                            close(file_name)
                                            close(sockets)
                                            exit(0)
                                        else
                                            go to outerloop
                    other things: 
                        count packets sent in total 
                        print(count) on exit 
                        DONT FORGET TO CLOSE()        


            Channel 
                Proper Protocol 
                    Send- Wait Protocol 
                        complete and in order
                    four sockets 
                        Csin Csout Crin Crout  //int between 1024-64000
                    two port numbers sin and rin 
                    float P (0<= P < 1 ) //packet loss rate

                How to start channel: 
                    parameters/ check all 
                    create/ bind the sockets 
                    connect all out sockets 
                    set default port numbers used by sender 
                        set them as distinct 
                    infinite loop/ main 
                        in the loop 
                        select() waits for input csin srin
                            -return number of sockets 
                            -must process all packets/ data 
                            -use in a blocking style to save cpu time
                        after recieving packet 
                            -check magicno field == 0x497E
                                when False stop return to beginning of loop
                            -u = random.uniform(0,1)  
                                    ?? - pseudo random numbers instead of true random numbers
                                    pick one until project is complete to check for correctness
                                if u < P  
                                    drop packet return to beginning of loop
                                else 
                                   channel sends the packet to its own socket 
                                    crout -> rin 
                                    csout -> sin

            Receiver
                3 command line parameters 
                    2 port number 
                        check i for int and 1024 < i < 64000
                         rin/ rout = port_nums  
                         rout sends to crin 
                         rin accepts packets from crout 
                    1 file name 
                create() 2 sockets 
                bind() both sockets 
                connect() rout set default to port_num of crin 

                intialization 
                    open(file_name)
                        abort program if file_name exists 
                    expected = 0 //local int var 

                if successful loop 
                    wait() for rin 
                        -blocking style 
                    magicno != 0x497E 
                        start loop again 
                    packet type != dataPacket
                        stop / restart loop
                    rcvd.seqno != seqno
                            magicno = 0x497E
                            type = acknowledgementPacket
                            seqno = rcvd.seqno
                            dataLen = 0
                        send to rout 
                        start loop again
                    rcvd.seqno == expected
                        magicno = 0x497E
                            type = acknowledgementPacket
                            seqno = rcvd.seqno
                            dataLen = 0
                        send to rout 
                        expected = 1-expected 
                        if rcvd.dataLen > 0 
                            append data in file 
                            restart loop 
                        else (rcvd.dataLen == 0)
                            close(file_name) 
                            close(sockets)
                            exit()

                    



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
