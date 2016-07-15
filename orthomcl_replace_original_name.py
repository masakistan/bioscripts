'''
This script is designed to replace the species names in the groups.txt output from OrthoMCL with their original names after being substituted using orthomclAdjustFasta.

the <species name> file needs to have the format:

    <temporary name><whitespace><real name>

Usage: progName <groups.txt> <species names>
'''

import sys

groups = open( sys.argv[ 1 ] ).read()

names = dict()
with open( sys.argv[ 2 ] ) as fh:
    for line in fh:
        line = line.split()
        names[ line[ 0 ] ] = line[ 1 ]

for tname, rname in names.iteritems():
    groups = groups.replace( tname + '|', rname + '|' )


print groups
