# rundigital_prios.py - web scrapping

"""Lister uniquement les sujets, dans les 18 boîtes qu'on a retenu."""

import json
from lxml import etree, html

#-------------------------------------------------------------------------------
# dump_text
#-------------------------------------------------------------------------------

prios = [
    'STORENGY',
    'ALGECO',
    'DELPHI TECHNOLOGIES',
    'TOTAL DIRECT ENERGIE',
    'ACIAL',
    'APRC',
    'GALIAN',
    'FCA FRANCE',
    'ILE DE FRANCE MOBILITE',
    'INNOTHERA',
    'POUEY INTERNATIONAL',
    'RTE',
    'STPI SOCIETE TECHNIQUE DE PRODUCTIONS INDUSTRIELLES',
    'CARREFOUR FRANCE',
    'SMARTADSERVER',
    'ALKAN',
    'GRT GAZ',
    'MAN TRUCK & BUS FRANCE',
]

#-------------------------------------------------------------------------------
# get_prio_sujets
#-------------------------------------------------------------------------------

def get_prio_sujets(sociétés):
    d = []
    for société in sociétés:
        if société['nom'] not in prios:
            continue

        # Sections
        sections = []
        for sect in société['sections']:
            dd = {}
            if not sect['section'].startswith('Quel sujet'):
                continue
            dd['sujet'] = sect['section']

            for q in sect['questions']:
                if q['question'].startswith('Détails de vos sujets'):
                    dd['texte'] = q['réponse']
                    break

            sections.append(dd)

        if len(sections) > 0:
            d.append((société['nom'], sections))

    return d

#-------------------------------------------------------------------------------
# get_sociétés
#-------------------------------------------------------------------------------

def get_sociétés(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        obj = f.read()

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

filename = r'C:\a\rundigital\rundigital.json'
with open(filename, 'r', encoding='utf-8') as f:
    obj = json.load(f)

result = get_prio_sujets(obj)

filename = r'C:\a\rundigital\priorités.json'
print(f'Writing {filename}')
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)
