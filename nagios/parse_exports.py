# parse_exports.py - parse the result of a Centreon export

"""Read a Centreon exports file, i.e. a text file produced by running the
"centreon -u admin -p admin -e > /tmp/clapi-export.txt" command. Build a data
structure similar to the one in objects.json (which is itself similar to
Centreon's config files) so that we can run inherit.py on it to extract the
tree of template derivation. Run this as:

    py parse_exports.py exported_data_centreon.txt > exports.json

so then we can tun

    py inherit.py exports.json

"""

import sys
import csv
import json

from hierarchy import parse_object_types, print_node
from restapi.excel import SvcInfo, ExcelData

#-------------------------------------------------------------------------------

def parse_export_data(rdr):
    svcs = []
    d = None
    cmds = {}
    for row in rdr:
        if row[0] == 'SERVICE':
            if row[1] == 'ADD':
                if d is not None:
                    svcs.append(d)
                d = {
                    'host': row[2],
                    'service_description': row[3],
                    'use': row[4],
                    # The 'name' key is essential to ensure service name
                    # uniqueness.
                    'name': f'{row[2]};{row[3]}'
                }
            else:
                d[row[4].replace('service_', '')] = row[5]
        elif row[0] == 'STPL':
            if row[1] == 'ADD':
                if d is not None:
                    svcs.append(d)
                d = {
                    'service_description': row[3],
                    'name': row[2],
                }
                if row[4] != '':
                    d['use'] = row[4]
            elif row[1] == 'addhosttemplate':
                continue
            else:
                d[row[3].replace('service_', '')] = row[4]
        elif row[0] == 'CMD' and row[1] == 'ADD':
            cmds[row[2]] = row[4]
        else:
            continue
    svcs.append(d)
    return svcs, cmds
 
#-------------------------------------------------------------------------------

def get_svc_node(nd, ancestry, svcs):
    """Ancestry is the list of nd's ancestors."""
    name, obj, kids = nd
    check = None
    if obj is not None:
        if 'register' in obj:
            if obj['register'] == '1':
                # This is a service, not a template
                svc = {
                    'name': name,
                    'ancestors': ancestry,
                }
                if 'host' in obj:
                    svc['host'] = obj['host']
                if 'check_command' in obj:
                    svc['check_command'] = obj['check_command']
                svcs.append(svc)
            else:
                # This is a template
                if 'check_command' in obj:
                    check = obj['check_command']

    me_as_ancestor = name if check is None else (name, check)
    
    for k in kids:
        svcs = get_svc_node(k, ancestry + [me_as_ancestor], svcs)

    return svcs
 
#-------------------------------------------------------------------------------
  
def get_services(trees, cmds):
    # FIXME We know there's only one object type, "service"
    for t in trees:
        # Get each service and its ancestors
        svcs = []
        svcs = get_svc_node(t, [], svcs)
        # print(json.dumps(svcs, indent=4))

        # Get each service and its check command
        svc_cmds = []
        for svc in svcs:
            host, name = svc['name'].split(';')
            if host != svc['host']:
                msg = f'Inconsistency: svc["name"]={svc["name"]}' \
                    f', svc["host"]={svc["host"]}'
                print(msg)
            cmd = None
            if 'check_command' in svc:
                cmd = svc['check_command']
            else:
                for x in reversed(svc['ancestors']):
                    if type(x) == tuple:
                        cmd = x[1]
                        break
            svc_cmds.append((host, name, cmd, cmds.get(cmd)))

        # FIXME only once inside the loop, this is wrong
        return svc_cmds

#-------------------------------------------------------------------------------

def build_excel(svc_cmds, filepath):
    # Create the ExcelData object
    n = 0
    dst = []
    for host, name, cmd, cmd_line in svc_cmds:
        x = SvcInfo(n, None, None, None, None, host,
                    name, cmd_line, None, None,
                    None, None, None, cmd, None, None, None)
        dst.append(x)
        n += 1

    # Output to an Excel file
    print(f'Write AppControl excel data to {filepath}')
    ExcelData(dst).to_excel('Centreon export', filepath)

#-------------------------------------------------------------------------------

def parse_exports_file(filepath):
    with open(filepath) as f:
        rdr = csv.reader(f, delimiter=';')
        svcs, cmds = parse_export_data(rdr)
        objects = {'service': svcs}
        # print(json.dumps(objects, indent=4))

    # When reading a Centreon configuration from all the files, there are all
    # kinds of objects, but here we've only kept the services and service
    # templates.

    # Call functionality from "inherit" to build the hierarchy tree
    trees = parse_object_types(objects)

    # Build the set of services and their commands
    svc_cmds = get_services(trees, cmds)
    outpath = f'{filepath.rsplit(".", maxsplit=1)[0]}_cmds.txt'
    with open(outpath, 'w') as f:
         # json.dump(svc_cmds, f, indent=4)
         wrt = csv.writer(f, delimiter=';')
         for svc in svc_cmds:
             wrt.writerow(svc)

    # Build the excel file for AppControl
    outpath = f'{filepath.rsplit(".", maxsplit=1)[0]}.xlsx'
    build_excel(svc_cmds, outpath)

    # Text output
    outpath = f'{filepath.rsplit(".", maxsplit=1)[0]}_hierarchy.txt'
    with open(outpath, 'w') as f:
        for t in trees:
            print_node(f, t, 0)

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

# Command line argument
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <exports file>')
    exit(-1)

parse_exports_file(sys.argv[1])