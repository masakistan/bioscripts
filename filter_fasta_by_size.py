import sys, argparse


def main( args ):
    with open( args.fasta ) as fh:
        head = ""
        seq = ""
        counter = 0

        for line in fh:
            if line[ 0 ] == '>':

                if len( seq ) > 0 and len( seq ) >= args.len:
                   print head
                   print seq
                else:
                   counter += 1

                head = line.strip()
                seq = ""
            else:
                seq += line.strip()

        if len( seq ) > 0 and len( seq ) >= args.len:
            print head
            print seq
        else:
            counter += 1

        sys.stderr.write( "Removed " + str( counter ) + " sequences\n" )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Filter a FASTA file based on length of sequence"
            )
    parser.add_argument( "--fasta",
            type = str,
            required = True,
            help = "FASTA file to be filtered."
            )
    parser.add_argument( "--len",
            type = int,
            required = True,
            help = "Sequence length must be greater than or equal to this parameter."
            )
    args = parser.parse_args()
    main( args )
