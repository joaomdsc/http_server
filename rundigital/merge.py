# merge.py - merge the two json files

"""Merge the two files rundigital.json et rundigital_societe.json. From
the second file, we add the following keys:

    - adresse
    - tels
    - url
    - ape_code
    - contact

"""

import json
  
#-------------------------------------------------------------------------------
# find_in_2
#-------------------------------------------------------------------------------

def find_in_2(name, obj2):
    for o in obj2:
        if o['nom'] == name:
            return o
      
#-------------------------------------------------------------------------------
# merge
#-------------------------------------------------------------------------------

def merge(obj1, obj2):
    obj = []
    for o1 in obj1:
        o2 = find_in_2(o1['nom'], obj2)
        if o2 is None:
            obj.append(o1)
            continue
        # Both o1 and o2 exist, and represent the same company
        o1['adresse'] = o2['adresse']
        o1['tels'] = o2['tels']
        o1['url'] = o2['url']
        o1['ape_code'] = o2['ape_code']
        o1['contact'] = o2['contact']
        obj.append(o1)

    return obj

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

filename = 'rundigital.json'
with open(filename, 'r', encoding='utf-8') as f:
    obj1 = json.load(f)

filename = 'rundigital_societe.json'
with open(filename, 'r', encoding='utf-8') as f:
    obj2 = json.load(f)

o = merge(obj1, obj2)
with open('rundigital_merged.json', 'w', encoding='utf-8') as f:
    json.dump(o, f, indent=4, ensure_ascii=False)