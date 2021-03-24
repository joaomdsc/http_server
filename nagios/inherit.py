# inherit.py - parse Nagios/Centreon configuration files

"""Build and print the inheritance tree (assuming single inheritance only)

Read the objects.json file and reconstruct the (independent) inheritance trees
for each type of object.

"""

import os
import re
import json
from hierarchy import parse_object_types, print_node

#-------------------------------------------------------------------------------

def inherit(filepath):
    with open(filepath) as f:
        trees = parse_object_types(json.load(f))

    # In both the text output, and in the 'xxx_tree.json' file, the services
    # repeat the host, when in fact they're all different.
    
    # Text output
    outpath = f'{filepath.rsplit(".", maxsplit=1)[0]}_hierarchy.txt'
    with open(outpath, 'w') as f:
        for t in trees:
            print_node(f, t, 0)

    # Json output
    outpath = f'{filepath.rsplit(".", maxsplit=1)[0]}_tree.json'
    with open(outpath, 'w') as f:
        json.dump(trees, f, indent=4)

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

# Command line argument
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <objects file>')
    exit(-1)

inherit(sys.argv[1])