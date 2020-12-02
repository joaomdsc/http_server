# json_ini.py - turn .ini files into json

"""This is originally done for NSClient++ ini files that are very hard to grasp
(lots of blank lines, comments on their own lines, etc). The idea is to
generate a json file, to reveal the hierarchical nature of the sections, while
kkeping the comments.

"""

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
# parse_ini
#-------------------------------------------------------------------------------

def parse_ini(f):
    """Lines starting with # or ; are comments (non-standard ini format)."""
    d = {}
    section = None
    for line in f.readlines():
        # Remove blank-only or empty lines
        m = re.match('\s*$', line)
        if m:
            continue

        # Ignore these comments for nsclient.ini 
        if line[0] == '#':
            continue

        # Comments on sections or parameters 
        if line[0] == ';':
            # Get the text of the comment, keep it for the next element
            name = None
            comment = line
            # Comments with a section or parameter name
            m = re.match(';\s*(.*) - (.*)', line)
            if m:
                name = m.group(1).capitalize()
                comment = m.group(2)
            else:
                m = re.match(';\s*(.*)', line)
                if m:
                    comment = m.group(1)
            # print(f'n={name}, c={comment}')

        # Section
        elif line[0] == '[':
            m = re.match('\[(.*)]', line)
            elems = m.group(1).split('/')
            p = d
            for e in elems:
                if len(e) == 0:
                    continue
                if not (e in p and isinstance(p[e], dict)):
                    # nsclient-sample.ini has a strange case in the
                    # /settings/WEB/server/users path where a "sample" key
                    # exists, and at the same time we want a sub-section called
                    # "sample", at the same place in the hierarchy. This code
                    # will overwrite the key with the sub-section.
                    p[e] = {}
                p = p[e]
            section = p

        # Parameter
        else:
            m = re.match('([^=]+) = (.*)', line)
            if m:
                key = m.group(1)
                val = m.group(2)
                # print(f'section={section}, k={key}, v={val}')
                section[key] = val

    return d

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

if len(sys.argv[0]) == 2:
    print(f'Usage: {sys.argv[0]} <filepath>')
    sys.exit(1)

filepath = sys.argv[1]
with open(filepath) as f:
    obj = parse_ini(f)

outpath = filepath.rsplit('.', maxsplit=1)[0] + '.json'
with open(outpath, 'w') as f:
    json.dump(obj, f, indent=4)
    