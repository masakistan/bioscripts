import sys, argparse, re, os
import numpy as np
from subprocess import call

bins = "0,10,20,30,40,50,60,70,80,90,100"

def main( args ):

    # parse args
    num_spec = float( args.num_species )
    ortho_path = args.ortho_path

    # format bins
    bins = map( int, args.bins.split( ',' ) )

    # regex for removing sequence name so we have just the species
    groups_regex = re.compile( "\|m\.\S*" )
    seqs_regex = re.compile( "\s\S*\|" )

    if bins[ -1 ] == 100:
        bins = bins[ : -1 ]

    # create output dirs
    for bin in bins:
        call( [ "mkdir", args.output_dir + "/" + str( bin ) ] )

    percs = []

    # store seqs and there cluster locations
    # spec -> seq -> cluster
    seq2clust = dict()

    # store cluster percentage
    # cluster -> bin
    clust2bin = dict()

    with open( ortho_path, 'r' ) as ortho_fh:
        for line in ortho_fh:
            #print line
            if len( line.strip() ) < 1:
                continue
            cluster_name = line.strip().split()[ 0 ][ : -1 ]
            groups = groups_regex.sub( " ", line.strip() ).split()[ 1 : ]
            seqs = seqs_regex.sub( " ", line.strip() ).split()[ 1 : ]
            #print seqs
            groups_uniq = list( set( groups ) )

            perc = ( float( len( groups_uniq ) ) / num_spec ) * 100
            percs.append( perc )
            fh_idx =  np.digitize( perc, bins ) - 1

            #print cluster_name
            #print "\t" + str( groups )
            #print "\t" + str( seqs )

            for idx, spec_name in enumerate( groups ):
                clust2bin[ cluster_name ] = fh_idx
                try:
                    seq2clust[ spec_name ]
                except KeyError:
                    seq2clust[ spec_name ] = { seqs[ idx ] : [ cluster_name ] }
                    continue

                try:
                    seq2clust[ spec_name ][ seqs[ idx ] ].append( cluster_name )
                except KeyError:
                    seq2clust[ spec_name ][ seqs[ idx ] ] = [ cluster_name ]

    failed_check = False
    print "validate cluster assignment unicity"
    for spec, seqs in seq2clust.iteritems():
        for seq, clusters in seqs.iteritems():
            if len( clusters ) > 1:
                print spec + "\t" + seq + "\t" + str( clusters )
                failed_check = True
    print "done check!"
    if failed_check:
        #sys.exit( "multiple clustering for sequence! Aboart!" )
        print "multiple clustering for sequence!"

    seq_name_regex = re.compile( "^>\S*\|" )
    for i in os.listdir( args.fasta_dir ):
        print i
        spec = i
        full_path = args.fasta_dir + "/" + i
        cur_fh = 0
        try:
            seq2clust[ spec ]
        except KeyError:
            continue

        if os.path.isfile( full_path ):
            with open( full_path, 'r' ) as ffh:
                skip = False
                cur_seq = ""
                cur_hea = ""
                cur_seq_name = ""
                cur_spec = ""
                for line in ffh:
                    if line[ 0 ] == '>':
                        seq_name = seq_name_regex.sub( '', line.strip().split()[ 0 ] )
                        #print spec + "\t" + seq_name

                        if len( cur_hea ) > 0:
                            for cluster in seq2clust[ cur_spec ][ cur_seq_name ]:
                                bin = bins[ clust2bin[ cluster ] ]
                                file_path = args.output_dir + "/" + str( bin ) + "/" + cluster
                                cur_fh = open( file_path, 'a' )
                                cur_fh.write( ">" + cur_spec + "|" + cur_hea[ 1 : ] )
                                cur_fh.write( cur_seq )
                                cur_fh.close()
                        
                        try:
                            cluster = seq2clust[ spec ][ seq_name ]
                        except KeyError:
                            skip = True
                            cur_seq = ""
                            cur_hea = ""
                            cur_seq_name = ""
                            cur_spec = ""
                            continue

                        cur_hea = line
                        cur_seq_name = seq_name
                        cur_spec = spec
                        cur_seq = ""

                        skip = False
                        #print "\t" + str( cluster )

                        #print "\t" + str( bin )
                        
                        #try:
                        #    cur_fh.close()
                        #except:
                        #    pass
                        #file_path = args.output_dir + "/" + str( bin ) + "/" + cluster
                        #cur_fh = open( file_path, 'a' )
                        #cur_fh.write( line )
                    else:
                        if skip:
                            continue

                        cur_seq += line

                if len( cur_hea ) > 0:
                    for cluster in seq2clust[ cur_spec ][ cur_seq_name ]:
                        bin = bins[ clust2bin[ cluster ] ]
                        file_path = args.output_dir + "/" + str( bin ) + "/" + cluster
                        cur_fh = open( file_path, 'a' )
                        cur_fh.write( ">" + cur_spec + "|" + cur_hea[ 1 : ] )
                        cur_fh.write( cur_seq )
                        cur_fh.close()


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
    parser.add_argument( "--fasta_dir",
            type = str,
            required = True,
            help = "Directory containing all fasta files."
            )
    parser.add_argument( "--output_dir",
        type = str,
        default = '.',
        help = "Output dir."
        )

    args = parser.parse_args()

    main( args )

