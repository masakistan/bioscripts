import sys, argparse

def main( args ):
    specs = []
    with open( args.spec_list ) as fh:
        for line in fh:
            specs.append( line.strip() )

    files = []
    with open( args.fasta_files ) as fh:
        for line in fh:
            files.append( line.strip() )

    all_seqs = { key : "" for key in specs }

    for file in files:
        with open( file ) as fh:
            added_specs = []
            seq = ""
            head = ""
            align_len = 0
            for line in fh:
                if line[ 0 ] == '>':
                    if len( seq ) > 0:
                        all_seqs[ head ] += seq
                        align_len = len( seq )
                        added_specs.append( head )
                    head = line.strip()[ 1 : ]
                    seq = ""
                else:
                    seq += line.strip()
            all_seqs[ head ] += seq
            added_specs.append( head )

            for spec in specs:
                if spec not in added_specs:
                    all_seqs[ spec ] += "-" * align_len

    for spec, seq in all_seqs.iteritems():
        print ">" + spec
        print seq


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Generate a supermatrix of all specified files from a list of aligned fasta files."
            )
    parser.add_argument( "--spec_list",
            type = str,
            required = True,
            help = "Complete list of species, one per line."
            )
    parser.add_argument( "--fasta_files",
            type = str,
            required = True,
            help = "List of paths to all aligned fasta files for concatenation."
            )

    args = parser.parse_args()

    main( args )
