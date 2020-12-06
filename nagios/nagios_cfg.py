# nagios_cfg.py - parse Nagios/Centreon configuration files

"""The main configuration file uses an include directive (cfg_file=XXX) to
include other files. A different syntax in object files (with the same
semantics) is include_file=XXX.

We start by reading in nagios.cfg and going over all the includes. Each of the
included files defines objects (command, connector, host, service, timeperiod),
each object in our code becomes a dictionary, where some keys are used to
implement inheritance:

  - the 'name' key identifies the object
  - the 'use' key indicates a parent object
  - the 'register' key distinguishes templates from actual objects

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

# These should be arguments, configuration, or environment variables
# ref = '/etc/centreon-engine'
# src = r'c:/a/centreon/server/192.168.0.43/centreon-engine'
# dst = r'c:\tmp\cfg\centreon_192.168.0.43'

# src = r'c:/a/centreon/server/172.18.0.13/centreon-engine'
# dst = r'c:\tmp\cfg\centreon_172.18.0.13'

ref = '/usr/local/nagios/etc/objects'
src = r'c:\a\centreon\server\192.168.0.45_nagios'
dst = r'c:\tmp\cfg\nagios_192.168.0.45'

#-------------------------------------------------------------------------------
# parse_main
#-------------------------------------------------------------------------------

def parse_main(f):
    """Parse the main configuration file into a dictionary.

    Keys must appear only once, and define a single value, with the exception
    of the cfg_file key. Each new cfg_file entry add to a sub-dictionary of
    files to be included.

    Lines starting with # are comments.

    """
    d = {}
    for line in f.readlines():
        # Remove blank-only or empty lines
        m = re.match('\s*$', line)
        if m:
            continue

        # Ignore comment lines
        if line[0] == '#':
            continue

        # Parameter
        m = re.match('([^=]+)=(.*)', line)
        if not m:
            raise RuntimeError(f'Error in line "{line}"')
        key = m.group(1)
        val = m.group(2)

        if key == 'cfg_file':
            # Create a table of include files 
            if 'cfg_file' not in d:
                d['cfg_file'] = []

            # Change path of include files to local settings
            head, tail = os.path.split(val)
            if head == ref:
                val = os.path.join(src, tail)
                print(val)
                
            d['cfg_file'].append(val)
        else:
            d[key] = val

    return d

#-------------------------------------------------------------------------------
# dump_to_file
#-------------------------------------------------------------------------------

def dump_to_file(filename, obj):
    filepath = os.path.join(dst, filename.rsplit('.', maxsplit=1)[0] + '.json')
    with open(filepath, 'w') as f:
        json.dump(obj, f, indent=4)

#-------------------------------------------------------------------------------
# parse_obj_file
#-------------------------------------------------------------------------------

def parse_obj_file(f):
    """Return a structure representing all the object definitions from the file.

    The structure is a dictionary where keys are objects types, and values are
    arrays of object definitions. Object definitions are simple dictionaries of
    directives.

    """
    object_types = [
        'host',
        'hostgroup',
        'service',
        'servicegroup',
        'contact',
        'contactgroup',
        'timeperiod',
        'command',
        'servicedependency',
        'serviceescalation',
        'hostdependency',
        'hostescalation',
        'hostextinfo',
        'serviceextinfo',
        'connector',
    ]

    d = {}
    otype = odict = None
    in_obj = False
    for line in f.readlines():
        # Remove blank-only or empty lines
        m = re.match('\s*$', line)
        if m:
            continue

        # Ignore comment lines
        if line[0] == '#':
            continue

        # Remove partial-line comments
        n = line.find(';')
        if n != -1:
            line = line[:n]
            # Remove if remains is blank-only or empty lines
            m = re.match('\s*$', line)
            if m:
                continue

        # Begin object
        pat = rf"\s*define\s+({'|'.join(object_types)})\s*{{"
        m = re.match(pat, line)
        if m:
            # Beginning of an object definition
            if in_obj:
                raise RuntimeError("Can't nest object definitions")
            otype = m.group(1)
            odict = {}
            in_obj = True
        else:
            # Look for include directives
            pat = r'\s*(include_file|include_dir)\s*=\s*(.*)'
            m = re.match(pat, line)
            if m:
                # (they are only allowed outside object definitions)
                raise NotImplementedError

            # Look for a directive
            pat = r'\s*([a-zA-Z0-9_]+)\s+(.*)'
            m = re.match(pat, line)
            if m:
                if not in_obj:
                    raise RuntimeError('Directives must be inside object definitions')
                key = m.group(1)
                val = m.group(2).rstrip()
                odict[key] = val
            elif line[0] == '}':
                if not in_obj:
                    raise RuntimeError("Unmatched '}'")
                # otype, odict must be added to the global structure
                if otype not in d:
                    d[otype] = []
                d[otype].append(odict)
                
                in_obj = False
            else:
                raise RuntimeError(f'Unable to parse "{line}"')
    return d

#-------------------------------------------------------------------------------
# merge_objects
#-------------------------------------------------------------------------------

def merge_objects(objs, o):
    for k, v in o.items():
        if k in objs:
            objs[k].extend(v)
        else:
            objs[k] = v

    return objs

#-------------------------------------------------------------------------------
# parse_objects
#-------------------------------------------------------------------------------

def parse_objects(cfg):
    objs = {}
    for path in cfg['cfg_file']:
        with open(path, 'r') as f:
            print(f'Parsing file "{path}"')
            o = parse_obj_file(f)
            if len(o) > 0:
                dump_to_file(os.path.split(path)[1], o)
                objs = merge_objects(objs, o)

    dump_to_file('objects.json', objs)

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

if len(sys.argv[0]) == 2:
    print(f'Usage: {sys.argv[0]} <filepath>')
    sys.exit(1)

# Process the main configuration file
filepath = sys.argv[1]
with open(filepath) as f:
    cfg = parse_main(f)
dump_to_file(os.path.split(filepath)[1], cfg)

# Process included files (object definitions)
obj = parse_objects(cfg)