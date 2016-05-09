'''
this script is designed to be add the necessary #1 to all branch sites used for PAML testing.
'''

import argparse


def main( args ):
    # open the tree file and read in the tree
    with open( args.tree ) as fh:
        tree = fh.read()

    #print tree

    counter = 0
    for idx, char in enumerate( tree ):
        if char == ':':
            with open( args.out_prefix + "_" + str( counter ), 'w' ) as fh:
                fh.write( tree[ : idx ] + "#1" + tree[ idx : ] )
            counter += 1

    print "Created " + str( counter ) + " trees!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description = "Generate a tree per branch site with #1 added to each of the different branch sites."
            )
    parser.add_argument( "--tree",
            type = str,
            required = True,
            help = "The path to the tree file."
            )
    parser.add_argument( "--out_prefix",
            type = str,
            default = "tree_branch",
            help = "Prefix to prepend to created trees."
            )

    args = parser.parse_args()

    main( args )
