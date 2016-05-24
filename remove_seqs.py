import sys, argparse

def main( args ):
    seqs_to_remove = []
    with open( args.removal_list ) as fh:
        for line in fh:
            if line[ 0 ] != '>':
                seqs_to_remove.append( '>' + line.strip() )
            else:
                seqs_to_remove.append( line.strip() )

    removed_seqs = 0

    with open( args.fasta ) as fh:
        output = True
        for line in fh:
            line = line.strip() 

            if line[ 0 ] == '>':
                head = line.split()[ 0 ]
                if head in seqs_to_remove:
                    #print head + " in " + str( seqs_to_remove )
                    output = False
                    seqs_to_remove.remove( head )
                    removed_seqs += 1
                else:
                    #print head + " not in " + str( seqs_to_remove )
                    output = True
            
            if output:
                print line

    sys.stderr.write( "Removed " + str( removed_seqs ) + " sequences.\n" )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Remove sequences from a fasta file."
            )
    parser.add_argument( "--removal_list",
            type = str,
            required = True,
            help = "List of all sequences to remove. One sequence per line, sequence header."
            )
    parser.add_argument( "--fasta",
            type = str,
            required = True,
            help = "Fasta file that will have sequences removed"
            )
    args = parser.parse_args()

    main( args )
