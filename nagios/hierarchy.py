# hierarchy.py - parse Nagios/Centreon configuration files

"""Build the inheritance tree (assuming single inheritance only) for each type
of object.

"""

import os
import re
import json

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
    'connector': 'connector_name',
}

#-------------------------------------------------------------------------------

def print_node(f, nd, level):
    name, obj, kids = nd
    ind = ' '*4
    s = f'{ind*level}{name}'
    if obj is not None:
        if 'host' in obj:
            s += f' [{obj["host"]}]'
        if 'register' in obj:
            s += f' [{"SVC" if obj["register"] == "1" else "STPL"}]'
        if 'check_command' in obj:
            s += f' CMD="{obj["check_command"]}"'
            
    f.write(f'{s}\n')
    for k in kids:
        print_node(f, k, level+1)

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
            # The child doesn't refer to any parent with 'use', so make it a
            # child of 'otype', e.g. 'service'.
            temp[otype][2].append(temp[name])

    return temp[otype]

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

if __name__ == '__main__':
    print('This module is not meant to be executed directly.')