# check.py - 

"""Comparaisons entre les deux fichiers rundigital.json et rundigital_societe.json."""

import json

#-------------------------------------------------------------------------------
# dump_csv
#-------------------------------------------------------------------------------

def dump_csv(obj1, obj2):
    with open('runs.csv', 'w') as f:
        f.write('RunDigital\tR_societe\n')

        names1 = sorted([x['nom'] for x in obj1])
        names2 = sorted([x['nom'] for x in obj2])
        # print(f'Length mismatch: len1={len(names1)}, len2={len(names2)}')
        i = 0
        while i < len(names1):
            s1 = names1[i]
            s2 = names2[i] if i < len(names2) else ''
            f.write(f'{s1}\t{s2}\n')
            i += 1

#-------------------------------------------------------------------------------
# find_in_2
#-------------------------------------------------------------------------------

def find_in_2(name, obj2):
    for o in obj2:
        if o['nom'] == name:
            return o
     
#-------------------------------------------------------------------------------
# compare_panel
#-------------------------------------------------------------------------------

def compare_panel(nom, o1, o2, panel):
    result1 = 'none1'
    for x1 in o1['sections']:
        if x1['section'] == 'Votre entreprise':
            for q in x1['questions']:
                if q['question'] == panel:
                    result1 = q['réponse'][2:]

    result2 = 'none2'
    for p in o2['panels']:
        if p[0] == panel:
            result2 = p[1]

    if result1 != result2:
        print(f'ERROR: "{nom[:20]}": panel={panel}, 1="{result1}", 2="{result2}"')
    # else:
    #     print(f'OK: panel={panel}')
        
#-------------------------------------------------------------------------------
# compare
#-------------------------------------------------------------------------------

def compare(obj1, obj2):
    if len(obj1) != len(obj2):
        print(f'Length mismatch: len1={len(obj1)}, len2={len(obj2)}')
    for o1 in obj1:
        o2 = find_in_2(o1['nom'], obj2)
        if o2 is None:
            continue
        # Both o1 and o2 exist, and represent the same company
        if o1['Code ape'] != o2['ape_text']:
            print('ape error')

        compare_panel(o1['nom'], o1, o2, 'Effectif du groupe')
        compare_panel(o1['nom'], o1, o2, 'Effectif sur site')
        compare_panel(o1['nom'], o1, o2, "Votre fonction dans l'entreprise")
        # compare_panel(o1['nom'], o1, o2, 'Nombre Serveurs')
        # compare_panel(o1['nom'], o1, o2, 'Nombre Postes')
        # compare_panel(o1['nom'], o1, o2, 'Détails des solutions')


#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

filename = 'rundigital.json'
with open(filename, 'r', encoding='utf-8') as f:
    obj1 = json.load(f)

filename = 'rundigital_societe.json'
with open(filename, 'r', encoding='utf-8') as f:
    obj2 = json.load(f)

# dump_csv(obj1, obj2)
compare(obj1, obj2)


# =IF(A9<>B9;"differ";"")