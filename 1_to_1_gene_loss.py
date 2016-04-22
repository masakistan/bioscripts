import sys, argparse, re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

bins = "0,10,20,30,40,50,60,70,80,90,100"

def main( args ):

    # parse args
    num_spec = float( args.num_species )
    ortho_path = args.ortho_path

    # format bins
    bins = map( int, args.bins.split( ',' ) )

    # open files for writing
    fhs_uniq = []
    fhs_mult = []
    for idx, bin_max in enumerate( bins ):
        if idx == 0:
            continue
        else:
            fhs_mult.append( open( "ortho.mult." + str( bins[ idx - 1 ] ) + "." + str( bin_max ), 'w' ) )
            fhs_uniq.append( open( "ortho.1to1." + str( bins[ idx - 1 ] ) + "." + str( bin_max ), 'w' ) )

    #print bins
    if bins[ -1 ] == 100:
        bins = bins[ : -1 ]
    else:
        fhs_mult.append( open( "ortho.mult." + str( bins[ -1 ] ) + ".100", 'w' ) )
        fhs_mult.append( open( "ortho.1to1." + str( bins[ -1 ] ) + ".100", 'w' ) )

    # regex for removing sequence name so we have just the species
    regex = re.compile( "\|m\.\S*" )

    percs = []

    with open( ortho_path, 'r' ) as ortho_fh:
        for line in ortho_fh:
            groups = regex.sub( " ", line.strip() ).split()[ 1: ]
            groups_uniq = set( groups )

            #print str( groups[ : 20 ] ) + "..."
            #print len( groups )
            #print len( groups_uniq )
            perc = ( float( len( groups_uniq ) ) / num_spec ) * 100
            percs.append( perc )
            #print perc
            #print perc
            fh_idx =  np.digitize( perc, bins ) - 1
            #print fh_idx
            try:
                if len( groups_uniq ) != len( groups ):
                    cur_fh = fhs_mult[ fh_idx ]
                else:
                    cur_fh = fhs_uniq[ fh_idx ]
     
                cur_fh.write( line )
            except IndexError:
                sys.exit( "Index Error at " + str( fh_idx ) )

            #print "*" * 20

    for fh in fhs_uniq:
        fh.close()
    for fh in fhs_mult:
        fh.close()

    if args.histo:
        fig = plt.hist( percs, bins = bins )
        pp = PdfPages( args.histo )
        plt.savefig( pp, format= 'pdf' )
        pp.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "This will find 1:1 orthology clustes with gene loss sorted by percent loss bins.",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter
            )
    parser.add_argument( "--ortho_path",
            type = str,
            required = True,
            help = "Path to the orthology groups."
            )
    parser.add_argument( "--num_species",
            type = int,
            required = True,
            help = "The number of species in your analysis."
            )
    parser.add_argument( "--bins",
            type = str,
            default = bins,
            help = "Comma separated list of integer bin sizes. First number is starting range, if 0 is excluded you may miss some groups. Last value maximum is 100. If it is less than 100 groups will be excluded."
            )
    parser.add_argument( "--histo",
            type = str,
            help = "Path for histogram of the gene loss percentages."
            )

    args = parser.parse_args()

    main( args )

