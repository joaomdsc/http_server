# walk.py -

import os
import json
from shutil import copy

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
# Globals
#-------------------------------------------------------------------------------

src = r'D:'
dst = r'C:\tmp\Photos01Avr2002Aou2006\exemplaire2'
global_state = None
state_path = os.path.join(dst, 'walk_state.json')

#-------------------------------------------------------------------------------
# MyEncoder
#-------------------------------------------------------------------------------
        
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, TreeState):
            return super(MyEncoder, self).default(obj)
        return obj.__dict__

#-------------------------------------------------------------------------------
# TreeState
#-------------------------------------------------------------------------------

class TreeState:
    """Current state of the walk over a given tree or sub-tree.

    This is a recursive structure.
"""
    def __init__(self, dir, subs=None, files=None):
        self.dir = dir

        # self.subs is a dict of sub-directories, key is the sub-directory name
        # (just the last component, not the whole path), and value is an
        # instance of TreeState
        self.subs = {}
        if subs is not None:
            self.subs = subs

        # key = filename, value = ok/corrupt
        self.files = {}
        if files is not None:
            self.files = files

    def __str__(self):
        return json.dumps(self, cls=MyEncoder, indent=4)
    
    @classmethod
    def from_json_decoded(cls, obj):
        """Return an object instance from a json-decoded object."""
        d = {}
        # We iterate on the members actually present, ignoring absent ones.
        for k, v in obj.items():
            d[k] = v

        # Properties with non-json-serializable values
        if 'subs' in obj:
            d['subs'] = {k: TreeState.from_json_decoded(v)
                         for k, v in obj['subs'].items()}

        return cls(**d)

#-------------------------------------------------------------------------------
# persist
#-------------------------------------------------------------------------------

def persist():
    """Write the global state structure to file, override the existing one"""
    
    with open(state_path, 'w') as f:
        f.write(str(global_state))

#-------------------------------------------------------------------------------
# handle_dir
#-------------------------------------------------------------------------------

def handle_dir(dir_path, dst, state):
    """Process an entire directory.

    Copy individual files to the destination, if possible. Mark them
    preventively (and persistently) as 'corrupt', and change that to 'ok' if
    the copy was successful. Call itself recursively on sub-directories.

    Note that we update the state of the local subtree, but we persist to file
    the entire global state.

    dir_path is a given directory path, dst is the matching directory path in
    the destination, state is the corresponding TreeState instance.

    """
    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        print(path)
        if os.path.isdir(path):
            dst_path = os.path.join(dst, f)
            if f not in state.subs:
                # First time we attempt to traverse this subdirectory
                state.subs[f] = TreeState(path)
                persist()
                # Create subdirectory in destination, if needed
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)
            handle_dir(path, dst_path, state.subs[f])
        else:
            if f in state.files:
                # File has already been processed once
                if state.files[f] == 'corrupt':
                    print(f'{path}: marked as corrupt, skipping')
            else:
                # First time handling this file
                state.files[f] = 'corrupt'
                persist()
                try:
                    copy(path, dst)
                except Exception as e:
                    print(f'{path}: {e}')
                    continue
                state.files[f] = 'ok'
                persist()

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

# Get or build the state for the toplevel source directory 
if os.path.isfile(state_path):
    # The file exists, created by a previous run, we reuse it
    with open(state_path, 'r') as f:
        # Re-create an instance of TreeState from a dict
        global_state = TreeState.from_json_decoded(json.load(f))
        # FIXME don't call handle_dir from the top, pick up where we left
else:
    # Start from scratch
    global_state = TreeState(src)

handle_dir(src, dst, global_state)

print('End of walk, the entire tree has been traversed.')
