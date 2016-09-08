
if __name__ == "__main__":

    port_sout = sys.argv[0]
    file_name_in = sys.argv[1]
    port_csin = sys.argv[2]
    port_csout = sys.argv[3]
    port_sin = sys.argv[4]
    p_rate = sys.argv[5]
    port_rin = sys.argv[6]
    port_rout = sys.argv[7]
    port_crin = sys.argv[8]
    file_name_out = sys.argv[9]

    sender(port_sin, port_sout, port_csin, file_name_in)
    channel(port_csin, port_csout, port_rout, port_rin, port_sin, port_rin,
            p_rate)
    receiver(port_rin, port_rout, port_crin, file_name_out)

    # somehow read from command line
