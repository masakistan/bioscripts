import sys, argparse, re

def filter_fasta( file_path ):
    #names = []
    #seqs = []

    longest = dict()

    regex = re.compile( "(_i\d*\|m\..*|\|m\..*)" )
    
    with open( file_path ) as fh:
        seq = ""
        name = ""
        for line in fh:
            if line[ 0 ] == '>':
                if len( name ) > 0:
                    #names.append( name.strip() )
                    #seqs.append( seq.strip() )

                    name = name.strip()
                    sub_name = name.split()[ 0 ]
                    #print name
                    prefix = regex.sub( " ", sub_name )
                    seq = seq.strip()
                    #print "prefix" + prefix

                    try:
                        if len( seq ) > len( longest[ prefix ][ 1 ] ):
                            longest[ prefix ] = ( name, seq )
                    except:
                        longest[ prefix ] = ( name, seq )

                seq = ""
                name = line
            else:
                seq += line
        try:

            name = name.strip()
            sub_name = name.split()[ 0 ]
            #print name
            prefix = regex.sub( " ", sub_name )
            seq = seq.strip()
            #print "prefix" + prefix
            if len( seq ) > len( longest[ prefix ][ 1 ] ):
                longest[ prefix ] = ( name, seq )
        except:
            longest[ prefix ] = ( name, seq )

    return longest

def main( args ):
    longest_isoforms = filter_fasta( args.file_path )

    for prefix, seq in longest_isoforms.iteritems():
        name, seq = seq
        print name
        print seq

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Filter a fasta file leaving only the longest isoform of a gene."
            )
    parser.add_argument( "file_path",
            type = str,
            help = "Path to fasta file"
            )
    args = parser.parse_args()
    main( args )
