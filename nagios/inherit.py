# inherit.py - parse Nagios/Centreon configuration files

"""Build and print the inheritance tree (assuming single inheritance only)

Read the objects.json file and reconstruct the (independent) inheritance trees
for each type of object.

"""

import os
import re
import json
      
#-------------------------------------------------------------------------------
# I want stdout to be unbuffered, always
#-------------------------------------------------------------------------------

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)

#-------------------------------------------------------------------------------
# globals
#-------------------------------------------------------------------------------

obj_names = {
    'host': 'host_name',
    'hostgroup': 'hostgroup_name',
    'service': 'service_description',
    'servicegroup': 'servicegroup_name',
    'contact': 'contact_name',
    'contactgroup': 'contactgroup_name',
    'timeperiod': 'timeperiod_name',
    'command': 'command_name',
    'servicedependency': None,
    'serviceescalation': None,
    'hostdependency': None,
    'hostescalation': None,
    'hostextinfo': None,
    'serviceextinfo': None,
    'connector': None,
}

#-------------------------------------------------------------------------------
# print_node
#-------------------------------------------------------------------------------

def print_node(nd, level):
    name, obj, kids = nd
    ind = ' '*4
    print(f'{ind*level}{name}')
    for k in kids:
        print_node(k, level+1)

#-------------------------------------------------------------------------------
# parse_obj_type
#-------------------------------------------------------------------------------

def parse_obj_type(otype, objs):
    # objs is an array of object type definitions
    temp = {}
    # temp is a dict with key=name and value is a [name, object, kids]
    temp[otype] = [otype, None, []]
    
    for o in objs:
        # How does this object identify itself ?
        key = obj_names[otype]
        if 'name' in o:
            key = 'name'
        if key not in o:
            raise RuntimeError(f'"{otype}" unidentified object "{o}"')
        name = o[key]
        
        # Create my own entry
        if name not in temp:
            temp[name] = [name, o, []]
        elif temp[name][1] is None:
            # This entry was created by a child, before the parent was read, so
            # it didn't have its object yet. Now we can fill it in.
            temp[name][1] = o

        # Represent parent-child relationships
        if 'use' in o:
            # We've found a (parent -> child) relationship from used to o
            parent = o['use']
            if parent not in temp:
                # If I haven't read the parent yet, what do I put in here ?
                temp[parent] = [parent, None, []]
            temp[parent][2].append(temp[name])
        else:
            temp[otype][2].append(temp[name])

    # print_node(temp[otype], 0)
    return temp[otype]

#-------------------------------------------------------------------------------
# parse_object_types
#-------------------------------------------------------------------------------

def parse_object_types(objs):
    trees = []
    for k, v in objs.items():
        # root is [otype, k, kids]
        trees.append(parse_obj_type(k, v))
    return trees

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

# Process the main objects file
dirpath = os.path.join(os.getenv('HOME'), '.nagios_cfg')
filepath = os.path.join(dirpath, 'objects.json')

with open(filepath) as f:
    trees = parse_object_types(json.load(f))

for t in trees:
    print_node(t, 0)