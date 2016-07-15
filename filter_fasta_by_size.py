import sys, argparse


def main( args ):
    with open( args.fasta ) as fh:
        head = ""
        seq = ""
        counter = 0
        removed = []

        processed = 0
        for line in fh:
            if line[ 0 ] == '>':

                if len( seq ) > 0 and len( seq ) >= args.len:
                    print head
                    print seq
                else:
                    if processed > 0:

                        counter += 1
                        sys.stederr.write( line + "\n" )
                        removed.append( head )

                head = line.strip()
                seq = ""
                processed += 1
            else:
                seq += line.strip()

        if len( seq ) > 0 and len( seq ) >= args.len:
            print head
            print seq
        else:
            counter += 1
            removed.append( head )

        sys.stderr.write( "Removed " + str( counter ) + " sequences\n" )
        for i in removed:
            sys.stderr.write( "\t" + i + "\n" )


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
