import sys, argparse, re


def filter_file( file_path, num_species ):
    regex = re.compile( "\|m\.\S*" )
    with open( file_path ) as fh:
        for line in fh:
            line_mod = regex.sub( " ", line.strip() )
            ids = line_mod.split()[ 1 : ]

            ids_unique = set( ids )

            print "*" * 20
            print "ids:\t" + str( len( ids ) )
            print "uniq:\t" + str( len( ids_unique ) )
            print "spec:\t" + str( num_species )

            if len( ids ) == len( ids_unique ) and len( ids ) == num_species:
                print line.strip()


def main( args ):
    filter_file( args.file_path, args.num_species )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Find 1-to-1 orthology groups."
            )
    parser.add_argument( "num_species",
            type = int,
            help = "The number of species necessary for 1-to-1 groupings."
            )
    parser.add_argument( "file_path",
            type = str,
            help = "Path to OrthoMCL output."
            )

    
    args = parser.parse_args()
    main( args )
