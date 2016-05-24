import sys, argparse, re
import numpy as np


exclude = []
trim = []
duplicate = []
dup_seqs = dict()

regex = re.compile( r"N+$" )

# strip Ns of the end
def fix_seq( seq ):
    return regex.sub( '', seq )

def fix_dup( head, name, seq ):
    dup_seqs[ name ] = ( head, seq )


def fix_trim( head, name, seq ):
    coords = trim[ name ]

    for coord in coords:
        left, right = coord
        #print "\t", left, right
        seq = seq[ : left ] + seq[ right : ]

    print '>' + head
    print fix_seq( seq )


def check_seq( head, seq ):
    #print head
    name = head.split()[ 0 ]
    #sys.stderr.write( name + "\n" )
    #sys.stderr.write( str( exclude ) )

    if name in exclude:
        sys.stderr.write( "Excluding: " + name + "\n" )
        return

    if name in trim:
        fix_trim( head, name, seq )
    elif name in duplicate:
        fix_dup( head, name, seq )
    else:
        print '>' + head
        print fix_seq( seq )


def main( args ):
    # parse the fcs report
    global trim
    global exclude
    global duplicate

    with open( args.fcsreport, 'r' ) as fh:
        cur_list = None

        for line in fh:
            if line.strip() == "Exclude:":
                cur_list = exclude
                continue
            elif line.strip() == "Trim:":
                cur_list = trim
                continue
            elif line.strip() == "Duplicated:":
                cur_list = duplicate
                continue
            elif line.strip() == "":
                cur_list = None
                continue

            if cur_list is not None:
                if line.split()[ 0 ] == "Sequence":
                    continue
                else:
                    cur_list.append( line.strip() )

    #print exclude
    #sys.exit()
    '''print "*" * 20
    print trim
    print "*" * 20
    print duplicate'''

    # fix exclude
    for idx in range( len( exclude ) ):
        exclude[ idx ] = exclude[ idx ].split( '\t' )[ 0 ]

    #print exclude
    #print "*" * 20

    # fix trim
    t_trim = dict()
    for idx in range( len( trim ) ):
        parsed = trim[ idx ].split( '\t' )
        coords = []
        for entry in parsed[ 2 ].split( ',' ):
            #entry = np.array( map( int, entry.split( ".." ) ) ) - 1
            entry = map( int, entry.split( ".." ) )
            entry = ( entry[ 0 ] - 1, entry [ 1 ] )
            coords.append( entry )

        #trim[ idx ] = ( parsed[ 0 ], coords )
        t_trim[ parsed[ 0 ] ] = coords
    trim = t_trim

    #print trim
    #print "*" * 20

    # fix duplicate
    t_dup = dict()
    for idx in range( len( duplicate ) ):
        #print duplicate[ idx ].split()
        left, right, length, _ = duplicate[ idx ].split()

        if '~' in left:
            lentry = left.split( '~' )
            name = lentry[ 0 ].replace( "lcl|", '' )
            lcoords = map( int, lentry[ 1 ].split( ".." ) )
            left = ( name, lcoords[ 0 ] - 1, lcoords[ 1 ] - 1 )
            
            rentry = right.split( '~' )
            name = rentry[ 0 ].replace( "lcl|", '' )
            rcoords = map( int, rentry[ 1 ].split( ".." ) )
            right = ( name, rcoords[ 0 ] - 1, rcoords[ 1 ] )
        else:
            length = int( length.replace( '(', '' ) )
            left = ( left.replace( "lcl|", '' ), 0, length - 1 )
            right = ( right.replace( "lcl|", '' ), 0 , length )

        duplicate[ idx ] = ( left, right )
        t_dup[ left[ 0 ] ] = ( left, right )
        t_dup[ right[ 0 ] ] = ( right, left )
    duplicate_processed = duplicate
    duplicate = t_dup

    #for dup in duplicate:
    #    print dup
    #print "*" * 20

    with open( args.fasta, 'r' ) as fh:
        head = ""
        seq = ""
        for line in fh:
            if line[ 0 ] == ">":
                if len( seq ) > 0:
                    check_seq( head, seq )

                head = line.strip()[ 1 : ]
                seq = ""
            else:
                seq += line.strip()
        check_seq( head, seq )

    counter = 0
    for dup in duplicate_processed:
        sys.stderr.write( str( dup ) + "\n" )
        with open( "dup_seqs." + str( counter ) + ".fa", 'w' ) as fh:
            left_name = dup[ 0 ][ 0 ]
            left_head = dup_seqs[ left_name ][ 0 ]
            left_seq = dup_seqs[ left_name ][ 1 ]

            right_name = dup[ 1 ][ 0 ]
            right_head = dup_seqs[ right_name ][ 0 ]
            right_seq = dup_seqs[ right_name ][ 1 ]
            fh.write( '>' + left_head + "\n" + left_seq + "\n" )
            fh.write( '>' + right_head + "\n" + right_seq + "\n" )

        counter += 1
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "This script will remove all the badness that is specified by the NCBI FCS Report."
            )
    parser.add_argument( "--fasta",
            required = True,
            help = "The FASTA file to fix."
            )
    parser.add_argument( "--fcsreport",
            required = True,
            help = "The NCBI FCS Report."
            )
    args = parser.parse_args()
    main( args )
