import sys

seqs_per_file = int( sys.argv[ 2 ] )
prefix = sys.argv[ 3 ]
postfix = 0

with open( sys.argv[ 1 ] ) as fh:
    seq = ""
    seq_name = ""
    counter = 0
    

    out_fh = open( prefix + str( postfix ), 'w' )

    for line in fh:
        if line[ 0 ] == '>' and len( seq ) > 0:
            if counter == seqs_per_file:
                postfix += 1
                counter = 0
                out_fh = open( prefix + str( postfix ), 'w' )
            out_fh.write( seq_name )
            out_fh.write( seq )
            counter += 1

            seq_name = line
            seq = ""
        else:
            seq += line

    out_fh.write( seq_name )
    out_fh.write( seq )

