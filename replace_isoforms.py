import sys, argparse

def parse_gene_seq_ids_file( file_path ):
    seq_to_gene = dict()
    with open( file_path ) as fh:
        for line in fh:
            line = line.strip().split()
            seq_to_gene[ line[ 1 ] ] = line[ 0 ]
    #print len( seq_to_gene )
    return seq_to_gene

def parse_gene_seq_ids_files( file_path ):
    all_seq_to_gene = dict()
    with open( file_path ) as fh:
        for line in fh:
            base_name = line[ line.rfind( '/' ) + 1 : ].strip()
            all_seq_to_gene[ base_name ] = parse_gene_seq_ids_file( line.strip() )
    return all_seq_to_gene

def parse_longest_seqs_file( file_path ):
    longest_ids = dict()
    with open( file_path ) as fh:
        for line in fh:
            line = line.strip().split()
            longest_ids[ line[ 0 ] ] = line[ 1 ]
    #print len( longest_ids )
    return longest_ids

def parse_longest_seqs_files( file_path ):
    all_longest_ids = dict()
    with open( file_path ) as fh:
        for line in fh:
            base_name = line[ line.rfind( '/' ) + 1 : ].strip()
            all_longest_ids[ base_name ] = parse_longest_seqs_file( line.strip() )
    return all_longest_ids

def filter_groups( orthomcl_path, gene_seq_ids, longest_seq_ids ):
    groups = []
    with open( orthomcl_path ) as fh:
        for line in fh:
            line = line.strip().split()
            if len( line ) <= 0:
                continue

            group_specs = dict()
            bad_group = False

            for spec in line[ 1 : ]:
                spec, seq_id = spec.split( '|' )
                if spec in group_specs:
                    if gene_seq_ids[ spec ][ group_specs[ spec ] ] != gene_seq_ids[ spec ][ seq_id ]:
                        bad_group = True
                        break
                
                group_specs[ spec ] = longest_seq_ids[ spec ][ gene_seq_ids[ spec ][ seq_id ] ]

            if bad_group:
                #print "Bad group"
                continue
            else:
                group = []
                if len( group_specs ) < 2:
                    continue
                for spec, longest_seq_id in group_specs.iteritems():
                    #try:
                    #longest_iso = longest_seq_ids[ spec ][ gene ]
                    longest_iso = longest_seq_id
                    #except KeyError:
                    #    print spec + "\t" + gene
                    group.append( spec + "|" + longest_iso )
                #print line
                groups.append( line[ 0 ] + " " + " ".join( group ) )
    return groups

def main( args ):
    gene_seq_ids = parse_gene_seq_ids_files( args.gene_list_path )

    #print gene_seq_ids.keys()

    #print "*" * 20

    #sys.exit( "step 1" )

    longest_seq_ids = parse_longest_seqs_files( args.longest_list_path )

    #print longest_seq_ids.keys()

    #print "*" * 20

    #sys.exit( "step 2" )

    filtered_groups = filter_groups( args.orthomcl_path, gene_seq_ids, longest_seq_ids )

    for group in filtered_groups:
        print group

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Replace sequences in OrthoMCL output with longest isoform. Ensure that all sequences in a group are isoforms of the same gene."
            )
    parser.add_argument( 'gene_list_path',
            type = str,
            help = "The path to a file containing a list of the files that contain the gene to sequence ids."
            )
    parser.add_argument( 'longest_list_path',
            type = str,
            help = "The path to a file containining a list of the files that contain the longest isoform ids."
            )
    parser.add_argument( 'orthomcl_path',
            type = str,
            help = "The path to the OrthoMCL output file."
            )
    args = parser.parse_args()
    main( args )
